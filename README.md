# AMON Client

This project contains AMON HTTPS Post client used to sent alerts to  the AMON servers.
Before running this plugin, create a subdirectory alert and alerts/archive. As of July 2nd 2019, it is compatibley with Python3. 

Download or clone this git repository. 
The main directory `client` contains the AMON client module *amon_client_post_ssl.py*.
The `twisted/plugin` directory containes the plugin *amon_client_post_ssl_plugin.py*

This client is run as a plugin with the *twisted* program. 
*Twisted* can be installed using the command 

```
pip install twisted
```

Once you know *twisted* is installed, you can clone this directory and install the AMON-client using 

```
python setup.py install 
```

You can add the flag `--user` depending on how you manage your python installations.

To check that the installation work you can run the command `twistd --help`. This should display the available commands that can be used with *twisted*.

The command that should appear in the list is `clientpostssl`.    

<!-- Each alert sent to AMON is moved to the archive subdirectory alerts/archive. -->

## How to use it:

You will need to receive the certificate and key files for SSL connection for both Development and Production machines. Ask any of the AMON team members for them. 

### START DAEMON - run the command bellow 

_You can also define a directory for the log files_

#### Send to the AMON machine
```
twistd -l client.log --pidfile client.pid clientpostssl --hostport "<amon-dev-host>, <amon-prod-host>" --epath /path/to/alerts/ --finaldir NAME_OF_FINALDIR --cfile "client_dev.crt, client_prod.crt" --kfile client.key
```
This is if the events produced are in one computer, which will have the same key file for both certificates (unless you have produced two different key files). 

_An extra option is available to define the time in seconds to check files in epath_ `--looptime` 

#### Kill Daemon
```
kill `cat client.pid`
```

## Dependencies:
 * Twisted >=19.2.1 (recommended >=15.1.1) 
 * PyOpenSSL >=0.14 (recommended >=0.15.11) 
 * pycrypto >= 2.6.1 
 * cffi (recommended >=1.1.0) 
 * cryptography (recommended >=0.9) 
 * service_identity > 14.0.0 (recommneded >=16.0.0) 

## Uninstall

To uninstall the twisted plugin run the command

```
pip uninstall AMON-client
```

This will remove the command from the *twisted* program. 

