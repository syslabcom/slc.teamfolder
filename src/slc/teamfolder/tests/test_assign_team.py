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
        teamfolder = self.portal.teamfolder
        self.teamfolder_uuid = api.content.get_uuid(obj=teamfolder)
        self.assign_team_view = teamfolder.unrestrictedTraverse("assign-team")

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
