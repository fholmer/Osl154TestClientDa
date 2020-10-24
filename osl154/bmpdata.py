import os
from PIL import Image, ImageDraw

def create_bmp_data(tag, width, height):
    root = "data"
    os.makedirs(os.path.join(root,tag), exist_ok=True)
    img = Image.new('RGB', (width, height), color = (0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([(1,1), (width-2, height-2)], outline=(255,255,255))
    d.text((4,4),  "R", fill=(255, 0, 0), align="center")
    d.text((28,4), "G", fill=(0, 255, 0), align="center")
    d.text((56,4), "B", fill=(0, 0, 255), align="center")
    d.multiline_text((4,32), "Test of\nRGB Sign", fill=(255, 255, 255), align="center")
    img.save(os.path.join(root, tag, "1.bmp"))
