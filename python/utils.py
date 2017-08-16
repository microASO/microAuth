"""
Utilities
"""
import os
import time
import logging
import hashlib
import subprocess

from WMCore.Services.SiteDB.SiteDB import SiteDBJSON
from WMCore.Credential.Proxy import Proxy

__version__ = '0.0.1'


def getProxy(defaultDelegation, log):
    """
    _getProxy_
    """
    log.debug("Retrieving proxy for %s" % defaultDelegation['userDN'])
    proxy = Proxy(defaultDelegation)
    proxyPath = proxy.getProxyFilename(True)
    timeleft = proxy.getTimeLeft(proxyPath)
    if timeleft is not None and timeleft > 3600:
        return (True, proxyPath)
    proxyPath = proxy.logonRenewMyProxy()
    timeleft = proxy.getTimeLeft(proxyPath)
    if timeleft is not None and timeleft > 0:
        return (True, proxyPath)
    return (False, None)
