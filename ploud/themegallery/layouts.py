import ptah

from theme import Theme
from themefile import ThemeFile
from gallery import ThemeGallery


ptah.layout.register(
    '', Theme, parent='page',
    renderer="ploud.themegallery:templates/layoutdefault.pt")


ptah.layout.register(
    '', ThemeFile, parent='page',
    renderer="ploud.themegallery:templates/layoutdefault.pt")


ptah.layout.register(
    '', ThemeGallery, parent='page',
    renderer="ploud.themegallery:templates/layoutdefault.pt")
