from django.urls import path, include, re_path
from django.shortcuts import render
from django.views.static import serve
from django.conf import settings


def _page(template_name):
    """Render through Django's template engine so {% static %} tags resolve."""
    def view(request):
        return render(request, template_name)
    return view


urlpatterns = [
    # Page routes
    path('',           _page('Library_web_landing_page.html')),
    path('landing',    _page('Library_web_landing_page.html')),
    path('welcome',    _page('Welcome_main.html')),
    path('lbas',       _page('LBAS.html')),
    path('admin-page', _page('admin_dashboard.html')),

    # API endpoints
    path('api/', include('api.urls')),

    # Static files — served by Django/waitress directly (no WhiteNoise needed)
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.BASE_DIR / 'static'}),

    # Uploaded profile photos from Profile/
    re_path(r'^profile/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
