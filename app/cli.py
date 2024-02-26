import os
from flask import current_app
import click

from app.db import get_db, get_uploads
from app.upload import list_upload_dir, get_upload_path


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


def init_app(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(prune_uploads_command)
