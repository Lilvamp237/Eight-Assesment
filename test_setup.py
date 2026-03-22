"""
Quick validation script to test the audit pipeline without Streamlit.
Run this to verify your setup before launching the full app.
"""
from scraper import WebsiteScraper
from analyzer import AuditAnalyst
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_audit(url: str = "https://example.com"):
    """
    Test the complete audit pipeline.

    Args:
        url: URL to test (default: example.com)
    """
    print("=" * 60)
    print("🔍 Website Audit Tool - Validation Script")
    print("=" * 60)

    # Check API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("\n❌ ERROR: GOOGLE_API_KEY not found in environment")
        print("   Set it in .env file or export GOOGLE_API_KEY=your_key")
        return

    print(f"\n✅ API key found: {api_key[:8]}...{api_key[-4:]}")

    # Test scraping
    print(f"\n📡 Testing scraper with URL: {url}")
    try:
        scraper = WebsiteScraper()
        metrics = scraper.scrape(url)
        print("✅ Scraping successful!")
        print(f"   - Word count: {metrics.word_count}")
        print(f"   - H1s: {metrics.h1_count}, H2s: {metrics.h2_count}, H3s: {metrics.h3_count}")
        print(f"   - CTAs: {metrics.cta_count}")
        print(f"   - Images: {metrics.image_count} ({metrics.missing_alt_percentage}% missing alt)")
    except Exception as e:
        print(f"❌ Scraping failed: {str(e)}")
        return

    # Test AI analysis
    print("\n🤖 Testing AI analyzer...")
    try:
        analyst = AuditAnalyst(api_key=api_key)
        report = analyst.analyze(metrics, log_prompts=False)
        print("✅ AI analysis successful!")
        print(f"\n🎯 Sample insight:")
        print(f"   {report.seo_analysis[:150]}...")
        print(f"\n💡 First recommendation:")
        print(f"   {report.recommendations[0]}")
    except Exception as e:
        print(f"❌ AI analysis failed: {str(e)}")
        return

    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED! Ready to run: streamlit run app.py")
    print("=" * 60)


if __name__ == "__main__":
    import sys

    # Allow custom URL as command line argument
    test_url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    test_audit(test_url)
