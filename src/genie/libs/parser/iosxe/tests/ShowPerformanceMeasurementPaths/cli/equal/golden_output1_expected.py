
expected_output = {
    'Path-7': {
        'source': '1:2:3:3::1',
        'endpoint': '1:1:1:7::1',
        'next_hop': '1:1:1:7::1',
        'dest': '1:1:1:7::1',
        'outgoing_intf': 'Ethernet1/2',
        'backoff': 1,
        'used_cnt': 1,
        'cleanup': 3599,
    },
    'Path-8': {
        'source': '1.1.1.3',
        'endpoint': '1.1.1.7',
        'next_hop': '1.1.1.7',
        'dest': '1.1.1.7',
        'outgoing_intf': 'Loopback0',
        'backoff': 0,
        'used_cnt': 1,
        'cleanup': 3599,
    },
    'Path-11': {
        'source': '1.1.1.3',
        'endpoint': '1.1.1.7',
        'next_hop': '1.2.3.4',
        'dest': '1.1.1.7',
        'sr_labels': '25, 17',
        'outgoing_intf': 'Ethernet1/2',
        'backoff': 0,
        'used_cnt': 1,
    },
    'Path-10': {
        'source': '1.1.1.3',
        'endpoint': '1.1.1.7',
        'next_hop': '110.1.1.4',
        'dest': '1.1.1.7',
        'sr_labels': 16230,
        'outgoing_intf': 'Ethernet0/1',
        'backoff': 0,
        'used_cnt': 3,
        'cleanup': 3600,
    },
    'Path-3': {
        'source': '1.2.3.3',
        'outgoing_intf': 'Ethernet1/2',
        'backoff': 0,
        'used_cnt': 1,
        'cleanup': 3598,
    },
    'Path-6': {
        'source': '1.2.3.3',
        'endpoint': '1.1.1.7',
        'next_hop': '1.1.1.7',
        'dest': '1.1.1.7',
        'outgoing_intf': 'Ethernet1/2',
        'backoff': 0,
        'used_cnt': 1,
        'cleanup': 3599,
    },
    'Path-1': {
        'source': '19.1.1.3',
        'outgoing_intf': 'Ethernet0/0',
        'backoff': 1,
        'used_cnt': 1,
        'cleanup': 3598,
    },
    'Path-5': {
        'source': '19.1.1.3',
        'endpoint': '65.1.1.7',
        'next_hop': '65.1.1.7',
        'dest': '65.1.1.7',
        'outgoing_intf': 'Ethernet0/0',
        'backoff': 0,
        'used_cnt': 1,
        'cleanup': 3599,
    },
    'Path-2': {
        'source': '110.1.1.3',
        'outgoing_intf': 'Ethernet0/1',
        'backoff': 0,
        'used_cnt': 2,
        'cleanup': 3598,
    },
    'Path-4': {
        'source': '112.112.112.3',
        'outgoing_intf': 'Tunnel1',
        'backoff': 0,
        'used_cnt': 1,
        'cleanup': 3600,
    },
    'Path-9': {
        'source': '112.112.112.3',
        'endpoint': '112.112.112.6',
        'next_hop': '112.112.112.6',
        'dest': '112.112.112.6',
        'backoff': 1,
        'used_cnt': 1,
        'cleanup': 3599,
    },
}