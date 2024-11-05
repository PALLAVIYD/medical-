from fastapi import FastAPI, Depends, HTTPException, status,Form
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, User, MoodTracking
from schemas import UserCreate, UserResponse, UserLogin, MoodData
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("api_key"))
model = genai.GenerativeModel("gemini-1.5-flash-latest")


app = FastAPI()
# Add the following CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, but you can restrict this to specific domains
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods like GET, POST, etc.
    allow_headers=["*"],  # Allows all headers
)

# Initialize the app


# Initialize the database
Base.metadata.create_all(bind=engine)

# Password hashing utility
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Hash password utility
def get_password_hash(password):
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Register a new user
@app.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    # Create new user
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password,email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# User login
@app.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    print([i.email for i in db.query(User).all()])
    db_user = db.query(User).filter(User.email == user.email).first()
    print(db_user)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"message": "Login successful"}

# Chatbot API - Empty Implementation
@app.post("/chatbot")
async def chatbot(prompt: str = Form(...)):  # Use Form to extract form data
    result = model.generate_content(f"User: {prompt}, respond as a mental health help chatbot and no formating ")
    print(result.text)  # This will show in your server logs
    return {"message": result.text}


@app.post("/submit_mood")
async def submit_mood(mood_data: MoodData):
    db = SessionLocal()
    db_mood = MoodTracking(mood_description=mood_data.mood_description, mood=mood_data.mood)
    db.add(db_mood)
    db.commit()
    db.refresh(db_mood)
    db.close()
    return {"message": "Mood data successfully saved!", "data": mood_data}