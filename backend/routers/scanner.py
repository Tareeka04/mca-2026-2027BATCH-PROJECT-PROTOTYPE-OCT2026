"""
Fridge Scanner Router.
Answers: "What can I make from ingredients visible in my fridge?"
"""
from typing import List
from fastapi import APIRouter, File, UploadFile, HTTPException
from backend.core.image_classifier import FridgeScanner

router = APIRouter(prefix="/api/scanner", tags=["scanner"])

@router.post("/detect")
async def detect_fridge_ingredients(file: UploadFile = File(...)):
    """
    Process an uploaded fridge image and return detected ingredient tags with confidence scores.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image (PNG, JPG, JPEG, WEBP)")

    try:
        contents = await file.read()
        detections = FridgeScanner.process_image_bytes(contents)
        return {
            "filename": file.filename,
            "detected_count": len(detections),
            "detections": detections
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image processing error: {str(e)}")
