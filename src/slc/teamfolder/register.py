from plone.app.users.browser.register import getGroupIds
from zope.schema.vocabulary import SimpleVocabulary


def get_non_teamfolder_group_ids(context):
    return SimpleVocabulary([
        i for i in getGroupIds(context) if not i.value.startswith("{")])
