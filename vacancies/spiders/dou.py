import csv
import random
import time
from typing import Any

import scrapy
from scrapy.http import Response
from selenium import webdriver
from selenium.webdriver.common.by import By

from vacancies.items import VacanciesItem


class DouSpider(scrapy.Spider):
    name = "dou"
    allowed_domains = ["jobs.dou.ua"]
    start_urls = [
        "https://jobs.dou.ua/vacancies/?category=Python&exp=1-3",
        "https://jobs.dou.ua/vacancies/?category=Python&exp=3-5"
    ]
    output_files = {
        "https://jobs.dou.ua/vacancies/?category=Python&exp=1-3": "python_jobs_exp_1_3.csv",
        "https://jobs.dou.ua/vacancies/?category=Python&exp=3-5": "python_jobs_exp_3_5.csv",
    }

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.driver = webdriver.Chrome()

    def close(self, reason) -> None:
        self.driver.quit()

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={"output_file": self.output_files[url]}
            )

    def parse(self, response: Response, **kwargs):
        self.driver.get(response.url)

        time.sleep(random.randint(4, 5))

        cur_count = 1
        while True:

            more_btn = self.driver.find_element(
                By.CSS_SELECTOR, ".more-btn > a"
            )
            more_btn_style_attr = more_btn.get_attribute("style")
            if "display: none" in more_btn_style_attr:
                print("display NONE in load more btn")
                break
            else:
                print("CONTINUE", cur_count)
                cur_count += 1
            more_btn.click()
            time.sleep(random.randint(4, 5))

        detail_link_tag_list = self.driver.find_elements(
            By.CSS_SELECTOR, "li.l-vacancy > .title > a"
        )
        detail_links = [
            vacancy.get_attribute("href") for vacancy in detail_link_tag_list
        ]

        for link in detail_links:
            yield scrapy.Request(
                url=link,
                callback=self.parse_detail_vacancy,
                meta={"file_name": response.meta["output_file"]}
            )

    def parse_detail_vacancy(self, response: Response, **kwargs):
        item = VacanciesItem()
        item["company"] = response.css("div.l-n > a::text").extract_first()
        item["title"] = response.css("h1.g-h2::text").get()
        item["location"] = response.css("div.sh-info > span::text").extract_first()

        ul_elements = response.xpath("//div[@class='b-typo vacancy-section']//ul")

        description = ""
        for ul in ul_elements:
            li_elements = ul.xpath('.//li//text()').getall()
            description += " ".join(li_elements) + " "

        if not description:
            paragraphs = response.css("div.b-typo.vacancy-section p::text").extract()
            description = " ".join(paragraphs)

        item["description"] = description

        file_name = response.meta.get("file_name", 'default_file.csv')

        with open(file_name, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=item.keys())

            if file.tell() == 0:
                writer.writeheader()

            writer.writerow(dict(item))

        time.sleep(random.randint(4, 5))
        yield item
