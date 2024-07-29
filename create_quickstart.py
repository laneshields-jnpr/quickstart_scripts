#!/usr/bin/python3
import argparse
import base64
import gzip
import json
from lxml import etree
from lxml.builder import ElementMaker

NS = {'t128':'http://128technology.com/t128',
      'authy':'http://128technology.com/t128/config/authority-config',
      'sys':'http://128technology.com/t128/config/system-config',
      'if':'http://128technology.com/t128/config/interface-config',
      'svc':'http://128technology.com/t128/config/service-config'}

def process_args():
    parser = argparse.ArgumentParser(description="Create quickstart file with only conductor address(es)")
    parser.add_argument('--conductor1', help='Primary conductor address', required=True)
    parser.add_argument('--conductor2', help='Secondary conductor address', required=False)
    return parser.parse_args()

def main(conductor1=None, conductor2=None):
    Et128 = ElementMaker(namespace=NS['t128'], nsmap=NS)
    Eauthy = ElementMaker(namespace=NS['authy'], nsmap=NS)
    Esys = ElementMaker(namespace=NS['sys'], nsmap=NS)
    config = Et128('config',
        Eauthy('authority',
            Eauthy('conductor-address', conductor1),
            Eauthy('conductor-address', conductor2) if conductor2 else '',
            Eauthy('router',
                Eauthy('name', 'dummy-router'),
                Esys('node',
                    Esys('name', 'dummy-node'),
                    Esys('role', 'combo'),
                    Esys('asset-id', 'dummy_asset')
                )
            )
        )
    )

    c = str(base64.b64encode(gzip.compress(etree.tostring(config))), 'utf-8')

    quickstart = {
        'n': 'dummy-node',
        'a': ''
    }

    quickstart['c'] = c
    print(json.dumps(quickstart))

if __name__ == '__main__':
    args = process_args()
    main(conductor1=args.conductor1,conductor2=args.conductor2)
