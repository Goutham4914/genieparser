''' show_protocols.py

IOSXE parsers for the following show commands:
    * show ip protocols
'''

# Python
import re
import xmltodict
from netaddr import IPAddress

# Metaparser
from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Schema, Any, Or, Optional
from genie.libs.parser.utils.common import Common


# ==============================
# Schema for 'show ip protocols'
# ==============================
class ShowIpProtocolsSchema(MetaParser):

    ''' Schema for "show ip protocols" '''

    schema = {
        'protocols':
            {Optional('rip'):
                {'vrf': {
                    Any(): {
                        'address_family': {
                            Any(): {
                                Optional('instance'): {
                                    Any(): {
                                        'distance': int,
                                        'maximum_paths': int,
                                        Optional('output_delay'): int,
                                        'send_version': Or(int,str),
                                        'receive_version': Or(int,str),
                                        Optional('automatic_network_summarization_in_effect'): bool,
                                        'outgoing_update_filterlist': {
                                            'outgoing_update_filterlist': str,
                                            Optional('interfaces'): {
                                                Any(): {
                                                    'filter': str,
                                                    'per_user': bool,
                                                    'default': str,
                                                },
                                            },
                                        },
                                        'incoming_update_filterlist': {
                                            'incoming_update_filterlist': str,
                                            Optional('interfaces'): {
                                                Any(): {
                                                    'filter': str,
                                                    'per_user': bool,
                                                    'default': str,
                                                },
                                            },
                                        },
                                        Optional('incoming_route_metric'): {
                                            'added': str,
                                            'list': str,
                                        },
                                        'network': list,
                                        Optional('default_redistribution_metric'): int,
                                        'redistribute': {
                                            Any(): {
                                                Optional(Any()): {
                                                    Optional('metric'): int,
                                                    Optional('route_policy'): int,
                                                    Optional('route_type'): str,
                                                },
                                                Optional('metric'): int,
                                                Optional('route_policy'): int,
                                            },
                                        },
                                        Optional('timers'): {
                                            'update_interval': int,
                                            'next_update': int,
                                            'invalid_interval': int,
                                            'holddown_interval': int,
                                            'flush_interval': int,
                                        },
                                        'interfaces': {
                                            Any(): {
                                                Optional('neighbors'): {
                                                    Any(): {
                                                        Optional('address'): str,
                                                    },
                                                },
                                                Optional('summary_address'): {
                                                    Any(): {
                                                        Optional('metric'): str,
                                                    },
                                                },
                                                Optional('filtered_per_user'): int,
                                                Optional('default_set'): bool,
                                                Optional('passive'): bool,
                                                'send_version': str,
                                                'receive_version': str,
                                                'triggered_rip': str,
                                                'key_chain': str,
                                            },
                                        },
                                        Optional('neighbors'): {
                                            Any(): {
                                                'last_update': str,
                                                'distance': int,
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                }
            },
            Optional('eigrp'):
                {'protocol_under_dev': bool},
            Optional('ospf'):
                {'vrf':
                    {Any():
                        {'address_family':
                            {Any():
                                {'instance':
                                    {Any():
                                        {'spf_control':
                                            {'paths': int},
                                        'preference':
                                            {'single_value':
                                                {'all': int},
                                            Optional('multi_values'):
                                                {'granularity':
                                                    {'detail':
                                                        {'intra_area': int,
                                                        'inter_area': int},
                                                    Optional('coarse'):
                                                        {'internal': int}},
                                                'external': int},
                                            },
                                        'router_id': str,
                                        'outgoing_filter_list': str,
                                        'incoming_filter_list': str,
                                        'total_areas': int,
                                        'total_stub_area': int,
                                        'total_normal_area': int,
                                        'total_nssa_area': int,
                                        Optional('passive_interfaces'): list,
                                        Optional('routing_information_sources'):
                                            {'gateway':
                                                {Any():
                                                    {'distance': int,
                                                    'last_update': str},
                                                },
                                            },
                                        Optional('areas'):
                                            {Any():
                                                {Optional('configured_interfaces'): list},
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            Optional('application'):
                {'outgoing_filter_list': str,
                'incoming_filter_list': str,
                'maximum_path': int,
                'preference':
                    {'single_value':
                        {'all': int}},
                'update_frequency': int,
                'invalid': int,
                'holddown': int,
                'flushed': int,
                },
            Optional('bgp'):
                {'instance':
                    {'default':
                        {'bgp_id': int,
                        'vrf':
                            {'default':
                                {'address_family':
                                    {'ipv4':
                                        {'outgoing_filter_list': str,
                                        'incoming_filter_list': str,
                                        'igp_sync': bool,
                                        'automatic_route_summarization': bool,
                                        'maximum_path': int,
                                        Optional('preference'):
                                            {'multi_values':
                                                {'external': int,
                                                'local': int,
                                                'internal': int,
                                                },
                                            },
                                        Optional('neighbor'):
                                            {Any():
                                                {'neighbor_id': str,
                                                'distance': int,
                                                'last_update': str,
                                                },
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            Optional('isis'):
                {'vrf':
                    {Any():
                        {'address_family':
                            {Any():
                                {'instance':
                                    {Any():
                                        {'outgoing_filter_list': str,
                                        'incoming_filter_list': str,
                                        'redistributing': str,
                                        Optional('address_summarization'): list,
                                        Optional('maximum_path'): int,
                                        'preference':
                                            {'single_value':
                                                {'all': int},
                                            },
                                        Optional('configured_interfaces'): list,
                                        Optional('passive_interfaces'): list,
                                        Optional('routing_information_sources'):
                                            {'gateway':
                                                {Any():
                                                    {'distance': int,
                                                    'last_update': str,
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        }



# ==============================
# Parser for 'show ip protocols'
# ==============================
class ShowIpProtocols(ShowIpProtocolsSchema):

    ''' Parser for "show ip protocols" '''

    cli_command = ['show ip protocols','show ip protocols vrf {vrf}']

    def cli(self, vrf="" ,cmd="",output=None):

        if output is None:
            if not cmd :
                if vrf:
                    cmd = self.cli_command[1].format(vrf=vrf)
                else:
                    vrf = 'default'
                    cmd = self.cli_command[0]
            # get output from device
            out = self.device.execute(cmd)
        else:
            out = output

        # Init vars
        ret_dict = {}

        if not vrf:
            vrf = "default"
        protocol = None
        # Routing for Networks:
        routing_networks = False
        routing_network_intfs = []
        # Routing on Interfaces Configured Explicitly
        routing_on_interfaces = False
        routing_on_interfaces_intfs = []
        # Routing Information Sources:
        routing_information = False
        routing_info_gateways = []
        # Passive Interface(s):
        passive_interfaces = False
        passive_intfs = []

        # Routing Protocol is "ospf 1"
        # Routing Protocol is "application"
        # Routing Protocol is "bgp 100"
        # Routing Protocol is "isis"
        # Routing Protocol is "isis banana"
        # Routing Protocol is "eigrp 1"
        p1 = re.compile(r"^Routing +Protocol +is"
                         " +\"(?P<protocol>(ospf|bgp|isis|eigrp|application|rip))"
                         "(?: *(?P<pid>(\S+)))?\"$")

        # Outgoing update filter list for all interfaces is not set
        # Incoming update filter list for all interfaces is not set
        p2 = re.compile(r"^(?P<dir>(Outgoing|Incoming)) +update +filter +list"
                         " +for +all +interfaces +is +(?P<state>([a-zA-Z\s]+))$")

        # Router ID 10.4.1.1
        p3 = re.compile(r"^Router +ID +(?P<router_id>(\S+))$")

        # Number of areas in this router is 1. 1 normal 0 stub 0 nssa
        p4 = re.compile(r"^Number +of +areas +in +this +router +is"
                         " +(?P<areas>(\d+)). +(?P<normal>(\d+)) +normal"
                         " +(?P<stub>(\d+)) +stub +(?P<nssa>(\d+)) +nssa$")

        # Maximum path: 4
        p5 = re.compile(r"^Maximum +path: +(?P<max>(\d+))$")

        # Routing for Networks:
        p6_1 = re.compile(r"^Routing +for +Networks:$")

        # Routing on Interfaces Configured Explicitly (Area 0):
        p6_2 = re.compile(r"^Routing +on +Interfaces +Configured +Explicitly"
                         " +\(Area +(?P<area>[\d\.]+)\)\:$")


        # Routing Information Sources:
        p6_3 = re.compile(r"^Routing +Information +Sources:$")

        # Passive Interface(s):
        p6_4 = re.compile(r"^Passive +Interface\(s\):$")

        # Address Summarization:
        p6_5 = re.compile(r"^Address +Summarization:$")

        # Loopback0
        # GigabitEthernet2
        # GigabitEthernet1
        # TenGigabitEthernet0/0/26
        p7 = re.compile(r"^(?P<interface>(Lo.*|Gi.*|Ten.*|.*(SL|VL).*))$")


        # Gateway         Distance      Last Update
        # 10.36.3.3            110      07:33:00
        # 10.16.2.2            110      07:33:00
        # 10.64.4.4            110      00:19:15
        p8 = re.compile(r"^(?P<gateway>([0-9\.]+)) +(?P<distance>(\d+))"
                         " +(?P<last_update>([a-zA-Z0-9\:\.]+))$")

        # Distance: (default is 110)
        p9 = re.compile(r"^Distance: +\(default +is +(?P<num>(\d+))\)$")

        # Distance: intra-area 112 inter-area 113 external 114
        p10 = re.compile(r"^Distance: +intra-area +(?P<intra>(\d+)) +inter-area"
                          " +(?P<inter>(\d+)) +external +(?P<external>(\d+))$")

        # Sending updates every 0 seconds
        p11 = re.compile(r"^Sending +updates +every +(?P<update>(\d+)) +seconds$")

        # Invalid after 0 seconds, hold down 0, flushed after 0
        p12 = re.compile(r"^Invalid +after +(?P<invalid>(\d+)) +seconds, +hold"
                          " +down +(?P<holddown>(\d+)), +flushed +after"
                          " +(?P<flushed>(\d+))$")

        # IGP synchronization is disabled
        p13 = re.compile(r"^IGP +synchronization +is +(?P<igp>(enabled|disabled))$")

        # Automatic route summarization is disabled
        p14 = re.compile(r"^Automatic +route +summarization +is"
                          " +(?P<route>(enabled|disabled))$")

        # Distance: external 20 internal 200 local 200
        p15 = re.compile(r"^Distance: +external +(?P<external>(\d+)) +internal"
                          " +(?P<internal>(\d+)) +local +(?P<local>(\d+))$")


        # Redistributing: isis banana
        p16 = re.compile(r"^Redistributing: +(?P<redistributing>([a-zA-Z\_\s]+))$")


        passive_interface_flag = False
        routing_network_flag = False

        # Routing Protocol is "rip"
        p100 = re.compile(r'^\s*Routing Protocol +is +\"(?P<protocol>[\w]+)\"$')

        # Output delay 50 milliseconds between packets
        p102 = re.compile(r'^\s*Output +delay +(?P<output_delay>[\d]+) +milliseconds +between +packets$')

        # Outgoing update filter list for all interfaces is not set
        # Outgoing update filter list for all interfaces is 150
        p103 = re.compile(
            r'^\s*Outgoing +update +filter +list +for all +interfaces +is +(?P<outgoing_update_filterlist>[\S\s]+)$')

        # Incoming update filter list for all interfaces is not set
        # Incoming update filter list for all interfaces is 100
        p104 = re.compile(
            r'^\s*Incoming +update +filter +list +for all +interfaces +is +(?P<incoming_update_filterlist>[\S\s]+)$')

        # GigabitEthernet3.100 filtered by 130 (per-user), default is not set
        p104_1 = re.compile(
            r'^\s*(?P<interface>\S+) +filtered +by +(?P<filter>\d+)( +\((?P<per_user>\S+)\))?,'
            ' +default +is +(?P<default>[\w\s]+)$')
        # Incoming routes will have 10 added to metric if on list 21
        p105 = re.compile(r'^\s*Incoming +routes +will +have +(?P<added>\S+) +added +to +metric'
                          ' +if +on +list +(?P<list>\S+)$')

        # Sending updates every 10 seconds, next due in 8 seconds
        p106 = re.compile(
            r'^\s*Sending +updates every +(?P<update_interval>\d+) +seconds, +next +due +in (?P<next_update>\d+) +seconds$')

        # Invalid after 21 seconds, hold down 22, flushed after 23
        p107 = re.compile(
            r'^\s*Invalid +after +(?P<invalid_interval>\d+) +seconds, +hold +down +(?P<holddown_interval>\d+)'
            ', +flushed +after +(?P<flush_interval>\d+)$')

        # Default redistribution metric is 3
        p108 = re.compile(r'^\s*Default +redistribution +metric +is +(?P<default_redistribution_metric>\d+)$')

        # Redistributing: connected, static, rip
        p109 = re.compile(r'^\s*Redistributing: +(?P<Redistributing>[\w\,\s]+)$')

        # Neighbor(s):
        p110 = re.compile(r'^\s*Neighbor\(s\):$')

        #   10.1.2.2
        p111 = re.compile(r'^\s*(?P<neighbor>[\d\.]+)$')

        # Default version control: send version 2, receive version 2
        p112 = re.compile(r'^\s*Default +version +control: +send +version +(?P<send_version>\d+)'
                          ', receive version +(?P<receive_version>\d+)$')

        # Default version control: send version 1, receive any version
        p112_1 = re.compile(r'^\s*Default +version +control: +send +version +(?P<send_version>\d+)'
                          ', receive +(?P<receive_version>\w+) version$')

        #   Interface                           Send  Recv  Triggered RIP  Key-chain
        #   GigabitEthernet3.100                2     2          No        1
        #   GigabitEthernet3.100                1 2   2          No        none
        p113 = re.compile(r'^\s*(?P<interface>[\S]+) +(?P<send>\d( \d)?)'
                          ' +(?P<receive>\d( \d)?)?'
                          ' +(?P<triggered_rip>\S+) +(?P<key_chain>\S+)$')

        # Automatic network summarization is not in effect
        # Automatic network summarization is in effect
        p114 = re.compile(
            r'^\s*Automatic +network +summarization +is( +(?P<automatic_network_summarization>\S+))? +in +effect$')

        # Address Summarization:
        p115 = re.compile(r'^\s*Address +Summarization:$')

        #   172.16.0.0/17 for GigabitEthernet3.100
        p116 = re.compile(r'^\s*(?P<prefix>[\d\.\/]+) +for +(?P<interface>[\w\.]+)$')

        # Maximum path: 4
        p117 = re.compile(r'^\s*Maximum +path: +(?P<maximum_path>\d+)$')

        # Routing for Networks:
        p118 = re.compile(r'^\s*Routing +for +Networks:$')

        #   10.0.0.0
        p119 = re.compile(r'^\s*(?P<network>[\d\.]+)$')

        # Passive Interface(s):
        p120 = re.compile(r'^\s*Passive +Interface\(s\):$')

        #   GigabitEthernet2.100
        p121 = re.compile(r'^\s*(?P<passive_interface>[\w\.]+)$')

        # Routing Information Sources:
        p122 = re.compile(r'^\s*Routing +Information +Sources:$')

        #   Gateway         Distance      Last Update
        #   10.1.2.2             120      00:00:04
        p123 = re.compile(r'^\s*(?P<gateway>[\d\.]+) +(?P<distance>\d+) +(?P<last_update>[\w\:]+)$')

        # Distance: (default is 120)
        p124 = re.compile(r'^\s*Distance: +\(default +is +(?P<distance>\d+)\)$')

        network_list = []

        for line in out.splitlines():
            line = line.strip()

            # Routing Protocol is "ospf 1"
            # Routing Protocol is "application"
            # Routing Protocol is "bgp 100"
            # Routing Protocol is "isis banana"
            # Routing Protocol is "eigrp 1"
            m = p1.match(line)
            if m:
                group = m.groupdict()
                protocol = group['protocol']
                if group['pid']:
                    instance = str(m.groupdict()['pid'])

                # Set protocol dict
                protocol_dict = ret_dict.setdefault('protocols', {}). \
                    setdefault(protocol, {})

                if protocol == 'ospf':
                    # Get VRF information based on OSPF instance
                    out = self.device.execute("show running-config | section "
                                              "router ospf {}".format(instance))
                    # Parse for VRF
                    for line in out.splitlines():
                        line = line.strip()
                        # router ospf 1
                        # router ospf 2 vrf VRF1
                        p = re.search('router +ospf +(?P<instance>(\S+))'
                                      '(?: +vrf +(?P<vrf>(\S+)))?', line)
                        if p:
                            p_instance = str(p.groupdict()['instance'])
                            if p_instance == instance:
                                if p.groupdict()['vrf']:
                                    vrf = str(p.groupdict()['vrf'])
                                    break
                                else:
                                    vrf = 'default'
                                    break

                    # Set ospf_dict
                    ospf_dict = protocol_dict.setdefault('vrf', {}). \
                        setdefault(vrf, {}). \
                        setdefault('address_family', {}). \
                        setdefault('ipv4', {}). \
                        setdefault('instance', {}). \
                        setdefault(instance, {})
                elif protocol == 'bgp':
                    instance_dict = protocol_dict.setdefault('instance', {}). \
                        setdefault('default', {})
                    instance_dict['bgp_id'] = int(group['pid'])
                    # Set bgp_dict
                    bgp_dict = instance_dict.setdefault('vrf', {}). \
                        setdefault('default', {}). \
                        setdefault('address_family', {}). \
                        setdefault('ipv4', {})
                elif protocol == 'isis':
                    # Set isis_dict
                    if not group['pid']:
                        instance = 'default'
                    isis_dict = protocol_dict.setdefault('vrf', {}). \
                        setdefault('default', {}). \
                        setdefault('address_family', {}). \
                        setdefault('ipv4', {}). \
                        setdefault('instance', {}). \
                        setdefault(instance, {})
                elif protocol == 'application':
                    application_dict = protocol_dict
                elif protocol == 'eigrp':
                    protocol_dict['protocol_under_dev'] = True
                    eigrp_dict = protocol_dict
                elif protocol == 'rip':
                    address_family = 'ipv4'
                    rip_dict = ret_dict.setdefault('protocols', {}).\
                                            setdefault('rip', {}).\
                                            setdefault('vrf',{}).\
                                            setdefault(vrf, {}).\
                                            setdefault('address_family', {}). \
                                            setdefault(address_family, {}).\
                                            setdefault('instance', {}).\
                                            setdefault(protocol, {})
                    continue

            if protocol == 'rip':
                # Output delay 50 milliseconds between packets
                m = p102.match(line)
                if m:
                    group = m.groupdict()
                    rip_dict.update({'output_delay': int(group['output_delay'])})
                    continue

                # Outgoing update filter list for all interfaces is not set
                # Outgoing update filter list for all interfaces is 150
                m = p103.match(line)
                if m:
                    outgoing_flag = True
                    incoming_flag = False
                    group = m.groupdict()
                    outgoing_dict = rip_dict.setdefault('outgoing_update_filterlist', {})
                    outgoing_dict.update({'outgoing_update_filterlist': group['outgoing_update_filterlist']})
                    continue

                # Incoming update filter list for all interfaces is 100
                m = p104.match(line)
                if m:
                    incoming_flag = True
                    outgoing_flag = False
                    group = m.groupdict()
                    incoming_dict = rip_dict.setdefault('incoming_update_filterlist', {})
                    incoming_dict.update({k: v for k, v in group.items() if v})
                    continue

                # GigabitEthernet3.100 filtered by 130 (per-user), default is not set
                m = p104_1.match(line)
                if m:
                    if outgoing_flag:
                        temp_dict = outgoing_dict
                    if incoming_flag:
                        temp_dict = incoming_dict

                    group = m.groupdict()
                    interface_out_dict = temp_dict.setdefault('interfaces', {}).setdefault(group['interface'],
                                                                                           {})
                    interface_out_dict.update({"filter": group['filter']})
                    if group['per_user']:
                        if 'per-user' in group['per_user']:
                            per_user = True
                        else:
                            per_user = False
                    else:
                        per_user = False

                    interface_out_dict.update({"per_user": per_user})
                    interface_out_dict.update({"default": group['default']})
                    continue

                # Incoming routes will have 10 added to metric if on list 21
                m = p105.match(line)
                if m:
                    group = m.groupdict()
                    incoming_route_dict = rip_dict.setdefault('incoming_route_metric', {})
                    incoming_route_dict.update({k: v for k, v in group.items() if v})
                    continue

                # Sending updates every 10 seconds, next due in 8 seconds
                m = p106.match(line)
                if m:
                    group = m.groupdict()
                    timers_dict = rip_dict.setdefault('timers', {})
                    timers_dict.update({'update_interval': int(group['update_interval'])})
                    timers_dict.update({'next_update': int(group['next_update'])})
                    continue

                # Invalid after 21 seconds, hold down 22, flushed after 23
                m = p107.match(line)
                if m:
                    group = m.groupdict()
                    if 'timers' not in rip_dict:
                        timers_dict = rip_dict.setdefault('timers', {})
                    timers_dict.update({'invalid_interval': int(group['invalid_interval'])})
                    timers_dict.update({'holddown_interval': int(group['holddown_interval'])})
                    timers_dict.update({'flush_interval': int(group['flush_interval'])})
                    continue

                # Default redistribution metric is 3
                m = p108.match(line)
                if m:
                    group = m.groupdict()
                    rip_dict.update(
                        {'default_redistribution_metric': int(group['default_redistribution_metric'])})
                    continue

                # Redistributing: connected, static, rip
                m = p109.match(line)
                if m:
                    group = m.groupdict()
                    redistributes = group['Redistributing'].split(',')
                    redistribute_dict = rip_dict.setdefault('redistribute', {})
                    for key in redistributes:
                        redistribute_dict.setdefault(key.strip(), {})
                    continue

                m = p112.match(line)
                if m:
                    group = m.groupdict()
                    rip_dict.update({k: int(v) for k, v in group.items() if v})
                    continue

                m = p112_1.match(line)
                if m:
                    group = m.groupdict()
                    rip_dict.update({k: v for k, v in group.items() if v})
                    continue

                # Automatic network summarization is not in effect
                # Automatic network summarization is in effect
                m = p114.match(line)
                if m:
                    group = m.groupdict()
                    if group['automatic_network_summarization']:
                        automatic_network_summarization = False
                    else:
                        automatic_network_summarization = True
                    rip_dict.update(
                        {'automatic_network_summarization_in_effect': automatic_network_summarization})
                    continue

                # Interface                           Send  Recv  Triggered RIP  Key-chain
                #   GigabitEthernet3.100                2     2          No        1
                m = p113.match(line)
                if m:
                    group = m.groupdict()
                    interface_dict = rip_dict.setdefault('interfaces', {}).setdefault(group['interface'], {})
                    send = group['send']
                    receive = group['receive']

                    interface_dict.update({'send_version': send})
                    interface_dict.update({'receive_version': receive})
                    interface_dict.update({'triggered_rip': group['triggered_rip'].lower()})
                    interface_dict.update({'key_chain': group['key_chain']})
                    continue

                # 172.16.0.0/17 for GigabitEthernet3.100
                m = p116.match(line)
                if m:
                    group = m.groupdict()
                    summary_dict = interface_dict.setdefault('summary_address', {})
                    summary_dict.setdefault(group['prefix'], {})
                    continue

                # Maximum path: 4
                m = p117.match(line)
                if m:
                    group = m.groupdict()
                    rip_dict.update({'maximum_paths': int(group['maximum_path'])})
                    continue

                # Routing for Networks:
                m = p118.match(line)
                if m:
                    routing_network_flag = True
                    continue

                # 10.0.0.0
                m = p119.match(line)
                if m:
                    if routing_network_flag:
                        group = m.groupdict()
                        network_list.append(group['network'])
                        rip_dict.update({'network': list(set(network_list))})
                    continue

                # Passive Interface(s):
                m = p120.match(line)
                if m:
                    passive_interface_flag = True
                    routing_network_flag = False
                    continue

                # GigabitEthernet2.100
                m = p121.match(line)
                if m:
                    if passive_interface_flag == True:
                        group = m.groupdict()
                        interface_dict.update({'passive': True})
                    continue

                # Routing Information Sources:
                m = p122.match(line)
                if m:
                    passive_interface_flag = False
                    routing_network_flag = False
                    continue

                # Gateway         Distance      Last Update
                #   10.1.2.2             120      00:00:04
                m = p123.match(line)
                if m:
                    group = m.groupdict()
                    neighbor_dict = rip_dict.setdefault('neighbors', {}).setdefault(group['gateway'], {})
                    neighbor_dict.update({'last_update': group['last_update']})
                    neighbor_dict.update({'distance': int(group['distance'])})
                    continue

                # Distance: (default is 120)
                m = p124.match(line)
                if m:
                    group = m.groupdict()
                    rip_dict.update({'distance': int(group['distance'])})
                    continue
            else:
                # Outgoing update filter list for all interfaces is not set
                # Incoming update filter list for all interfaces is not set
                m = p2.match(line)
                if m:
                    group = m.groupdict()
                    if protocol == 'ospf':
                        pdict = ospf_dict
                    elif protocol == 'isis':
                        pdict = isis_dict
                    elif protocol == 'application':
                        pdict = application_dict
                    elif protocol == 'bgp':
                        pdict = bgp_dict
                    else:
                        continue
                    direction = str(group['dir']).lower() + '_' + 'filter_list'
                    pdict[direction] = str(group['state']).lower()
                    continue

                # Router ID 10.4.1.1
                m = p3.match(line)
                if m:
                    ospf_dict['router_id'] = str(m.groupdict()['router_id'])
                    continue

                # Number of areas in this router is 1. 1 normal 0 stub 0 nssa
                m = p4.match(line)
                if m:
                    group = m.groupdict()
                    ospf_dict['total_areas'] = int(group['areas'])
                    ospf_dict['total_normal_area'] = int(group['normal'])
                    ospf_dict['total_stub_area'] = int(group['stub'])
                    ospf_dict['total_nssa_area'] = int(group['nssa'])
                    continue

                # Maximum path: 4
                m = p5.match(line)
                if m:
                    group = m.groupdict()
                    if protocol == 'ospf':
                        if 'spf_control' not in ospf_dict:
                            ospf_dict['spf_control'] = {}
                        ospf_dict['spf_control']['paths'] = int(group['max'])
                    elif protocol == 'application':
                        application_dict['maximum_path'] = int(group['max'])
                    elif protocol == 'bgp':
                        bgp_dict['maximum_path'] = int(group['max'])
                    elif protocol == 'isis':
                        isis_dict['maximum_path'] = int(group['max'])
                    continue

                # Routing for Networks:
                m = p6_1.match(line)
                if m:
                    # Routing for Networks:
                    routing_networks = True
                    routing_network_intfs = []
                    # Routing on Interfaces Configured Explicitly
                    routing_on_interfaces = False
                    routing_on_interfaces_intfs = []
                    # Routing Information Sources:
                    routing_information = False
                    routing_info_gateways = []
                    # Passive Interface(s):
                    passive_interfaces = False
                    passive_intfs = []
                    # Address Summarization:
                    address_summarization = False
                    address_summarization_intfs = []
                    continue

                # Routing on Interfaces Configured Explicitly (Area 0):
                m = p6_2.match(line)
                if m:
                    area = str(IPAddress(str(m.groupdict()['area'])))
                    ospf_area_dict = ospf_dict.setdefault('areas', {}). \
                        setdefault(area, {})
                    # Routing for Networks:
                    routing_networks = False
                    routing_network_intfs = []
                    # Routing on Interfaces Configured Explicitly
                    routing_on_interfaces = True
                    routing_on_interfaces_intfs = []
                    # Routing Information Sources:
                    routing_information = False
                    routing_info_gateways = []
                    # Passive Interface(s):
                    passive_interfaces = False
                    passive_intfs = []
                    # Address Summarization:
                    address_summarization = False
                    address_summarization_intfs = []
                    continue

                # Routing Information Sources:
                m = p6_3.match(line)
                if m:
                    # Routing for Networks:
                    routing_networks = False
                    routing_network_intfs = []
                    # Routing on Interfaces Configured Explicitly
                    routing_on_interfaces = False
                    routing_on_interfaces_intfs = []
                    # Routing Information Sources:
                    routing_information = True
                    routing_info_gateways = []
                    # Passive Interface(s):
                    passive_interfaces = False
                    passive_intfs = []
                    # Address Summarization:
                    address_summarization = False
                    address_summarization_intfs = []
                    continue

                # Passive Interface(s):
                m = p6_4.match(line)
                if m:
                    # Routing for Networks:
                    routing_networks = False
                    routing_network_intfs = []
                    # Routing on Interfaces Configured Explicitly
                    routing_on_interfaces = False
                    routing_on_interfaces_intfs = []
                    # Routing Information Sources:
                    routing_information = False
                    routing_info_gateways = []
                    # Passive Interface(s):
                    passive_interfaces = True
                    passive_intfs = []
                    # Address Summarization:
                    address_summarization = False
                    address_summarization_intfs = []
                    continue

                # Address Summarization:
                m = p6_5.match(line)
                if m:
                    # Routing for Networks:
                    routing_networks = False
                    routing_network_intfs = []
                    # Routing on Interfaces Configured Explicitly
                    routing_on_interfaces = False
                    routing_on_interfaces_intfs = []
                    # Routing Information Sources:
                    routing_information = False
                    routing_info_gateways = []
                    # Passive Interface(s):
                    passive_interfaces = True
                    passive_intfs = []
                    # Address Summarization:
                    address_summarization = True
                    address_summarization_intfs = []
                    continue

                # Loopback0
                # GigabitEthernet2
                # GigabitEthernet1
                m = p7.match(line)
                if m:
                    if routing_networks:
                        routing_network_intfs.append(str(m.groupdict()['interface']))
                        if protocol == 'ospf':
                            ospf_dict['areas'][area]['configured_interfaces'] = routing_network_intfs
                        elif protocol == 'isis':
                            isis_dict['configured_interfaces'] = routing_network_intfs
                    elif routing_on_interfaces:
                        routing_on_interfaces_intfs.append(str(m.groupdict()['interface']))
                        if protocol == 'ospf':
                            ospf_dict['areas'][area]['configured_interfaces'] = routing_on_interfaces_intfs
                    elif passive_interfaces:
                        passive_intfs.append(str(m.groupdict()['interface']))
                        if protocol == 'ospf':
                            ospf_dict['passive_interfaces'] = passive_intfs
                        elif protocol == 'isis':
                            isis_dict['passive_interfaces'] = passive_intfs
                    elif address_summarization:
                        address_summarization_intfs.append(str(m.groupdict()['interface']))
                        if protocol == 'isis':
                            isis_dict['address_summarization'] = address_summarization_intfs
                    continue

                # Gateway         Distance      Last Update
                # 10.36.3.3            110      07:33:00
                # 10.16.2.2            110      07:33:00
                # 10.64.4.4            110      00:19:15
                m = p8.match(line)
                if m:
                    group = m.groupdict()
                    gateway = str(group['gateway'])
                    distance = int(group['distance'])
                    last_update = str(group['last_update'])
                    if routing_information:
                        if protocol == 'ospf':
                            gateway_dict = ospf_dict. \
                                setdefault('routing_information_sources', {}). \
                                setdefault('gateway', {}).setdefault(gateway, {})
                            gateway_dict['distance'] = distance
                            gateway_dict['last_update'] = last_update
                        elif protocol == 'bgp':
                            gateway_dict = bgp_dict.setdefault('neighbor', {}). \
                                setdefault(gateway, {})
                            gateway_dict['neighbor_id'] = gateway
                            gateway_dict['distance'] = distance
                            gateway_dict['last_update'] = last_update
                        elif protocol == 'isis':
                            gateway_dict = isis_dict. \
                                setdefault('routing_information_sources', {}). \
                                setdefault('gateway', {}).setdefault(gateway, {})

                            gateway_dict['distance'] = distance
                            gateway_dict['last_update'] = last_update

                    continue

                # Distance: (default is 110)
                m = p9.match(line)
                if m:
                    if protocol == 'ospf':
                        pdict = ospf_dict
                    elif protocol == 'application':
                        pdict = application_dict
                    elif protocol == 'isis':
                        pdict = isis_dict
                    else:
                        continue
                    # Set values
                    pref_dict = pdict.setdefault('preference', {})
                    single_value_dict = pref_dict.setdefault('single_value', {})
                    single_value_dict['all'] = int(m.groupdict()['num'])
                    continue

                # Distance: intra-area 112 inter-area 113 external 114
                m = p10.match(line)
                if m:
                    group = m.groupdict()
                    if protocol == 'ospf':
                        multi_values_dict = ospf_dict.setdefault('preference', {}). \
                            setdefault('multi_values', {})
                        multi_values_dict['external'] = int(group['external'])
                        detail_dict = multi_values_dict. \
                            setdefault('granularity', {}). \
                            setdefault('detail', {})
                        detail_dict['intra_area'] = int(group['intra'])
                        detail_dict['inter_area'] = int(group['inter'])
                    continue

                # Sending updates every 0 seconds
                m = p11.match(line)
                if m:
                    if protocol == 'application':
                        application_dict['update_frequency'] = \
                            int(m.groupdict()['update'])
                    continue

                # Invalid after 0 seconds, hold down 0, flushed after 0
                m = p12.match(line)
                if m:
                    group = m.groupdict()
                    if protocol == 'application':
                        application_dict['invalid'] = int(group['invalid'])
                        application_dict['holddown'] = int(group['holddown'])
                        application_dict['flushed'] = int(group['flushed'])
                    continue

                # IGP synchronization is disabled
                m = p13.match(line)
                if m:
                    if 'enabled' in m.groupdict()['igp']:
                        bgp_dict['igp_sync'] = True
                    else:
                        bgp_dict['igp_sync'] = False

                # Automatic route summarization is disabled
                m = p14.match(line)
                if m:
                    if 'enabled' in m.groupdict()['route']:
                        bgp_dict['automatic_route_summarization'] = True
                    else:
                        bgp_dict['automatic_route_summarization'] = False

                # Distance: external 20 internal 200 local 200
                m = p15.match(line)
                if m:
                    group = m.groupdict()
                    if protocol == 'bgp':
                        multi_values_dict = bgp_dict.setdefault('preference', {}).setdefault('multi_values', {})
                        multi_values_dict['external'] = int(group['external'])
                        multi_values_dict['internal'] = int(group['internal'])
                        multi_values_dict['local'] = int(group['local'])
                    continue

                # Redistributing: isis banana
                m = p16.match(line)
                if m:
                    if protocol == 'isis':
                        isis_dict['redistributing'] = m.groupdict()['redistributing']

        return ret_dict



# ====================================================
#  parser for show ip route
# ====================================================
class ShowIpProtocolsSectionRip(ShowIpProtocols):
    """Parser for :
       show ip protocols | sec rip
       show ip protocols vrf {vrf} | sec rip
       """

    cli_command = ["show ip protocols | sec rip", "show ip protocols vrf {vrf} | sec rip"]

    def cli(self, vrf="", cmd ="",output=None):
        if vrf:
            cmd = self.cli_command[1].format(vrf=vrf)
        else:
            cmd = self.cli_command[0]

        return super().cli(cmd=cmd, vrf=vrf,output=output)

# ====================================================
#  schema for show ipv6 protocols | sec rip
# ====================================================
class ShowIpv6ProtocolsSectionRipSchema(MetaParser):
    """Schema for
            show ipv6 protocols | sec rip
            show ipv6 protocols vrf {vrf} | sec rip"""
    schema = {
        'vrf': {
            Any(): {
                'address_family': {
                    Any(): {
                        Optional('instance'): {
                            Any(): {
                                Optional('redistribute'): {
                                    Any(): {
                                        Optional('metric'): int,
                                        Optional('route_policy'): str,
                                    },
                                },
                                Optional('interfaces'): {
                                    Any():{},
                                },
                            },
                        },
                    },
                },
            },
        }
    }


# ======================================================
#  parser for show ipv6 protocols | sec rip
# =======================================================
class ShowIpv6ProtocolsSectionRip(ShowIpv6ProtocolsSectionRipSchema):
    """Parser for :
           show ipv6 protocols | sec rip
           show ipv6 protocols vrf {vrf} | sec rip
           """

    cli_command = ["show ipv6 protocols | sec rip", "show ipv6 protocols vrf {vrf} | sec rip"]

    def cli(self, vrf="", output=None):
        if output is None:
            if vrf:
                cmd = self.cli_command[1].format(vrf=vrf)
            else:
                vrf = 'default'
                cmd = self.cli_command[0]
            out = self.device.execute(cmd)
        else:
            out = output

        address_family= "ipv6"

        #IPv6 Routing Protocol is "rip ripng"
        p1 = re.compile(r'^\s*IPv6 +Routing +Protocol +is +\"(?P<protocol>[\w\s]+)\"$')

        # Interfaces:
        p2 = re.compile(r'^\s*Interfaces$')

        #   GigabitEthernet3.200
        p3 = re.compile(r'^\s*(?P<interface>[\w\.\/]+)$')

        # Redistribution:
        #   Redistributing protocol connected with metric 3
        #   Redistributing protocol connected with transparent metric 3
        p4 = re.compile(r'^\s*Redistributing +protocol +(?P<redistribute>\w+) +with( +transparent)? +metric( +(?P<metric>\d+))?$')
        #   Redistributing protocol static with transparent metric route-map static-to-rip
        p5 = re.compile(
            r'^\s*Redistributing +protocol +(?P<redistribute>\w+) +with +transparent +metric( +route-map +(?P<route_policy>[\w\-]+))?$')

        result_dict = {}

        for line in out.splitlines():
            if line:
                line = line.rstrip()
            else:
                continue

            # Routing Protocol is "rip ripng"
            m = p1.match(line)
            if m:
                group = m.groupdict()
                protocol = group['protocol']
                rip_dict = result_dict.setdefault('vrf', {}).setdefault(vrf, {}).setdefault('address_family',{}). \
                    setdefault(address_family, {}).setdefault('instance', {}).setdefault(protocol, {})
                continue

            #   GigabitEthernet2.100
            m = p3.match(line)
            if m:
                group = m.groupdict()
                rip_dict.setdefault('interfaces', {}).setdefault(group['interface'], {})
                continue

            # Redistributing protocol connected with metric 3
            m = p4.match(line)
            if m:
                group = m.groupdict()
                redistribute = group['redistribute']
                redistribute_dict = rip_dict.setdefault('redistribute', {}).setdefault(redistribute, {})

                if group['metric']:
                    redistribute_dict.update({'metric': int(group['metric'])})
                continue
            # Redistributing protocol static with transparent metric route-map static-to-rip
            m = p5.match(line)
            if m:
                group = m.groupdict()
                redistribute = group['redistribute']

                redistribute_dict = rip_dict.setdefault('redistribute', {}).setdefault(redistribute, {})
                redistribute_dict.update({'route_policy': group['route_policy']})
                continue

        return result_dict