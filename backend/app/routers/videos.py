from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app import models, auth
from app.database import get_db


router = APIRouter(
    prefix="/videos",
    tags=["Videos"]
)


@router.get("/{video_id}")
def get_video(
    video_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)
):
    video = db.query(models.Video).filter(
        models.Video.id == video_id,
        models.Video.user_id == int(current_user)
    ).first()

    if not video:
        raise HTTPException(
            status_code=404,
            detail="Video not found"
        )

    return {
        "id": video.id,
        "user_id": video.user_id,
        "youtube_url": video.youtube_url,
        "status": video.status
    }