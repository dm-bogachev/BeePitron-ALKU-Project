from sqlalchemy import Column, Integer, String
from database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class LogEntry(Base):
    __tablename__ = "log_entries"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(String, index=True)  # Date and time of the log
    log_type = Column(String, index=True)  # Type of log (e.g., warning, error, etc.)
    message = Column(String)  # Text of the log message
    details = Column(String, nullable=True)  # Additional details (optional)