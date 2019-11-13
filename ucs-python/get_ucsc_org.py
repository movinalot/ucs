""" Retrieve UCS Central Orgs """

from ucscsdk.ucschandle import UcscHandle

handle = UcscHandle("10.200.0.150", "admin", "C1sco12345!")
handle.login()

ucsc_objs = handle.query_classid("orgOrg")
for ucsc_obj in ucsc_objs:
    print("Org Name: " + ucsc_obj.name, "Org Dn: " + ucsc_obj.dn)

handle.logout()