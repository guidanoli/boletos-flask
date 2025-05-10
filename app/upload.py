import os
import uuid

from flask import current_app, send_from_directory
from PyPDF2 import PdfReader, PdfWriter


IMAGE = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
PDF = {'pdf'}

def get_upload_dir():
    return current_app.config['UPLOADS_DIR']


def get_upload_path(filename):
    return os.path.join(get_upload_dir(), filename)


def send_upload(filename):
    return send_from_directory(get_upload_dir(), filename)


def generate_filename(ext):
    while True:
        filename = str(uuid.uuid4()) + '.' + ext
        filepath = get_upload_path(filename)
        if not os.path.exists(filepath):
            return filename, filepath


def remove_upload(filename):
    os.remove(get_upload_path(filename))


def get_extension(filename):
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()


def store_upload(file, allowed_extensions, password=None):
    ext = get_extension(file.filename).lower()
    if ext not in allowed_extensions:
        return None, "Unsupported extension"

    filename, filepath = generate_filename(ext)
    file.save(filepath)

    if ext == "pdf":
        from PyPDF2 import PdfReader, PdfWriter
        try:
            reader = PdfReader(filepath)
            if reader.is_encrypted:
                if password is None:
                    return None, "Missing password"
                if not reader.decrypt(password):
                    return None, "Incorrect password"
                writer = PdfWriter()
                for page in reader.pages:
                    writer.add_page(page)
                new_filename, new_filepath = generate_filename("pdf")
                with open(new_filepath, "wb") as f:
                    writer.write(f)
                os.remove(filepath)
                return new_filename, None
        except Exception as e:
            return None, "Error processing PDF"

    return filename, None


def list_upload_dir():
    return os.listdir(get_upload_dir())
