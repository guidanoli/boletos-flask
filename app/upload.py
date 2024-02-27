import os
import uuid

from flask import current_app, send_from_directory


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


def store_upload(file, allowed_extensions):
    ext = get_extension(file.filename)
    if ext in allowed_extensions:
        filename, filepath = generate_filename(ext)
        file.save(filepath)
        return filename


def list_upload_dir():
    return os.listdir(get_upload_dir())
