def create_image_from_bytes(file, file_name, internal_source):
    from .models import MatteImage
    image = MatteImage()
    image.file = file
    image.title = file_name
    image.internal_source = internal_source
    image.save()

    return image
