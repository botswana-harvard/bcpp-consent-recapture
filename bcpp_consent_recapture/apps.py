from datetime import datetime
from dateutil.tz import gettz
from django.apps import AppConfig as DjangoAppConfig

from edc_identifier.apps import AppConfig as BaseEdcIdentifierAppConfigs
from edc_base.apps import AppConfig as BaseEdcBaseAppConfig
from edc_protocol.apps import AppConfig as BaseEdcProtocolAppConfig, SubjectType, Cap


class AppConfig(DjangoAppConfig):
    name = 'bcpp_consent_recapture'


class EdcBaseAppConfig(BaseEdcBaseAppConfig):
    project_name = 'BCPP'
    institution = 'Botswana-Harvard AIDS Institute Partnership'
    copyright = '2018-11-24'
    license = 'GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007'


class EdcProtocolAppConfig(BaseEdcProtocolAppConfig):
    protocol = 'BHP066'
    protocol_number = '066'
    protocol_name = 'BCPP'
    protocol_title = 'Botswana Combination Prevention Project'
    subject_types = [
        SubjectType('subject', 'Research Subject',
                    Cap(model_name='bcpp_subject.subjectconsent', max_subjects=99999)),
        SubjectType('subject', 'Anonymous Research Subject',
                    Cap(model_name='bcpp_subject.anonymousconsent', max_subjects=9999)),
    ]
    study_open_datetime = datetime(2013, 10, 18, 0, 0, 0)
    study_close_datetime = datetime(2018, 12, 1, 0, 0, 0, tzinfo=gettz('UTC'))


class EdcIdentifierAppConfig(BaseEdcIdentifierAppConfigs):
    identifier_prefix = '066'
