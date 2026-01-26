from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.services.youtube_analysis import run_youtube_analysis
from src.services.fx import get_fx_rates, FXError

router = APIRouter()


# ---------- MODELS ----------

class AnalysisRequest(BaseModel):
    youtube_url: str = Field(..., min_length=3)
    video_count: int = Field(default=8, ge=1, le=25)


# ---------- ROUTES ----------

@router.get("/health")
def health():
    """
    Simple health check to verify the API is running.
    """
    return {"status": "ok"}


@router.post("/analysis")
def analyse(req: AnalysisRequest):
    """
    Run YouTube influencer analysis.
    """
    try:
        return run_youtube_analysis(
            req.youtube_url,
            video_count=req.video_count,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/fx")
def fx(base: str = "USD", symbols: str = "ZAR,EUR,GBP"):
    """
    Get cached FX rates.
    Example:
      /api/fx?base=USD&symbols=ZAR,EUR,GBP
    """
    try:
        symbol_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]
        return get_fx_rates(base=base, symbols=symbol_list)
    except FXError as e:
        raise HTTPException(status_code=502, detail=str(e))

