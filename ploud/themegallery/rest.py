""" rest actions """
import ptah
from pyramid.httpexceptions import HTTPNotFound

from theme import Theme
from themefile import ThemeFile


@ptah.cms.restaction('data', ThemeFile, ptah.cms.View)
def ThemeFileData(content, request):
    """Download theme file"""
    blob = ptah.resolve(content.data)
    if not blob:
        return HTTPNotFound()

    response = request.response
    response.content_type = blob.mimetype.encode('utf-8')
    if blob.filename:
        response.headerlist = {
            'Content-Disposition':
            'filename="%s"'%blob.filename.encode('utf-8')}

    response.body = blob.read()
    return response


@ptah.cms.restaction('', Theme, ptah.cms.View)
def ThemeRestInfo(content, request):
    """Theme information"""
    info = ptah.cms.wrap(content).info()
    info['__link__'] = '%s%s/'%(request.application_url, content.__uri__)
    info['thumbnail'] = content.thumbnail

    files = [(f.modified, f) for f in content.values()]
    files.sort()
    if files:
        info['theme-file'] = files[-1][1].__uri__

    return info
