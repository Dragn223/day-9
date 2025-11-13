from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from jose import jwt
import bcrypt
import secrets
from datetime import datetime, timedelta

# -------------------------------
# Database setup
# -------------------------------
DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)


Base.metadata.create_all(bind=engine)


# -------------------------------
# FastAPI app setup
# -------------------------------
app = FastAPI()
security = HTTPBasic()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # not actually used as form login


# -------------------------------
# JWT Configuration
# -------------------------------
SECRET_KEY = "SUPER_SECRET_KEY_CHANGE_THIS"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# -------------------------------
# Dependencies
# -------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_user(db: Session, username: str, password: str):
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    user = User(username=username, hashed_password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# -------------------------------
# Routes
# -------------------------------

@app.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    if get_user(db, username):
        raise HTTPException(status_code=400, detail="Username already exists")
    create_user(db, username, password)
    return {"message": "User created successfully"}


@app.post("/login")
def login(credentials: HTTPBasicCredentials = Depends(security),
          db: Session = Depends(get_db)):

    user = get_user(db, credentials.username)

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    #  Create JWT access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in_minutes": ACCESS_TOKEN_EXPIRE_MINUTES
    }


@app.get("/protected")
def protected_route(token: str = Depends(oauth2_scheme)):
    """Protected endpoint requiring JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"message": f"Hello {username}, you accessed a protected API!"}