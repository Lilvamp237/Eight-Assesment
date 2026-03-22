"""
Quick test script to verify Playwright installation.
"""
from playwright.sync_api import sync_playwright

def test_playwright():
    """Test if Playwright can launch a browser and load a page."""
    print("Testing Playwright...")

    try:
        with sync_playwright() as p:
            print("✓ Playwright imported successfully")

            browser = p.chromium.launch(headless=True)
            print("✓ Browser launched successfully")

            page = browser.new_page()
            print("✓ New page created")

            page.goto("https://example.com", timeout=30000)
            print("✓ Page loaded successfully")

            title = page.title()
            print(f"✓ Page title: {title}")

            browser.close()
            print("\n✅ All tests passed! Playwright is working correctly.")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_playwright()
