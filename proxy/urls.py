from django.urls import path

from proxy.views import upload_file, index

urlpatterns = [
    path('', index, name='home'),
    path('upload/', upload_file, name='upload'),
]
