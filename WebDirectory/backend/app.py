from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional
import uvicorn

from .scanner import ScanConfig, start_scan
from .database import get_scan_history, delete_scan_record

app = FastAPI(title="WebDirectory API")

class ScanRequest(BaseModel):
    domain: str = Field(..., description="Target domain, e.g., https://example.com")
    max_depth: Optional[int] = Field(3, ge=1, le=10, description="Maximum crawl depth")
    max_urls: Optional[int] = Field(1000, ge=10, description="Maximum URLs to fetch")
    request_delay: Optional[float] = Field(0.5, ge=0.0, description="Delay between requests (seconds)")
    timeout: Optional[float] = Field(10.0, ge=1.0, description="HTTP request timeout (seconds)")
    wordlist_path: Optional[str] = Field(None, description="Path to optional wordlist for directory brute‑forcing")

class ScanResult(BaseModel):
    scan_id: str
    status: str
    discovered: int
    duration_seconds: Optional[float]

@app.post("/scan", response_model=ScanResult)
async def launch_scan(request: ScanRequest, background_tasks: BackgroundTasks):
    # Basic domain validation / normalization
    if not request.domain.startswith("http://") and not request.domain.startswith("https://"):
        target = f"https://{request.domain}"  # default to https
    else:
        target = request.domain
    # Prevent disallowed targets (localhost / private IPs) – simplified placeholder
    if any(forbidden in target for forbidden in ["localhost", "127.0.0.1", "10.", "172.", "192.168."]):
        raise HTTPException(status_code=400, detail="Scanning of private/internal hosts is not allowed.")
    config = ScanConfig(
        target=target,
        max_depth=request.max_depth,
        max_urls=request.max_urls,
        request_delay=request.request_delay,
        timeout=request.timeout,
        wordlist_path=request.wordlist_path,
    )
    scan_id = await start_scan(config, background_tasks)
    return ScanResult(scan_id=scan_id, status="queued", discovered=0)

@app.get("/scan/{scan_id}")
async def get_scan_status(scan_id: str):
    # In a real implementation this would query the DB for progress.
    # Here we return a stub.
    return {"scan_id": scan_id, "status": "in_progress", "discovered": 0}

@app.get("/history")
async def history():
    return get_scan_history()

@app.delete("/history/{scan_id}")
async def delete_history(scan_id: str):
    delete_scan_record(scan_id)
    return {"deleted": scan_id}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
