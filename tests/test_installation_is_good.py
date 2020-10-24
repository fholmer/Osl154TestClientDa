import OpenOPC

def test_create_client_and_list_servers():
    opc = OpenOPC.client()
    servers = opc.servers()
    assert isinstance(servers, list)
