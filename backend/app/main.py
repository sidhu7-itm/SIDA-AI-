from fastapi import FastAPI, Query, Depends
from app.routers.videos import router as video_router
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException
from app import models, schemas
from app import auth
from app.database import engine, Base, get_db
from fastapi.security import OAuth2PasswordRequestForm
from app.services.video_downloader import download_video
from app.services.transcription import transcribe_video

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(video_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to SIDA AI 🚀"
    }


@app.get("/status")
def status():
    return {
        "status": "online"
    }


@app.get("/about")
def about():
    return {
        "name": "SIDA AI",
        "version": "1.0"
    }


@app.get("/health")
def health():
    return {
        "healthy": True
    }


class VideoRequest(BaseModel):
    youtube_url: str


@app.post("/users", response_model=schemas.UserResponse)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    hashed_password = auth.hash_password(user.password)

    new_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get("/users", response_model=list[schemas.UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)
):
    users = db.query(models.User).all()
    return users

@app.post("/login")
def login(
    user: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not auth.verify_password(
        user.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = auth.create_access_token(
        data={"sub": str(db_user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }



@app.post("/generate", status_code=201)
def generate(
    request: VideoRequest,
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)
):
    new_video = models.Video(
        user_id=int(current_user),
        youtube_url=request.youtube_url
    )

    db.add(new_video)
    db.commit()
    db.refresh(new_video)

    try:
        file_path = download_video(
            request.youtube_url,
            new_video.id
        )
        transcription = transcribe_video(file_path)

        print("\n--- TRANSCRIPTION ---")

        for segment in transcription:
            print(
                f"[{segment['start']:.2f}s - {segment['end']:.2f}s] "
                f"{segment['text']}"
        )

        print("--- TRANSCRIPTION COMPLETED ---\n")
        

        new_video.status = "downloaded"

        db.commit()
        db.refresh(new_video)

    except Exception as e:
        new_video.status = "failed"

        db.commit()

        raise HTTPException(
            status_code=500,
            detail=f"Video download failed: {str(e)}"
        )

    return {
        "message": "Video downloaded successfully!",
        "video_id": new_video.id,
        "user_id": new_video.user_id,
        "url": new_video.youtube_url,
        "status": new_video.status,
        "file_path": file_path
    }

@app.get("/search")
def search_video(
    name: str = Query(
        ...,
        min_length=3,
        max_length=20,
        description="Search for videos"
    )
):
    return {
        "search": name
    }