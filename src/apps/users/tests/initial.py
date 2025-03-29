import logging
import abc
from django.contrib.auth.models import Group, Permission
from django.db.models import Q
from rest_framework.authtoken.models import Token

from apps.users.models import User


logger = logging.getLogger("console")


def create_groups():
    """Initial groups base on model permissions"""

    if not Group.objects.filter(name="後台管理員").exists():
        admin = Group.objects.create(name="後台管理員")
        for permission in Permission.objects.filter(content_type__app_label="users"):
            admin.permissions.add(permission)

        logger.info(f"""User groups have been created: '後台管理員'.""")

    for year, app in zip(
        (106, 107, 108, 110, 111, 112, 113),
        ("surveys18", "surveys19", "surveys20", "surveys22", "surveys23", "surveys24", "surveys25"),
    ):
        editor_group_name = f"{year}年審表員"

        if not Group.objects.filter(name=editor_group_name).exists():
            editor_group = Group.objects.create(name=editor_group_name)
            for permission in Permission.objects.filter(
                content_type__app_label=app, content_type__model="survey"
            ).exclude(Q(codename="delete_survey") | Q(codename="add_survey")):
                editor_group.permissions.add(permission)

        viewer_group_name = f"僅能檢視{year}年調查表"

        if not Group.objects.filter(name=viewer_group_name).exists():
            viewer_group = Group.objects.create(name=viewer_group_name)
            viewer_group.permissions.add(
                Permission.objects.get(
                    content_type__app_label=app,
                    content_type__model="survey",
                    codename="view_survey",
                )
            )

            logger.info(
                f"""User groups have been created: {editor_group_name}, {viewer_group_name}."""
            )


def create_superuser():
    """Initial fake superuser only for testing. Use in docker-compose."""
    email = "admin@test.test"
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

    email = "staff@test.test"
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

        group_names = []

        for group in Group.objects.filter(Q(name="後台管理員") | Q(name__icontains="審表員")):
            user.groups.add(group)
            group_names.append(group.name)

        logger.info(
            f"""

An staff has been create, grant to groups: {','.join(group_names)}:

    Email: {email}
    Password: {password}
"""
        )
