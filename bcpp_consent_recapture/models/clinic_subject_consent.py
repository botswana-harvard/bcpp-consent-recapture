from django.core.exceptions import ValidationError
from django.db import models
from django_crypto_fields.fields import IdentityField
from edc_base.model_mixins import BaseUuidModel
from edc_base.utils import age
from edc_consent.field_mixins import ReviewFieldsMixin, PersonalFieldsMixin
from edc_consent.field_mixins import SampleCollectionFieldsMixin
from edc_consent.field_mixins import VulnerabilityFieldsMixin
from edc_consent.managers import ConsentManager
from edc_consent.model_mixins import ConsentModelMixin
from edc_constants.choices import YES_NO
from edc_constants.constants import YES, NO

from edc_base.model_fields import IdentityTypeField
from edc_consent.field_mixins.bw import IdentityFieldsMixin


def is_minor(dob, reference_datetime):
    return 16 <= age(dob, reference_datetime).years < 18


class ClinicSubjectConsent(
        ConsentModelMixin,
        IdentityFieldsMixin, ReviewFieldsMixin, PersonalFieldsMixin,
        SampleCollectionFieldsMixin,
        VulnerabilityFieldsMixin, BaseUuidModel):
    """ A model completed by the user that captures the ICF.
    """

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50,
        unique=True)

    is_minor = models.CharField(
        verbose_name=("Is subject a minor?"),
        max_length=10,
        choices=YES_NO,
        null=True,
        blank=False,
        help_text=('Subject is a minor if aged 16-17. A guardian must '
                   'be present for consent. HIV status may NOT be '
                   'revealed in the household.'),
        editable=False)

    identity = IdentityField(
        verbose_name='Identity number (OMANG, etc)',
        help_text=(
            'Use Omang, Passport number, driver\'s license '
            'number or Omang receipt number')
    )

    identity_type = IdentityTypeField()

    confirm_identity = IdentityField(
        help_text='Retype the identity number from the identity card',
        null=True,
        blank=False
    )

    is_signed = models.BooleanField(
        default=False,
        editable=False)

    lab_identifier = models.CharField(
        verbose_name=("lab allocated identifier"),
        max_length=50,
        null=True,
        blank=True,
        help_text="if known.")

    htc_identifier = models.CharField(
        verbose_name=("HTC Identifier"),
        max_length=50,
        null=True,
        blank=True,
        help_text="if known.")

    pims_identifier = models.CharField(
        verbose_name=("PIMS identifier"),
        max_length=50,
        null=True,
        blank=True,
        help_text="if known.")

    consent = ConsentManager()

    def __str__(self):
        return f'{self.subject_identifier}, {self.version}'

    def save(self, *args, **kwargs):

        if self.identity != self.confirm_identity:
            raise ValidationError(
                '\'Identity\' must match \'confirm_identity\'. '
                'Catch this error on the form'
            )
        self.is_minor = YES if is_minor(
            self.dob, self.consent_datetime) else NO
        super().save(*args, **kwargs)

    @property
    def visit_code(self):
        """Returns a value for edc_reference.
        """
        return 'CONSENT'

    class Meta(ConsentModelMixin.Meta):
        app_label = 'bcpp_consent_recapture'
        get_latest_by = 'consent_datetime'
        unique_together = (('subject_identifier', 'version'),
                           ('first_name', 'dob', 'initials', 'version'))
        ordering = ('-created',)
