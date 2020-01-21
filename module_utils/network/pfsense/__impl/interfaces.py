# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Orion Poplawski <orion@nwra.com>
# Copyright: (c) 2019, Frederic Bor <frederic.bor@wanadoo.fr>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


def get_interface_by_display_name(self, name):
    """ return interface_id by name """
    for interface in self.interfaces:
        descr_elt = interface.find('descr')
        if descr_elt is not None and descr_elt.text.strip().lower() == name.lower():
            return interface.tag
    return None


def get_interface_by_port(self, name):
    """ return interface_id by port (os name) """
    for interface in self.interfaces:
        if interface.find('if').text.strip() == name:
            return interface.tag
    return None


def get_interface_display_name(self, interface_id):
    """ return interface display name if found, otherwhise return the interface_id """
    if interface_id == 'enc0':
        return 'IPsec'
    if interface_id == 'openvpn':
        return 'OpenVPN'

    for interface in self.interfaces:
        if interface.tag == interface_id:
            descr_elt = interface.find('descr')
            if descr_elt is not None:
                return descr_elt.text.strip()
            break

    return interface_id


def get_interface_port(self, interface_id):
    """ return interface port """
    for interface in self.interfaces:
        if interface.tag == interface_id:
            return interface.find('if').text.strip()
    return None


def get_interface_port_by_display_name(self, name):
    """ return interface port """
    for interface in self.interfaces:
        descr_elt = interface.find('descr')
        if descr_elt is not None and descr_elt.text.strip().lower() == name.lower():
            return interface.find('if').text.strip()
    return None


def is_interface_port(self, interface_port):
    """ determines if arg is a pfsense interface port or not """
    for interface in self.interfaces:
        interface_elt = interface.tag.strip()
        if interface_elt == interface_port:
            return True
    return False


def is_interface_display_name(self, name):
    """ determines if arg is an interface name or not """
    for interface in self.interfaces:
        descr_elt = interface.find('descr')
        if descr_elt is not None:
            if descr_elt.text.strip().lower() == name.lower():
                return True
    return False


def parse_interface(self, interface, fail=True, with_virtual=True):
    """ validate param interface field """
    if with_virtual and (interface == 'enc0' or interface.lower() == 'ipsec') and self.is_ipsec_enabled():
        return 'enc0'
    if with_virtual and (interface == 'openvpn' or interface.lower() == 'openvpn') and self.is_openvpn_enabled():
        return 'openvpn'

    if self.is_interface_display_name(interface):
        return self.get_interface_by_display_name(interface)
    elif self.is_interface_port(interface):
        return interface

    if fail:
        self.module.fail_json(msg='%s is not a valid interface' % (interface))
    return None
