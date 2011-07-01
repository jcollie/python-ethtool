#! /usr/bin/python
# -*- python -*-
# -*- coding: utf-8 -*-
#   Copyright (C) 2008 Red Hat Inc.
#
#   Arnaldo Carvalho de Melo <acme@redhat.com>
#
#   This application is free software; you can redistribute it and/or
#   modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation; version 2.
#
#   This application is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   General Public License for more details.

import getopt, ethtool, sys
from optparse import OptionParser

def flags2str(flags):
	string = ""
	if flags & ethtool.IFF_UP:
		string += "UP "
	if flags & ethtool.IFF_BROADCAST:
		string += "BROADCAST "
	if flags & ethtool.IFF_DEBUG:
		string += "DEBUG "
	if flags & ethtool.IFF_LOOPBACK:
		string += "LOOPBACK "
	if flags & ethtool.IFF_POINTOPOINT:
		string += "POINTOPOINT "
	if flags & ethtool.IFF_NOTRAILERS:
		string += "NOTRAILERS "
	if flags & ethtool.IFF_RUNNING:
		string += "RUNNING "
	if flags & ethtool.IFF_NOARP:
		string += "NOARP "
	if flags & ethtool.IFF_PROMISC:
		string += "PROMISC "
	if flags & ethtool.IFF_ALLMULTI:
		string += "ALLMULTI "
	if flags & ethtool.IFF_MASTER:
		string += "MASTER "
	if flags & ethtool.IFF_SLAVE:
		string += "SLAVE "
	if flags & ethtool.IFF_MULTICAST:
		string += "MULTICAST "
	if flags & ethtool.IFF_PORTSEL:
		string += "PORTSEL "
	if flags & ethtool.IFF_AUTOMEDIA:
		string += "AUTOMEDIA "
	if flags & ethtool.IFF_DYNAMIC:
		string += "DYNAMIC "

	return string.strip()

def show_config(device):
	ipaddr = ethtool.get_ipaddr(device)
	netmask = ethtool.get_netmask(device)
	flags = ethtool.get_flags(device)
	print '%-9.9s' % device,
	if not (flags & ethtool.IFF_LOOPBACK):
		print "HWaddr %s" % ethtool.get_hwaddr(device),
	print '''
          inet addr:%s''' % ipaddr,
	if not (flags & (ethtool.IFF_LOOPBACK | ethtool.IFF_POINTOPOINT)):
		print "Bcast:%s" % ethtool.get_broadcast(device),
	print '  Mask:%s' % netmask
	for info in ethtool.get_interfaces_info(device):
		for addr in info.get_ipv6_addresses():
			print ("	  inet6 addr: %s/%s Scope: %s"
			       % (addr.address,
				  addr.netmask,
				  addr.scope))
	print '	  %s' % flags2str(flags)
	print

def main():
	global all_devices

        usage="usage: %prog [interface [interface [interface] ...]]"
        parser = OptionParser(usage=usage)
        (opts, args) = parser.parse_args()

        if args is None or len(args) == 0:
                sel_devs = ethtool.get_active_devices()
        else:
                sel_devs = args

	for device in sel_devs:
                try:
                        show_config(device)
                except Exception, ex:
                        print "** ERROR ** [Device %s]: %s" % (device, str(ex))
                        sys.exit(2)

if __name__ == '__main__':
    main()
