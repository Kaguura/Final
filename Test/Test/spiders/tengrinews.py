# -*- coding: utf-8 -*-
import scrapy

from scrapy.spiders import CrawlSpider
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

class Article:
    def __init__(self, title, text):
        self.title = title
        self.text = text
    

class TengrinewsSpider(CrawlSpider):
    name = "tengrinews"
    allowed_domains = ["tengrinews.kz"]
    fieldnames = ['title', 'text']
    
    def __init__(self):
        self.driver = webdriver.Firefox()
    
    def start_requests(self):
        yield scrapy.Request('https://tengrinews.kz/news/', self.parse)
        
    def parse(self, response):
        with open('articles.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = self.fieldnames)
            writer.writeheader()
        self.driver.get(response.url)
        button = self.driver.find_element_by_xpath('//div[@class="load_more_block"]/a')
        button.click()
        listLinks = [a.get_attribute('href') for a in self.driver.find_elements_by_xpath('//div[@class="news clearAfter pl mb"]/a')]
        articles = []
        for url in listLinks:
            article = self.parseANews(url)
            articles.append(article)
        self.writeToFile(articles)
    
    def parseANews(self, url):
        self.driver.get(url)
                
        title = self.driver.find_element_by_xpath('//h1').text
        text = self.driver.find_element_by_xpath('//div[@class="text sharedText js-mediator-article"]/p').text
        article = Article(title, text)
        return article

    def writeToFile(self, articles):
        with open('article.csv', 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = self.fieldnames)
            for article in articles:
                writer.writerow({self.fieldnames[0]: article.title, self.fieldnames[1]: article.text})
