import pytesseract
from PIL import Image
import easyocr


try:
    reader = easyocr.Reader(['en']) 
    text = reader.readtext('image.jpeg', detail=0)
    print(text)
except Exception as e:
    print("An error has occurred.")