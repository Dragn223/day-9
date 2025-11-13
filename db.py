from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = (
    "postgresql://neondb_owner:npg_YtT4Gm9LEOoX@"
    "ep-ancient-queen-adol6505-pooler.c-2.us-east-1.aws.neon.tech/"
    "neondb?sslmode=require&channel_binding=require"
)

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# Dependency for FastAPI or script use
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Function to create all tables
def create_tables():
    from models import Book  # ✅ Import model here so metadata registers
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")
