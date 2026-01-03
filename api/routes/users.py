"""
Users API Routes
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List

router = APIRouter()

class UserProfile(BaseModel):
    username: str
    email: str
    full_name: str
    quantum_experience: str = "beginner"
    api_usage: dict = {}

@router.get("/", response_model=List[UserProfile])
async def get_users():
    """Get all users"""
    return [
        UserProfile(
            username="admin",
            email="admin@envr.com",
            full_name="Administrator",
            quantum_experience="expert"
        ),
        UserProfile(
            username="quantum_user",
            email="research@envr.com",
            full_name="Quantum Researcher",
            quantum_experience="intermediate"
        )
    ]

@router.get("/{username}", response_model=UserProfile)
async def get_user(username: str):
    """Get user by username"""
    if username == "admin":
        return UserProfile(
            username="admin",
            email="admin@envr.com",
            full_name="Administrator",
            quantum_experience="expert"
        )
    elif username == "quantum_user":
        return UserProfile(
            username="quantum_user",
            email="research@envr.com",
            full_name="Quantum Researcher",
            quantum_experience="intermediate"
        )
    else:
        raise HTTPException(status_code=404, detail="User not found")
