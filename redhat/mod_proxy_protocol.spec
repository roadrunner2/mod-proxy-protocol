%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn || echo 0-0)}}
%{!?_httpd_apxs:       %{expand: %%global _httpd_apxs       %%{_sbindir}/apxs}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir:    %{expand: %%global _httpd_moddir    %%{_libdir}/httpd/modules}}

Name:           mod_proxy_protocol
Summary:        Apache module that implements the downstream server side of HAProxy's Proxy Protocol.
Version:        0.1
Release:        1.20141031git62d2df6%{?dist}
License:        ASL 2.0
Group:          System Environment/Daemons
Source0:        https://github.com/roadrunner2/mod-proxy-protocol/archive/62d2df6.tar.gz
Source1:        proxy_protocol.module
Source2:        proxy_protocol.conf
Patch0:         mod_proxy_protocol.c-fix-apr14-compat.patch
BuildRequires:  httpd-devel
Requires:       httpd
URL:            https://github.com/roadrunner2/mod-proxy-protocol

# Suppress auto-provides for module DSO per
# https://fedoraproject.org/wiki/Packaging:AutoProvidesAndRequiresFiltering#Summary
%{?filter_provides_in: %filter_provides_in %{_libdir}/httpd/modules/.*\.so$}
%{?filter_setup}

%description
HAProxy's Proxy Protocol is a way for upstream proxies and load balancers to
report the IP address of the original remote client to the downstream server,
without having to modify things like HTTP headers in the actual payload.
This package contains an Apache module that implements the downstream (i.e. the
receiving) server side of this protocol, thereby allowing other modules to see
and use the actual client's IP address instead of that of the upstream proxy or
load balancer.

%prep
#%setup -q -n mod_proxy_protocol-%{version}
%setup -q -n mod-proxy-protocol-62d2df6c94eb0a18605e47f6236c08130d7e120d
%patch0

%build
%{_httpd_apxs} -c mod_proxy_protocol.c

%install
rm -rf $RPM_BUILD_ROOT
install -Dm 755 .libs/mod_proxy_protocol.so $RPM_BUILD_ROOT%{_httpd_moddir}/mod_proxy_protocol.so

%if "%{_httpd_modconfdir}" == "%{_httpd_confdir}"
# httpd <= 2.2.x
cat %{SOURCE1} > unified.conf
echo >> unified.conf
cat %{SOURCE2} >> unified.conf
touch -c -r %{SOURCE1} unified.conf
install -Dp -m 644 unified.conf $RPM_BUILD_ROOT%{_httpd_confdir}/proxy_protocol.conf
%else
# httpd >= 2.4.x
install -Dp -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_httpd_modconfdir}/10-proxy_protocol.conf
install -Dp -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_httpd_confdir}/proxy_protocol.conf
%endif

%files
%doc README.md LICENSE
%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
%config(noreplace) %{_httpd_modconfdir}/10-proxy_protocol.conf
%endif
%config(noreplace) %{_httpd_confdir}/proxy_protocol.conf
%{_httpd_moddir}/*.so

%changelog
* Fri May 20 2016 earsdown <earsdown@github.com> 0.1-1.20141031git62d2df6
- First package release. Includes mamanguy patch to fix APR 1.4.x compatibility.
