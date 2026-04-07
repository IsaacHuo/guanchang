from app.core.database import db_conn

class GraphService:
    @staticmethod
    def create_official(name: str, gender: str = None, birth_date: str = None, identifier: str = None):
        """创建或更新官员节点 (Person/Official)"""
        query = """
        MERGE (o:Official {name: $name})
        ON CREATE SET o.identifier = $identifier, o.gender = $gender, o.birth_date = $birth_date, o.created_at = datetime()
        ON MATCH SET o.gender = coalesce($gender, o.gender), o.birth_date = coalesce($birth_date, o.birth_date)
        RETURN o
        """
        result = db_conn.query(query, parameters={
            "name": name, 
            "identifier": identifier, 
            "gender": gender, 
            "birth_date": birth_date
        })
        return result[0]['o'] if result else None

    @staticmethod
    def create_position(title: str):
        """创建职务节点 (Position)"""
        query = """
        MERGE (p:Position {title: $title})
        ON CREATE SET p.created_at = datetime()
        RETURN p
        """
        result = db_conn.query(query, parameters={"title": title})
        return result[0]['p'] if result else None

    @staticmethod
    def create_organization(name: str, org_type: str = None):
        """创建组织/机构节点 (Organization)"""
        query = """
        MERGE (org:Organization {name: $name})
        ON CREATE SET org.type = $org_type, org.created_at = datetime()
        RETURN org
        """
        result = db_conn.query(query, parameters={"name": name, "org_type": org_type})
        return result[0]['org'] if result else None

    @staticmethod
    def add_held_position(official_name: str, position_title: str, organization_name: str = None, start_date: str = None, end_date: str = None):
        """
        创建关系：Official -[HELD_POSITION]-> Position
        如果提供了机构，同时创建 Position -[BELONGS_TO]-> Organization
        """
        query_parts = [
            "MATCH (o:Official {name: $official_name})",
            "MATCH (p:Position {title: $position_title})"
        ]
        
        # Merge relationship
        query_parts.append("""
        MERGE (o)-[r:HELD_POSITION]->(p)
        ON CREATE SET r.start_date = $start_date, r.end_date = $end_date
        ON MATCH SET r.start_date = coalesce($start_date, r.start_date), r.end_date = coalesce($end_date, r.end_date)
        """)
        
        # Optional organization link
        if organization_name:
            query_parts.append("""
            WITH o, p, r
            MERGE (org:Organization {name: $organization_name})
            MERGE (p)-[:BELONGS_TO]->(org)
            """)
            
        query_parts.append("RETURN o, r, p")
        
        result = db_conn.query("\n".join(query_parts), parameters={
            "official_name": official_name,
            "position_title": position_title,
            "organization_name": organization_name,
            "start_date": start_date,
            "end_date": end_date
        })
        return result

    @staticmethod
    def add_investigation_event(official_name: str, event_desc: str, date: str):
        """记录落马/被查事件"""
        query = """
        MATCH (o:Official {name: $official_name})
        MERGE (e:Event:Investigation {description: $event_desc, date: $date})
        MERGE (o)-[r:INVESTIGATED_FOR]->(e)
        RETURN e
        """
        result = db_conn.query(query, parameters={
            "official_name": official_name,
            "event_desc": event_desc,
            "date": date
        })
        return result[0]['e'] if result else None
