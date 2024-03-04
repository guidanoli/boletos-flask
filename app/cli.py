import os
from flask import current_app
import click
import tarfile

from app.db import get_db, get_uploads
from app.upload import list_upload_dir, get_upload_path, generate_filename


def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def prune_uploads():
    uploads_in_db = set(get_uploads())
    uploads_in_dir = set(list_upload_dir())

    for upload in uploads_in_db - uploads_in_dir:
        click.echo(click.style('Warning: {} in database but not in directory'.format(upload), fg='yellow'))

    for upload in uploads_in_dir - uploads_in_db:
        os.remove(get_upload_path(upload))
        click.echo(click.style('Removed: {} in directory but not in database'.format(upload), fg='green'))


@click.command('prune-uploads')
def prune_uploads_command():
    """Remove uploads that are not referenced in the database."""
    prune_uploads()
    click.echo('Pruned uploads.')


@click.command('generate-upload-name')
@click.option('--ext', required=True)
def generate_upload_name_command(ext):
    """Generate a unique name for an upload."""
    filename, filepath = generate_filename(ext)
    click.echo('Name: {}'.format(filename))
    click.echo('Path: {}'.format(filepath))


def backup(output_file):
    with tarfile.open(output_file, mode='x:xz') as tar:
        tar.add(current_app.instance_path)

@click.command('backup')
@click.option('--output-file', default='boletos.tar.xz')
def backup_command(output_file):
    """Store a backup of the application instance directory."""
    backup(output_file)
    click.echo('Backup stored in {}.'.format(output_file))


def init_app(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(prune_uploads_command)
    app.cli.add_command(generate_upload_name_command)
    app.cli.add_command(backup_command)
