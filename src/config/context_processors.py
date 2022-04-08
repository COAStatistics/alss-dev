from django.conf import settings


def get_session_cookie_age(request):
    try:
        return {'session_cookie_age': settings.SESSION_COOKIE_AGE}
    except AttributeError:
        return {'session_cookie_age': 60 * 60 * 2}


def get_environment(request):
    return {
        'environment': "debug" if settings.DEBUG else "production"
    }
