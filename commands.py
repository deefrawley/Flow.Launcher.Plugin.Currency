# -*- coding: utf-8 -*-

import json
import os

import click

from plugin import (
    ICON_PATH,
    PLUGIN_ACTION_KEYWORD,
    PLUGIN_AUTHOR,
    PLUGIN_EXECUTE_FILENAME,
    PLUGIN_ID,
    PLUGIN_PROGRAM_LANG,
    PLUGIN_URL,
    __long_description__,
    __package_name__,
    __short_description__,
    __version__,
    basedir,
)


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


@click.group()
def plugin():
    """Translation and localization commands."""
    ...


@plugin.command()
def gen_plugin_info():
    """Auto generate the `plugin.json` file for Flow"""

    plugin_infos = {
        "ID": PLUGIN_ID,
        "ActionKeyword": PLUGIN_ACTION_KEYWORD,
        "Name": __package_name__.title(),
        "Description": __short_description__,
        "Author": PLUGIN_AUTHOR,
        "Version": __version__,
        "Language": PLUGIN_PROGRAM_LANG,
        "Website": PLUGIN_URL,
        "IcoPath": ICON_PATH,
        "ExecuteFileName": PLUGIN_EXECUTE_FILENAME,
    }

    json_path = os.path.join(basedir, "plugin.json")
    with open(json_path, "w") as f:
        json.dump(plugin_infos, f, indent=" " * 4)

    click.echo("Done.")


cli = click.CommandCollection(sources=[plugin, translate])

if __name__ == "__main__":
    cli()