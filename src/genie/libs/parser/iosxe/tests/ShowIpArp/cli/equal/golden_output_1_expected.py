expected_output = {
    "interfaces":{
        "Vlan200":{
            "ipv4":{
                "neighbors":{
                    "172.16.255.1":{
                        "ip":"172.16.255.1",
                        "link_layer_address":"28af.fdea.ccdf",
                        "type":"ARPA",
                        "origin":"static",
                        "age":"-",
                        "protocol":"Internet"
                    }
                }
            }
        },
        "Vlan201":{
            "ipv4":{
                "neighbors":{
                    "192.168.1.201":{
                        "ip":"192.168.1.201",
                        "link_layer_address":"0000.0000.0001",
                        "type":"ARPA",
                        "origin":"dynamic",
                        "private_vlan":202,
                        "age":"3",
                        "protocol":"Internet"
                    },
                    "192.168.1.203":{
                        "ip":"192.168.1.203",
                        "link_layer_address":"0015.0100.0001",
                        "type":"ARPA",
                        "origin":"dynamic",
                        "private_vlan":203,
                        "age":"3",
                        "protocol":"Internet"
                    }
                }
            }
        }
    }
}