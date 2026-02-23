import json

with open("sample-data.json") as f:
    data = json.load(f)

print("Interface Status")
print("-" * 80)
print("DN".ljust(45), "Description".ljust(15), "Speed".ljust(10), "MTU")
print("-" * 80)

for item in data["imdata"]:
    attr = item["l1PhysIf"]["attributes"]
    
    dn = attr["dn"]
    descr = attr["descr"]
    speed = attr["speed"]
    mtu = attr["mtu"]

    print(dn.ljust(45), descr.ljust(15), speed.ljust(10), mtu)
