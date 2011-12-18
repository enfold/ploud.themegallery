""" ploud.themegallery """
from pyramid.i18n import TranslationStringFactory

MessageFactory = _ = TranslationStringFactory('ploud.themegallery')


def includeme(config):
    config.scan('ploud.themegallery')