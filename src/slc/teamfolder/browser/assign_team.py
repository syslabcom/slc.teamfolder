# -*- coding: utf-8 -*-
"""Custom version of the sharing view to allow a "Head of Department"
group member to be assigned the local role of Checker on a
QualityStandard item.
"""
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.workflow.browser.sharing import SharingView
from plone.app.workflow.interfaces import ISharingPageRole
from plone.memoize.instance import memoize
from zope.component import queryUtility


class AssignTeam(SharingView):
    """Custom version of the SharingView which assigns users to folder
    specific groups instead of local_roles
    """

    template = ViewPageTemplateFile(
        'templates/assign_team.pt')

