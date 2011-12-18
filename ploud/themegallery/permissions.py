""" theme gallery permissions """
import ptah

ptah.Everyone.allow(ptah.cms.View)
ptah.Authenticated.allow(ptah.cms.AddContent)

Viewer = ptah.Role('viewer', 'Viewer')
Viewer.allow(ptah.cms.View)

Editor = ptah.Role('editor', 'Editor')
Editor.allow(ptah.cms.View, ptah.cms.ModifyContent)

Manager = ptah.Role('manager', 'Manager')
Manager.allow(ptah.cms.ALL_PERMISSIONS)

ptah.Owner.allow(ptah.cms.DeleteContent)

# permissions
AddTheme = ptah.Permission('ploud:AddTheme', 'Add theme')
AddThemeFile = ptah.Permission('ploud:AddFile', 'Add theme file')
RetractTheme = ptah.Permission('ploud:RetractTheme', 'Retract theme')
ManageGallery = ptah.Permission('ploud:ManageGallery', 'Manage gallery')

# Gallery ACL
GALLERY_ACL = ptah.ACL('ploud-themegallery', 'Ploud theme gallery ACL')
GALLERY_ACL.allow(ptah.Everyone, ptah.cms.View)
GALLERY_ACL.allow(ptah.Authenticated, AddTheme)
GALLERY_ACL.allow(ptah.Authenticated, ptah.cms.View)
GALLERY_ACL.allow(ptah.Owner, AddThemeFile)
GALLERY_ACL.allow(ptah.Owner, ptah.cms.ModifyContent)
GALLERY_ACL.allow(ptah.Owner, ptah.cms.DeleteContent)
GALLERY_ACL.allow(Manager, ptah.cms.ALL_PERMISSIONS)

# ACL for private state
PRIVATE = ptah.ACL('ploud-private-theme', 'Private ploud theme')
PRIVATE.allow(Manager, ptah.cms.ALL_PERMISSIONS)
PRIVATE.allow(ptah.Owner, ptah.cms.View)
PRIVATE.allow(ptah.Owner, ptah.cms.ModifyContent)
PRIVATE.deny(ptah.Owner, RetractTheme)
PRIVATE.deny(ptah.Everyone, ptah.cms.View)

# ACL for submitted state
SUBMITTED = ptah.ACL('ploud-submitted-theme', 'Submitted ploud theme')
SUBMITTED.allow(Manager, ptah.cms.ALL_PERMISSIONS)
SUBMITTED.allow(ptah.Owner, ptah.cms.View)
SUBMITTED.allow(ptah.Owner, RetractTheme)
SUBMITTED.allow(ptah.Owner, ptah.cms.DeleteContent)
SUBMITTED.deny(ptah.Owner, ptah.cms.ModifyContent)
SUBMITTED.deny(ptah.Everyone, ptah.cms.View)

# ACL for public state
PUBLIC = ptah.ACL('ploud-public-theme', 'Public ploud theme')
PUBLIC.allow(Manager, ptah.cms.ALL_PERMISSIONS)
PUBLIC.allow(ptah.Everyone, ptah.cms.View)
PUBLIC.allow(ptah.Owner, RetractTheme)
PUBLIC.deny(ptah.Owner, ptah.cms.ModifyContent)
PUBLIC.deny(ptah.Owner, ptah.cms.DeleteContent)

status = {
    'private': PRIVATE,
    'public': PUBLIC,
    'submitted': SUBMITTED}
