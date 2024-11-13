from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.conf import settings
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import status


from config.export.tasks import (
    async_export_full_data,
    async_export_statistics,
    async_export_yearly_compare_statistics,
    async_export_examination_work_hours,
    async_export_raw_data,
    async_export_farmer_stat,
)


class Index(LoginRequiredMixin, TemplateView):
    login_url = "/users/login/"
    redirect_field_name = "redirect_to"
    template_name = "index.html"


class Chart(LoginRequiredMixin, TemplateView):
    login_url = "/users/login/"
    redirect_field_name = "redirect_to"
    template_name = "charts.html"


class SessionTimeout(TemplateView):
    template_name = "session-timeout.html"


class SessionViewSet(ViewSet):
    http_method_names = ["get"]
    permission_classes = [IsAuthenticated]

    @action(methods=["GET"], detail=False)
    def keep_alive(self, request):
        """Extend session by reset the max age."""
        request.session.set_expiry(settings.SESSION_COOKIE_AGE)
        return HttpResponse(status=status.HTTP_200_OK)


class ExportViewSet(ViewSet):
    http_method_names = ["get"]
    permission_classes = [IsAdminUser]

    @action(methods=["GET"], detail=False)
    def full_data(self, request):
        year = int(request.query_params.get("year"))
        async_export_full_data.delay(year, request.user.email)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["GET"], detail=False)
    def statistic(self, request):
        year = int(request.query_params.get("year"))
        async_export_statistics.delay(year, request.user.email)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["GET"], detail=False)
    def statistic_compare(self, request):
        y1 = int(request.query_params.get("y1"))
        y2 = int(request.query_params.get("y2"))
        async_export_yearly_compare_statistics.delay(y1, y2, request.user.email)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["GET"], detail=False)
    def work_hours_examination(self, request):
        year = int(request.query_params.get("year"))
        async_export_examination_work_hours.delay(year, request.user.email)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["GET"], detail=False)
    def raw_data(self, request):
        year = int(request.query_params.get("year"))
        async_export_raw_data.delay(year, request.user.email)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["GET"], detail=False)
    def farmer_stat(self, request):
        year = int(request.query_params.get("year"))
        async_export_farmer_stat.delay(year, request.user.email)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
