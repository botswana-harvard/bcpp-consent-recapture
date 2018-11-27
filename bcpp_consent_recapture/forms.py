import pytz
import re
from django import forms
from django.conf import settings
from edc_constants.constants import NOT_APPLICABLE, YES, NO


from .models import SubjectConsent

tz = pytz.timezone(settings.TIME_ZONE)

subject_identifier = '066\-[0-9]{9}\-[0-9{1}]$'


class ConsentModelFormMixin(forms.ModelForm):

    def clean(self):
        if 'consent_datetime' in self.cleaned_data:
            if not self.cleaned_data.get('consent_datetime'):
                raise forms.ValidationError(
                    'Please indicate the consent datetime.')
        cleaned_data = super().clean()
        self.clean_citizen_is_citizen()
        self.clean_citizen_is_not_citizen()
        self.validate_subject_identifier()
        return cleaned_data

    def validate_max_age(self):
        cleaned_data = self.cleaned_data
        is_consented = self._meta.model.objects.filter(
            identity=cleaned_data.get('identity')).exists()
        if self.age:
            if self.age.years > self.consent_config.age_max and not is_consented:
                raise forms.ValidationError(
                    'Subject\'s age is %(age)s. Subject is not eligible for '
                    'consent. Maximum age of consent is %(max)s.',
                    params={
                        'age': self.age.years,
                        'max': self.consent_config.age_max},
                    code='invalid')

    def clean_citizen_is_not_citizen(self):
        citizen = self.cleaned_data.get('citizen')
        legal_marriage = self.cleaned_data.get('legal_marriage')
        marriage_certificate = self.cleaned_data.get('marriage_certificate')
        marriage_certificate_no = self.cleaned_data.get(
            'marriage_certificate_no')
        if citizen == NO:
            if legal_marriage == NOT_APPLICABLE:
                raise forms.ValidationError({
                    'legal_marriage':
                    'You wrote subject is NOT a citizen. Is the subject '
                    'legally married to a citizen?'})
            elif legal_marriage == NO:
                raise forms.ValidationError({
                    'legal_marriage':
                    'You wrote subject is NOT a citizen and is NOT legally '
                    'married to a citizen. Subject cannot be consented'})
            elif legal_marriage == YES and marriage_certificate != YES:
                raise forms.ValidationError({
                    'marriage_certificate':
                    'You wrote subject is NOT a citizen. Subject needs to '
                    'produce a marriage certificate'})
            elif legal_marriage == YES and marriage_certificate == YES:
                if not marriage_certificate_no:
                    raise forms.ValidationError({
                        'marriage_certificate_no':
                        'You wrote subject is NOT a citizen and has marriage '
                        'certificate. Please provide certificate number.'})

    def clean_citizen_is_citizen(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('citizen') == YES:
            if cleaned_data.get('legal_marriage') != NOT_APPLICABLE:
                raise forms.ValidationError({
                    'legal_marriage': 'This field is not applicable'})
            elif cleaned_data.get('marriage_certificate') != NOT_APPLICABLE:
                raise forms.ValidationError({
                    'marriage_certificate': 'This field is not applicable'})

    def validate_legal_marriage(self):
        if self.cleaned_data.get("legal_marriage") == NO:
            if not (self.cleaned_data.get("marriage_certificate") in [YES, NO]):
                raise forms.ValidationError({
                    'marriage_certificate': 'This field is required.'})

    def validate_subject_identifier(self):
        pattern = re.compile(subject_identifier)
        if not pattern.match(self.cleaned_data.get("subject_identifier")):
            raise forms.ValidationError({
                'subject_identifier': 'Invalid subject identifier length'})


class SubjectConsentForm(ConsentModelFormMixin, forms.ModelForm):

    form_validator_cls = None

    class Meta:
        model = SubjectConsent
        fields = '__all__'
