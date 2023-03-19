from PIL import Image


def resize_image(img, max_width, max_height):
    original_width, original_height = img.size

    aspect_ratio = original_width / original_height

    new_width = min(original_width, max_width)
    new_height = int(new_width / aspect_ratio)
    if new_height > max_height:
        new_height = max_height
        new_width = int(new_height * aspect_ratio)

    resized_image = img.resize((new_width, new_height), Image.LANCZOS)

    return resized_image
