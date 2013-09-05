from p4a.subtyper.interfaces import IPortalTypedFolderishDescriptor
from zope.interface import Interface
from zope.interface import implements


class ITeamFolder(Interface):
    """Marker interface for Team Folders"""
    pass


class TeamFolderDescriptor(object):
    implements(IPortalTypedFolderishDescriptor)
    title = "Team"
    description = "Team Folder"
    type_interface = ITeamFolder
    for_portal_type = 'Folder'
