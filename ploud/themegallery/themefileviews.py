import ptah
from pyramid.view import view_config

import permissions
from theme import Theme
from themefile import ThemeFile


@view_config(
    context=ThemeFile,
    permission=ptah.cms.View,
    renderer="ploud.themegallery:templates/themefile.pt")

class ThemeFileView(ptah.View):

    def update(self):
        self.actions = [ac for ac in 
                        ptah.list_uiactions(self.context, self.request)
                        if ac['id'] != 'view']


@view_config('download.html', context=ThemeFile, permission=ptah.cms.View)
def themeFileDownload(context, request):
    blob = ptah.resolve(context.data)
    if not blob:
        return ' '

    response = request.response
    response.content_type = blob.mimetype.encode('utf-8')
    if blob.filename:
        response.headerlist = {
            'Content-Disposition':'filename="%s"'%blob.filename.encode('utf-8')}
    response.body = blob.read()
    return response


@view_config('uploadfile.html',
             context=Theme,
             wrapper=ptah.wrap_layout())

class AddThemeFileForm(ptah.cms.AddForm):

    tinfo = ThemeFile.__type__
    name_show = False

    def chooseName(self, **kw):
        filename = kw['data']['filename']
        name = filename.split('\\')[-1].split('/')[-1]

        i = 1
        n = name
        while n in self.container:
            i += 1
            n = u'%s-%s'%(name, i)

        return n

    def nextUrl(self, content):
        return '.'


@view_config('edit.html', context=ThemeFile,
             permission=ptah.cms.ModifyContent)
class ThemeFileEditForm(ptah.cms.EditForm):
    """ """
