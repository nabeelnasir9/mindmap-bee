import easyocr

def process_image(image_path: str) -> str:
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image_path, detail=0)
    return " ".join(result)
