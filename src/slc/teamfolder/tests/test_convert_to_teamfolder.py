# -*- coding: utf-8 -*-

from p4a.subtyper.interfaces import ISubtyper
from plone import api
from slc.teamfolder.tests.base import FUNCTIONAL_TESTING
from zope.component import getUtility

import unittest2 as unittest


class TestConvertToTeamFolder(unittest.TestCase):
    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        subtyper = getUtility(ISubtyper)
        teamfolder = self.portal.teamfolder
        subtyper.change_type(teamfolder, "teamfolder")
        teamfolder.unrestrictedTraverse("@@convert-to-teamfolder")()
        self.assign_team_view = teamfolder.unrestrictedTraverse("assign-team")


    def test_teams_are_created(self):
        contributor_team = api.group.get(
            groupname=self.assign_team_view.get_team_id("Contributor"))
        self.assertTrue(contributor_team is not None)

    def test_users_are_added_to_teams(self):
        contributor_team_id = self.assign_team_view.get_team_id("Contributor")
        contributor_group_ids = [
            i.getId() for i in api.group.get_groups(username="contributor")]
        self.assertTrue(contributor_team_id in contributor_group_ids)

    def test_local_roles_are_cleared(self):
        local_roles = api.user.get_roles(
            username="contributor", obj=self.portal.teamfolder)
        self.assertTrue("contributor" not in local_roles)
