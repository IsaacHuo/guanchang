from __future__ import annotations
import json
from openai import OpenAI
from app.core.config import settings

# Configure DeepSeek via OpenAI compatible interface
client = OpenAI(
    api_key=settings.DEEPSEEK_API_KEY, 
    base_url="https://api.deepseek.com/v1"
)

class LLMService:
    @staticmethod
    def extract_official_data(text: str) -> dict | None:
        """
        Extract structured official career and investigation info from raw text.
        Returns a dictionary or None if failed.
        """
        print("[LLMService] Calling DeepSeek API structure extraction...")
        
        prompt = """
        你是一个专门处理中国官员履历与反腐纪检通报的AI助手。你的任务是从提供的长文本履历/新闻通报中提取出结构化信息。
        要求提取的字段：
        1. name: 官员姓名。
        2. gender: 性别（男/女），不确定填空字符串""。
        3. birth_date: 出生年月（格式 YYYY-MM，如果是纯年份则 YYYY，不确定则为空字符串""）。
        4. identifier: 如果文本中有籍贯等信息，用来作为唯一标示辅助，可空。
        5. positions: 历任职务及组织数组。每个元素包含：
           - title: 职务名称（如：市长、局长）
           - organization: 组织机构名称（如：某市人民政府、某省交通厅）。如缺失可填空。
           - start_date: 开始时间（格式 YYYY-MM，未知填""）
           - end_date: 结束时间（格式 YYYY-MM，如果"至今"或无结束时间，填""）
        6. events: 纪检调查事件数组。如果有落马/被查/双开经历。每个元素包含：
           - description: 事件描述（例如："涉嫌严重违纪违法接受调查"、"被开除党籍和公职"）
           - date: 发生时间（格式 YYYY-MM-DD 或 YYYY-MM，未知填""）

        请严格以 JSON 格式输出，务必不要加入额外的 markdown 标记（如 ```json 和 ```），不要附带任何解释文字，只返回合法 JSON 字符串。
        示范 JSON 格式：
        {
            "name": "张三",
            "gender": "男",
            "birth_date": "1960-01",
            "identifier": "湖北某地人",
            "positions": [{"title": "市长", "organization": "A市政府", "start_date": "2010-02", "end_date": "2015-06"}],
            "events": [{"description": "接受纪律审查", "date": "2020-10-15"}]
        }
        """
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text}
                ],
                temperature=0.1
            )
            content = response.choices[0].message.content.strip()
            
            # Simple JSON string cleaning if model adds markdown blocks ignoring instructions
            if content.startswith("```json"):
                content = content.replace("```json\n", "", 1)
            if content.startswith("```"):
                content = content.replace("```\n", "", 1)
            if content.endswith("```"):
                content = content[:-3].strip()
                
            return json.loads(content)
        except Exception as e:
            print(f"[LLMService] DeepSeek API Error or JSON Parsing Failed: {e}")
            return None