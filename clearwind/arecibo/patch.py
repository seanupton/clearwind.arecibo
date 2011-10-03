from Products.SiteErrorLog import SiteErrorLog
from zope.app.component.hooks import getSite
from wrapper import arecibo 
import traceback


def is_contained(context, site):
    if not hasattr(site, 'getPhysicalPath'):
        return False
    sitepath = site.getPhysicalPath()
    l = len(sitepath)
    return sitepath[:l] == context.getPhysicalPath()[:l]


old_raising = SiteErrorLog.SiteErrorLog.raising
def raising(self, *args, **kw): 
    site = getSite()
    if site and site.meta_type == "Plone Site" and is_contained(self, site):
        err = str(getattr(args[0][0], '__name__', args[0][0]))
        tb = "\n".join(traceback.format_tb(args[0][2]))
        msg = args[0][1]
        arecibo(self, error_type=err, error_tb=tb, error_msg=msg)
    return old_raising(self, *args, **kw)
                             
SiteErrorLog.SiteErrorLog.raising = raising
