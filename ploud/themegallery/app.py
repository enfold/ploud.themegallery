import ptah
import transaction
from pyramid.config import Configurator
from pyramid.asset import abspath_from_asset_spec
from pyramid.traversal import DefaultRootFactory

from .permissions import Manager
from .gallery import ThemeGallery, ThemeGalleryPolicy


APP_FACTORY = ptah.cms.ApplicationFactory(
    ThemeGallery, '/',
    policy=ThemeGalleryPolicy,
    name='themes', title='Ploud theme gallery')


def main(global_config, **settings):
    """ themes app """
    config = Configurator(root_factory=APP_FACTORY, settings=settings)
    config.include('ploud.themegallery')

    # init sqlalchemy engine
    config.ptah_init_sql()

    # init ptah settings
    config.ptah_init_settings()

    # enable rest api
    config.ptah_init_rest()

    # enable ptah manage
    config.ptah_init_manage(manager_role=Manager.id)

    # standalone layouts
    config.ptah_layout(
        'page', context=ThemeGallery, view=WorkspaceLayout,
        renderer='ploud.themegallery:templates/layout-page.pt')

    config.ptah_layout(
        'ptah-page', ThemeGallery, parent='page',
        renderer="ploud.themegallery:templates/layout-ptahpage.pt")

    # populate database
    config.commit()
    config.begin()

    # create sql tables
    Base = ptah.get_base()
    Base.metadata.create_all()

    # your application configuration
    ptah.auth_service.set_userid(ptah.SUPERUSER_URI)
    root = APP_FACTORY()

    # admin user
    from ptah_crowd import CrowdUser, CrowdFactory

    Session = ptah.get_session()
    user = Session.query(CrowdUser).first()
    if user is None:
        user = CrowdUser(title='Admin', login='admin', 
                         email='admin@ptahproject.org',
                         password='{plain}12345')
        CrowdFactory().add(user)

    # give manager role to admin
    if user.__uri__ not in root.__local_roles__:
        root.__local_roles__[user.__uri__] = [Manager.id]

    # We are not in a web request; we need to manually commit.
    transaction.commit()

    return config.make_wsgi_app()


class WorkspaceLayout(ptah.View):

    def update(self):
        self.user = ptah.auth_service.get_current_principal()
        self.ptahManager = ptah.manage.check_access(
            ptah.auth_service.get_userid(), self.request)
        self.isAnon = self.user is None
