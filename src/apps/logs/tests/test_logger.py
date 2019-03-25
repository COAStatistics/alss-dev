from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from apps.logs.models import ReviewLog
import logging


class ModelTestCase(TestCase):
    def setUp(self):
        self.logger = logging.getLogger('review')

    def test_logger(self):
        self.logger.error({'test_error': 'this is a test error message'}, extra={
            'object_id': 1,
            'content_type': ContentType.objects.filter(app_label='surveys18', model='survey').first(),
            'user': User.objects.first(),
        })
        self.assertEqual(1, ReviewLog.objects.count())




