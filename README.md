# AMON Client

This project contains AMON HTTPS Post client used to sent alerts to  the AMON servers.
Before running this plugin, create a subdirectory alert and alerts/archive.

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

You will need to receive the certificate and key files for SSL connection. Ask any of the AMON team members for them. 

### START DAEMON - run one of the two commands bellow 

_You can also define a directory for the log files_

#### Send to the development AMON machine
```
twistd -l client.log --pidfile client.pid clientpostssl --hostport "https://192.5.158.145/amon" --epath /path/to/alerts/ --finaldir $NAMEOFFINALDIR --cfile client_ic_dev.crt --kfile client_ic_dev.key
```

#### Send to the production AMON dual servers
```
twistd -l client.log --pidfile client.pid clientpostssl --hostport "https://192.5.158.139/amon" --epath /path/to/alerts/ --finaldir $NAMEOFFINALDIR --cfile client_ic_dev.crt --kfile client_ic_dev.key
```

#### Kill Daemon
```
kill `cat client.pid`
```

## Dependencies:
 * Twisted >=18.9.0 (recommended >=15.1.1) 
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

