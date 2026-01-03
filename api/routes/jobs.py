"""
Quantum Jobs API Routes
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

router = APIRouter()

class QuantumJob(BaseModel):
    job_id: str
    circuit_name: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime]
    results: Optional[dict]
    backend: str

# Mock job database
jobs_db = []

@router.get("/", response_model=List[QuantumJob])
async def get_jobs():
    """Get all quantum jobs"""
    return jobs_db

@router.get("/{job_id}", response_model=QuantumJob)
async def get_job(job_id: str):
    """Get job by ID"""
    for job in jobs_db:
        if job.job_id == job_id:
            return job
    raise HTTPException(status_code=404, detail="Job not found")

@router.post("/submit")
async def submit_job(circuit_name: str, backend: str = "qasm_simulator"):
    """Submit a new quantum job"""
    job_id = str(uuid.uuid4())[:8]
    new_job = QuantumJob(
        job_id=job_id,
        circuit_name=circuit_name,
        status="pending",
        created_at=datetime.now(),
        backend=backend,
        results=None
    )
    jobs_db.append(new_job)
    
    # Simulate job completion
    new_job.status = "completed"
    new_job.completed_at = datetime.now()
    new_job.results = {"00": 512, "11": 512}
    
    return {"job_id": job_id, "message": "Job submitted successfully"}
