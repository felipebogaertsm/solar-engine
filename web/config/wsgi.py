# -*- coding: utf-8 -*-
# Copyright © Felipe Bogaerts de Mattos
# Contact: me@felipebm.com

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
