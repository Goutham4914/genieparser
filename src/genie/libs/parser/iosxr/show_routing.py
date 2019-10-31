'''
show_route.py

'''
import re
from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Schema, \
    Any, \
    Optional

class ShowRouteIpv4Schema(MetaParser):
    """Schema for show route ipv4"""
    schema = {
        'vrf': {
            Any(): {
                'address_family': {
                    Any(): {
                        Optional('routes'): {
                            Any(): {
                                'route': str,
                                'active': bool,
                                Optional('ip'): str,
                                Optional('mask'): str,
                                Optional('route_preference'): int,
                                Optional('metric'): int,
                                Optional('source_protocol'): str,
                                Optional('source_protocol_codes'): str,
                                Optional('known_via'): str,
                                Optional('distance'): int,
                                Optional('type'): str,
                                Optional('installed'): {
                                    'date': str,
                                    'for': str,
                                },
                                Optional('redist_advertisers'): {
                                    Any(): {
                                        'protoid': int,
                                        'clientid': int,
                                    },
                                },
                                'next_hop': {
                                    Optional('outgoing_interface'): {
                                        Any(): {
                                            'outgoing_interface': str,
                                            Optional('updated'): str,
                                            Optional('metric'): int,
                                        }
                                    },
                                    Optional('next_hop_list'): {
                                        Any(): { # index
                                            'index': int,
                                            'next_hop': str,
                                            Optional('outgoing_interface'): str,
                                            Optional('updated'): str,
                                            Optional('metric'): int,
                                            Optional('from'): str,
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

class ShowRouteIpv4(ShowRouteIpv4Schema):
    cli_command = [
        'show route ipv4',
        'show route vrf {vrf} ipv4',
        'show route ipv4 {protocol}',
        'show route vrf {vrf} ipv4 {protocol}',
        'show route ipv4 {route}',
        'show route vrf {vrf} ipv4 {route}'
    ]

    """
     Codes: C - connected, S - static, R - RIP, B - BGP, (>) - Diversion path
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP
       i - ISIS, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, su - IS-IS summary null, * - candidate default
       U - per-user static route, o - ODR, L - local, G  - DAGR, l - LISP
       A - access/subscriber, a - Application route
       M - mobile route, r - RPL, t - Traffic Engineering, (!) - FRR Backup path
    """
    source_protocol_dict = {
        'ospf': ['O', 'IA', 'N1', 'N2', 'E1', 'E2'],
        'odr': ['o'],
        'isis': ['i', 'su', 'L1', 'L2', 'ia'],
        'eigrp': ['D', 'EX'],
        'static': ['S'],
        'egp': ['E'],
        'dagr': ['G'],
        'rpl': ['r'],
        'mobile router': ['M'],
        'lisp': ['I', 'l'],
        'nhrp': ['H'],
        'local': ['L'],
        'connected': ['C'],
        'bgp': ['B'],
        'rip': ['R'],
        'per-user static route': ['U'],
        'access/subscriber': ['A'],
        'traffic engineering': ['t'],
    }


    protocol_set = {'ospf', 'odr', 'isis', 'eigrp', 'static', 'mobile',
                    'rip', 'lisp', 'nhrp', 'local', 'connected', 'bgp'}
    def cli(self, vrf=None, route=None, protocol=None, output=None):

        if output is None:
            if vrf and route:
                cmd = self.cli_command[5].format(
                    vrf=vrf,
                    route=route
                )
            elif vrf and protocol:
                cmd = self.cli_command[3].format(
                    vrf=vrf,
                    protocol=protocol
                )
            elif vrf:
                cmd = self.cli_command[1].format(
                    vrf=vrf
                )
            elif protocol:
                cmd = self.cli_command[2].format(
                    protocol=protocol
                )
            elif route:
                cmd = self.cli_command[4].format(
                    route=route
                )
            else:
                cmd = self.cli_command[0]
            out = self.device.execute(cmd)
        else:
            out = output
        
        # VRF: VRF501
        p1 = re.compile(r'^\s*VRF: +(?P<vrf>[\w]+)$')

        # R    1.0.0.0/8 [120/1] via 10.12.120.1, 1w0d, GigabitEthernet0/0/0/0.120
        # B    10.21.33.33/32 [200/0] via 10.166.13.13, 00:52:31
        p2 = re.compile(r'^(?P<code1>[\w](\*)*)\s*(?P<code2>\S+)? +(?P<network>\S+) +\[(?P<route_preference>\d+)\/(?P<metric>\d+)\] +via +(?P<next_hop>\S+)( +\(nexthop +in +vrf +\w+\))?,( +(?P<date>[\w:]+),?)?( +(?P<interface>[\w\/\.\-]+))?( +(?P<code3>[\w\*\(\>\)\!]+))?$')

        # [90/15360] via 10.23.90.3, 1w0d, GigabitEthernet0/0/0/1.90
        p3 = re.compile(r'^\[(?P<route_preference>\d+)\/(?P<metric>\d+)\] +via +(?P<next_hop>\S+),( +(?P<date>[\w:]+))?,? +(?P<interface>[\w\/\.\-]+)$')

        # L    2.2.2.2/32 is directly connected, 3w5d, Loopback0
        # is directly connected, 01:51:13, GigabitEthernet0/0/0/3
        p4 = re.compile(r'^((?P<code1>[\w](\*)*)\s*(?P<code2>\S+)? +'
                        r'(?P<network>\S+) +)?is +directly +'
                        r'connected, +(?P<date>[\w:]+),? +(?P<interface>[\w\/\.\-]+)$')

        # Routing entry for 10.151.0.0/24, 1 known subnets
        # Routing entry for 0.0.0.0/0, supernet
        # Routing entry for 192.168.154.0/24
        p5 = re.compile(r'^Routing +entry +for +(?P<network>(?P<ip>[\w\:\.]+)'
                        r'\/(?P<mask>\d+))(?:, +(?P<net>[\w\s]+))?$')
        
        # Known via "connected", distance 0, metric 0 (connected)
        # Known via "eigrp 1", distance 130, metric 10880, type internal
        # Known via "bgp 65161", distance 20, metric 0, candidate default path
        p6 = re.compile(r'^Known +via +\"(?P<known_via>[\w ]+)\", +distance +(?P<distance>\d+), +metric +(?P<metric>\d+)( \(connected\))?(, +type +(?P<type>\S+))?(, +candidate +default +path)?$')

        # * directly connected, via GigabitEthernet1.120
        p7 = re.compile(r'^(\* +)?directly +connected, via +(?P<interface>\S+)$')
        
        # Route metric is 10880, traffic share count is 1
        p8 = re.compile(r'^Route +metric +is +(?P<metric>\d+)(, +'
                        r'traffic +share +count +is +(?P<share_count>\d+))?$')

        # eigrp/100 (protoid=5, clientid=22)
        p9 = re.compile(r'^(?P<redist_advertiser>\S+) +\(protoid=(?P<protoid>\d+)'
                        r', +clientid=(?P<clientid>\d+)\)$')
        
        # Installed Oct 23 22:09:38.380 for 5d21h
        p10 = re.compile(r'^Installed +(?P<date>[\S\s]+) +for +(?P<for>\S+)$')

        # 10.12.90.1, from 10.12.90.1, via GigabitEthernet0/0/0/0.90
        p11 = re.compile(r'^(?P<nexthop>\S+), from +(?P<from>\S+), '
                        r'+via +(?P<interface>\S+)$')

        # initial variables
        ret_dict = {}
        index = 0
        address_family = 'ipv4'
        if not vrf:
            vrf = 'default'

        for line in out.splitlines():
            line = line.strip()

            # VRF: VRF501
            m = p1.match(line)
            if m:
                vrf = m.groupdict()['vrf']
                continue
            
            # R    1.0.0.0/8 [120/1] via 10.12.120.1, 1w0d, GigabitEthernet0/0/0/0.120
            m = p2.match(line)
            if m:
                group = m.groupdict()
                code1 = group['code1']
                source_protocol_code = re.split('\*|\(\!\)|\(\>\)', code1)[0].strip()
                for key,val in self.source_protocol_dict.items():
                    if source_protocol_code in val:
                        source_protocol = key
                
                code2 = group['code2']
                if code2:
                    code1 = '{} {}'.format(code1, code2)

                code3 = group['code3']
                if code3:
                    code1 = '{} {}'.format(code1, code3)
                
                network = group['network']
                route_preference = int(group['route_preference'])
                metric = int(group['metric'])
                next_hop = group['next_hop']
                updated = group['date']
                interface = group['interface']

                route_dict = ret_dict.setdefault('vrf', {}). \
                    setdefault(vrf, {}). \
                    setdefault('address_family', {}). \
                    setdefault(address_family, {}). \
                    setdefault('routes', {}). \
                    setdefault(network, {})

                route_dict.update({'route': network})
                route_dict.update({'active': True})
                route_dict.update({'route_preference': route_preference})
                route_dict.update({'metric': metric})
                route_dict.update({'source_protocol': source_protocol})
                route_dict.update({'source_protocol_codes': code1})

                index = 1

                next_hop_list_dict = route_dict.setdefault('next_hop', {}). \
                    setdefault('next_hop_list', {}). \
                    setdefault(index, {})
                
                next_hop_list_dict.update({'index': index})
                next_hop_list_dict.update({'next_hop': next_hop})
                if interface:
                    next_hop_list_dict.update({'outgoing_interface': interface})
                if updated:
                    next_hop_list_dict.update({'updated': updated})
                continue
            
            # [90/15360] via 10.23.90.3, 1w0d, GigabitEthernet0/0/0/1.90
            m = p3.match(line)
            if m:
                group = m.groupdict()
                route_preference = int(group['route_preference'])
                metric = int(group['metric'])
                next_hop = group['next_hop']
                updated = group['date']
                interface = group['interface']
                route_dict.update({'route_preference': route_preference})
                route_dict.update({'metric': metric})
                index += 1

                next_hop_list_dict = route_dict.setdefault('next_hop', {}). \
                    setdefault('next_hop_list', {}). \
                    setdefault(index, {})
                
                next_hop_list_dict.update({'index': index})
                next_hop_list_dict.update({'next_hop': next_hop})
                if interface:
                    next_hop_list_dict.update({'outgoing_interface': interface})
                if updated:
                    next_hop_list_dict.update({'updated': updated})
                continue
            
            # L    2.2.2.2/32 is directly connected, 3w5d, Loopback0
            #                 is directly connected, 01:51:13, GigabitEthernet0/0/0/3
            m = p4.match(line)
            if m:
                group = m.groupdict()
                code1 = group.get('code1', None)
                source_protocol = None
                network = group.get('network', None)
                updated = group.get('date', None)
                interface = group.get('interface', None)

                if network:
                    route_dict = ret_dict.setdefault('vrf', {}). \
                        setdefault(vrf, {}). \
                        setdefault('address_family', {}). \
                        setdefault(address_family, {}). \
                        setdefault('routes', {}). \
                        setdefault(network, {})

                    route_dict.update({'route': network})
                    route_dict.update({'active': True})
                
                if code1:
                    source_protocol_code = re.split('\*|\(\!\)|\(\>\)', code1)[0].strip()
                    for key,val in self.source_protocol_dict.items():
                        if source_protocol_code in val:
                            source_protocol = key
                    
                    code2 = group.get('code2', None)
                    if code2:
                        code1 = '{} {}'.format(code1, code2)
                    route_dict.update({'source_protocol': source_protocol})
                    route_dict.update({'source_protocol_codes': code1})
                
                outgoing_interface_dict = route_dict.setdefault('next_hop', {}). \
                    setdefault('outgoing_interface', {}). \
                    setdefault(interface, {})
                
                if interface:
                    outgoing_interface_dict.update({'outgoing_interface': interface})
                
                if updated:
                    outgoing_interface_dict.update({'updated': updated})
                continue
            
            # Routing entry for 10.151.0.0/24, 1 known subnets
            # Routing entry for 0.0.0.0/0, supernet
            # Routing entry for 192.168.154.0/24
            m = p5.match(line)
            if m:
                group = m.groupdict()
                network = group['network']
                ip = group['ip']
                mask = group['mask']
                route_dict = ret_dict.setdefault('vrf', {}). \
                    setdefault(vrf, {}). \
                    setdefault('address_family', {}). \
                    setdefault(address_family, {}). \
                    setdefault('routes', {}). \
                    setdefault(network, {})
                route_dict.update({'route': network})
                route_dict.update({'ip': ip})
                route_dict.update({'mask': mask})
                route_dict.update({'active': True})
                continue

            # Known via "static", distance 1, metric 0, candidate default path
            # Known via "eigrp 1", distance 130, metric 10880, type internal
            # Known via "rip", distance 120, metric 2
            # Known via "connected", distance 0, metric 0 (connected)
            # Known via "eigrp 1", distance 130, metric 10880, type internal
            # Known via "bgp 65161", distance 20, metric 0, candidate default path
            m = p6.match(line)
            if m:
                group = m.groupdict()
                known_via = group['known_via']
                metric = int(group['metric'])
                distance = int(group['distance'])
                _type = group['type']
                route_dict.update({'known_via': known_via})
                route_dict.update({'metric': metric})
                route_dict.update({'distance': distance})
                if _type:
                    route_dict.update({'type': _type})
                continue

            # * directly connected, via GigabitEthernet1.120
            m = p7.match(line)
            if m:
                group = m.groupdict()
                code1 = group.get('code1', None)
                source_protocol = None
                network = group.get('network', None)
                updated = group.get('date', None)
                interface = group.get('interface', None)

                if network:
                    route_dict = ret_dict.setdefault('vrf', {}). \
                        setdefault(vrf, {}). \
                        setdefault('address_family', {}). \
                        setdefault(address_family, {}). \
                        setdefault('routes', {}). \
                        setdefault(network, {})

                    route_dict.update({'route': network})
                    route_dict.update({'active': True})
                
                if code1:
                    source_protocol_code = re.split('\*|\(\!\)|\(\>\)', code1)[0].strip()
                    for key,val in self.source_protocol_dict.items():
                        if source_protocol_code in val:
                            source_protocol = key
                    
                    code2 = group.get('code2', None)
                    if code2:
                        code1 = '{} {}'.format(code1, code2)
                    route_dict.update({'source_protocol': source_protocol})
                    route_dict.update({'source_protocol_codes': code1})
                
                outgoing_interface_dict = route_dict.setdefault('next_hop', {}). \
                    setdefault('outgoing_interface', {}). \
                    setdefault(interface, {})
                
                if interface:
                    outgoing_interface_dict.update({'outgoing_interface': interface})
                
                if updated:
                    outgoing_interface_dict.update({'updated': updated})

            # Route metric is 10880, traffic share count is 1
            m = p8.match(line)
            if m:
                group = m.groupdict()
                metric = int(group['metric'])
                outgoing_interface_dict.update({'metric': metric})
                if group.get('share_count', None):
                    share_count = int(group['share_count'])
                    outgoing_interface_dict.update({'share_count': share_count})
                # outgoing_interface_dict.update({k:v for k,v in group.items() if v})
                continue
            
            # eigrp/100 (protoid=5, clientid=22)
            m = p9.match(line)
            if m:
                group = m.groupdict()
                redist_advertiser = group['redist_advertiser']
                protoid = int(group['protoid'])
                clientid = int(group['clientid'])
                redist_advertiser_dict = route_dict.setdefault('redist_advertisers', {}). \
                                setdefault(redist_advertiser, {})
                redist_advertiser_dict.update({'protoid': protoid})
                redist_advertiser_dict.update({'clientid': clientid})
                continue
            
            # Installed Oct 23 22:09:38.380 for 5d21h
            m = p10.match(line)
            if m:
                group = m.groupdict()
                installed_dict = route_dict.setdefault('installed', {})
                installed_dict.update({k:v for k,v in group.items() if v})
                continue

            # 10.12.90.1, from 10.12.90.1, via GigabitEthernet0/0/0/0.90
            m = p11.match(line)
            if m:
                group = m.groupdict()
                nexthop = group['nexthop']
                _from = group['from']
                interface = group['interface']

                index += 1
                outgoing_interface_dict = route_dict.setdefault('next_hop', {}). \
                    setdefault('next_hop_list', {}). \
                    setdefault(index, {})
                outgoing_interface_dict.update({'index': index})
                outgoing_interface_dict.update({'outgoing_interface': interface})
                outgoing_interface_dict.update({'from': _from})
                outgoing_interface_dict.update({'next_hop': nexthop})
                continue

        return ret_dict

# ====================================================
#  parser for show route ipv6
# ====================================================

class ShowRouteIpv6(ShowRouteIpv4Schema):
    """Parser for :
       show route ipv6
       show route vrf <vrf> ipv6"""
    
    cli_command = [
        'show route ipv6',
        'show route vrf {vrf} ipv6',
        'show route ipv6 {protocol}',
        'show route vrf {vrf} ipv6 {protocol}',
        'show route ipv6 {route}',
        'show route vrf {vrf} ipv6 {route}'
    ]

    """
     Codes: C - connected, S - static, R - RIP, B - BGP, (>) - Diversion path
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP
       i - ISIS, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, su - IS-IS summary null, * - candidate default
       U - per-user static route, o - ODR, L - local, G  - DAGR, l - LISP
       A - access/subscriber, a - Application route
       M - mobile route, r - RPL, t - Traffic Engineering, (!) - FRR Backup path
    """
    source_protocol_dict = {
        'ospf': ['O', 'IA', 'N1', 'N2', 'E1', 'E2'],
        'odr': ['o'],
        'isis': ['i', 'su', 'L1', 'L2', 'ia'],
        'eigrp': ['D', 'EX'],
        'static': ['S'],
        'egp': ['E'],
        'dagr': ['G'],
        'rpl': ['r'],
        'mobile router': ['M'],
        'lisp': ['I', 'l'],
        'nhrp': ['H'],
        'local': ['L'],
        'connected': ['C'],
        'bgp': ['B'],
        'rip': ['R'],
        'per-user static route': ['U'],
        'access/subscriber': ['A'],
        'traffic engineering': ['t'],
    }


    protocol_set = {'ospf', 'odr', 'isis', 'eigrp', 'static', 'mobile',
                    'rip', 'lisp', 'nhrp', 'local', 'connected', 'bgp'}

    def cli(self, vrf=None, route=None, protocol=None, output=None):

        if output is None:
            if vrf and route:
                cmd = self.cli_command[5].format(
                    vrf=vrf,
                    route=route
                )
            elif vrf and protocol:
                cmd = self.cli_command[3].format(
                    vrf=vrf,
                    protocol=protocol
                )
            elif vrf:
                cmd = self.cli_command[1].format(
                    vrf=vrf
                )
            elif protocol:
                cmd = self.cli_command[2].format(
                    protocol=protocol
                )
            elif route:
                cmd = self.cli_command[4].format(
                    route=route
                )
            else:
                cmd = self.cli_command[0]
            out = self.device.execute(cmd)
        else:
            out = output
        
        # VRF: VRF501
        p1 = re.compile(r'^\s*VRF: +(?P<vrf>[\w]+)$')

        # S    2001:1:1:1::1/128
        p2 = re.compile(r'^(?P<code1>\w(\*)?) *(?P<code2>\w+)? +(?P<network>[\w\:\/]+)$')

        # [1/0] via 2001:20:1:2::1, 01:52:23, GigabitEthernet0/0/0/0
        # [200/0] via 2001:13:13:13::13, 00:53:22
        p3 = re.compile(r'^\[(?P<route_preference>\d+)\/(?P<metric>\d+)\] +via +(?P<next_hop>\S+)( +\(nexthop +in +vrf +\w+\))?,( +(?P<date>[\w:]+))?,?( +(?P<interface>[\w\/\.\-]+))?$')

        # L    2001:2:2:2::2/128 is directly connected,
        p4 = re.compile(r'^((?P<code1>[\w](\*)*)\s*(?P<code2>\S+)? +(?P<network>\S+) +)?is +directly +connected,$')

        # 01:52:24, Loopback0
        p5 = re.compile(r'^(?P<date>[\w+:]+), +(?P<interface>\S+)$')

        # Routing entry for 2001:1:1:1::1/128, 1 known subnets
        # Routing entry for 2001:1:1:1::1/128, supernet
        # Routing entry for 2001:1:1:1::1/128
        p6 = re.compile(r'^Routing +entry +for +(?P<network>(?P<ip>[\w\:\.]+)'
                        r'\/(?P<mask>\d+))(?:, +(?P<net>[\w\s]+))?$')
        
        # Known via "connected", distance 0, metric 0 (connected)
        # Known via "eigrp 1", distance 130, metric 10880, type internal
        # Known via "bgp 65161", distance 20, metric 0, candidate default path
        p7 = re.compile(r'^Known +via +\"(?P<known_via>[\w ]+)\", +distance +(?P<distance>\d+), +metric +(?P<metric>\d+)( \(connected\))?(, +type +(?P<type>\S+))?(, +candidate +default +path)?$')

        # * directly connected, via GigabitEthernet1.120
        p8 = re.compile(r'^(\* +)?directly +connected, via +(?P<interface>\S+)$')
        
        # Route metric is 10880, traffic share count is 1
        p9 = re.compile(r'^Route +metric +is +(?P<metric>\d+)(, +'
                        r'traffic +share +count +is +(?P<share_count>\d+))?$')

        # eigrp/100 (protoid=5, clientid=22)
        p10 = re.compile(r'^(?P<redist_advertiser>\S+) +\(protoid=(?P<protoid>\d+)'
                        r', +clientid=(?P<clientid>\d+)\)$')
        
        # Installed Oct 23 22:09:38.380 for 5d21h
        p11 = re.compile(r'^Installed +(?P<date>[\S\s]+) +for +(?P<for>\S+)$')

        # fe80::f816:3eff:fe76:b56d, from fe80::f816:3eff:fe76:b56d, via GigabitEthernet0/0/0/0.390
        p12 = re.compile(r'^(?P<nexthop>\S+), from +(?P<from>\S+), '
                        r'+via +(?P<interface>\S+)$')

        ret_dict = {}
        address_family = 'ipv6'
        index = 0
        if not vrf:
            vrf = 'default'

        for line in out.splitlines():
            line = line.strip()

            # VRF: VRF501
            m = p1.match(line)
            if m:
                vrf = m.groupdict()['vrf']
                continue

            # S    2001:1:1:1::1/128
            m = p2.match(line)
            if m:
                group = m.groupdict()
                code1 = group['code1']
                source_protocol_code = re.split('\*|\(\!\)|\(\>\)', code1)[0].strip()
                for key,val in self.source_protocol_dict.items():
                    if source_protocol_code in val:
                        source_protocol = key
                
                code2 = group['code2']
                if code2:
                    code1 = '{} {}'.format(code1, code2)
                
                network = group['network']

                route_dict = ret_dict.setdefault('vrf', {}). \
                    setdefault(vrf, {}). \
                    setdefault('address_family', {}). \
                    setdefault(address_family, {}). \
                    setdefault('routes', {}). \
                    setdefault(network, {})

                route_dict.update({'source_protocol': source_protocol})
                route_dict.update({'source_protocol_codes': code1})
                route_dict.update({'route': network})
                route_dict.update({'active': True})
                index = 0
                continue
            
            # [1/0] via 2001:20:1:2::1, 01:52:23, GigabitEthernet0/0/0/0
            m = p3.match(line)
            if m:
                group = m.groupdict()
                route_preference = int(group['route_preference'])
                metric = int(group['metric'])
                next_hop = group['next_hop']
                updated = group['date']
                interface = group['interface']
                route_dict.update({'route_preference': route_preference})
                route_dict.update({'metric': metric})
                index += 1

                next_hop_list_dict = route_dict.setdefault('next_hop', {}). \
                    setdefault('next_hop_list', {}). \
                    setdefault(index, {})
                
                next_hop_list_dict.update({'index': index})
                next_hop_list_dict.update({'next_hop': next_hop})
                if interface:
                    next_hop_list_dict.update({'outgoing_interface': interface})
                if updated:
                    next_hop_list_dict.update({'updated': updated})
                continue
            
            # L    2001:2:2:2::2/128 is directly connected,
            m = p4.match(line)
            if m:
                group = m.groupdict()
                code1 = group.get('code1', None)
                source_protocol = None
                network = group.get('network', None)
                updated = group.get('date', None)
                interface = group.get('interface', None)

                if network:
                    route_dict = ret_dict.setdefault('vrf', {}). \
                        setdefault(vrf, {}). \
                        setdefault('address_family', {}). \
                        setdefault(address_family, {}). \
                        setdefault('routes', {}). \
                        setdefault(network, {})

                    route_dict.update({'route': network})
                    route_dict.update({'active': True})
                
                if code1:
                    source_protocol_code = re.split('\*|\(\!\)|\(\>\)', code1)[0].strip()
                    for key,val in self.source_protocol_dict.items():
                        if source_protocol_code in val:
                            source_protocol = key
                    
                    code2 = group.get('code2', None)
                    if code2:
                        code1 = '{} {}'.format(code1, code2)
                    route_dict.update({'source_protocol': source_protocol})
                    route_dict.update({'source_protocol_codes': code1})

                continue

            # 01:52:24, Loopback0
            m = p5.match(line)
            if m:
                group = m.groupdict()
                updated = group['date']
                interface = group['interface']
                
                outgoing_interface_dict = route_dict.setdefault('next_hop', {}). \
                    setdefault('outgoing_interface', {}). \
                    setdefault(interface, {})
                outgoing_interface_dict.update({'outgoing_interface': interface})
                outgoing_interface_dict.update({'updated': updated})
                continue
            
            # Routing entry for 2001:1:1:1::1/128, 1 known subnets
            # Routing entry for 2001:1:1:1::1/128, supernet
            # Routing entry for 2001:1:1:1::1/128
            m = p6.match(line)
            if m:
                group = m.groupdict()
                network = group['network']
                ip = group['ip']
                mask = group['mask']
                route_dict = ret_dict.setdefault('vrf', {}). \
                    setdefault(vrf, {}). \
                    setdefault('address_family', {}). \
                    setdefault(address_family, {}). \
                    setdefault('routes', {}). \
                    setdefault(network, {})
                route_dict.update({'route': network})
                route_dict.update({'ip': ip})
                route_dict.update({'mask': mask})
                route_dict.update({'active': True})
                continue

            # Known via "static", distance 1, metric 0, candidate default path
            # Known via "eigrp 1", distance 130, metric 10880, type internal
            # Known via "rip", distance 120, metric 2
            # Known via "connected", distance 0, metric 0 (connected)
            # Known via "eigrp 1", distance 130, metric 10880, type internal
            # Known via "bgp 65161", distance 20, metric 0, candidate default path
            m = p7.match(line)
            if m:
                group = m.groupdict()
                known_via = group['known_via']
                metric = int(group['metric'])
                distance = int(group['distance'])
                _type = group['type']
                route_dict.update({'known_via': known_via})
                route_dict.update({'metric': metric})
                route_dict.update({'distance': distance})
                if _type:
                    route_dict.update({'type': _type})
                continue

            # * directly connected, via GigabitEthernet1.120
            m = p8.match(line)
            if m:
                group = m.groupdict()
                code1 = group.get('code1', None)
                source_protocol = None
                network = group.get('network', None)
                updated = group.get('date', None)
                interface = group.get('interface', None)

                if network:
                    route_dict = ret_dict.setdefault('vrf', {}). \
                        setdefault(vrf, {}). \
                        setdefault('address_family', {}). \
                        setdefault(address_family, {}). \
                        setdefault('routes', {}). \
                        setdefault(network, {})

                    route_dict.update({'route': network})
                    route_dict.update({'active': True})
                
                if code1:
                    source_protocol_code = re.split('\*|\(\!\)|\(\>\)', code1)[0].strip()
                    for key,val in self.source_protocol_dict.items():
                        if source_protocol_code in val:
                            source_protocol = key
                    
                    code2 = group.get('code2', None)
                    if code2:
                        code1 = '{} {}'.format(code1, code2)
                    route_dict.update({'source_protocol': source_protocol})
                    route_dict.update({'source_protocol_codes': code1})
                
                outgoing_interface_dict = route_dict.setdefault('next_hop', {}). \
                    setdefault('outgoing_interface', {}). \
                    setdefault(interface, {})
                
                if interface:
                    outgoing_interface_dict.update({'outgoing_interface': interface})
                
                if updated:
                    outgoing_interface_dict.update({'updated': updated})

            # Route metric is 10880, traffic share count is 1
            m = p9.match(line)
            if m:
                group = m.groupdict()
                metric = int(group['metric'])
                outgoing_interface_dict.update({'metric': metric})
                if group.get('share_count', None):
                    share_count = int(group['share_count'])
                    outgoing_interface_dict.update({'share_count': share_count})
                # outgoing_interface_dict.update({k:v for k,v in group.items() if v})
                continue
            
            # eigrp/100 (protoid=5, clientid=22)
            m = p10.match(line)
            if m:
                group = m.groupdict()
                redist_advertiser = group['redist_advertiser']
                protoid = int(group['protoid'])
                clientid = int(group['clientid'])
                redist_advertiser_dict = route_dict.setdefault('redist_advertisers', {}). \
                                setdefault(redist_advertiser, {})
                redist_advertiser_dict.update({'protoid': protoid})
                redist_advertiser_dict.update({'clientid': clientid})
                continue
            
            # Installed Oct 23 22:09:38.380 for 5d21h
            m = p11.match(line)
            if m:
                group = m.groupdict()
                installed_dict = route_dict.setdefault('installed', {})
                installed_dict.update({k:v for k,v in group.items() if v})
                continue
            
            # fe80::f816:3eff:fe76:b56d, from fe80::f816:3eff:fe76:b56d, via GigabitEthernet0/0/0/0.390
            m = p12.match(line)
            if m:
                group = m.groupdict()
                nexthop = group['nexthop']
                _from = group['from']
                interface = group['interface']

                index += 1
                outgoing_interface_dict = route_dict.setdefault('next_hop', {}). \
                    setdefault('next_hop_list', {}). \
                    setdefault(index, {})
                outgoing_interface_dict.update({'index': index})
                outgoing_interface_dict.update({'outgoing_interface': interface})
                outgoing_interface_dict.update({'from': _from})
                outgoing_interface_dict.update({'next_hop': nexthop})
                continue
        
        return ret_dict
