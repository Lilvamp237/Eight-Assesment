"""
AI-powered website audit analysis using Google Gemini.
"""
import google.generativeai as genai
from models import PageMetrics, AuditReport
from logger import PromptLogger
from typing import Optional
import os
import json


class AuditAnalyst:
    """Generates structured audit insights using Google Gemini."""

    # System prompt that enforces grounded, metric-based analysis
    SYSTEM_PROMPT = """You are an expert website auditor analyzing a webpage based on factual metrics.

CRITICAL INSTRUCTIONS:
1. ALL insights must reference specific numbers from the metrics
2. NO generic advice - tie every observation to actual data
3. Use phrases like "With only X CTAs..." or "At Y% missing alt text..."
4. Compare numbers to industry standards when relevant
5. Recommendations must be specific and actionable (e.g., "Add 3 more CTAs" not "Improve CTAs")

Your analysis must be:
- Data-driven: Reference actual counts and percentages
- Concrete: Avoid phrases like "could improve" - say "increase from X to Y"
- Prioritized: Most critical issues first
- Actionable: Clear next steps tied to metrics

Focus areas:
- SEO: Meta tags, heading hierarchy, content structure
- Messaging: Word count distribution, content clarity
- CTAs: Quantity, placement, effectiveness
- Content Depth: Heading structure, content organization
- UX: Accessibility (alt text), link ratios, navigation

Remember: Each insight must cite at least one specific metric."""

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-3.0-flash"):
        """
        Initialize the audit analyst.

        Args:
            api_key: Google API key (if not provided, uses GOOGLE_API_KEY env var)
            model_name: Gemini model to use (default: gemini-3.0-flash)
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Google API key must be provided or set in GOOGLE_API_KEY environment variable")

        self.model_name = model_name

        # Configure Google Generative AI
        genai.configure(api_key=self.api_key)

        # Initialize model
        self.model = genai.GenerativeModel(model_name=model_name)

        # Generation config for consistent output
        self.generation_config = {
            "temperature": 0.3,  # Low temperature for consistent, factual output
            "top_p": 0.95,
            "top_k": 40,
        }

    def analyze(self, metrics: PageMetrics, log_prompts: bool = True) -> AuditReport:
        """
        Analyze page metrics and generate an audit report.

        Args:
            metrics: The factual metrics extracted from the webpage
            log_prompts: Whether to log prompts to session state

        Returns:
            AuditReport with AI-generated insights and recommendations
        """
        # Construct combined prompt with system instructions, metrics, and JSON schema request
        user_prompt = self._build_user_prompt(metrics)
        json_instructions = """

IMPORTANT: Respond ONLY with valid JSON in this exact format (no markdown, no extra text):
{
  "seo_analysis": "string (your analysis referencing specific metrics)",
  "messaging_analysis": "string (your analysis referencing specific metrics)",
  "cta_analysis": "string (your analysis referencing specific metrics)",
  "content_depth_analysis": "string (your analysis referencing specific metrics)",
  "ux_concerns": "string (your analysis referencing specific metrics)",
  "recommendations": ["string", "string", "string"]
}"""
        full_prompt = f"{self.SYSTEM_PROMPT}\n\n{user_prompt}\n{json_instructions}"

        # Get structured response
        response = self.model.generate_content(full_prompt, generation_config=self.generation_config)

        # Clean response text (remove markdown code blocks if present)
        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]  # Remove ```json
        if response_text.startswith("```"):
            response_text = response_text[3:]  # Remove ```
        if response_text.endswith("```"):
            response_text = response_text[:-3]  # Remove trailing ```
        response_text = response_text.strip()

        # Parse JSON response into AuditReport
        response_data = json.loads(response_text)
        audit_report = AuditReport(**response_data)

        # Log the interaction if requested
        if log_prompts:
            PromptLogger.log_interaction(
                system_prompt=self.SYSTEM_PROMPT,
                user_prompt=user_prompt,
                structured_input=metrics.model_dump(),
                raw_output=audit_report.model_dump(),
                model_name=self.model_name
            )

        return audit_report

    def _build_user_prompt(self, metrics: PageMetrics) -> str:
        """
        Build a detailed user prompt with all metrics.

        Args:
            metrics: PageMetrics object

        Returns:
            Formatted prompt string
        """
        return f"""Analyze this webpage and provide grounded insights based on the following factual metrics:

URL: {metrics.url}

CONTENT METRICS:
- Total Words: {metrics.word_count}
- H1 Tags: {metrics.h1_count}
- H2 Tags: {metrics.h2_count}
- H3 Tags: {metrics.h3_count}

CONVERSION METRICS:
- CTAs (Buttons/Links): {metrics.cta_count}

LINK METRICS:
- Internal Links: {metrics.internal_link_count}
- External Links: {metrics.external_link_count}

MEDIA METRICS:
- Total Images: {metrics.image_count}
- Missing Alt Text: {metrics.missing_alt_percentage}%

SEO METADATA:
- Meta Title: {metrics.meta_title or "MISSING"}
- Meta Description: {metrics.meta_description or "MISSING"}

Based on these specific numbers, provide:
1. SEO analysis (reference heading counts, meta tags)
2. Messaging analysis (reference word count, heading distribution)
3. CTA analysis (reference actual CTA count vs. content length)
4. Content depth analysis (reference heading hierarchy)
5. UX concerns (reference alt text %, link ratios)
6. 3-5 prioritized recommendations with specific target numbers

Every insight must cite at least one metric. No generic advice."""
