import threading
import os
from sqlalchemy import TEXT, Column, Numeric, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from config import DB_URI, LOGGER

def start() -> scoped_session:
    try:
        # Handle different database URL formats
        database_url = DB_URI
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        
        # Create engine with better configuration
        engine = create_engine(
            database_url, 
            client_encoding="utf8",
            pool_pre_ping=True,
            pool_recycle=300,
            echo=False
        )
        
        BASE.metadata.bind = engine
        BASE.metadata.create_all(engine)
        
        # Test connection
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        
        LOGGER(__name__).info("✅ Database connected successfully")
        return scoped_session(sessionmaker(bind=engine, autoflush=False))
        
    except Exception as e:
        LOGGER(__name__).error(f"❌ Database connection failed: {e}")
        raise e

BASE = declarative_base()

# Initialize session with error handling
try:
    SESSION = start()
except Exception as e:
    LOGGER(__name__).error(f"Failed to initialize database: {e}")
    SESSION = None

INSERTION_LOCK = threading.RLock()

class Broadcast(BASE):
    __tablename__ = "broadcast"
    id = Column(Numeric, primary_key=True)
    user_name = Column(TEXT)

    def __init__(self, id, user_name):
        self.id = id
        self.user_name = user_name

# Create table with error handling
try:
    if SESSION:
        Broadcast.__table__.create(checkfirst=True)
        LOGGER(__name__).info("✅ Database tables created/verified")
except Exception as e:
    LOGGER(__name__).error(f"Error creating tables: {e}")

# Database operations with better error handling
async def add_user(id, user_name):
    if not SESSION:
        LOGGER(__name__).warning("Database not available")
        return False
    
    try:
        with INSERTION_LOCK:
            msg = SESSION.query(Broadcast).get(id)
            if not msg:
                usr = Broadcast(id, user_name)
                SESSION.add(usr)
                SESSION.commit()
                LOGGER(__name__).info(f"User {id} added to database")
        return True
    except Exception as e:
        LOGGER(__name__).error(f"Error adding user {id}: {e}")
        try:
            SESSION.rollback()
        except:
            pass
        return False

async def delete_user(id):
    if not SESSION:
        return False
    
    try:
        with INSERTION_LOCK:
            SESSION.query(Broadcast).filter(Broadcast.id == id).delete()
            SESSION.commit()
            LOGGER(__name__).info(f"User {id} deleted from database")
        return True
    except Exception as e:
        LOGGER(__name__).error(f"Error deleting user {id}: {e}")
        try:
            SESSION.rollback()
        except:
            pass
        return False

async def full_userbase():
    if not SESSION:
        return []
    
    try:
        users = SESSION.query(Broadcast).all()
        return users
    except Exception as e:
        LOGGER(__name__).error(f"Error getting userbase: {e}")
        return []
    finally:
        try:
            SESSION.close()
        except:
            pass

async def query_msg():
    if not SESSION:
        return []
    
    try:
        result = SESSION.query(Broadcast.id).order_by(Broadcast.id)
        return result
    except Exception as e:
        LOGGER(__name__).error(f"Error querying messages: {e}")
        return []
    finally:
        try:
            SESSION.close()
        except:
            pass
