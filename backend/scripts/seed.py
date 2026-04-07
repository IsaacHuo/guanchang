import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.graph_service import GraphService

def seed_initial_data():
    print("🌱 正在向 Neo4j 插入系统初始测试数据...")
    try:
        # Person 1
        GraphService.create_official("李雷", "男", "1965-01")
        GraphService.create_position("市委书记")
        GraphService.create_organization("A市委")
        GraphService.add_held_position("李雷", "市委书记", "A市委", "2015-01", "2020-01")
        
        # Person 2
        GraphService.create_official("韩梅梅", "女", "1970-05")
        GraphService.create_position("副市长")
        GraphService.create_organization("A市政府")
        GraphService.add_held_position("韩梅梅", "副市长", "A市政府", "2016-01", "2021-01")
        GraphService.add_investigation_event("韩梅梅", "涉嫌严重违纪违法接受纪律审查", "2021-02-10")

        # Person 3
        GraphService.create_official("王刚", "男", "1968-08")
        GraphService.create_position("局长")
        GraphService.create_organization("A市公安局")
        GraphService.add_held_position("王刚", "局长", "A市公安局", "2010-01", "2018-01")
        GraphService.add_investigation_event("王刚", "严重违纪违法被双开", "2018-05-12")
        
        print("✅ 初始演示关系数据插入成功！图形网络已有基本实体。")
    except Exception as e:
        print(f"❌ 数据插入失败，请确保 Neo4j 正在运行中。({e})")

if __name__ == "__main__":
    seed_initial_data()