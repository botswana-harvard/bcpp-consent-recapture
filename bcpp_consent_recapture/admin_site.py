from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):
    site_title = 'BCPP Consent ReCapture'
    site_header = 'BCPP Consent ReCapture'
    index_title = 'BCPP Consent ReCapture'


bcpp_consent_recapture_admin = AdminSite(name='bcpp_consent_recapture_admin')
