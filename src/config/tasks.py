from __future__ import absolute_import, unicode_literals
import logging
from celery.task import task

import datetime
import time

from django.core.mail import EmailMessage
from django.conf import settings

db_logger = logging.getLogger('aprp')
