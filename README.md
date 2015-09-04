# PIAPortForward
This is a Deluge plugin for Private Internet Access (PIA) users.  This plugin will monitor for listening ports on the PIA VPN server.  If none exist, it will open one automatically and configure Deluge to that new opened listening port.  It will periodically do this from time to time to ensure that the port doesn't get closed by PIA.

In order for this plugin to work, you will need to provide your PIA account username and password in the plugin options.  Unfortunately, this is inherently unsafe because it leaves your password exposed in plain text on your system.  I can obfuscate the password if there are any requests to do so.  But, this is again inherently insecure.
