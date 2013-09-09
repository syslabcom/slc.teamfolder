# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collections import defaultdict
from plone import api
from plone.app.workflow.browser.sharing import SharingView
from plone.memoize.instance import memoize
from slc.teamfolder.config import TEAMS


class AssignTeam(SharingView):
    """Custom version of the SharingView which assigns users to folder
    specific groups instead of local_roles
    """

    template = ViewPageTemplateFile('templates/assign_team.pt')

    @memoize
    def existing_role_settings(self):
        """Return a data structure which mimics the one returned by the
        SharingView method except that this one is generated by
        looking up the members of the folder specific groups (teams)
        rather than looking at the local or inherited roles.
        """
        context = self.context
        uuid = api.content.get_uuid(obj=context)

        member_roles = defaultdict(list)
        for team in TEAMS:
            team_id = uuid+"-"+team.lower()
            try:
                members = api.user.get_users(groupname=team_id)
            except api.exc.GroupNotFoundError:
                members = []
            for member in members:
                member_id = member.getId()
                member_roles[member_id].append(team)

        def roles_dict(roles_list):
            rdict = {}
            for team in TEAMS:
                rdict[team] = team in roles_list
            return rdict

        role_settings = []
        for member in member_roles.keys():
            role_settings.append({
                'disabled': False,
                'id': member,
                'title': api.user.get(username=member).getProperty("fullname"),
                'type': 'user',
                'roles': roles_dict(member_roles[member]),
            })
        return role_settings
