from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

class CrawlerService:
    @staticmethod
    async def fetch_article_text(url: str) -> str:
        try:
            print(f"[CrawlerService] Using Headless Browser to fetch: {url}")
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page(
                    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36"
                )
                await page.goto(url, wait_until="networkidle", timeout=30000)
                html = await page.content()
                await browser.close()
            
            soup = BeautifulSoup(html, 'html.parser')
            
            for script_or_style in soup(['script', 'style', 'nav', 'header', 'footer']):
                script_or_style.extract()
                
            paragraphs = soup.find_all('p')
            if not paragraphs:
                paragraphs = soup.find_all('div', class_=lambda c: c and 'content' in c.lower())
                
            text = "\\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True) and len(p.get_text(strip=True)) > 5])
            print(f"[CrawlerService] Extracted {len(text)} chars from HTML")
            return text
        except Exception as e:
            print(f"[CrawlerService] Failed to fetch article: {e}")
            return ""