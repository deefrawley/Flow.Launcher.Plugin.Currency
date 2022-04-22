# -*- coding: utf-8 -*-
import os
import click


@click.group()
def translate():
    """Translation and localization commands."""
    ...


@translate.command()
@click.argument("locale")
def init(locale):
    """Initialize a new language."""

    if os.system("pybabel extract -F babel.cfg -k _l -o messages.pot ."):
        raise RuntimeError("extract command failed")
    if os.system("pybabel init -i messages.pot -d plugin/translations -l " + locale):
        raise RuntimeError("init command failed")
    os.remove("messages.pot")

    click.echo("Done.")


@translate.command()
def update():
    """Update all languages."""
    if os.system("pybabel extract -F babel.cfg -k _l -o messages.pot ."):
        raise RuntimeError("extract command failed")
    if os.system("pybabel update -i messages.pot -d plugin/translations"):
        raise RuntimeError("update command failed")
    os.remove("messages.pot")

    click.echo("Done.")


@translate.command()
def compile():
    """Compile all languages."""
    if os.system("pybabel compile -d plugin/translations"):
        raise RuntimeError("compile command failed")

    click.echo("Done.")


cli = click.CommandCollection(sources=[translate])

if __name__ == "__main__":
    cli()
