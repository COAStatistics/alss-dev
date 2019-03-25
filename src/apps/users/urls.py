from django.conf.urls import url, include
from .views import (
    login_view,
    logout_view,
    register_view,
    forget_password_view,
    reset_password_view,
    edit_info_view,
    user_activate,
    resend_mail_view,
    reset_email_view
)

urlpatterns = [
    url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),
]
