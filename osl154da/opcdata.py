import OpenOPC
import pathlib
import json
import time
import copyreg
import pywintypes
from PIL import Image
from . import utils

pywintypes.datetime = pywintypes.TimeType
copyreg.pickle(memoryview, lambda x: (memoryview, (x.tobytes(),)))

def raw_to_img(width, height, rawbytes):
    im = Image.frombytes("RGB",(width, height),rawbytes)
    im = Image.frombytes("RGB",(width, height),im.convert("BGR;24").tobytes())
    return im

def make_tag_dict(nodeids):
    return {nodeid.upper().rsplit(".", 1)[-1]: nodeid for nodeid in nodeids}

def _safe_bool(boolstr):
    _bool = boolstr.lower()
    if _bool in ("1", "on", "t", "true", "yes", "y") or _bool.startswith("true"):
        return True
    return False

def list_servers():
    opc = OpenOPC.client()
    print("Available OPC-servers:")
    for s in opc.servers():
        print(f" * {s}")

def discover_sign_data(server, add_tag, name):
    interactive = True

    client = OpenOPC.client()
    client.connect(server)

    tag_list = client.list(paths='*', recursive=True, flat=True)

    client.remove(client.groups())
    client.close()

    add_tags = []
    if add_tag and name:
        add_tags.append((add_tag, name))
    else:
        prefix_end = len(".image_onsign")
        matches = [tag for tag in tag_list if tag.lower().endswith(".image_onsign")]
        if not matches:
            print("No sign detected. Expected tag structure: **.IMAGE_ONSIGN")
            return
        for match in matches:
            tag = match[:-prefix_end]
            print(f"Found sign prefix: {tag}")
            if interactive:
                if _safe_bool(input(f"Add {tag}? (y/[n]): ")):
                    short_name = input(f"Use short name: [{name}]: ")
                    if not short_name:
                        short_name = name
                    add_tags.append((tag, short_name))
            else:
                print(f"Add using arguments: discover-sign {server} -add-tag {tag} -name default")
                print("")
    if not add_tags:
        return

    client.connect(server)
    for tag, name in add_tags:
        matches = [opctag for opctag in tag_list if opctag.startswith(tag)]
        tags = make_tag_dict(matches)
        pixelwidth = client.read(tags["PIXELWIDTH"])
        pixelheight = client.read(tags["PIXELHEIGHT"])
        width = pixelwidth[0]
        height = pixelheight[0]
        utils.create_sign_data(name, server, tag, width, height, tags)
        print(f"Added {tag} as {name}.")
    client.remove(client.groups())
    client.close()

def sign_read(name):
    root = utils.get_sign_path(name)
    data = json.load(root.joinpath("sign.json").open("r"))

    server = data["server"]

    print(f"Connecting to {server}")

    client = OpenOPC.client()
    client.connect(server)

    command = client.read(data["tags"]["COMMAND"])
    status = client.read(data["tags"]["STATUS"])
    value = client.read(data["tags"]["VALUE"])
    active_value = client.read(data["tags"]["ACTIVE_VALUE"])
    image_onsign = client.read(data["tags"]["IMAGE_ONSIGN"])
    image_toset = client.read(data["tags"]["IMAGE_TOSET"])
    pixelheight = client.read(data["tags"]["PIXELHEIGHT"])
    pixelpp = client.read(data["tags"]["PIXELPP"])
    pixelwidth = client.read(data["tags"]["PIXELWIDTH"])

    print("Values from server:")
    height = pixelheight[0]
    width = pixelwidth[0]
    print(f"status: {status[0]}")
    print(f"active_value: {active_value[0]}")
    print(f"command: {command[0]}")
    print(f"value: {value[0]}")
    print(f"pixelpp: {pixelpp[0]}")
    print(f"pixelheight: {height}")
    print(f"pixelwidth: {width}")

    onsign = image_onsign[0].tobytes()
    if onsign:
        raw_to_img(width, height, onsign).save(root.joinpath("_image_onsign.bmp"))
        print(f"image_onsign: {root}/_image_onsign.bmp")
    else:
        print(f"image_onsign: {onsign}")

    to_set = image_toset[0].tobytes()
    if to_set:
        raw_to_img(width, height, to_set).save(root.joinpath("_image_toset.bmp"))
        print(f"image_toset: {root}/_image_toset.bmp")
    else:
        print(f"image_toset: {to_set}")

    print("Disconnect")
    client.remove(client.groups())
    client.close()
    print("Done")

def rgb_on(name, image):
    root = pathlib.Path(".", "signs", name)
    data = json.load(root.joinpath("sign.json").open("r"))

    im = Image.open(root.joinpath(image))
    bmp = im.convert(mode="BGR;24").tobytes()

    assert data["width"] == im.width
    assert data["height"] == im.height

    server = data["server"]
    print(f"Connecting to {server}")

    client = OpenOPC.client()
    client.connect(server)

    command = data["tags"]["COMMAND"]
    value = data["tags"]["VALUE"]
    image_toset = data["tags"]["IMAGE_TOSET"]

    print(f"set_value({command}, 0)")
    client.write((command, 0))

    print("set_values(")
    print(f"  [{value}, 9999],")
    print(f"  [{image_toset}, <bmp-data::{image}>]")
    print(")")
    client.write([(value, 9999), (image_toset, bmp)])
    #client.write((value, 9999))
    #client.write((image_toset, bmp))

    print("await 4 seconds")
    time.sleep(4)

    print(f"set_value({command}, 4)")
    client.write((command, 4))

    client.remove(client.groups())
    client.close()
    print("Done")
