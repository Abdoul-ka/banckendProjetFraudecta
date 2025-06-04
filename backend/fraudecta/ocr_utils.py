import pytesseract
import re
from PIL import Image

def extract_id(image_file):
    img = Image.open(image_file)
    text = pytesseract.image_to_string(img)
    match = re.search(r'\bID[:\s]*([0-9]{4,})', text)
    return match.group(1) if match else None
