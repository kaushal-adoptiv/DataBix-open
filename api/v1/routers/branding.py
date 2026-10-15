from fastapi import APIRouter, Response

from auth.dependencies import DatabaseSession
from services.branding import BrandingResponse, load_branding

router = APIRouter(prefix="/branding", tags=["branding"])


@router.get("", response_model=BrandingResponse)
def get_branding(db: DatabaseSession, response: Response) -> BrandingResponse:
    """Public: the login page needs the brand before anyone signs in."""
    # Revalidate every time so a saved brand shows up on the next page load.
    response.headers["Cache-Control"] = "no-cache"
    return load_branding(db)
