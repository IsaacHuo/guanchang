from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from pydantic import BaseModel
from typing import List, Optional
from app.services.graph_service import GraphService
from app.services.crawler_service import CrawlerService
from app.services.llm_service import LLMService

app = FastAPI(title="Guanchang API", description="官员变动与深度利益关联评估系统")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3333"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Guanchang API", "neo4j_uri": settings.NEO4J_URI}

class PromptRequest(BaseModel):
    text: str

class OfficialCreateRequest(BaseModel):
    name: str
    gender: str | None = None
    birth_date: str | None = None

class HeldPositionRequest(BaseModel):
    official_name: str
    position_title: str
    organization_name: str | None = None
    start_date: str | None = None
    end_date: str | None = None

@app.post("/officials")
def create_official(request: OfficialCreateRequest):
    node = GraphService.create_official(request.name, request.gender, request.birth_date)
    return {"status": "success", "official": dict(node) if node else None}

@app.post("/officials/position")
def add_held_position(request: HeldPositionRequest):
    # 提前保证节点存在
    GraphService.create_official(request.official_name)
    GraphService.create_position(request.position_title)
    if request.organization_name:
        GraphService.create_organization(request.organization_name)
        
    GraphService.add_held_position(
        request.official_name, 
        request.position_title, 
        request.organization_name,
        request.start_date, 
        request.end_date
    )
    return {"status": "success", "message": f"{request.official_name} held position {request.position_title}"}

class ProcessUrlRequest(BaseModel):
    url: str

class PositionItem(BaseModel):
    title: str
    organization: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class EventItem(BaseModel):
    description: str
    date: str

class ExtractedOfficialData(BaseModel):
    name: str
    gender: Optional[str] = None
    birth_date: Optional[str] = None
    identifier: Optional[str] = None
    positions: List[PositionItem] = []
    events: List[EventItem] = []

@app.post("/api/crawl-and-analyze")
async def crawl_and_analyze(request: ProcessUrlRequest):
    """
    一键化全链路：
    爬取包含官员新闻通报的网页URL -> DeepSeek大模型抽取结构化图实体 -> Neo4j 图数据库建链存储
    """
    # 1. 抓取正文
    text = await CrawlerService.fetch_article_text(request.url)
    if not text or len(text) < 50:
        raise HTTPException(status_code=400, detail="Failed to fetch readable article content from URL.")
    
    # 2. 调用大模型解析提取网络
    data_dict = LLMService.extract_official_data(text)
    if not data_dict:
        raise HTTPException(status_code=500, detail="DeepSeek parsing failed or returned invalid JSON.")
    
    # 3. 将结构化结果保存进 Neo4j Graph
    official_name = data_dict.get('name')
    if not official_name:
        raise HTTPException(status_code=500, detail="Extracted JSON did not contain 'name'.")
    
    # 3.1 创建人物基节
    GraphService.create_official(
        official_name, 
        gender=data_dict.get('gender'),
        birth_date=data_dict.get('birth_date'),
        identifier=data_dict.get('identifier')
    )
    
    # 3.2 遍历提取到的职务链表，建立连接与组织
    for pos in data_dict.get('positions', []):
        if pos.get('title'):
            GraphService.create_position(pos['title'])
            if pos.get('organization'):
                GraphService.create_organization(pos['organization'])
            
            GraphService.add_held_position(
                official_name, 
                pos['title'],
                pos.get('organization'),
                pos.get('start_date'),
                pos.get('end_date')
            )
            
    # 3.3 记录落马/双开事件日志
    events_created = []
    for evt in data_dict.get('events', []):
        if evt.get('description'):
             GraphService.add_investigation_event(
                 official_name,
                 evt['description'],
                 evt.get('date', "")
             )
             events_created.append(evt)
             
    return {
        "status": "success",
        "message": f"Successfully parsed and ingested graph for: {official_name}",
        "raw_extracted": data_dict
    }

@app.get("/api/dashboard/stats")
def get_dashboard_stats():
    """提供给大屏看板的实时图统计数据"""
    from app.core.database import db_conn
    
    try:
        officials = db_conn.query("MATCH (n:Official) RETURN count(n) as count")[0]["count"]
        positions = db_conn.query("MATCH (n:Position) RETURN count(n) as count")[0]["count"]
        events = db_conn.query("MATCH (n:Event) RETURN count(n) as count")[0]["count"]
        organizations = db_conn.query("MATCH (n:Organization) RETURN count(n) as count")[0]["count"]
        return {
            "officials": officials,
            "positions": positions,
            "events": events,
            "organizations": organizations
        }
    except Exception as e:
        print(f"Error fetching stats: {e}")
        return {"officials": 0, "positions": 0, "events": 0, "organizations": 0}

@app.get("/api/officials/recent")
def get_recent_officials():
    """获取最新入库的官员列表"""
    query = """
    MATCH (o:Official)
    OPTIONAL MATCH (o)-[:HELD_POSITION]->(p:Position)
    OPTIONAL MATCH (o)-[:INVESTIGATED_FOR]->(e:Event)
    RETURN o.name AS name, o.gender AS gender, o.birth_date AS birth_date,
           o.identifier AS identifier, o.created_at AS created_at,
           collect(DISTINCT p.title) AS titles,
           collect(DISTINCT e.description) AS investigations
    ORDER BY created_at DESC
    LIMIT 10
    """
    from app.core.database import db_conn
    result = db_conn.query(query) or []
    
    officials = []
    for record in result:
        officials.append({
            "name": record['name'],
            "gender": record['gender'],
            "birth_date": record['birth_date'],
            "identifier": record['identifier'],
            "titles": record['titles'],
            "investigations": record['investigations']
        })
    return {"officials": officials}

@app.get("/api/officials/search")
def search_officials(query_name: str):
    """根据姓名、职务或违纪事件进行模糊检索"""
    query = """
    MATCH (o:Official)
    OPTIONAL MATCH (o)-[:HELD_POSITION]->(p:Position)
    OPTIONAL MATCH (o)-[:INVESTIGATED_FOR]->(e:Event)
    WITH o, collect(DISTINCT p.title) AS titles, collect(DISTINCT e.description) AS investigations
    WHERE o.name CONTAINS $query_name 
       OR any(t IN titles WHERE t CONTAINS $query_name)
       OR any(evt IN investigations WHERE evt CONTAINS $query_name)
    RETURN o.name AS name, o.gender AS gender, o.birth_date AS birth_date,
           o.identifier AS identifier, o.created_at AS created_at,
           titles, investigations
    ORDER BY created_at DESC
    LIMIT 20
    """
    from app.core.database import db_conn
    result = db_conn.query(query, parameters={"query_name": query_name}) or []
    
    officials = []
    for record in result:
        officials.append({
            "name": record['name'],
            "gender": record['gender'],
            "birth_date": record['birth_date'],
            "identifier": record['identifier'],
            "titles": record['titles'],
            "investigations": record['investigations']
        })
    return {"officials": officials}

@app.get("/api/officials/profile/{name}")
def get_official_profile(name: str):
    """获取某个官员的个人详细档案、时间轴等微观数据"""
    query = """
    MATCH (o:Official {name: $name})
    OPTIONAL MATCH (o)-[r1:HELD_POSITION]->(p:Position)
    OPTIONAL MATCH (o)-[r2:INVESTIGATED_FOR]->(e:Event)
    RETURN o.name AS name, o.gender AS gender, o.birth_date AS birth_date,
           o.identifier AS identifier,
           collect(DISTINCT {title: p.title, start_date: r1.start_date, end_date: r1.end_date, organization: r1.organization}) AS career,
           collect(DISTINCT {description: e.description, date: r2.date}) AS events
    """
    from app.core.database import db_conn
    result = db_conn.query(query, parameters={"name": name})
    if not result:
        raise HTTPException(status_code=404, detail="Official not found")
        
    record = result[0]
    
    # 按照时间稍微排序一下 career
    career_list = [c for c in record['career'] if c.get('title')]
    events_list = [e for e in record['events'] if e.get('description')]
    
    return {
        "name": record['name'],
        "gender": record['gender'],
        "birth_date": record['birth_date'],
        "identifier": record['identifier'],
        "career": career_list,
        "events": events_list
    }

@app.get("/api/graph/network")
def get_graph_network():
    """提供给 ECharts 的全局点线关系图谱"""
    query = """
    MATCH (n)
    OPTIONAL MATCH (n)-[r]->(m)
    RETURN n, r, m LIMIT 500
    """
    from app.core.database import db_conn
    result = db_conn.query(query) or []
    
    nodes = {}
    links = []
    
    for record in result:
        n = record['n']
        if n.element_id not in nodes:
            # Note: neo4j python driver structure
            nodes[n.element_id] = {
                "id": str(n.element_id),
                "name": n.get('name', n.get('title', n.get('description', 'Unknown'))),
                "category": list(n.labels)[0]
            }
            
        m = record['m']
        r = record['r']
        if m and r:
             if m.element_id not in nodes:
                 nodes[m.element_id] = {
                     "id": str(m.element_id),
                     "name": m.get('name', m.get('title', m.get('description', 'Unknown'))),
                     "category": list(m.labels)[0]
                 }
             links.append({
                 "source": str(r.nodes[0].element_id),
                 "target": str(r.nodes[1].element_id),
                 "label": r.type
             })
             
    # Deduplicate links
    unique_links = []
    seen = set()
    for l in links:
        key = (l['source'], l['target'], l['label'])
        if key not in seen:
            seen.add(key)
            unique_links.append(l)
            
    return {
        "nodes": list(nodes.values()),
        "links": unique_links
    }
