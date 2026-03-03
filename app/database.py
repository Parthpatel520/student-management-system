from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from app.config import settings

engine = create_engine(settings.URL,echo=True)

sessionLocal = sessionmaker(bind=engine)

Base = declarative_base()