import csv
import requests

from concurrent import futures
from lxml import html
from nameparser import HumanName



def get_links():
    cookies = {
        'JSESSIONID': 'B8CBE7811775459DD715',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'uk-UA,uk;q=0.8,en-US;q=0.5,en;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    data = [
      ('SearchSurname', ''),
      ('SearchAka', ''),
      ('SearchEmail', ''),
      ('SearchTelephone', ''),
      ('SearchTitle', 'Professor'),
      ('SearchOrgUnit', ''),
      ('SearchSortBy', 'sortBySurname'),
      ('eventSubmit_doSearch', 'Search'),
      ('eventSubmit_doSearch', 'Search'),
    ]

    r = requests.post('https://.vm', headers=headers, cookies=cookies, data=data)
    tree = html.fromstring(r.text)

    return tree.xpath("//a[contains(@href, 'atlas.cafe.uit.yorku.ca/atlas/servlet/atlas/action/AtlasAction/template/person.vm')]/@href")


def parse(url):
    r = requests.get(url)
    tree = html.fromstring(r.text)
    full_name = tree.xpath("//p[@class='heading']/text()")[0]
    f = HumanName(full_name)
    fname = f.first
    lname = f.last
    try:
        email = tree.xpath("//b/a[contains(@href,'mailto')]/text()")[0]
    except:
        email = ''
    try:
        title = tree.xpath("//tr[./td/span[contains(text(), 'Title')]]//b/text()")[0]
    except:
        title = ''
    try:
        dep = tree.xpath("//tr[./td/span[contains(text(), 'Department')]]//b//text()")[0].strip()
    except:
        dep = ''
    print(full_name, ':', email)
    if email not in emails:
        wr.writerow([full_name, fname, lname, title, email, dep])
        emails.add(email)


def run():
    urls = get_links()
    with futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(parse, url): url for url in urls}
        for future in futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                future.result()
            except Exception as ex:
                print(f'{url}: {ex}')


if __name__ == '__main__':
    emails = set()
    w = open('yorku.csv', 'w', encoding='utf8', newline='')
    wr = csv.writer(w, delimiter=',')
    wr.writerow(['Full Name', 'First Name', 'Last Name', 'Title', 'Email', 'Department'])
    run()

