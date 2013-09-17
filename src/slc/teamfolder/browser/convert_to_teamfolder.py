from Products.Five.browser import BrowserView
from plone import api
from zope.interface import Interface
from slc.teamfolder.config import TEAMS
from zope.component import getMultiAdapter


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
        assign_view = getMultiAdapter(
            (self.context, self.request), name="assign-team")
        for team in self.teams:
            group_id = assign_view.get_team_id(team)
            group = api.group.get(groupname=group_id)
            if group is None:
                group = api.group.create(
                    groupname=group_id,
                    title=assign_view.get_team_title(team),
                    roles=[],
                )
            api.group.grant_roles(
                groupname=group_id,
                roles=[team],
                obj=self.context,
            )
            local_roles = self.context.__ac_local_roles__
            for username in local_roles.keys():
                if team in local_roles[username] \
                   and username != group_id:
                    api.group.add_user(groupname=group_id, username=username)
                    local_roles[username].remove(team)
