import logging

from django.contrib.auth.models import Group, Permission
from django.db.models import Q
from rest_framework.authtoken.models import Token

from apps.users.models import User


logger = logging.getLogger("console")


def create_groups():
    """Initial three groups base on model permissions"""

    if not Group.objects.filter(name='後台管理員').exists():
        admin = Group.objects.create(name='後台管理員')
        for permission in Permission.objects.filter(content_type__app_label='users'):
            admin.permissions.add(permission)

    if not Group.objects.filter(name='106年審表員').exists():
        auditor106 = Group.objects.create(name='106年審表員')
        for permission in Permission.objects.filter(
                content_type__app_label='surveys18',
                content_type__model='survey'
        ).exclude(Q(codename='delete_survey') | Q(codename='add_survey')):
            auditor106.permissions.add(permission)

    if not Group.objects.filter(name='107年審表員').exists():
        auditor107 = Group.objects.create(name='107年審表員')
        for permission in Permission.objects.filter(
                content_type__app_label='surveys19',
                content_type__model='survey'
        ).exclude(Q(codename='delete_survey') | Q(codename='add_survey')):
            auditor107.permissions.add(permission)

        logger.info(
            f"""

These user groups have been created: '後台管理員', '106年審表員', '107年審表員' ...

"""
        )


def create_superuser():
    """Initial fake superuser only for testing. Use in docker-compose."""
    email = "admin@atri.org"
    password = "123456"
    mobile = "0900000000"

    if not User.objects.filter(email=email).exists():
        user = User.objects.create_user(
            email=email,
            password=password,
            full_name="Test Superuser",
            mobile=mobile,
            is_staff=True,
            is_superuser=True,
        )
        token = Token.objects.create(user=user)
        logger.info(
            f"""

Your initial superuser has been set for testing, use this user to sign in Django admin:

    Email: {email}
    Password: {password}

Use this token for testing:

    Authorization: Token {token}
"""
        )


def create_staff():
    """Initial fake staff only for testing. Use in docker-compose."""

    email = "staff@atri.org"
    password = "123456"
    mobile = "0900000001"

    if not User.objects.filter(email=email).exists():

        user = User.objects.create_user(
            email=email,
            password=password,
            full_name="Test Staff",
            mobile=mobile,
            is_staff=True,
            is_superuser=False,
        )
        for group in Group.objects.filter(Q(name='後台管理員') | Q(name='106年審表員') | Q(name='107年審表員')):
            user.groups.add(group)

        logger.info(
            f"""

An staff has been create, grant to groups: '後台管理員', '106年審表員', '107年審表員':

    Email: {email}
    Password: {password}
"""
        )


def create_auditor106():
    """Initial fake auditor only for testing. Use in docker-compose."""

    email = "auditor106@atri.org"
    password = "123456"
    mobile = "0900000002"

    if not User.objects.filter(email=email).exists():

        user = User.objects.create_user(
            email=email,
            password=password,
            full_name="106年測試審表員",
            mobile=mobile,
            is_staff=False,
            is_superuser=False,
        )
        for group in Group.objects.filter(Q(name='106年審表員')):
            user.groups.add(group)

        logger.info(
            f"""

An auditor has been create, grant to groups: '106年審表員':

    Email: {email}
    Password: {password}
"""
        )


def create_auditor107():
    """Initial fake auditor only for testing. Use in docker-compose."""

    email = "auditor107@atri.org"
    password = "123456"
    mobile = "0900000003"

    if not User.objects.filter(email=email).exists():

        user = User.objects.create_user(
            email=email,
            password=password,
            full_name="107年測試審表員",
            mobile=mobile,
            is_staff=False,
            is_superuser=False,
        )
        for group in Group.objects.filter(Q(name='107年審表員')):
            user.groups.add(group)

        logger.info(
            f"""

An auditor has been create, grant to groups: '107年審表員':

    Email: {email}
    Password: {password}
"""
        )
