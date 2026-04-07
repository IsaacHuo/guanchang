# ✦ GuanChang (官场档案) - 自动化官员变动与深度利益图谱抽取系统

GuanChang 是一个数据可视化追踪平台，结合了最新的**无头浏览器异步爬虫**、**大语言模型零样本提取(DeepSeek)**以及**图数据库(Neo4j)**。系统旨在自动化监测各大公检法机构（如最高检等）官网，实时抓取并解析官员的任免、落马及违纪通报，将非结构化新闻提炼为结构化的实体节点图谱，并在前端通过赛博朋克风格的大盘看板进行点线跟踪展示。

## 🌟 核心特性
- 🕸️ **幽灵爬虫系统**：基于 `async_playwright`，成功绕过官方网站（如 spp.gov.cn）严格的 Akamai / JS 反爬盾。
- 🧠 **AI 深度抽取**：全面接入 **DeepSeek API**，从数百字的冗长通报中精准抽离出：人物（姓名、性别、年龄）、职位、机构以及违纪事实/落马日志。
- 🗄️ **图谱网络引擎**：使用 **Neo4j** 底层驱动，智能自动合并(MERGE)人物、职位、机构及事件节点，支持亿级关系网络穿透运算。
- 📊 **赛博数据看板大屏**：基于 Nuxt 3 与 TailwindCSS 构建深色主题仪表盘。集成 ECharts 力导向图 (Force-Directed Graph)，全局数据每 10 秒静默轮询，后台抓取动态即刻呈现在屏幕前。
- 🔍 **全库秒级检索**：支持按照官员姓名、特征进行全时空履历和案卷回溯。

## 🛠️ 技术栈
- **前端 (Frontend)**: Nuxt 3, Vue 3, Tailwind CSS, ECharts
- **后端 (Backend)**: Python 3.12, FastAPI, Uvicorn 
- **依赖管理**: `uv` (极致迅速的 Python 包管理工具)
- **数据库 (Database)**: Neo4j (Docker 部署)
- **抽取与抓取 (Data/AI)**: Playwright Chromium, BeautifulSoup4, OpenAI SDK (代理 DeepSeek 模型) 

## 📂 项目结构
```text
guanchang/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI 主入口、核心路由 (Stats, Search, Network)
│   │   ├── core/
│   │   │   ├── config.py            # 环境变量配置
│   │   │   └── database.py          # Neo4j 数据库连接与查询封装
│   │   ├── models/                  # 数据结构模型
│   │   └── services/
│   │       ├── crawler_service.py   # Playwright 网页抓取服务
│   │       ├── graph_service.py     # Cypher 语句及图谱实体构建业务
│   │       └── llm_service.py       # DeepSeek NLP 分析及 JSON 结构化格式化
│   ├── scripts/
│   │   ├── run_crawler.py           # 自动化批量爬行入口脚本
│   │   └── seed.py                  # 初始样本种子入库脚本
│   ├── pyproject.toml               # 后端 uv 依赖配置
│   └── .env                         # 后端密钥及配置（未追踪提交）
├── frontend/
│   ├── app.vue                      # 核心大盘 UI 与暗黑主题组件
│   ├── nuxt.config.ts               # Nuxt 3 设置与 Tailwind 整合
│   └── package.json                 # 前端依赖 Node 模块
├── docker-compose.yml               # Neo4j 基础设施启动配置
└── start.sh                         # 全局项目一键部署/后台维持脚本
```

## 🚀 快速启动指南

### 1. 环境准备
确保你的电脑上安装好了 `docker`, `docker-compose`, `node` (推荐 v18+), 以及 `uv` (可以用 `curl -LsSf https://astral.sh/uv/install.sh | sh` 安装)。

### 2. 配置环境变量
在 `backend` 根目录下创建 `.env` 文件，内容如下：
```env
# 你的 DeepSeek API 密钥
OPENAI_API_KEY="sk-xxxxxxx"
# 使用了 OpenAI SDK 的兼容端点
OPENAI_API_BASE="https://api.deepseek.com/v1"

# 本地 Neo4j 设置
NEO4J_URI="bolt://localhost:7687"
NEO4J_USER="neo4j"
NEO4J_PASSWORD="your-strong-password"
```

### 3. 启动图数据库
在项目的根目录启动 Neo4j 服务：
```bash
docker-compose up -d
```

### 4. 启动后端环境 (FastAPI)
```bash
cd backend
uv sync
uv run playwright install chromium   # 必须安装无头浏览器引擎
uv run uvicorn app.main:app --reload --port 8000
```

### 5. 启动前端大盘 (Nuxt 3)
新开一个终端窗口：
```bash
cd frontend
npm install
npm run dev
```
前端启动后，打开浏览器访问 `http://localhost:3333` 即可看到赛博大屏看板。

### 6. 开始猎取数据
新开一个终端窗口跑起无限制后台爬行动力引擎。脚本将自动绕开防护墙获取全网最新履历：
```bash
cd backend
uv run python scripts/run_crawler.py
```
> *注项：后台只要探测出新的案件与官员，前台的大屏节点数量和关系连线将自动上涨和连结。*

## 📜 免责声明
> 本项目代码仅供技术架构演示、网络图谱研究和深度学习(LLM)抽取探索。不要对爬虫进行激进的并发魔改以免增加对方目标站点的负担。
