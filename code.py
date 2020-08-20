import json
import requests


headers = {
    '',
}
data = {'results': []}


def get_brands():
    r = requests.get('https://www.---.sg/_c/v1/desktop/list_catalog_full', headers=headers)
    rs = r.json()
    brands = rs['brands']
    with open('id.txt', 'w') as w:
        for b in brands:
            _id = brands[b]['id_catalog_brand']
            amount = brands[b]['count']
            w.write(f'{_id},{amount}\n')


def get_links():
    with open('id.txt') as f:
        params = f.read().split('\n')
    with open('links.txt', 'w') as w:
        for p in params:
            _id = p.split(',')[0]
            amount = int(p.split(',')[1])
            for i in range(0, int(amount / 200) + 1):
                url = f'https://www.---.sg/_c/v1/desktop/list_catalog_full?' \
                      f'sort=popularity&dir=desc&offset={i * 200}&limit=200&brand={_id}\n '
                w.write(url)
                print(url)


def ready_data():
    with open('links.txt') as f:
        links = f.read().split('\n')
    mass = []
    for res in links:
        r = requests.get(res, headers=headers)
        rs = r.json()
        doc = rs['response']['docs']
        for b in doc:
            _sku = b['meta']['sku']
            name = b['meta']['name']
            price = b['meta']['price']
            mass.append({
                'name': name,
                'price': price,
                'sku:': _sku
            })
            print(f'{res} done...\n')
        data['results'] = mass
        with open('result.txt', 'w', encoding='utf8') as outfile:
            json.dump(data, outfile)


if __name__ == '__main__':
    get_brands()
    get_links()
    ready_data()
