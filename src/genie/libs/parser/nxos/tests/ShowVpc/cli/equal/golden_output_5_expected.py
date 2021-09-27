

expected_output = {
    'vpc_domain_id': '100',
    'vpc_peer_status': 'peer link is down',
    'vpc_peer_keepalive_status': 'peer is alive, but domain IDs do not match',
    'vpc_configuration_consistency_status': 'success',
    'vpc_per_vlan_consistency_status': 'success',
    'vpc_type_2_consistency_status': 'success',
    'vpc_role': 'primary',
    'num_of_vpcs': 1,
    'peer_gateway': 'Disabled',
    'dual_active_excluded_vlans': '-',
    'vpc_graceful_consistency_check_status': 'Enabled',
    'peer_link': {
        1: {
            'peer_link_id': 1,
            'peer_link_ifindex': 'Port-channel100',
            'peer_link_port_state': 'down',
            'peer_up_vlan_bitset': '-'
        }
    },
    'vpc': {
        1: {
            'vpc_id': 1,
            'vpc_ifindex': 'Port-channel1',
            'vpc_port_state': 'down',
            'vpc_consistency': 'success',
            'vpc_consistency_status': 'success',
            'up_vlan_bitset': '-'
        }
    }
}
