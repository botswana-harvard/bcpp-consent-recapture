from django.contrib import admin
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin

from edc_base.modeladmin_mixins import (
    ModelAdminInstitutionMixin, audit_fieldset_tuple, audit_fields,
    ModelAdminNextUrlRedirectMixin)
from edc_consent.modeladmin_mixins import ModelAdminConsentMixin

from .forms import SubjectConsentForm
from .models import SubjectConsent
from .admin_site import bcpp_consent_recapture_admin


@admin.register(SubjectConsent, site=bcpp_consent_recapture_admin)
class SubjectConsentAdmin(ModelAdminConsentMixin, ModelAdminRevisionMixin,
                          ModelAdminInstitutionMixin, ModelAdminNextUrlRedirectMixin,
                          admin.ModelAdmin):

    form = SubjectConsentForm

    fieldsets = (
        (None, {
            'fields': (
                'subject_identifier',
                'first_name',
                'last_name',
                'initials',
                'language',
                'is_literate',
                'witness_name',
                'consent_datetime',
                'gender',
                'dob',
                'guardian_name',
                'is_dob_estimated',
                'citizen',
                'legal_marriage',
                'marriage_certificate',
                'marriage_certificate_no',
                'identity',
                'identity_type',
                'confirm_identity',
                'is_incarcerated',
                'may_store_samples',
                'comment',
                'consent_reviewed',
                'study_questions',
                'assessment_score',
                'consent_copy')}),
        audit_fieldset_tuple)

    radio_fields = {
        "assessment_score": admin.VERTICAL,
        "consent_copy": admin.VERTICAL,
        "consent_reviewed": admin.VERTICAL,
        "gender": admin.VERTICAL,
        "identity_type": admin.VERTICAL,
        "is_dob_estimated": admin.VERTICAL,
        "is_incarcerated": admin.VERTICAL,
        "is_literate": admin.VERTICAL,
        "is_minor": admin.VERTICAL,
        "language": admin.VERTICAL,
        "may_store_samples": admin.VERTICAL,
        "study_questions": admin.VERTICAL,
        'citizen': admin.VERTICAL,
        'legal_marriage': admin.VERTICAL,
        'marriage_certificate': admin.VERTICAL,
    }

    def get_readonly_fields(self, request, obj=None):
        super(ModelAdminConsentMixin, self).get_readonly_fields(request, obj)
        if obj:
            return (
                'subject_identifier_as_pk',
                'study_site',
                'consent_datetime',) + self.readonly_fields + audit_fields
        else:
            return (('subject_identifier_as_pk',)
                    + self.readonly_fields + audit_fields)
