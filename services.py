from models import Book
from sqlalchemy.orm import Session
from schemas import BookCreate, Book as BookSchema

def create_book(db: Session, book: BookCreate) -> BookSchema:
    db_book = Book(
        title=book.title,
        author=book.author,
        publisher=book.publisher,
        # year=book.year,
        # price=book.price,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_book(db: Session, book_id: int) -> BookSchema | None:
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        return db_book
    return None

def get_books(db: Session, skip: int = 0, limit: int = 10) -> list[BookSchema]:
    books = db.query(Book).offset(skip).limit(limit).all()
    return books

def update_book(db: Session, book_id: int, book: BookCreate) -> BookSchema | None:
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        db_book.title = book.title
        db_book.author = book.author
        db_book.publisher = book.publisher
        db_book.year = book.year
        db_book.price = book.price
        db.commit()
        db.refresh(db_book)
        return db_book
    return None