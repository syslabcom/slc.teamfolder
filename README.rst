=====================================================================================
 slc.teamfolder: assign users to folder specific groups instead of using local roles
=====================================================================================

Changing the local_roles of a top level folder causes all sub-items to
be re-indexed. On a large site this can be a significant performance
issue.

slc.teamfolder works around this issue by allowing a normal folder to
be changed into a "Team Folder". This replaces the Sharing tab with a
Team tab which looks very similar to the Sharing tab, but is
implemented differently.

Implementation
==============

slc.teamfolder uses p4a.subtyper to allow a folder to be changed into
a "Team Folder". Upon conversion three groups are created which
correspond to the Contributor, Editor, Reviewer and Reader local
roles. Users which have been assigned the equivalent local roles will
be added to the relevant groups and then removed from the local
roles. Additional users can be added to these groups in the same way
as users can be assigned local roles in the sharing tab.
