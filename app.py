from pathlib import Path
import io

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image

from matcher import find_matches


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

STATIC_DIR = BASE_DIR / "static"

IMAGE_DIR = BASE_DIR / "data" / "Jewelry Images"


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="AI Jewellery Matcher",
    description="Visual necklace-to-earring recommendation system",
    version="1.0.0"
)


# ============================================================
# FRONTEND
# ============================================================

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)


# ============================================================
# JEWELLERY IMAGE ROUTE
# ============================================================

@app.get("/jewellery-image/{filename}")
def get_jewellery_image(filename: str):

    file_path = IMAGE_DIR / filename

    # Security check
    if file_path.parent != IMAGE_DIR:
        raise HTTPException(
            status_code=400,
            detail="Invalid filename"
        )

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Jewellery image not found"
        )

    return FileResponse(file_path)


# ============================================================
# HOME PAGE
# ============================================================

@app.get("/")
def home():

    return FileResponse(
        STATIC_DIR / "index.html"
    )


# ============================================================
# MATCH API
# ============================================================

@app.post("/match")
async def match_earrings(
    file: UploadFile = File(...)
):

    # --------------------------------------------------------
    # Validate image type
    # --------------------------------------------------------

    allowed_types = {
        "image/jpeg",
        "image/png",
        "image/webp"
    }

    if file.content_type not in allowed_types:

        raise HTTPException(
            status_code=400,
            detail="Please upload JPG, PNG or WEBP image."
        )


    try:

        # ----------------------------------------------------
        # Read uploaded image
        # ----------------------------------------------------

        contents = await file.read()
        if len(contents) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="Image must be smaller than 10 MB."
    )

        # ----------------------------------------------------
        # Convert to PIL image
        # ----------------------------------------------------

        image = Image.open(
            io.BytesIO(contents)
        ).convert("RGB")


        # ----------------------------------------------------
        # Find matching earrings
        # ----------------------------------------------------

        matches = find_matches(
            image,
            top_k=3
        )


        # ----------------------------------------------------
        # Return JSON
        # ----------------------------------------------------

        return {
            "success": True,
            "matches": matches
        }


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )