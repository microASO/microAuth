"""
proxy cache REST
"""
import logging
import re
import sys
import traceback

from python import getProxy

try:
    userDN = '/DC=ch/DC=cern/OU=Organic Units/OU=Users/CN=erupeika/CN=775659/CN=Emilis Antanas Rupeika'
    group = ''
    role = ''
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logger = logging.getLogger('spam_application')

    serviceCert = '/data/certs/hostcert.pem'
    serviceKey = '/data/certs/hostkey.pem'

    defaultDelegation = {'logger': logger,
                         'credServerPath': 'credentials',
                         'myProxySvr': 'myproxy.cern.ch',
                         'min_time_left': 36000,
                         'serverDN': "/DC=ch/DC=cern/OU=computers/CN=vocms0105.cern.ch",
                         'uisource': "/data/srv/tmp.sh"
                        }

    cache_area = 'https://cmsweb.cern.ch/crabserver/prod/filemetadata'
    getCache = re.compile('https?://([^/]*)/.*')
    myproxyAccount = getCache.findall(cache_area)[0]
    defaultDelegation['myproxyAccount'] = myproxyAccount

    defaultDelegation['server_cert'] = serviceCert
    defaultDelegation['server_key'] = serviceKey

    valid = False
    defaultDelegation['userDN'] = userDN
    defaultDelegation['group'] = group
    defaultDelegation['role'] = role
    valid, proxy = getProxy(defaultDelegation, logger)
except Exception as ex:
    msg = "Error getting the user proxy"
    print msg
    msg += str(ex)
    msg += str(traceback.format_exc())
    logger.error(msg)
if valid:
    userProxy = proxy
else:
    logger.error('Did not get valid proxy.')

print ("Sending %s" % userProxy)
