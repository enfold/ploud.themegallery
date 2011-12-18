""" Theme gallery """
import ptah
import sqlalchemy as sqla
from pyramid.view import view_config
from pyramid.renderers import render

import permissions
from theme import Theme


class ThemeGalleryPolicy(ptah.cms.ApplicationPolicy):

    __acl__ = permissions.GALLERY_ACL


class ThemeGallery(ptah.cms.ApplicationRoot):

    __type__ = ptah.cms.Type(
        'ploud-themegallery',
        'Theme gallery',
        filter_content_types = True,
        allowed_content_types = ('diazo-theme',))


ptah.uiaction(
    ThemeGallery, 'submited', 'Submited themes',
    action='submitted.html', permission = permissions.ManageGallery)

ptah.uiaction(
    ThemeGallery, 'private', 'Private themes',
    action='private.html', permission = permissions.ManageGallery)

ptah.uiaction(
    ThemeGallery, 'mythemes', 'My themes',
    action='mythemes.html', permission = permissions.AddTheme)

ptah.uiaction(
    ThemeGallery, 'upload-theme', 'Upload new',
    action='newtheme.html', permission = permissions.AddTheme)


@view_config(context=ThemeGallery,
             permission=ptah.cms.View,
             wrapper=ptah.wrap_layout(),
             renderer='ploud.themegallery:templates/themegallery.pt')
class GalleryView(ptah.View):
    """ Main gallery view """

    themes_tmpl = 'ploud.themegallery:templates/listthemes.pt'

    status = 'public'
    page = ptah.Pagination(8, 3, 3)

    def render_tmpl(self, themes, url):
        return render(self.themes_tmpl, {'themes': themes, 'url': url})

    def getCurrent(self):
        id = 'gallery-batch-%s'%self.status

        request = self.request
        try:
            current = int(request.params.get('batch', None))
            if not current:
                current = request.session.get(id)
                if not current:
                    current = 1
            else:
                request.session[id] = current
        except:
            current = request.session.get(id)
            if not current:
                current = 1

        return current

    def getCount(self):
        return ptah.get_session().query(Theme)\
            .filter(Theme.status == self.status).count()

    def listThemes(self, offset, size):
        return ptah.get_session().query(Theme)\
            .filter(Theme.status == self.status).order_by(Theme.modified)\
            .offset(offset).limit(size).all()

    def update(self):
        self.actions = [ac for ac in
                        ptah.list_uiactions(self.context, self.request)
                        if ac['id'] != 'view']

        size = self.getCount()
        self.current = current = self.getCurrent()

        self.pages, self.prev, self.next = self.page(size, current)
        self.themes = self.listThemes(*self.page.offset(current))


@view_config('submitted.html', context=ThemeGallery,
             permission = permissions.ManageGallery,
             wrapper=ptah.wrap_layout(),
             renderer='ploud.themegallery:templates/themegallery.pt')
class SubmittedView(GalleryView):

    status = 'submitted'


@view_config('private.html', context=ThemeGallery,
             permission = permissions.ManageGallery,
             wrapper=ptah.wrap_layout(),
             renderer='ploud.themegallery:templates/themegallery.pt')
class PrivateView(GalleryView):

    status = 'private'


@view_config('mythemes.html', context=ThemeGallery,
             permission=permissions.AddTheme,
             wrapper=ptah.wrap_layout(),
             renderer='ploud.themegallery:templates/mythemes.pt')
class MyThemesView(GalleryView):

    status = 'mythemes'

    def getCount(self):
        return list(ptah.get_session().execute(
            "select count(*) from ptah_nodes "
            "where owner = '%s' and type = '%s'"%(
                ptah.auth_service.get_userid(), Theme.__type__.__uri__)))[0][0]

    def listThemes(self, offset, size):
        return ptah.get_session().query(Theme)\
            .filter(Theme.__owner__ == ptah.auth_service.get_userid())\
            .order_by(Theme.modified)\
            .offset(offset).limit(size).all()


@view_config('edit.html', context=ThemeGallery,
             permission=ptah.cms.ModifyContent, wrapper=ptah.wrap_layout())
class GalleryEditForm(ptah.cms.EditForm):
    """ """
