from django.conf.urls import url

from .admin_site import bcpp_consent_recapture_admin

urlpatterns = [url(r'^admin/', bcpp_consent_recapture_admin.urls)]
