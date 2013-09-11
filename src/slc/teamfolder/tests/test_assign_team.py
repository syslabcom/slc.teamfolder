# -*- coding: utf-8 -*-

from Products.Five.security import newInteraction
from p4a.subtyper.interfaces import ISubtyper
from plone import api
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
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
        teamfolder = self.portal.teamfolder
        self.teamfolder_uuid = api.content.get_uuid(obj=teamfolder)
        self.assign_team_view = teamfolder.unrestrictedTraverse("assign-team")
        sub_folder = teamfolder.subfolder1
        subtyper.change_type(sub_folder, "teamfolder")
        self.unconverted_assign_team_view = sub_folder.unrestrictedTraverse(
            "assign-team")
        # Create an interaction, so that we can use checkPermission
        newInteraction()

    def test_existing_role_settings(self):
        contributor = {
            'disabled': False,
            'type': 'user',
            'id': 'contributor',
            'roles': {u'Contributor': True,
                      u'Reviewer': False,
                      u'Editor': False,
                      u'Reader': False},
            'title': 'A Contributor',
        }
        self.assertIn(
            contributor, self.assign_team_view.existing_role_settings())

    def test_update_role_settings(self):
        new_settings = [{
            'id': 'editor',
            'roles': [u'Contributor'],
            'type': 'user',
        }]
        self.assign_team_view.update_role_settings(new_settings)
        editor_group = api.group.get(groupname=self.teamfolder_uuid+"-editor")
        contributor_group = api.group.get(
            groupname=self.teamfolder_uuid+"-contributor")
        editor = api.user.get(username="editor")
        self.assertIn(editor, api.user.get_users(group=contributor_group))
        self.assertNotIn(editor, api.user.get_users(group=editor_group))

    def test_editor_cannot_convert(self):
        login(self.portal, "editor")
        self.assertFalse(self.unconverted_assign_team_view.can_convert)

    def test_manager_can_convert(self):
        self.assertTrue(self.unconverted_assign_team_view.can_convert)

    def test_manager_cannot_convert_already_converted(self):
        self.assertFalse(self.assign_team_view.can_convert)
