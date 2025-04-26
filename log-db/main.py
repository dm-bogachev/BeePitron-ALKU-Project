from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, crud, database, schemas

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.post("/items/")
def create_item(name: str, db: Session = Depends(database.get_db)):
    return crud.create_item(db=db, name=name)

@app.get("/items/")
def read_items(db: Session = Depends(database.get_db)):
    return crud.get_items(db=db)

@app.post("/log_entries/")
def create_log_entry(log_entry: schemas.LogEntryCreate, db: Session = Depends(database.get_db)):
    # Adjust the CRUD function accordingly to accept the Pydantic schema.
    return crud.add_log_entry(db=db, log_entry=log_entry)

@app.get("/log_entries/")
def read_log_entries(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return crud.get_log_entries(db=db, skip=skip, limit=limit)

@app.delete("/log_entries/{log_entry_id}")
def delete_log_entry(log_entry_id: int, db: Session = Depends(database.get_db)):
    result = crud.delete_log_entry(db=db, log_entry_id=log_entry_id)
    if not result:
        raise HTTPException(status_code=404, detail="Log entry not found")
    return {"message": "Log entry deleted"}

@app.get("/log_entries/{log_entry_id}")
def read_log_entry(log_entry_id: int, db: Session = Depends(database.get_db)):
    log_entry = db.query(models.LogEntry).filter(models.LogEntry.id == log_entry_id).first()
    if log_entry:
        return log_entry
    raise HTTPException(status_code=404, detail="Log entry not found")
