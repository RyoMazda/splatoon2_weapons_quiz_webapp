from typing import List, Dict, Union

from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
import requests


class Scraper:
    def __init__(self, url: str):
        self.url = url
        self.html = self._get_html(self.url)
        self.soup = BeautifulSoup(self.html, "html.parser")

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

    def _get_weapons(self) -> List[Dict[str, Union[str, int]]]:
        weapons = []

        tbody = self.soup.select_one('tbody')
        for tr in tbody.select('tr'):
            name = tr.select_one('.txt>a>span').getText()
            weapon_id = tr.select_one('.img>a').attrs['href'].split('/')[-1]
            sub_weapon_id = int(
                tr.select('td')[1].select('img')[0].attrs['data-src'].split('/')[-1].split('.')[0].split('_')[-1])
            special_weapon_id = int(
                tr.select('td')[1].select('img')[1].attrs['data-src'].split('/')[-1].split('.')[0].split('_')[-1])
            weapon = {
                'name': name,
                'id': weapon_id,
                'sub_weapon_id': sub_weapon_id,
                'special_weapon_id': special_weapon_id,
            }
            weapons.append(weapon)
        return weapons

    def run(self, output_path: str) -> None:
        data = {'weapons': self._get_weapons()}

        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template('weapons_template.txt')

        output = template.render(data)

        # htmlを上書き保存
        with open(output_path, 'w') as f:
            f.write(output)


if __name__ == '__main__':
    scraper = Scraper(url='https://www.ikaclo.jp/2/weapons/')
    scraper.run(output_path='../src/weapons.ts')
