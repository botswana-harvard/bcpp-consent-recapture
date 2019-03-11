from django import forms
from django.conf import settings
import pytz

from ..models import ClinicSubjectConsent
from .model_form_mixin import ConsentModelFormMixin


tz = pytz.timezone(settings.TIME_ZONE)

subject_identifier = '066\-[0-9]+'


class ClinicSubjectConsentForm(ConsentModelFormMixin, forms.ModelForm):

    form_validator_cls = None

    class Meta:
        model = ClinicSubjectConsent
        fields = '__all__'
