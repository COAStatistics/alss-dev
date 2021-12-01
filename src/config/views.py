from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import status


from config.export.tasks import (
    async_export_full_data,
    async_export_statistics,
    async_export_yearly_compare_statistics,
)


class Index(LoginRequiredMixin, TemplateView):
    login_url = "/users/login/"
    redirect_field_name = "redirect_to"
    template_name = "index.html"


class ExportViewSet(ViewSet):
    http_method_names = ['get']
    permission_classes = [IsAdminUser]

    @action(methods=['GET'], detail=False)
    def full_data(self, request):
        year = int(request.query_params.get('year'))
        async_export_full_data.delay(year, request.user.email)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'], detail=False)
    def statistic(self, request):
        year = int(request.query_params.get('year'))
        async_export_statistics.delay(year, request.user.email)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'], detail=False)
    def statistic_compare(self, request):
        y1 = int(request.query_params.get('y1'))
        y2 = int(request.query_params.get('y2'))
        async_export_yearly_compare_statistics.delay(y1, y2, request.user.email)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
