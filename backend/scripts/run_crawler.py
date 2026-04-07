from playwright.async_api import async_playwright
import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.crawler_service import CrawlerService
from app.services.llm_service import LLMService
from app.services.graph_service import GraphService

class BatchCrawler:
    async def start_batch_crawl(self, base_url: str, start_page: int = 0, max_pages: int = 5):
        """完全突破反爬的无头模式，支持多页抓取并限定2026年"""
        print(f"🕵️ 开始防封禁版无头浏览器连续跨页爬取，目标年份：2026")
        
        all_links = []
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36"
                )
                
                # 遍历多页
                for page_num in range(start_page, start_page + max_pages):
                    if page_num == 0:
                        current_url = f"{base_url}index.shtml"
                    else:
                        current_url = f"{base_url}index_{page_num}.shtml"
                        
                    print(f"🔄 正在渲染列表页 {current_url} ...")
                    try:
                        await page.goto(current_url, wait_until="networkidle", timeout=30000)
                    except Exception as e:
                         print(f"    [警告] 页面 {current_url} 加载失败或超时: {e}")
                         continue
                    
                    # 抽取链接
                    links_raw = await page.eval_on_selector_all("a", "elements => elements.map(e => e.href)")
                    
                    page_links_count = 0
                    for href in links_raw:
                        # 重点筛选包含 2026 年份的详情页 (网站中有时是 2026 也有可能只是纯新闻)
                        if href and len(href) > 25 and ('2026' in href or 'content' in href or 'detail' in href):
                            if href not in all_links:
                                all_links.append(href)
                                page_links_count += 1
                                
                    print(f"✅ 第 {page_num} 页提取完成，本页新增发现 2026 疑似记录或通报 {page_links_count} 条。")
                    await asyncio.sleep(2) # 页面翻页防封
                    
                await browser.close()
                
                print(f"🎯 共计汇总 {len(all_links)} 个通报链接进行深度排查。")
                
                # 过滤出最近的以保证精准命中2026及有效文章
                valid_links = [l for l in all_links if "2026" in l] 
                if not valid_links:
                    print("⚠️ 当前页面未在链接中发现包含 '2026' 的显式路径，使用全部可用内容替代探测...")
                    valid_links = all_links[:50]
                
                # 开始批量处理提取的数据
                for idx, url in enumerate(valid_links):
                    print(f"[{idx+1}/{len(valid_links)}] 开始处理...")
                    await self._process_single_url(url)
                    await asyncio.sleep(3) # 降低并发频率，避免大模型限流和对方服务器封禁
                    
                print("✅ 2026年度官员收集任务完结！所有节点已写入 Neo4j 并在前端实时渲染！")
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
    # 为保证效果，抓取一个含有确切列表的反腐要闻网站（如果SPP是 http://www.spp.gov.cn/spp/qwfb/index.shtml）
    # 大多数分页格式将是 index_1.shtml 等
    base_target = "https://www.spp.gov.cn/qwfb/" 
    asyncio.run(crawler.start_batch_crawl(base_target, start_page=0, max_pages=10))