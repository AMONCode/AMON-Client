"""@package amon_client_post_events_ssl
client that sends events to the server using HTTP
protocol with method=POST
Run with twistd. Default is run as a daemon process.
 twistd -l client.log --pidfile client.pid clientpostssl --hostport "<amon-hostport>"
 --epath /path_to_client_ents --cfile client.crt --kfile client.key
 Kill it with kill `cat client.pid`
 Before running make directory archive within directory where your client events live.
 Each sent event will be moved from client directory to archive directory.
 Modify if you do not want to save sent events.
"""
import sys, getopt, os, shutil, datetime
import resource
import fcntl

from zope.interface import implements,implementer
from twisted.application import internet, service
from twisted.application.internet import TimerService
from twisted.application.internet import task
from twisted.plugin import IPlugin
from twisted.python import usage, log

from client.amon_client_post_ssl import check_for_files
from twisted.python import usage, log
# Make a plugin using IServiceMaker



class Options(usage.Options):

    optParameters = [
        ['hostport', 'hp', None, 'The host for https address. For multiple hosts supply them seperated by commas. '],
        ['epath', None, None, 'Path to the directory with VOEvents'],
        ['finaldir', None, None, 'Directory name for final position'],
        ['kfile', None, None, 'Key file name. For multiple key files supply them seperated by commas. '],
        ['cfile', None, None, 'Certificate name. For multiple hosts supply cert file names seperated by commas. '],
        ['looptime','lt',10.0,'How often to check epath for files in seconds'],
        ]

    def postOptions(self):

        Nhosts = len(self['hostport'].split(','))
        hosts = [host.strip().encode() for host in self['hostport'].split(',')]
        fkeys = [fkey.strip() for fkey in self['kfile'].split(',')]
        fcerts = [fcert.strip() for fcert in self['cfile'].split(',')]
        if Nhosts != len(fcerts):
            raise usage.UsageError("There must be one certificate file for each host")
        elif Nhosts != len(fkeys) and len(fkeys) > 1:
            raise usage.UsageError("There must be one key file for each host or only one key file to use for all hosts")

        for fkey in fkeys:
            if not os.path.exists(fkey):
                raise usage.UsageError("keyfile %s doesn't exist"%(fkey))
        for fcert in fcerts:
            if not os.path.exists(fcert):
                raise usage.UsageError("certfile %s doesn't exist"%(fkey))

        self['hostport'] = hosts
        if len(fkeys) < Nhosts:
            self['kfile'] = [fkeys[0] for i in range(Nhosts)]
        else:
            self['kfile'] = fkeys
        self['cfile'] = fcerts



#@implementer(service.IServiceMaker, IPlugin)
@implementer(IPlugin, service.IServiceMaker)
class ClientPostServiceMaker(object):

    #implements(service.IServiceMaker, IPlugin)

    tapname = "clientpostssl"
    description = "Client http post events + ssl."
    options = Options

    def makeService(self, options):
        #check directory with events for an oldest file
        loop_service = TimerService(float(options['looptime']), check_for_files, options['hostport'],\
                                    options['epath'], options['finaldir'], options['kfile'], options['cfile'])
        # loop_service.startService()
        return loop_service

# finally, make a plugin
service_maker = ClientPostServiceMaker()
