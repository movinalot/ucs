""" Retrieve UCS Central Orgs """

from ucscsdk.ucschandle import UcscHandle

HANDLE = UcscHandle("10.200.0.150", "admin", "C1sco12345!")
HANDLE.login()

UCSC_OBJS = HANDLE.query_classid("orgOrg")
for ucsc_obj in UCSC_OBJS:
    print("Org Name: " + ucsc_obj.name, "Org Dn: " + ucsc_obj.dn)

HANDLE.logout()
