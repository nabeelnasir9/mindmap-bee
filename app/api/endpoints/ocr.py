from fastapi import APIRouter, File, UploadFile, HTTPException
from app.utils.ocr import process_image
import shutil

router = APIRouter()


@router.post("/notes/image-to-text")
async def image_to_text(file: UploadFile = File(...)):
    try:
        # Save the uploaded file temporarily
        temp_file_path = f"temp/{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Process the image to extract text
        text = process_image(temp_file_path)
        return {"text": text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
