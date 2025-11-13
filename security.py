from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

app = FastAPI()
security = HTTPBasic()

USERNAME="admin"
PASSWORD="password"  # cleartext password for demo purposes only

@app.get("/secure-data")
def read_secure_data(credentials: HTTPBasicCredentials = Depends(security)):
    # Hardcoded username and password for demo
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return {"message": f"Welcome, {credentials.username}! Access granted."}

@app.get("/un_secure-data")
def read_un_secure_data():
    # incorporate some unsecure data access logic here
    return {"message": "This data is accessible without authentication."}


# To run the app, use the command: uvicorn basic_auth:app --reload

