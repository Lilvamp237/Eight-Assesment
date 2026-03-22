"""
Streamlit UI for the AI-Powered Website Audit Tool.
"""
import streamlit as st
from scraper import WebsiteScraper
from analyzer import AuditAnalyst
from logger import PromptLogger
from models import PageMetrics, AuditReport
import os
from dotenv import load_dotenv
import traceback

# Load environment variables from .env file
load_dotenv()


# Page configuration
st.set_page_config(
    page_title="AI Website Auditor",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #1f77b4;
        margin: 10px 0;
    }
    .recommendation {
        background-color: #fff3cd;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
        margin: 8px 0;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    """Main application entry point."""

    # Title and description
    st.title("🔍 AI-Powered Website Audit Tool")
    st.markdown("""
    Enter a URL to get a comprehensive audit combining **factual metrics** with **AI-powered insights**.
    Powered by Google Gemini and grounded in real data.
    """)

    # Load API key from environment
    api_key = os.getenv("GOOGLE_API_KEY", "")

    # Sidebar for utilities
    with st.sidebar:
        st.header("⚙️ Configuration")
        if st.button("Clear Logs"):
            PromptLogger.clear_logs()
            st.success("Logs cleared!")

    # Main input section
    col1, col2 = st.columns([3, 1])

    with col1:
        url = st.text_input(
            "Website URL",
            placeholder="https://example.com",
            help="Enter the full URL including https://"
        )

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Spacer
        run_audit = st.button("🚀 Run Audit", type="primary", use_container_width=True)

    # Run audit when button is clicked
    if run_audit:
        if not url:
            st.error("Please enter a URL to audit.")
            return

        if not api_key:
            st.error("Please set GOOGLE_API_KEY in your .env file.")
            return

        # Run the audit pipeline
        with st.spinner("🔄 Scraping website..."):
            try:
                scraper = WebsiteScraper()
                metrics = scraper.scrape(url)
                st.success(f"✅ Successfully scraped {metrics.url}")
            except Exception as e:
                st.error(f"❌ Scraping failed: {str(e)}")
                with st.expander("🔍 Error Details"):
                    st.code(traceback.format_exc())
                return

        with st.spinner("🤖 Analyzing with AI..."):
            try:
                analyst = AuditAnalyst(api_key=api_key)
                report = analyst.analyze(metrics, log_prompts=True)
                st.success("✅ AI analysis complete!")
            except Exception as e:
                st.error(f"❌ AI analysis failed: {str(e)}")
                return

        # Display results
        display_results(metrics, report)

        # Display prompt logs at the bottom
        st.markdown("---")
        with st.expander("📜 Prompt Logs / Reasoning Trace", expanded=False):
            PromptLogger.display_logs()


def display_results(metrics: PageMetrics, report: AuditReport):
    """
    Display audit results in a clean, organized layout.

    Args:
        metrics: Extracted factual metrics
        report: AI-generated audit report
    """
    st.markdown("## 📊 Audit Results")

    # Create two main columns: Factual Metrics | AI Insights
    left_col, right_col = st.columns([1, 1])

    # LEFT COLUMN: Factual Metrics
    with left_col:
        st.markdown("### 📈 Factual Metrics")

        # Content Metrics
        with st.container():
            st.markdown("#### Content Structure")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Words", f"{metrics.word_count:,}")
            col2.metric("H1s", metrics.h1_count)
            col3.metric("H2s", metrics.h2_count)
            col4.metric("H3s", metrics.h3_count)

        # Conversion Metrics
        with st.container():
            st.markdown("#### Conversion Elements")
            st.metric("CTAs (Calls-to-Action)", metrics.cta_count)

        # Link Metrics
        with st.container():
            st.markdown("#### Link Distribution")
            col1, col2 = st.columns(2)
            col1.metric("Internal Links", metrics.internal_link_count)
            col2.metric("External Links", metrics.external_link_count)

        # Media Metrics
        with st.container():
            st.markdown("#### Media & Accessibility")
            col1, col2 = st.columns(2)
            col1.metric("Total Images", metrics.image_count)
            col2.metric(
                "Missing Alt Text",
                f"{metrics.missing_alt_percentage}%",
                delta=None if metrics.missing_alt_percentage == 0 else "Needs attention",
                delta_color="inverse"
            )

        # SEO Metadata
        with st.container():
            st.markdown("#### SEO Metadata")
            st.markdown(f"**Meta Title:** {metrics.meta_title or '⚠️ MISSING'}")
            st.markdown(f"**Meta Description:** {metrics.meta_description or '⚠️ MISSING'}")

    # RIGHT COLUMN: AI Insights
    with right_col:
        st.markdown("### 🤖 AI-Powered Insights")

        # SEO Analysis
        st.markdown("#### 🎯 SEO Analysis")
        st.markdown(f'<div class="insight-box">{report.seo_analysis}</div>', unsafe_allow_html=True)

        # Messaging Analysis
        st.markdown("#### 💬 Messaging Analysis")
        st.markdown(f'<div class="insight-box">{report.messaging_analysis}</div>', unsafe_allow_html=True)

        # CTA Analysis
        st.markdown("#### 🔘 CTA Analysis")
        st.markdown(f'<div class="insight-box">{report.cta_analysis}</div>', unsafe_allow_html=True)

        # Content Depth
        st.markdown("#### 📚 Content Depth")
        st.markdown(f'<div class="insight-box">{report.content_depth_analysis}</div>', unsafe_allow_html=True)

        # UX Concerns
        st.markdown("#### ⚠️ UX Concerns")
        st.markdown(f'<div class="insight-box">{report.ux_concerns}</div>', unsafe_allow_html=True)

    # Full-width recommendations section
    st.markdown("---")
    st.markdown("### ✨ Prioritized Recommendations")

    for idx, recommendation in enumerate(report.recommendations, 1):
        st.markdown(
            f'<div class="recommendation"><strong>#{idx}</strong> {recommendation}</div>',
            unsafe_allow_html=True
        )


if __name__ == "__main__":
    main()
