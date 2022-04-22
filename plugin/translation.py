# -*- coding: utf-8 -*-
import os
import gettext
from dotenv import load_dotenv

# TODO - Move language option to Flow setting and remove need for dotenv

LOCAL = os.getenv("local", "en")

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

dotenv_path = os.path.join(basedir, ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# localization
translation = gettext.translation("messages", "plugin/translations/", languages=[LOCAL])

_ = translation.gettext
