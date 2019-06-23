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

try:
    from setuptools.command import egg_info
    egg_info.write_toplevel_names
except (ImportError, AttributeError):
    pass
else:
    def _top_level_package(name):
        return name.split('.', 1)[0]

    def _hacked_write_toplevel_names(cmd, basename, filename):
        pkgs = dict.fromkeys(
            [_top_level_package(k)
                for k in cmd.distribution.iter_distribution_names()
                if _top_level_package(k) != "twisted"
            ]
        )
        cmd.write_file("top-level names", filename, '\n'.join(pkgs) + '\n')

    egg_info.write_toplevel_names = _hacked_write_toplevel_names


setup(
    name="AMON-client",
    version = "1.0",
    description = "AMON client to send events",
    author = __author__,
    author_email = 'hgayala@psu.edu',
    packages = [
        "client",
        "twisted/plugins",
    ],
    package_data={
       'twisted':['plugins/amon_client_post_ssl_plugin.py']
    },
    include_package_data = True,
    zip_safe=False,
    )

refresh_plugin_cache()
