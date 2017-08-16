"""
proxy cache REST
"""
import logging
import re

from . import getProxy

from flask import Flask, request, send_file
app = Flask(__name__)

@app.route('/getproxy', endpoint='127.0.0.1:8888')
def provideProxy():
    """

    """
    userDN = request.args.get("DN", "")
    group = ''
    role = ''
    logging.basicConfig(level="DEBUG", format="%(asctime)s:%(levelname)s:%(module)s:%(message)s")
    logger = logging.getLogger('microAuth')
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
    try:
        defaultDelegation['userDN'] = userDN
        defaultDelegation['group'] = group
        defaultDelegation['role'] = role
        valid, proxy = getProxy(defaultDelegation, logger)
    except Exception as ex:
        msg = "Error getting the user proxy"
        logger.exception(msg)
    if valid:
        userProxy = proxy
    else:
        logger.error('Did not get valid proxy.')

    return send_file(userProxy)