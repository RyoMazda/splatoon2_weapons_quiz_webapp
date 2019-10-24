from typing import List, Dict, Union

from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
import requests


Weapon = Dict[str, Union[str, int]]


class Scraper:
    def __init__(self):
        self.url = 'https://www.ikaclo.jp/2/weapons/'
        self.html = self._get_html(self.url)
        self.soup = BeautifulSoup(self.html, "html.parser")

        self.url_en = 'https://www.ikaclo.com/2/weapons/'
        self.html_en = self._get_html(self.url_en)
        self.soup_en = BeautifulSoup(self.html_en, "html.parser")

    @staticmethod
    def _get_html(url: str) -> str:
        print('Start running a browser and trying to get html...')
        if url[:4] == 'http':
            r = requests.get(url)
            html = r.content
        else:  # test用
            with open(url) as f:
                html = f.read()
        return html

    @staticmethod
    def _hot_fix_weapon(weapon: Weapon) -> None:
        """"Fix weapon data since the source html itself is wrong"""
        if weapon['id'] == "227":
            weapon['special_weapon_id'] = 21

    def _get_weapons(self) -> List[Weapon]:
        weapons = []

        tbody = self.soup.select_one('tbody')
        tbody_en = self.soup_en.select_one('tbody')
        for tr, tr_en in zip(tbody.select('tr'), tbody_en.select('tr')):
            name = tr.select_one('.txt>a>span').getText()
            name_en = tr_en.select_one('.txt>a>span').getText()
            weapon_id = tr.select_one('.img>a').attrs['href'].split('/')[-1]
            sub_weapon_id = int(
                tr.select('td')[1].select('img')[0].attrs['data-src'].split('/')[-1].split('.')[0].split('_')[-1])
            special_weapon_id = int(
                tr.select('td')[1].select('img')[1].attrs['data-src'].split('/')[-1].split('.')[0].split('_')[-1])
            weapon = {
                'name': name,
                'name_en': name_en.replace("'", "\\'"),
                'id': weapon_id,
                'sub_weapon_id': sub_weapon_id,
                'special_weapon_id': special_weapon_id,
            }
            self._hot_fix_weapon(weapon)
            weapons.append(weapon)
        return weapons

    def run(self, output_path: str) -> None:
        data = {'weapons': self._get_weapons()}

        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template('weapons_template.txt')

        output = template.render(data)

        with open(output_path, 'w') as f:
            f.write(output)
            f.write('\n')


if __name__ == '__main__':
    scraper = Scraper()
    scraper.run(output_path='weapons.ts')
