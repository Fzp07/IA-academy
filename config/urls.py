import mimetypes
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('text/javascript', '.js')

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from apps.courses import views as courses_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', courses_views.index, name='home'),
    path('courses/', include('apps.courses.urls')),
    path('users/', include('apps.users.urls')),
    path('exams/', include('apps.exams.urls')),
    path('regression/', include('apps.regression_demo.urls')),
    path('genetic/', include('apps.genetic_demo.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)
urlpatterns += [re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATICFILES_DIRS[0]})]