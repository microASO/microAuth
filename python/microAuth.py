"""
proxy cache REST
"""
import logging
import re
import sys
import traceback

from . import getProxy

from flask import Flask, request, send_file
app = Flask(__name__)

@app.route('/getproxy')
def provideProxy():
    """

    """
    try:
        userDN = request.args.get("DN", "")
        group = ''
        role = ''
        logger = app.logger

        serviceCert = '/data/certs/hostcert.pem'
        serviceKey = '/data/certs/hostkey.pem'

        defaultDelegation = {'logger': logger,
                             'credServerPath': 'credentials',
                             'myProxySvr': 'myproxy.cern.ch',
                             'min_time_left': 36000,
                             'serverDN': "/DC=ch/DC=cern/OU=computers/CN=vocms0105.cern.ch",
                             'uisource': "/data/srv/tmp.sh"
                            }

        cache_area = 'https://cmsweb-testbed.cern.ch/crabserver/preprod/filemetadata'
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
    return send_file(userProxy)
