from osl154 import opcdata

def test_list_servers(capfd):
    assert opcdata.list_servers() is None
    out = capfd.readouterr().out
    assert len(out) > 0
