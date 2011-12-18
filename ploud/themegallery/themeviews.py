import ptah
from ptah import form
from pyramid.view import view_config

import permissions
from gallery import ThemeGallery
from theme import Theme, ThemeSchema
from themefile import ThemeFileSchema


ptah.uiaction(
    Theme, 'submit', 'Submit',
    action='submit.html', permission=ptah.cms.ModifyContent)

ptah.uiaction(
    Theme, 'publish', 'Publish',
    action='publish.html', permission=permissions.ManageGallery,
    condition=lambda content, request: content.status!='public')

ptah.uiaction(
    Theme, 'retract', 'Retract',
    action='retract.html', permission = permissions.RetractTheme)

ptah.uiaction(
    Theme, 'upload', 'Upload file',
    action='uploadfile.html', permission = permissions.AddThemeFile)


@view_config('newtheme.html',
             context=ThemeGallery,
             wrapper=ptah.wrap_layout())
class AddThemeForm(ptah.cms.AddForm):

    tinfo = Theme.__type__
    fields = form.Fieldset(
        ThemeSchema, 
        form.Fieldset(ThemeFileSchema, name='theme-file', legend='Theme file'))

    def create(self, **data):
        theme = super(AddThemeForm, self).create(**data)

        # create theme file
        filedata = data.pop('theme-file')
        themefile = ptah.cms.wrap(theme).create(
            ThemeFile.__type__.__uri__, 
            'themfile-%s'%filedata['version'],
            **filedata)

        return theme


@view_config('edit.html', context=Theme,
             wrapper=ptah.wrap_layout(),
             permission=ptah.cms.ModifyContent)
class ThemeEditForm(ptah.cms.EditForm):
    """ """


@view_config('preview', context=Theme, permission=ptah.cms.View)
def themePreviewImage(context, request):
    blob = ptah.resolve(context.preview)
    if blob is None:
        return HTTPNotFound()

    response = request.response
    response.content_type = blob.mimetype.encode('utf-8')
    response.body = blob.read()
    return response


@view_config('thumbnail', context=Theme, permission=ptah.cms.View)
def thumbnailImage(context, request):
    blob = ptah.resolve(context.thumbnail)
    if blob is None:
        return HTTPNotFound()

    response = request.response
    response.content_type = blob.mimetype.encode('utf-8')
    response.body = blob.read()
    return response


@view_config(context=Theme,
             wrapper=ptah.wrap_layout(),
             permission=ptah.cms.View,
             renderer='ploud.themegallery:templates/theme.pt')
class ThemeView(ptah.View):

    def update(self):
        self.actions = [ac for ac in 
                        ptah.list_uiactions(self.context, self.request)
                        if ac['id'] != 'view']
        
        self.files = list(self.context.values())
        self.files.sort(key = lambda f: f.created)
        self.files.reverse()


@view_config('submit.html', context=Theme,
             permission=ptah.cms.ModifyContent,
             wrapper=ptah.wrap_layout(),
             renderer='ploud.themegallery:templates/submit.pt')

class ThemeSubmit(form.Form):

    @form.button('Cancel')
    def cancelHandler(self):
        return HTTPFound(location='.')

    @form.button('Submit', actype=form.AC_PRIMARY)
    def submitHandler(self):
        self.context.changeStatus('submitted')
        self.request.registry.notify(events.ThemeSubmittedEvent(self.context))

        self.message("Theme has been submitted to gallery.")
        return HTTPFound(location='.')


@view_config('publish.html', context=Theme,
             wrapper=ptah.wrap_layout(),
             permission=permissions.ManageGallery,
             renderer='ploud.themegallery:templates/publish.pt')

class ThemePublish(form.Form):

    @form.button('Cancel')
    def cancelHandler(self):
        return HTTPFound(location='.')

    @form.button('Publish', actype=form.AC_PRIMARY)
    def submitHandler(self):
        self.context.changeStatus('public')
        self.request.registry.notify(events.ThemePublishedEvent(self.context))

        self.message("Theme has been published to gallery.")
        return HTTPFound(location='.')


@view_config('retract.html', context=Theme,
             wrapper=ptah.wrap_layout(),
             permission=permissions.RetractTheme,
             renderer='ploud.themegallery:templates/retract.pt')

class ThemeRetract(form.Form):

    @form.button('Cancel')
    def cancelHandler(self):
        return HTTPFound(location='.')

    @form.button('Retract', actype=form.AC_PRIMARY)
    def submitHandler(self):
        self.context.changeStatus('private')
        self.request.registry.notify(events.ThemePublishedEvent(self.context))
        
        self.message("Theme has been published to gallery.")
        return HTTPFound(location='.')
