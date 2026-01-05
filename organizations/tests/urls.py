# organizations/tests/urls.py

from django.urls import path
from .views import ReadView, WriteView, DeleteView

urlpatterns = [
    path("org/<int:organization_pk>/read/", ReadView.as_view(), name="org-read"),
    path("org/<int:organization_pk>/write/", WriteView.as_view(), name="org-write"),
    path("org/<int:organization_pk>/delete/", DeleteView.as_view(), name="org-delete"),
]
