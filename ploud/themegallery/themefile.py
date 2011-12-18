""" theme file """
import ptah
import sqlalchemy as sqla
from pyramid.threadlocal import get_current_registry


from permissions import AddThemeFile


ThemeFileSchema = ptah.form.Fieldset(

    ptah.form.TextField(
        'version',
        title = u'Version'),

    ptah.form.FileField(
        'data',
        title = u'Theme file',
        widget = 'file'),
    )


class ThemeFile(ptah.cms.Content):

    __tablename__ = 'ploud_theme_files'

    __type__ = ptah.cms.Type(
        'diazo-theme-file', 'Theme file',
        add = 'uploadfile.html',
        fieldset = ThemeFileSchema,
        description = 'A theme file.',
        permission = AddThemeFile,
        global_allow = False,
        )

    version = sqla.Column(sqla.Unicode)
    data = sqla.Column(sqla.Unicode)

    @ptah.cms.action(permission=ptah.cms.ModifyContent)
    def update(self, **data):
        fd = data.pop('data')

        if fd:
            blob = ptah.resolve(self.data)
            if blob is None:
                blob = ptah.cms.blob_storage.create(self)
                self.data = blob.__uri__

            blob.write(fd['fp'].read())
            blob.updateMetadata(
                filename = fd['filename'],
                mimetype = fd['mimetype'])

        self.version = data['version']
        get_current_registry().notify(ptah.cms.ContentModifiedEvent(self))
