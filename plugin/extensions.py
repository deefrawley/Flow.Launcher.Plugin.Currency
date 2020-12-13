# -*- coding: utf-8 -*-

import gettext

from plugin.settings import LOCAL

# localization
translation = gettext.translation("messages", "plugin/translations/", languages=[LOCAL])

_ = translation.gettext