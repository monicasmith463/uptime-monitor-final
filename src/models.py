from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Site(Base):
    __tablename__ = "site"
    id = Column(Integer, primary_key=True)
    url= Column(String, unique=True, nullable=False)
    name = Column( String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    health_checks = relationship("HealthCheck", back_populates="site")




class HealthCheck(Base):
    __tablename__ = "health_checks"
    id = Column(Integer, primary_key=True)
    site_id = Column(Integer, ForeignKey('site.id'))
    response_time = Column(Float, nullable=True)
    status_code = Column(Integer, nullable=True)
    error = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    site = relationship("Site", back_populates="health_checks")






