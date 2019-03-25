import logging
from datetime import datetime, timedelta

from rest_framework.authtoken.models import Token

from apps.users.models import User


logger = logging.getLogger('console')


def create_superuser():
    """Initial fake superuser only for testing. Use in docker-compose."""
    email = 'test@test.test'
    password = '123456'
    mobile = '0912345678'
    if not User.objects.count():
        user = User.objects.create_user(email=email, password=password,
                                        full_name='Test Superuser', mobile=mobile,
                                        is_staff=True, is_superuser=True)
        token = Token.objects.create(user=user)
        logger.info(f"""

Your initial superuser has been set for testing, use this user to sign in Django admin:

    Email: {email}
    Password: {password}

Use this token for testing:

    Authorization: Token {token}

""")


create_superuser()
