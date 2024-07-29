#!/usr/bin/python3
import argparse
import base64
import gzip
import json
from lxml import etree

NS = {'t128':'http://128technology.com/t128',
      'authy':'http://128technology.com/t128/config/authority-config',
      'sys':'http://128technology.com/t128/config/system-config',
      'if':'http://128technology.com/t128/config/interface-config', 
      'svc':'http://128technology.com/t128/config/service-config'}

def process_args():
    parser = argparse.ArgumentParser(description="Modify conductor address in existing quickstart file")
    parser.add_argument('--in-file', help='Existing quickstart file', required=True)
    parser.add_argument('--conductor1', help='Primary conductor address', required=True)
    parser.add_argument('--conductor2', help='Secondary conductor address', required=False)
    return parser.parse_args()

def main(filename=None, conductor1=None, conductor2=None):
    with open(filename) as fh:
        contents = fh.read()

    json_contents = json.loads(contents)
    c = json_contents['c']
    decoded = base64.b64decode(c)
    config_string = str(gzip.decompress(decoded), 'utf-8')
    config = etree.fromstring(config_string)

    authy = config.xpath('authy:authority', namespaces=NS)[0]
    cond_addr_elems = config.xpath('//authy:conductor-address', namespaces=NS)
    for cond_addr_elem in cond_addr_elems:
        cond_addr_elem.getparent().remove(cond_addr_elem)

    c1 = etree.SubElement(authy, "{http://128technology.com/t128/config/authority-config}conductor-address")
    c1.text=conductor1
    if conductor2:
        c2 = etree.SubElement(authy, "{http://128technology.com/t128/config/authority-config}conductor-address")
        c2.text=conductor2

    new_c = str(base64.b64encode(gzip.compress(etree.tostring(config))), 'utf-8')
    json_contents['c'] = new_c
    print(json.dumps(json_contents))

if __name__ == '__main__':
    args = process_args()
    main(filename=args.in_file,conductor1=args.conductor1,conductor2=args.conductor2)
