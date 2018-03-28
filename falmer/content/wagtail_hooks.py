from wagtail.core import hooks

@hooks.register('construct_image_chooser_queryset')
def filter_to_cms_images(images, request):
    # Only show uploaded images
    images = images.filter(internal_source=100)

    return images
