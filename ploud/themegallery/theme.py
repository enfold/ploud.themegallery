""" theme """
import PIL, PIL.Image
import sqlalchemy as sqla
from cStringIO import StringIO
from pyramid.compat import text_type
from pyramid.threadlocal import get_current_registry
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

import ptah
from ptah import form

import permissions
from themefile import ThemeFile, ThemeFileSchema


class Email(form.Email):

    def __call__(self, field, value):
        if value != '':
            super(Email, self).__call__(field, value)


ThemeSchema = form.Fieldset(
    ptah.cms.ContentSchema,

    form.TextField(
        'author',
        title = 'Author name'),

    form.TextField(
        'email',
        missing = '',
        title = 'Author email',
        validator = Email()),

    form.TextField(
        'url',
        missing = '',
        title = 'Web site'),

    form.FileField(
        'preview',
        title = 'Preview image',
        missing = ''),
    )


class Theme(ptah.cms.Container):

    __tablename__ = 'ploud_themes'

    __type__ = ptah.cms.Type(
        'diazo-theme', 'Theme',
        add = 'newtheme.html',
        fieldset = ThemeSchema,
        description = 'A diazo theme.',
        permission = permissions.AddTheme,
        global_allow = False,
        filter_content_types = True,
        allowed_content_types = ('diazo-theme-file',),
        )

    _sql_values = ptah.QueryFreezer(
        lambda: ptah.get_session().query(ThemeFile)
            .filter(ThemeFile.__parent_uri__ == sqla.sql.bindparam('uri')))

    author = sqla.Column(sqla.Unicode)
    url = sqla.Column(sqla.Unicode)
    email = sqla.Column(sqla.Unicode)
    attribution = sqla.Column(sqla.Unicode)
    featured = sqla.Column(sqla.Boolean)
    status = sqla.Column(sqla.Unicode, default=text_type('private'))

    preview = sqla.Column(sqla.Unicode)
    thumbnail = sqla.Column(sqla.Unicode)

    def __init__(self, *args, **kw):
        super(Theme, self).__init__(*args, **kw)

        self.changeStatus('private')

    def changeStatus(self, status):
        self.status = status

        pmap = permissions.status[status]
        self.__acls__ = [pmap.id]

    @ptah.cms.action(permission=ptah.cms.ModifyContent)
    def update(self, **data):
        preview = data.pop('preview')

        for node in self.__type__.fieldset.fields():
            val = data.get(node.name, node.default)
            if val is not form.null:
                setattr(self, node.name, val)

        if preview:
            blob = ptah.resolve(self.preview)
            if blob is None:
                blob = ptah.cms.blob_storage.create(self)
                self.preview = blob.__uri__

            blob.write(preview['fp'].read())
            blob.updateMetadata(
                filename = preview['filename'],
                mimetype = preview['mimetype'])

            generateThumbnail(self)

        get_current_registry().notify(ptah.events.ContentModifiedEvent(self))


def generateThumbnail(theme, width=210):
    blob = ptah.resolve(theme.preview)
    if not blob:
        return

    data = StringIO(blob.read())
    image = PIL.Image.open(data)

    if image.mode == '1':
        image = image.convert('L')
    elif image.mode == 'P':
        image = image.convert('RGBA')

    # get width, height
    orig_size = image.size

    scale = float(width)/orig_size[0]
    height = int(round(orig_size[1] * scale))

    #convert image
    pilfilter = PIL.Image.NEAREST
    pilfilter = PIL.Image.ANTIALIAS

    image.thumbnail((width, height), pilfilter)

    newfile = StringIO()
    image.save(newfile, 'jpeg', quality=88)

    blob = ptah.resolve(theme.thumbnail)
    if blob is None:
        blob = ptah.cms.blob_storage.create(theme)
        theme.thumbnail = blob.__uri__

    blob.write(newfile.getvalue())
    blob.updateMetadata(mimetype = 'image/jpeg')
