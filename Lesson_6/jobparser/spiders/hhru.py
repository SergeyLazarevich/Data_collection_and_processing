import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=&fromSearchLine=true&st=searchVacancy&items_on_page=20&text=python']

    def parse(self, response: HtmlResponse):
        vacancy_listing = response.xpath("//div[@class='vacancy-serp-item']")
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").extract_first()

        for vacancy in vacancy_listing:
            print()
            name = vacancy.xpath(".//a[@class='bloko-link']/text()").get()
            link = vacancy.xpath(".//a[@class='bloko-link']/@href").get()
            pay = vacancy.xpath(".//span[@data-qa='vacancy-serp__vacancy-compensation']/text()").get()
            site = 'https://hh.ru'
            yield JobparserItem(name=name, link=link, pay=pay, site=site)

        if next_page:
            yield response.follow(next_page, callback=self.parse)

