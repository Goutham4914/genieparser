

expected_output = {
    'vrf': {
        'default': {
            'config': {
                'allow_encaps_count': 0,
                'default_peer_address': '0.0.0.0',
                'maximum_sa': 20000,
                'originator_address': '172.16.76.1',
                'originator_interface': 'Loopback150',
                'sa_holdtime': 150},
            'context_info': {
                'table_count': {
                    'active': 2,
                    'total': 2},
                'table_id': '0xe0000000',
                'vrf_id': '0x60000000'},
            'inheritable_config': {
                'keepalive_period': 30,
                'maximum_sa': 0,
                'peer_timeout_period': 75,
                'ttl': 2},
            'mrib_update_counts': {
                'g_routes': 26,
                'sg_routes': 447,
                'total_updates': 473,
                'with_no_changes': 0},
            'mrib_update_drops': {
                'auto_rp_address': 2,
                'invalid_group': 0,
                'invalid_group_length': 0,
                'invalid_source': 0},
            'sa_cache': {
                'external_sas': {
                    'current': 3,
                    'high_water_mark': 3},
                'groups': {
                    'current': 2,
                    'high_water_mark': 2},
                'rps': {
                    'current': 3,
                    'high_water_mark': 0},
                'sources': {
                    'current': 12,
                    'high_water_mark': 12}}}}}
