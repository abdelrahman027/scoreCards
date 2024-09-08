from django.urls import path,include
from . import views

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('role/',views.role,name='role')
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)