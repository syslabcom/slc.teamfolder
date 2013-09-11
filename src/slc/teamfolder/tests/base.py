# -*- coding: utf-8 -*-
"""Base module for unittesting."""

from plone import api
from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles


class TeamFolderLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Prepare Zope instance by loading appropriate ZCMLs."""
        import p4a.subtyper
        self.loadZCML(package=p4a.subtyper)
        import slc.teamfolder
        self.loadZCML(package=slc.teamfolder)

    def setUpPloneSite(self, portal):
        """Prepare a Plone instance for testing."""
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'Products.CMFPlone:plone')

        # Install p4a.subtyper
        self.applyProfile(portal, 'p4a.subtyper:default')

        # Install the TeamFolder profile
        self.applyProfile(portal, 'slc.teamfolder:default')

        # Create test content
        self.applyProfile(portal, 'slc.teamfolder:testfixture')

        # Login as Manager
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        # Add some users
        editor = api.user.create(
            email="editor@example.com",
            username="editor",
            properties={"fullname": "An Editor"},
        )
        contributor = api.user.create(
            email="contributor@example.com",
            username="contributor",
            properties={"fullname": "A Contributor"},
        )

        # Grant local roles on the teamfolder
        portal = api.portal.get()
        tf = portal.teamfolder
        api.user.grant_roles(username="editor", roles=["Editor"], obj=tf)
        api.user.grant_roles(
            username="contributor", roles=["Contributor"], obj=tf)


    def tearDownZope(self, app):
        """Tear down Zope."""


FIXTURE = TeamFolderLayer()
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name="TeamFolderLayer:Functional")
