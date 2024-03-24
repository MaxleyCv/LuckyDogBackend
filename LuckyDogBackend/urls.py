
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
import uuid
from pets.views import finder_view, searcher_view, searching_matches, finding_matches

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/finder', finder_view, name='finders'),
    path('api/searcher', searcher_view, name='searchers'),
    path('api/matchsearch/<uuid:searcher_id>', searching_matches, name="finder-matches"),
    path('api/matchfind/<uuid:finder_id>', finding_matches, name="searcher-matches"),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]
