from Products.Five.browser import BrowserView
from plone import api
from zope.interface import Interface
from slc.teamfolder.config import TEAMS

class IConvertToTeamFolder(Interface):
    pass


class ConvertToTeamFolder(BrowserView):

    teams = TEAMS

    def __call__(self):
        self.perform_conversion()
        self.request.response.redirect("@@assign-team")

    def perform_conversion(self):
        """Convert a standard Folder to a Team Folder

        Create three groups for the folder corresponding to
        Contributor, Editor and Viewer local roles. Add users who have
        these local roles on the Folder to the relevant groups,
        clear the local roles, then give groups their corresponding local roles

        """
        uuid = api.content.get_uuid(obj=self.context)
        for team in self.teams:
            group_id = uuid+"-"+team.lower()
            group = api.group.get(groupname=group_id)
            if group is None:
                group = api.group.create(
                    groupname=group_id,
                    title=team+" Team for "+uuid,
                    roles=[],
                )
            local_roles = self.context.__ac_local_roles__
            for username in local_roles.keys():
                if team in local_roles[username]:
                    api.group.add_user(group=group, username=username)
                    api.user.revoke_roles(
                        username=username,
                        roles=[team],
                        obj=self.context,
                    )
            api.group.grant_roles(
                groupname=group_id,
                roles=[team],
                obj=self.context,
            )
