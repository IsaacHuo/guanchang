#!/usr/bin/env bash

# 出错时退出
set -e

echo "🚀 正在启动 Guanchang (官场档案) 系统..."

# 定义清理函数，使得按下 Ctrl+C 时能同时关闭前后端服务
cleanup() {
    echo ""
    echo "🛑 正在停止所有服务..."
    # 杀死所有的后台子进程
    kill $(jobs -p) 2>/dev/null
    echo "👋 已退出。"
    exit
}

# 捕获 Ctrl+C (SIGINT) 和终止信号 (SIGTERM)
trap cleanup SIGINT SIGTERM

# 1. 启动后端 (FastAPI)
echo "--> 正在启动 FastAPI 后端 (端口: 8000)..."
cd backend
# 使用 uv 极速启动
uv run uvicorn app.main:app --reload --port 8000 &
cd ..

# 2. 启动前端 (Nuxt 3)
echo "--> 正在启动 Nuxt 3 前端 (端口: 3333)..."
cd frontend
export NUXT_TELEMETRY_DISABLED=1
npx nuxt dev &
cd ..

# 3. 打印相关信息
echo "==========================================="
echo "✅ 系统启动中！请稍候几秒钟让服务完全就绪。"
echo "🔗 前端页面: http://localhost:3333"
echo "🔗 后端 API 文档: http://localhost:8000/docs"
echo "==========================================="
echo "💡 (提示: 随时按 Ctrl + C 一键退出全部服务)"

# 挂起主脚本，等待后台任务，保持终端存活
wait