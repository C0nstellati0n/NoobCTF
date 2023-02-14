# EBE

[Problem](https://github.com/uclaacm/lactf-archive/tree/master/2023/misc/ebe)

It's a pcap file. Go to "menu" -> "Analyze" -> "Follow" -> "UDP Stream", we see a string, seems to be random. The description mentions "RFC 3514", let's search for it. Google tells us something about the [evil bit](https://en.wikipedia.org/wiki/Evil_bit): "The RFC recommended that the last remaining unused bit, the 'Reserved Bit' in the IPv4 packet header, be used to indicate whether a packet had been sent with malicious intent".

Go to "menu" -> "File" -> "Export Packet Dissections" -> "As JSON" to export the information of the pcap as a json file. The field name of the "Reserved Bit" is "ip.flags.rb", if it's 1, we should ignore the payload of that UDP packet.

```python
import json
with open("ctf.json",'r') as f:
    d=json.loads(f.read())
for i in d:
    if i["_source"]["layers"]["ip"]["ip.flags_tree"]["ip.flags.rb"]=='0':
        print(chr(int(i["_source"]["layers"]["udp"]["udp.payload"],16)),end='')
```

## Flag
> lactf{3V1L_817_3xf1l7R4710N_4_7H3_W1N_51D43c8000034d0c}