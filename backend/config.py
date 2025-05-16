from neomodel import config
import os
from dotenv import load_dotenv

load_dotenv()

NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "2kJAHn195lk")
NEO4J_HOST = os.getenv("NEO4J_HOST", "v2202411241288295404.powersrv.de")
NEO4J_PORT = os.getenv("NEO4J_BOLT_PORT", "7687")

config.DATABASE_URL = f'bolt://{NEO4J_USER}:{NEO4J_PASSWORD}@{NEO4J_HOST}:{NEO4J_PORT}'