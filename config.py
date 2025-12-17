from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
ALEMBIC_DATABASE_URL = os.getenv("ALEMBIC_DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")     


