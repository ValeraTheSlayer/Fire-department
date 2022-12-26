from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main_page/', include('application.urls'))
]

urlpatterns += [
    path('', RedirectView.as_view(url='/accounts/login/', permanent=True)),
]

urlpatterns += [
    path('accounts/password_change/done/', RedirectView.as_view(url='/main_page/', permanent=True)),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += [path('event_map/', include('event_map.urls')), ]
