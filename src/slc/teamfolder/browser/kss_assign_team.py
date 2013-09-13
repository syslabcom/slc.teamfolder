from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.workflow.browser.kss_sharing import KSSSharingView
from zope.component import getMultiAdapter


class KSSAssignTeam(KSSSharingView):
    """Override KSS view for sharing page to point it to another view and
    template.
    """
    template = ViewPageTemplateFile('templates/assign_team.pt')

    def updateSharingInfo(self, search_term=''):
        sharing = getMultiAdapter(
            (self.context, self.request), name="assign-team")

        # get the html from a macro
        ksscore = self.getCommandSet('core')

        the_id = 'user-group-sharing'
        macro = self.template.macros[the_id]
        res = self.macro_wrapper(
            the_macro=macro, instance=self.context, view=sharing)
        ksscore.replaceHTML(ksscore.getHtmlIdSelector(the_id), res)
        self.issueAllPortalMessages()
        return self.render()
