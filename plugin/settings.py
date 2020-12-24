# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

dotenv_path = os.path.join(basedir, ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


# The default value can work, if no user config.
LOCAL = os.getenv("local", "en")


ICON_PATH = "assets/favicon.ico"

# the information of package
__package_name__ = "Flow.Launcher.Plugin.Currency"
__version__ = "1.0.0"
__short_description__ = (
    "Currency converter using the euro and rates at https://www.ecb.europa.eu/"
)
GITHUB_USERNAME = "deefrawley"


readme_path = os.path.join(basedir, "README.md")
try:
    __long_description__ = open(readme_path, "r").read()
except:
    __long_description__ = __short_description__


# other information
PLUGIN_ID = "18892b78-63ac-43ab-a278-59a5a2866dd8"
ICON_PATH = "assets/favicon.ico"
PLUGIN_ACTION_KEYWORD = "cc"
PLUGIN_AUTHOR = "deefrawley"
PLUGIN_PROGRAM_LANG = "python"
PLUGIN_URL = f"https://github.com/{GITHUB_USERNAME}/{__package_name__}"
PLUGIN_EXECUTE_FILENAME = "main.py"
