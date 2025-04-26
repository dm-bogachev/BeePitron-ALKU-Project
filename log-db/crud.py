import models
from sqlalchemy.orm import Session

def add_log_entry(db: Session, log_entry: models.LogEntry):
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return log_entry

def get_log_entries(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.LogEntry).offset(skip).limit(limit).all()

def delete_log_entry(db: Session, log_entry_id: int):
    log_entry = db.query(models.LogEntry).filter(models.LogEntry.id == log_entry_id).first()
    if log_entry:
        db.delete(log_entry)
        db.commit()
        return log_entry
    return None

def create_item(db: Session, name: str):
    db_item = models.Item(name=name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items(db: Session):
    return db.query(models.Item).all()
