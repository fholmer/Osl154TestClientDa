from osl154da import signdata

def test_list_servers(capfd):
    assert signdata.list_signs() is None
    out = capfd.readouterr().out
    assert len(out) > 0
