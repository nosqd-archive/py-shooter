from pyray import *

IMAGE_REGISTRY = {}
TEXTURE_REGISTRY = {}


def load_imageres(path: str):
    global IMAGE_REGISTRY, TEXTURE_REGISTRY
    if path not in IMAGE_REGISTRY:
        IMAGE_REGISTRY[path] = load_image("res/" + path)

    def closure():
        if path not in TEXTURE_REGISTRY:
            TEXTURE_REGISTRY[path] = load_texture_from_image(IMAGE_REGISTRY[path])
        return TEXTURE_REGISTRY[path]
    return closure
