# organizations/tests/views.py (or inline in test file)

from django.http import HttpResponse
from django.views import View

from organizations.mixins import (
    OrganizationReadRequiredMixin,
    OrganizationWriteRequiredMixin,
    OrganizationDeleteRequiredMixin,
)


class ReadView(OrganizationReadRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("ok")


class WriteView(OrganizationWriteRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        return HttpResponse("ok")


class DeleteView(OrganizationDeleteRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        return HttpResponse("ok")
