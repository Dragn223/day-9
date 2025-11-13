from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
import schemas
import services
from db import get_db
 
app = FastAPI()
 
 
 
@app.get("/books/", response_model=list[schemas.Book])
def get_all_books(db: Session = Depends(get_db)):
    return services.get_books(db)
 
@app.get("/books/{book_id}", response_model=schemas.Book)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    book_query_set = services.get_book(db, book_id)   
    if book_query_set:
        return book_query_set
    raise HTTPException(status_code=404, detail="Book not found")
    
 
@app.post("/books/", response_model=schemas.Book)
def create_new_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return services.create_book(db, book)
 
@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book_by_id(book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    updated_book = services.update_book(db, book, book_id)
    if updated_book:
        return updated_book
    raise HTTPException(status_code=404, detail="Book not found, hence no update performed")
 
@app.delete("/books/{book_id}", response_model=schemas.Book)
def delete_book_by_id(book_id: int, db: Session = Depends(get_db)):
    deleted_book = services.delete_book(db, book_id)
    if deleted_book:
        return deleted_book
    raise HTTPException(status_code=404, detail="Book not found, hence no deletion performed")