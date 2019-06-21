'''setup.py for AMON client plugin

This will include the AMON Client plugin as part of the twisted ddirectory. This plugin is one way to send events to the AMON system.

After the installation, the plugin should be manageable as a twistd command. 

For example:
twistd -l client.log --pidfile client.pid clientpostssl --hostport "https://192.5.158.139/amon" --epath /path/to/alerts/ --finaldir $NAMEOFFINALDIR --cfile client_ic_dev.crt --kfile client_ic_dev.key

'''

__author__ = 'Hugo Ayala'

import sys

try:
  import twisted
except ImportError:
  raise SystemExit("twisted not found. Make sure"
                   "you have installed the Twisted core package.")

from setuptools import setup, find_packages
from setuptools.command.install import install

def refresh_plugin_cache():
    from twisted.plugin import IPlugin, getPlugins
    list(getPlugins(IPlugin))

setup(
    name="AMON-client",
    version = "1.0",
    description = "AMON client to send events",
    author = __author__,
    author_email = 'hgayala@psu.edu',
    packages = [
        "client",
        "twisted.plugins",
    ],
    package_data={
       'twisted':['plugins/amon_client_post_ssl_plugin.py']
    },
    include_package_data = True,
    )

refresh_plugin_cache()
