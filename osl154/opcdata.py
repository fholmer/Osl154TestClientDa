import OpenOPC
import pathlib
import json
import time

def list_servers():
    opc = OpenOPC.client()
    print("Available OPC-servers:")
    for s in opc.servers():
        print(f" - {s}")

def rgb_on(name, bmp="1.bmp"):
    root = pathlib.Path(".", "signs", name)
    data = json.load(root.joinpath("sign.json").open("r"))

    bmp = root.joinpath(bmp).open(mode="br").read()

    server = data["server"]

    command = data["tags"]["COMMAND"]
    image_toset = data["tags"]["IMAGE_TOSET"]
    value = data["tags"]["VALUE"]
    #status = data["tags"]["STATUS"]
    #active_value = data["tags"]["ACTIVE_VALUE"]
    #image_onsign = data["tags"]["IMAGE_ONSIGN"]

    print(f"Connecting to {server}")

    opc = OpenOPC.client()
    opc.connect(server)
    time.sleep(1)

    print(f"set {command} to 0")
    opc.write((command, 0))
    time.sleep(1)

    print(f"set {value} to 9999 and {image_toset} to bmp-data from 1.bmp")
    opc.write([
        (value, 9999),
        (image_toset, bmp)
    ])
    time.sleep(1)

    print("await 4 seconds")
    time.sleep(4)

    print(f"set {command} to 4")
    opc.write((command, 4))
    time.sleep(1)

    print("Disconnect")
    opc.remove(opc.groups())
    opc.close()

    print("Done")