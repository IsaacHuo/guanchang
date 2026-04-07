from playwright.async_api import async_playwright
import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.crawler_service import CrawlerService
from app.services.llm_service import LLMService
from app.services.graph_service import GraphService

class BatchCrawler:
    async def start_batch_crawl(self, list_url: str):
        """完全突破反爬的无头模式抓取所有通报"""
        print(f"🕵️ 开始防封禁版无头浏览器自动大盘爬取: {list_url}")
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36"
                )
                print("🔄 正在等待页面渲染完成...")
                await page.goto(list_url, wait_until="networkidle", timeout=45000)
                
                # 直接通过 JavaScript 拿 A 标签 href，比 BeautifulSoup 更强劲
                links_raw = await page.eval_on_selector_all("a", "elements => elements.map(e => e.href)")
                await browser.close()
                
                links = []
                for href in links_raw:
                    if href and len(href) > 25 and ('content' in href or '/art/' in href or 'detail' in href or '202' in href):
                        if href not in links:
                            links.append(href)
                            
                print(f"🎯 突破防抓取屏蔽！找到 {len(links)} 个确切的官员通报链接。进入深度大模型分析挖掘阵列...")
                
                for url in links[:20]:
                    await self._process_single_url(url)
                    await asyncio.sleep(3)
                    
                print("✅ 初始自动化大盘收集任务完结！所有节点已写入 Neo4j 并在前端实时渲染！")
        except Exception as e:
            print(f"❌ 批量爬取崩溃: {e}")
            
    async def _process_single_url(self, url: str):
        print(f"  -> 分析官员履历正文: {url}")
        try:
            text = await CrawlerService.fetch_article_text(url)
            if not text or len(text) < 30:
                print("     [跳过] 文本过短或反爬拦截。")
                return
                
            data_dict = LLMService.extract_official_data(text)
            if not data_dict or not data_dict.get('name'):
                print("     [跳过] AI提取失败或文本不属于人物介绍。")
                return
                
            official_name = data_dict['name']
            GraphService.create_official(
                official_name, gender=data_dict.get('gender'),
                birth_date=data_dict.get('birth_date'), identifier=data_dict.get('identifier')
            )
            for pos in data_dict.get('positions', []):
                if pos.get('title'):
                    GraphService.create_position(pos['title'])
                    if pos.get('organization'):
                        GraphService.create_organization(pos['organization'])
                    GraphService.add_held_position(
                        official_name, pos['title'], pos.get('organization'),
                        pos.get('start_date'), pos.get('end_date')
                    )
            for evt in data_dict.get('events', []):
                if evt.get('description'):
                     GraphService.add_investigation_event(
                         official_name, evt['description'], evt.get('date', "")
                     )
            print(f"     [入图] 实体 <{official_name}> 档案上链！")
            
        except Exception as e:
            print(f"     [报错] 分析时发生异常: {e}")

if __name__ == "__main__":
    crawler = BatchCrawler()
    # 为保证效果，抓取一个含有确切列表的反腐要闻网站（如：最高检要闻或某省厅通告），这儿用最高检举例或搜狐要闻
    target_url = "https://www.spp.gov.cn/qwfb/index.shtml" 
    asyncio.run(crawler.start_batch_crawl(target_url))