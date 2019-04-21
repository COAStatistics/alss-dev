from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class Index(LoginRequiredMixin, TemplateView):
    login_url = "/users/login/"
    redirect_field_name = "redirect_to"
    template_name = "index.html"
