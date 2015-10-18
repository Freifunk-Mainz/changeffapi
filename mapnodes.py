from requests import get as rget

from changeffapi import Loader

NODESJSON = 'http://map.freifunk-mainz.de/nodes.json'
FFAPIJSON = 'ffapi_file.json'


def scrape(url):
    '''returns remote json'''
    try:
        return rget(url).json()
    except Exception as ex:
        print('Error: %s' % (ex))

if __name__ == '__main__':
    nodes = scrape(NODESJSON)

    if nodes:
        online = 0
        nonclient = 0

        for node in nodes['nodes']:
            if node['flags']['online']:
                online += 1
                if not node['flags']['client']:
                    nonclient += 1

        loader = Loader(FFAPIJSON)
        if nonclient != int(loader.find(['state', 'nodes'])):
            loader.set(['state', 'nodes'], nonclient)
            loader.dump(overwrite=True)
