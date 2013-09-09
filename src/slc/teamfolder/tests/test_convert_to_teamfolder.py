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
        subtyper.change_type(self.portal.teamfolder, "teamfolder")
        self.portal.teamfolder.unrestrictedTraverse(
            "@@convert-to-teamfolder")()
        self.teamfolder_uuid = api.content.get_uuid(obj=self.portal.teamfolder)

    def test_teams_are_created(self):
        contributor_team = api.group.get(
            groupname=self.teamfolder_uuid+"-contributor")
        self.assertTrue(contributor_team is not None)

    def test_users_are_added_to_teams(self):
        contributor_team_id = self.teamfolder_uuid+"-contributor"
        contributor_group_ids = [
            i.getId() for i in api.group.get_groups(username="contributor")]
        self.assertTrue(contributor_team_id in contributor_group_ids)

    def test_local_roles_are_cleared(self):
        local_roles = api.user.get_roles(
            username="contributor", obj=self.portal.teamfolder)
        self.assertTrue("contributor" not in local_roles)
