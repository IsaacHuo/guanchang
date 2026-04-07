from neo4j import GraphDatabase, Driver
from app.core.config import settings

class Neo4jConnection:
    def __init__(self, uri, user, pwd):
        self._uri = uri
        self._user = user
        self._pwd = pwd
        self._driver = None
        try:
            self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._pwd))
            print("Successfully connected to Neo4j")
        except Exception as e:
            print(f"Failed to create the driver: {e}")

    def close(self):
        if self._driver is not None:
            self._driver.close()

    def query(self, query, parameters=None, db=None):
        assert self._driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self._driver.session(database=db) if db else self._driver.session()
            result = session.run(query, parameters)
            response = list(result)
        except Exception as e:
            print(f"Query failed: {e}")
        finally:
            if session is not None:
                session.close()
        return response

db_conn = Neo4jConnection(settings.NEO4J_URI, settings.NEO4J_USER, settings.NEO4J_PASSWORD)

def get_db():
    return db_conn
