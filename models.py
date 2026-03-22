"""
Pydantic models for website audit data structures.
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class PageMetrics(BaseModel):
    """Factual metrics extracted from a webpage."""

    url: str = Field(description="The URL that was audited")
    word_count: int = Field(description="Total word count on the page")
    h1_count: int = Field(description="Number of H1 tags")
    h2_count: int = Field(description="Number of H2 tags")
    h3_count: int = Field(description="Number of H3 tags")
    cta_count: int = Field(description="Number of call-to-action buttons/links")
    internal_link_count: int = Field(description="Number of internal links")
    external_link_count: int = Field(description="Number of external links")
    image_count: int = Field(description="Total number of images")
    missing_alt_percentage: float = Field(description="Percentage of images missing alt text")
    meta_title: Optional[str] = Field(default=None, description="Meta title tag content")
    meta_description: Optional[str] = Field(default=None, description="Meta description tag content")

    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://example.com",
                "word_count": 1250,
                "h1_count": 1,
                "h2_count": 5,
                "h3_count": 8,
                "cta_count": 3,
                "internal_link_count": 15,
                "external_link_count": 5,
                "image_count": 10,
                "missing_alt_percentage": 20.0,
                "meta_title": "Example Domain",
                "meta_description": "Example description for SEO"
            }
        }


class AuditReport(BaseModel):
    """AI-generated insights and recommendations based on PageMetrics."""

    seo_analysis: str = Field(
        description="Analysis of SEO factors including meta tags, heading structure, and content optimization. Must reference specific metrics."
    )
    messaging_analysis: str = Field(
        description="Evaluation of content clarity, messaging effectiveness, and tone. Must reference word count and heading distribution."
    )
    cta_analysis: str = Field(
        description="Assessment of call-to-action effectiveness and placement. Must reference actual CTA count."
    )
    content_depth_analysis: str = Field(
        description="Evaluation of content comprehensiveness and structure. Must reference word count and heading hierarchy."
    )
    ux_concerns: str = Field(
        description="User experience issues including accessibility (alt text), link distribution, and navigation. Must reference specific percentages and counts."
    )
    recommendations: List[str] = Field(
        min_length=3,
        max_length=5,
        description="3-5 prioritized, actionable recommendations tied to specific metrics. Each must be concrete and implementable."
    )

    class Config:
        json_schema_extra = {
            "example": {
                "seo_analysis": "With only 1 H1 tag and a meta title of 14 words, the SEO structure is solid. However, the meta description at 155 characters is near the limit.",
                "messaging_analysis": "The 1,250-word count indicates comprehensive coverage, with good distribution across 5 H2s and 8 H3s.",
                "cta_analysis": "Only 3 CTAs across the entire page is low for a 1,250-word page. Consider adding CTAs every 300-400 words.",
                "content_depth_analysis": "Strong hierarchical structure with 1 H1, 5 H2s, and 8 H3s suggests well-organized content sections.",
                "ux_concerns": "Critical: 20% of images (2 out of 10) are missing alt text, creating accessibility barriers. Link ratio of 15:5 (internal:external) is healthy.",
                "recommendations": [
                    "Add alt text to 2 images immediately to improve accessibility and SEO",
                    "Increase CTA count from 3 to 6-8 by adding mid-content conversion points",
                    "Shorten meta description by 10 characters to stay within optimal range"
                ]
            }
        }
