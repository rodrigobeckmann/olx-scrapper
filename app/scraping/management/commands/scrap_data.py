from django.core.management.base import BaseCommand

from scraping.models import ScrapedData, Product

from parsel import Selector
from datetime import datetime
from typing import TypedDict
import cloudscraper
import json
import time


class ScrapedDataDict(TypedDict):
    subject: str
    title: str
    price: str
    listId: str
    url: str
    thumbnail: str
    date: str
    location: str
        

class Command(BaseCommand):
    help = 'Executa a rotina de scraping'

    def handle(self, *args, **kwargs):
        print("Executando rotina de scraping...")

        new_files = 0

        scraper = cloudscraper.create_scraper()
        page = 1

        if not Product.objects.filter(deleted_at=None).exists():
            print("Nenhum produto cadastrado")
            return

        for product in Product.objects.filter(deleted_at=None).iterator():
    
            while True:
                print(f"Página: {page}")
                time.sleep(0.1)
                product_name = product.name.replace(" ", "+")
                r = scraper.get(f"https://www.olx.com.br/brasil?q={product_name}&opst=2&o={page}")

                if "Ops! Nenhum anúncio foi encontrado." in r.text:
                    print("Página final alcançada")
                    break

                response = Selector(text=r.text)
                html = json.loads(response.xpath('//script[@id="__NEXT_DATA__"]/text()').get())
                products: list[ScrapedDataDict] = html.get('props').get('pageProps').get('ads')
                for product_data in products:
                    price = product_data.get('price')
                    list_id = product_data.get('listId')
                    if (
                        not list_id or
                        not price or
                        ScrapedData.objects.filter(olx_id=list_id).exists()
                    ):
                        continue
                    
                    ScrapedData.objects.create(
                        product_id=product.id,
                        olx_id=list_id,
                        title=product_data.get('title'),
                        url=product_data.get('url'),
                        img_url=product_data.get('thumbnail'),
                        price=price,
                        listing_date=datetime.fromtimestamp(int(product_data.get('date'))),
                    )
                    new_files += 1
                page += 1

        print(f"{new_files} novos arquivos salvos no banco de dados")

        print("Rotina concluída com sucesso!")