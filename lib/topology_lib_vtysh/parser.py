# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
Parse vtysh commands with output to a python dictionary.
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division


import re


def parse_show_interface(raw_result):
    """

    Parse the 'show interface' command raw output.

    :param str raw_result: vtysh raw result string.
    :rtype: dict
    :return: The parsed result of the show interface command in a
    dictionary of the form:

     ::

        {
            'admin_state': 'down',
            'autonegotiation': True,
            'conection_type': 'Half-duplex',
            'hadrware': 'Ethernet',
            'input_flow_control': False,
            'interface_state': 'down',
            'mac_address': 'aa:55:aa:55:00:43',
            'mtu': 0,
            'output_flow_control': False,
            'port': 1,
            'rx_crc_fcs': 0,
            'rx_dropped': 0,
            'rx_input_bytes': 0,
            'rx_input_error': 0,
            'rx_input_packets': 0,
            'speed': 0,
            'speed_unit': 'Mb/s',
            'state_description': 'Administratively down',
            'state_information': 'admin_down',
            'tx_bytes': 0,
            'tx_collisions': 0,
            'tx_dropped': 0,
            'tx_input_errors': 0,
            'tx_output_packets': 0
        }
    """

    show_re = (
        r'\s+Interface (?P<port>\d+) is (?P<interface_state>\S+) '
        r'\((?P<state_description>.*)\)\s+'
        r'Admin state is (?P<admin_state>\S+)\s+'
        r'State information: (?P<state_information>\S+)\s+'
        r'Hardware: (?P<hardware>\S+), MAC Address: (?P<mac_address>\S+)\s+'
        r'MTU (?P<mtu>\d+)\s+'
        r'(?P<conection_type>\S+)\s+'
        r'Speed (?P<speed>\d+) (?P<speed_unit>\S+)\s+'
        r'Auto-Negotiation is turned (?P<autonegotiation>\S+)\s+'
        r'Input flow-control is (?P<input_flow_control>\w+),\s+'
        r'output flow-control is (?P<output_flow_control>\w+)\s+'
        r'RX\s+'
        r'(?P<rx_packets>\d+) input packets\s+'
        r'(?P<rx_bytes>\d+) bytes\s+'
        r'(?P<rx_error>\d+) input error\s+'
        r'(?P<rx_dropped>\d+) dropped\s+'
        r'(?P<rx_crc_fcs>\d+) CRC/FCS\s+'
        r'TX\s+'
        r'(?P<tx_packets>\d+) output packets\s+'
        r'(?P<tx_bytes>\d+) bytes\s+'
        r'(?P<tx_errors>\d+) input error\s+'
        r'(?P<tx_dropped>\d+) dropped\s+'
        r'(?P<tx_collisions>\d+) collision'
    )

    raw_result = re.match(show_re, raw_result)
    assert raw_result

    result = raw_result.groupdict()
    for key, value in result.items():
        if value.isdigit():
            result[key] = int(value)
        elif value == 'on':
            result[key] = True
        elif value == 'off':
            result[key] = False
    return result