from django.core.management.base import BaseCommand
from django.utils import timezone

from data_collection.models import (
    ScrapedData,
    Product,
    SearchTerm,
    ScrapLog,
)

from parsel import Selector
from datetime import datetime
from typing import TypedDict
import cloudscraper
import json


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
        print(f"Iniciada rotina de scraping {timezone.now()}")


        new_files = 0
        page_count = 0

        scraper = cloudscraper.create_scraper()

        if not Product.objects.filter(deleted_at=None).exists():
            print("Nenhum produto cadastrado")
            print(f"Rotina finalizada por falta de produtos {timezone.now()}")
            return

        for search_term in SearchTerm.objects.filter(deleted_at=None):
            page = 1
    
            while True:
                print(f"Página: {page}")
                product_name = search_term.term.replace(" ", "+")
                r = scraper.get(f"https://www.olx.com.br/brasil?q={product_name}&opst=2&o={page}")

                if "Ops! Nenhum anúncio foi encontrado." in r.text:
                    print(f"Rotina finalizada para o termo {search_term.term}")
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
                        product_id=search_term.product.pk,
                        olx_id=list_id,
                        title=product_data.get('title'),
                        url=product_data.get('url'),
                        img_url=product_data.get('thumbnail'),
                        price=price,
                        listing_date=datetime.fromtimestamp(int(product_data.get('date'))),
                    )
                    new_files += 1
                
                page_count += 1
                page += 1

        ScrapLog.objects.create(
            new_data_scraped=new_files,
            pages_scraped=page_count
        )

        print(f"{new_files} novos arquivos salvos no banco de dados")

        print(f"Finalizada rotina de scraping {timezone.now()}")