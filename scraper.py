"""
Web scraper for extracting factual metrics from websites.
"""
try:
    from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    PlaywrightTimeoutError = Exception

from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
from models import PageMetrics
from typing import Optional
import asyncio
import sys


class WebsiteScraper:
    """Extracts factual metrics from a webpage using Playwright (or fallback to requests)."""

    def __init__(self, timeout: int = 30000):
        """
        Initialize the scraper.

        Args:
            timeout: Page load timeout in milliseconds (default: 30 seconds)
        """
        self.timeout = timeout

    def scrape(self, url: str) -> PageMetrics:
        """
        Scrape a URL and extract all factual metrics.

        Args:
            url: The URL to scrape

        Returns:
            PageMetrics object containing all extracted data

        Raises:
            Exception: If scraping fails
        """
        # Try Playwright first (handles JavaScript), fallback to requests
        if PLAYWRIGHT_AVAILABLE:
            try:
                # Playwright launches a browser via subprocess; on Windows this requires
                # a proactor-based event loop policy.
                if sys.platform == 'win32':
                    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

                # Run the async scraping in a new event loop
                return asyncio.run(self._scrape_with_playwright(url))
            except Exception as e:
                # If Playwright fails, try requests fallback
                print(f"⚠️ Playwright failed ({str(e)}), using fallback scraper for static content...")
                return self._scrape_with_requests(url)
        else:
            # Playwright not available, use requests
            return self._scrape_with_requests(url)

    def _scrape_with_requests(self, url: str) -> PageMetrics:
        """
        Fallback scraper using requests (for static content only).

        Args:
            url: The URL to scrape

        Returns:
            PageMetrics object containing all extracted data
        """
        import requests

        # Ensure URL has a scheme
        if not url.startswith(('http://', 'https://')):
            url = f'https://{url}'

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            html_content = response.text
        except Exception as e:
            raise Exception(f"Failed to fetch page: {str(e)}")

        # Parse with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract all metrics using BeautifulSoup methods
        return self._extract_metrics(soup, url)

    async def _scrape_with_playwright(self, url: str) -> PageMetrics:
        """
        Scrape using Playwright (handles JavaScript-rendered content).

        Args:
            url: The URL to scrape

        Returns:
            PageMetrics object containing all extracted data

        Raises:
            Exception: If scraping fails
        """
        # Ensure URL has a scheme
        if not url.startswith(('http://', 'https://')):
            url = f'https://{url}'

        async with async_playwright() as p:
            # Try system Chromium first (Streamlit Cloud), fallback to bundled
            import shutil
            chromium_path = shutil.which('chromium') or shutil.which('chromium-browser')

            if chromium_path:
                browser = await p.chromium.launch(
                    headless=True,
                    executable_path=chromium_path,
                    args=['--no-sandbox', '--disable-setuid-sandbox']
                )
            else:
                browser = await p.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-setuid-sandbox']
                )

            page = await browser.new_page()

            try:
                await page.goto(url, timeout=self.timeout, wait_until='networkidle')
                html_content = await page.content()
            except PlaywrightTimeoutError:
                raise Exception(f"Page load timeout after {self.timeout}ms.")
            except Exception as e:
                raise Exception(f"Failed to load page: {str(e)}")
            finally:
                await browser.close()

        # Parse with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        return self._extract_metrics(soup, url)

    def _extract_metrics(self, soup: BeautifulSoup, url: str) -> PageMetrics:
        """
        Extract all metrics from BeautifulSoup object.

        Args:
            soup: Parsed HTML
            url: Original URL

        Returns:
            PageMetrics object
        """
        return PageMetrics(
            url=url,
            word_count=self._count_words(soup),
            h1_count=len(soup.find_all('h1')),
            h2_count=len(soup.find_all('h2')),
            h3_count=len(soup.find_all('h3')),
            cta_count=self._count_ctas(soup),
            internal_link_count=self._count_internal_links(soup, url),
            external_link_count=self._count_external_links(soup, url),
            image_count=len(soup.find_all('img')),
            missing_alt_percentage=self._calculate_missing_alt_percentage(soup),
            meta_title=self._extract_meta_title(soup),
            meta_description=self._extract_meta_description(soup)
        )

    def _count_words(self, soup: BeautifulSoup) -> int:
        """Count words in visible text content."""
        # Work on a copy so later extractors (e.g., meta tags) still see the full DOM.
        soup_for_text = BeautifulSoup(str(soup), 'html.parser')

        # Remove script, style, and other non-visible elements
        for element in soup_for_text(['script', 'style', 'meta', 'link', 'noscript']):
            element.decompose()

        # Get text and count words
        text = soup_for_text.get_text(separator=' ', strip=True)
        words = re.findall(r'\b\w+\b', text)
        return len(words)

    def _count_ctas(self, soup: BeautifulSoup) -> int:
        """
        Count call-to-action elements (buttons and prominent links).

        Looks for common CTA patterns:
        - <button> elements
        - Links with CTA-related text
        - Elements with CTA-related classes
        """
        cta_count = 0

        # Count button elements
        cta_count += len(soup.find_all('button'))

        # Count links with CTA keywords
        cta_keywords = [
            'sign up', 'signup', 'register', 'get started', 'start free',
            'try free', 'buy now', 'shop now', 'subscribe', 'download',
            'learn more', 'contact us', 'request demo', 'get quote',
            'join now', 'apply now', 'book now', 'order now'
        ]

        for link in soup.find_all('a'):
            link_text = link.get_text(strip=True).lower()
            link_class = ' '.join(link.get('class', [])).lower()

            # Check text content
            if any(keyword in link_text for keyword in cta_keywords):
                cta_count += 1
                continue

            # Check class names for CTA indicators
            if any(word in link_class for word in ['cta', 'button', 'btn']):
                cta_count += 1

        return cta_count

    def _count_internal_links(self, soup: BeautifulSoup, base_url: str) -> int:
        """Count links pointing to the same domain."""
        base_domain = urlparse(base_url).netloc
        internal_count = 0

        for link in soup.find_all('a', href=True):
            href = link['href']

            # Handle relative URLs
            if href.startswith('/') and not href.startswith('//'):
                internal_count += 1
            # Handle absolute URLs on same domain
            elif base_domain in href:
                internal_count += 1

        return internal_count

    def _count_external_links(self, soup: BeautifulSoup, base_url: str) -> int:
        """Count links pointing to external domains."""
        base_domain = urlparse(base_url).netloc
        external_count = 0

        for link in soup.find_all('a', href=True):
            href = link['href']

            # Skip relative links and same-domain links
            if href.startswith('/') or base_domain in href:
                continue

            # Check if it's an absolute URL to a different domain
            if href.startswith(('http://', 'https://', '//')):
                external_count += 1

        return external_count

    def _calculate_missing_alt_percentage(self, soup: BeautifulSoup) -> float:
        """Calculate percentage of images missing alt text."""
        images = soup.find_all('img')

        if not images:
            return 0.0

        missing_alt = sum(1 for img in images if not img.get('alt', '').strip())
        return round((missing_alt / len(images)) * 100, 2)

    def _extract_meta_title(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract the meta title (or <title> tag)."""
        # Try Open Graph title first
        og_title = soup.find('meta', property='og:title')
        if og_title and og_title.get('content'):
            return og_title['content'].strip()

        # Fall back to standard title tag
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text(strip=True)

        return None

    def _extract_meta_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract the meta description."""
        # Check common meta-description variants used across sites.
        description_selectors = [
            {'property': re.compile(r'^og:description$', re.IGNORECASE)},
            {'name': re.compile(r'^description$', re.IGNORECASE)},
            {'name': re.compile(r'^twitter:description$', re.IGNORECASE)},
            {'itemprop': re.compile(r'^description$', re.IGNORECASE)},
            {'property': re.compile(r'^description$', re.IGNORECASE)},
        ]

        for selector in description_selectors:
            tag = soup.find('meta', attrs=selector)
            if tag and tag.get('content') and tag['content'].strip():
                return tag['content'].strip()

        return None
