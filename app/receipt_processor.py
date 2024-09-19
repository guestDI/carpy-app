import pytesseract
from PIL import Image
import re

def process_receipt_image(image_path: str) -> dict:
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)

    price_match = re.search(r'(\d+[,.]\d{2})', text)  
    date_match = re.search(r'(\d{2}[./-]\d{2}[./-]\d{4})', text) 

    price = price_match.group(1) if price_match else "Cannot find price"
    date = date_match.group(1) if date_match else "Cannot find date"

    return {
        "content": text,
        "price": price,
        "date": date
    }
