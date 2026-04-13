from fastapi import APIRouter
import random

router = APIRouter(prefix="/api/v1/noise", tags=["noise"])

@router.get("/current")
async def get_current_noise():
    return {"score": round(random.uniform(0.0, 1.0), 3), "threshold": 0.85}
