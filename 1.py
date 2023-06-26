
from PIL import Image, ImageFilter, ImageEnhance

def apply_filter(image_path, filter_type):
    img = Image.open(image_path)

    if filter_type == "BLUR":
        img = img.filter(ImageFilter.BLUR)
    elif filter_type == "BRIGHTNESS":
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.5)
    elif filter_type == "CONTRAST":
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.5)
    elif filter_type == "SHARPNESS":
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(2)

    img.show()

apply_filter("sample.jpg", "BRIGHTNESS")
