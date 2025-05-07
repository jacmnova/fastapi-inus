from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "postgresql://apict:1q2w3e4r@192.168.1.48:5432/centrotransferencia"
DATABASE_URL = "postgresql://postgres:xVikwMFlkdcoItNNtEMNdapmMPgoXosl@gondola.proxy.rlwy.net:21975/railway"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()