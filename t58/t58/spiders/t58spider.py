# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from t58.items import T58AgentItem
from t58.items import T58PositionItem
from selenium.webdriver.support.ui import WebDriverWait
import re
import time
import redis
from scrapy_redis.spiders import RedisCrawlSpider

class t58agentspider(scrapy.Spider):
    name = "t58agentspider"

    def __init__(self):
        super(t58agentspider, self).__init__()
        self.allowed_domains = ["58.com"]
        self.start_urls = ["http://qy.58.com/cq_3527/?PGTID=0d211266-0000-0e4c-ad64-51ced8e3e7fa&ClickID=1"]
        self.driver = webdriver.Firefox()

    def parse(self, response):
        self.driver.get(response.url)
        item = T58AgentItem()

        for agent in self.driver.find_elements_by_xpath('//div[@class="compList"]/ul/li/span/a'):
            item['agentname'] = agent.find_element_by_xpath('.').text
            print item['agentname']
            item['source']    = '58'
            item['sourceurl'] = agent.find_element_by_xpath('.').get_attribute('href')
            yield item

        self.driver.close()

class t58positionspider(RedisCrawlSpider):
    name = "t58positionspider"
    redis_key = 'cqhrsp'

    def __init__(self):
        super(t58positionspider, self).__init__()
        self.allowed_domains = ["58.com"]
        #self.start_urls = ["http://qy.58.com/41192498241806/"]

    def parse(self, response):
        yield scrapy.Request(url=response.url, callback=self.parse_url)

    def parse_url(self, response):
        driver = webdriver.Firefox()
        driver.get(response.url)

        while True:
            wait = WebDriverWait(driver, 10)
            time.sleep(30)
            wait.until(lambda driver: driver.find_element_by_xpath('//table[@class="jobList"]/tbody/tr'))

            item = T58PositionItem()
            for position in driver.find_elements_by_xpath('//table[@class="jobList"]/tbody/tr'):
                line = re.split('\s', position.text)
                item['positionname'] = line[0]
                item['positionurl']  = '12324342'
                item['salary']       = line[1]
                item['location']     = line[2]
                item['education']    = line[3]
                item['experience']   = line[4]
                item['headcount']    = line[5]
                item['updatetime']   = line[6]
                item['agenturl']     = response.url
                yield item

            # 模拟点击下一页/判断是否已经到了下一页
            try:
                wait = WebDriverWait(driver, 10)
                time.sleep(10)
                wait.until(lambda driver: driver.find_element_by_xpath('//a[@class="next"]'))

                next_page = driver.find_element_by_xpath('//a[@class="next"]')
                if next_page:
                    next_page.click()
                else:
                    break
            except:
                print "#####Arrive thelast page.#####"
                break

        driver.close()