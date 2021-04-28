from selenium import webdriver
from time import sleep
from datetime import datetime
import json
import xlsxwriter


class VehicleBot:
    def __init__(self):
        # open config file
        with open('config.json') as json_file:
            self.config = json.load(json_file)
        # open links file
        with open('links.json') as json_file:
            self.links = json.load(json_file)
        # initialize web driver
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.vehicle_type = "bikes"
        # for spreadsheet
        self.row = 0
        self.workbook = xlsxwriter.Workbook(
            'C:/Users/Dan/Documents/Python Projects/VehicleBot/ads.xlsx')
        self.worksheet = self.workbook.add_worksheet()
        # loop through keywords
        for keyword in self.config['keywords']:
            for link in self.links[self.vehicle_type]:
                # search in Ikman
                self.search_ikman(link['ikman'], keyword)
                sleep(2)
                # search in Riyasewana
                # self.search_riyasewana(link['riyasewana'], keyword)
                sleep(2)

        self.workbook.close()
        exit()

    def search_ikman(self, link, keyword):
        self.driver.get(link)
        sleep(2)
        # Search by keyword
        self.driver.find_element_by_xpath(
            '//input[@type="search"]').send_keys(keyword)
        self.driver.find_element_by_xpath(
            '//button[contains(text(), "Search")]').click()
        sleep(4)
        # Get current url
        currentURL = self.driver.current_url
        # Get all ad links in page
        resultSet = self.driver.find_element_by_xpath(
            '//ul[contains(@class, "list--3NxGO")]')
        ads = resultSet.find_elements_by_tag_name("li")
        ad_links = []
        for ad in ads:
            ad_links.append(ad.find_element_by_tag_name(
                "a").get_attribute('href'))
        # Go through each ad
        for ad_link in ad_links:
            self.driver.get(ad_link)
            # Get title
            title = self.driver.find_element_by_xpath(
                '//h1[contains(@class, "title--3s1R8")]').text
            # Get price
            price = self.driver.find_element_by_xpath(
                '//div[contains(@class, "amount--3NTpl")]').text
            # Get date, time, city and District
            subTitle = self.driver.find_element_by_xpath(
                '//span[contains(@class, "sub-title--37mkY")]').text
            subTitle = subTitle.split(',')
            dateTime = subTitle[0].split(' ')
            dateTime.remove('Posted')
            dateTime.remove('on')
            dateTime = ' '.join(dateTime)
            city = subTitle[1].strip()
            district = subTitle[2].strip()
            # Get model year
            year = self.driver.find_element_by_xpath(
                '//div[contains(text(), "Model year: ")]/following-sibling::div').text
            # Get description
            description = self.driver.find_element_by_xpath(
                '//div[contains(@class, "description--1nRbz")]').text
            ad_list = [title, price, year, city, district,
                       dateTime, description, ad_link]
            print(
                f"{year} - {title} - {price} - {city} - {district} - {dateTime} - {description} - {ad_link}")
            self.write_sheet(ad_list, self.row)
            self.row += 1

    def search_riyasewana(self, link, keyword):
        self.driver.get(link)
        sleep(2)

    def write_sheet(self, ad_list, row):
        col = 0
        for item in (ad_list):
            self.worksheet.write(row, col, item)
            col += 1


my_bot = VehicleBot()
