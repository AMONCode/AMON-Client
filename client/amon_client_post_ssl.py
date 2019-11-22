"""@package amon_client_post_ssl
client that sends events to the server using HTTP
protocol with method=POST over TLS with certificate and key file client.crt and client.key
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys, getopt, os, shutil, logging, datetime, time
import resource
import fcntl
import traceback, io

from twisted.internet import reactor, ssl, tcp, interfaces
from twisted.python import usage, log
from twisted.internet.task import LoopingCall
from twisted.internet.defer import Deferred, succeed, DeferredList
from twisted.internet.protocol import Protocol
from twisted.web.client import Agent, FileBodyProducer
from twisted.web import http_headers
from twisted.internet.ssl import ClientContextFactory
from twisted.python.modules import getModule
from OpenSSL import SSL
from zope.interface import implements
#from zope.interface import implementer_only, implementedBy
from twisted.python.filepath import FilePath

path=host=False

MOVEFILE=True

class ResourcePrinter(Protocol):
    def __init__(self, finished):
        self.finished = finished

    def dataReceived(self, data):
        print(data)

    def connectionLost(self, reason):
        print('Finished receiving body:', reason.getErrorMessage())
        self.finished.callback(None)

def printResource(response):
    finished = Deferred()
    response.deliverBody(ResourcePrinter(finished))
    return finished

def printError(failure):
    failure.value.reasons[0].printTraceback()
    return failure


def moveFile_OnSucess(result, oldpos, newpos):

    # time.sleep(2.0)
    MOVE = True
    for (success, value) in result:
        if success:
            print('Success:', value)
        else:
            print('Failure:', value.getErrorMessage())
            MOVE = False
    if MOVE:
        shutil.move(oldpos,newpos)
        print("old location: %s, new location %s"%(oldpos, newpos))
    return result



def stop(result):
    reactor.stop()

def moveFile(path, fname):
    shutil.move(path+fname, path+"archive/"+fname)
    print("File %s sent" % (fname,))

def printSent(fname):
    print("File %s sent" % (fname,))

def printNotSent(filename):
    print("File %s not sent" % (fname,))

def check_open_fds():
    fds = []
    soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    for fd in range(0, soft):
        try:
            flags = fcntl.fcntl(fd, fcntl.F_GETFD)
        except IOError:
            continue
        fds.append(fd)
    return soft, fds


class MyClientContextFactory(object):
    """A context factory for SSL clients."""

    isClient = 1
    method = SSL.SSLv23_METHOD
    def __init__(self, certfile, keyfile):
        self.certificateFileName = certfile
        self.privateKeyFileName = keyfile
    def getContext(self, hostname, port):
        ctx = SSL.Context(self.method)
        ctx.set_options(SSL.OP_NO_SSLv2)
        ctx.set_options(SSL.OP_NO_SSLv3)
        ctx.use_certificate_file(self.certificateFileName)
        ctx.use_privatekey_file(self.privateKeyFileName)
        return ctx

def check_for_files(hostport, eventpath, finaldir, keyfile, certfile):
    # check a directory with events (eventpath) for an oldest xml file
    # if found post it to the server (hostport) using HTTP POST protocol

    # check for number of open file descriptors first, OS X is limited by default to 256
    # each OS has its own limitation, file descriptors are open not only when the file
    # is open, but for each new socket/connection opened as well

    # log.msg("Entering check_for_files", logLevel=logging.DEBUG)
    fds = []
    soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    for fd in range(0, soft):
        try:
            flags = fcntl.fcntl(fd, fcntl.F_GETFD)
        except IOError:
            continue
        fds.append(fd)

    if (len(fds)<=soft):
        Nhosts = len(hostport)
        hosts = hostport
        fkeys = keyfile
        fcerts = certfile
        # host=hostport.encode()
        path=eventpath
        if finaldir is None:
            fdir =os.path.join(eventpath,'archive')
            os.mkdir(fdir)
        else:
            fdir = finaldir
        # fkey = keyfile
        # fcert = certfile

        # agent = Agent(reactor, MyClientContextFactory(fcert, fkey))

        files = sorted(os.listdir(path), key=lambda p: os.path.getctime(os.path.join(path, p)))
        files_xml=[]

        for filename in files:
            if (os.path.isdir(path+filename) or filename[0]=='.' or filename.find(".log") !=-1):
                pass
            elif (filename.find(".xml")!=-1):
                files_xml.append(filename)
            else:
                pass

        # log.msg("%d xml files in directory"%(len(files_xml)), logLevel=logging.DEBUG)
        if len(files_xml)>0:
            oldest = files_xml[0]
            oldpos = os.path.join(path, oldest)
            newpos = os.path.join(fdir, oldest)

            d_list = []

            for host,fkey,fcert in zip(hosts,fkeys,fcerts):
                try:
                    print(host,fkey,fcert)
                    agent = Agent(reactor, MyClientContextFactory(fcert, fkey))

                    datafile=open(oldpos,'rb')
                    body=FileBodyProducer(datafile)
                    # since twisted v.15 length is string
                    length_data=str(body.length)
                    headers = http_headers.Headers({'User-Agent': ['Twisted HTTP Client'],
                                                'Content-Type':['text/xml'],
                                                'Content-Lenght': [length_data],
                                                'Content-Name':[oldest]})
                    method = b'POST'#.encode()
                    d = agent.request(method, host, headers=headers, bodyProducer=body)
                    # on success it returns Deferred with a response object
                    print("\nFound file")
                    d.addCallbacks(printResource, printError)
                    d_list.append(d)
                except (RuntimeError, TypeError, NameError, AttributeError, Exception) as e:
                    log.msg("Error sending file %s to host %s" % (oldest,host))
                    log.msg("Error: "+str(e))
                    log.msg(traceback.print_exc())
                    global MOVEFILE
                    MOVEFILE=False

            dl = DeferredList(d_list, consumeErrors=True)
            dl.addCallback(moveFile_OnSucess,oldpos,newpos)
            # time.sleep(3.0)
            # log.msg("Exiting check_for_files", logLevel=logging.DEBUG)
            return dl

            # if MOVEFILE:
            #     shutil.move(oldpos,newpos)
            #     print("old location: %s, new location %s"%(oldpos, newpos))
            # else:
            #     print("Check connection. File not moved")
        else:
            pass
    else:
        pass
