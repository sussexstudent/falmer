def create_image_from_bytes(file, file_name):
    from .models import MatteImage
    image = MatteImage()
    image.file = file
    image.title = file_name
    image.save()

    return image
