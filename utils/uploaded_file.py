from PIL import Image, ImageOps
from django.core.files.uploadedfile import SimpleUploadedFile

from utils.cropped_thumbnail import cropped_thumbnail


def fake_uploaded_file(file_path, mime_type):
    with open(file_path, 'rb') as fh:
        suf = SimpleUploadedFile(file_path.split('/')[-1], fh.read(), mime_type)
        suf.seek(0)
        return suf


def resize_image(path, w, h):
    file = Image.open(path)
    file = ImageOps.exif_transpose(file)
    file.thumbnail((w, h))
    file = file.convert('RGB')
    file.save(path, "JPEG", quality=100, optimize=False)
    return path
