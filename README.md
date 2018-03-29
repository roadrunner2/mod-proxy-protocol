# Apache Proxy Protocol Module

This is an [Apache](http://httpd.apache.org/) module that implements the
server side of HAProxy's
[Proxy Protocol](http://blog.haproxy.com/haproxy/proxy-protocol/).

Note: as of Apache 2.4.30 this code has been merged into
[mod_remoteip](https://httpd.apache.org/docs/2.4/mod/mod_remoteip.html),
with the `ProxyProtocol` directive renamed to `RemoteIPProxyProtocol`.

## Build and Install

You'll need the apache development packages installed (typically something
like `apache-devel` or `apache2-dev`). Then simply running `make` will
create the shared library in `.libs/mod_proxy_protocol.so`; `make install`
will attempt to install it in your current apache installation (you'll
probably need to be root for this).

## Configuration

Add the following directive to your apache config to load the module

    LoadModule proxy_protocol_module <path-to-module>/mod_proxy_protocol.so

or try running

    apxs -a mod_proxy_protocol.c

For configuration details see the
[module docs](http://roadrunner2.github.io/mod-proxy-protocol/mod_proxy_protocol.html)

## Amazon EC2 Notes

To properly secure Apache when using this on EC2 behind an ELB you'll probably
want to do something like the following to ensure that only the ELB can
provide the proxy protocol header while still being able to access the site
directly (not via the ELB):

1. In Apache create a copy of virtual host with a new port, and add the
   'ProxyProtocol On' directive to this new virtual host.
2. Add an entry to the security group for the server that only allows access
   to this new port from the ELB (specify the source as `amazon-elb/amazon-elb-sg`)
3. Point the ELB listener at this new port (and of course
   [enable](http://docs.aws.amazon.com/ElasticLoadBalancing/latest/DeveloperGuide/enable-proxy-protocol.html)
   the proxy protocol for that)

## TODO

* Add access-control (see commented out `ProxyProtocolTrustedProxies` in
  `mod_proxy_protocol.xml`)
* Add support for outgoing connections (`mod_proxy`)

