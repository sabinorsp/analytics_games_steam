import re
import pandas as pd
import requests
from datetime import datetime
from bs4 import BeautifulSoup


class EtlSteam:


    def __init__(self, url: str):
        self.url = url
        self.html_content = ""
        self.appIDs = []
        self.data_info = pd.DataFrame()
        self.data_links = pd.DataFrame()
        self.data_prices = pd.DataFrame()
        self.data_reviews = pd.DataFrame()
        self.total_counts = ""


    def get_summary_data(self) -> None:
        """
        Get summary data by scraping all search game steam list
        
        Return:
            None
        """
        response = requests.get(self.url).json()
        self.html_content = BeautifulSoup(response['results_html'],'html.parser')
        self.data_info, self.data_links = self.get_info()
        self.data_prices = self.get_prices()
        self.data_reviews = self.get_reviews()
        self.total_counts = response["total_count"]
        return None


    def get_info(self) -> tuple:
        """
        Retrivies information such as appID, title, tag_id, and links from the HTML content.

        Returns: 
            tuple: A tuple containing two dataframes. The first dataframe contains the columns
                   'steam_id', 'title', and 'tagid_steam'. The second dataframe contains the 
                   columns 'steam_id' and 'links' reference. 
        """
        tagIDs, titles, links = [],[],[]
        content = self.html_content  
        for tag in content.find_all('a', {'class':'search_result_row ds_collapse_flag'}):
                self.appIDs.append(tag.attrs.get('data-ds-appid'))
                tagIDs.append(tag.attrs.get('data-ds-tagids'))
                links.append(tag.attrs.get('href'))
        for tag in content.find_all('span', {'class':'title'}):
            titles.append(tag.get_text())           
        data_info = pd.DataFrame({
            'steam_id': self.appIDs,
            'title':titles,
            'tagid_steam':tagIDs
            })
        data_links = pd.DataFrame({
            'steam_id': self.appIDs,
            'links': links 
        })
        return data_info, data_links
    
    
    def get_prices(self) -> pd.DataFrame:
        """
        Get prices: Release_data, prices, discount, dateview

        Return:
            pandas.DataFrame() : dataframe contain Release_data, prices, discount and dataview
        """
        releases_data = []
        prices = []
        discounts = []
        content = self.html_content
        releases_data = [tag.get_text() for tag in self.html_content.
                         find_all('div', {'class':'col search_released responsive_secondrow'})]
        for tag in content.find_all('div', {'class':'col search_price_discount_combined responsive_secondrow'}):
            try:
                free1 = tag.find('div', {'class':'col search_price responsive_secondrow'}).get_text()
                free = free1.replace(' ','').replace('\r\n','')
            except AttributeError:
                free = None
            price = tag.attrs['data-price-final']
            if free == 'FreetoPlay':
                prices.append('freetoplay')
            else:
                price = list(price)
                price.insert(-2,'.')
                prices.append(''.join(price))
            try:
                discounts.append(tag.find('span').get_text())
            except AttributeError:
                discounts.append(None)
        data_prices = pd.DataFrame({
            'steam_id': self.appIDs,
            'release_date': releases_data,
            'price_real': prices,
            'discount': discounts 
            })
        data_prices['data_view'] = datetime.now().strftime('%d-%m-%Y')
        return data_prices


    def get_reviews(self) -> pd.DataFrame:
        """
        Get Total review and the % of positive review

        Return:
            pandas.DataFrame() : dataframe with the ID, Total Review, %positive review
        """
        reviews, positive_rev= [], []
        content = self.html_content
        for tag in content.find_all('a', {'class': 'search_result_row ds_collapse_flag'}):
            try:
                tag = tag.find('span', {'class': 'search_review_summary positive'})
                tag = tag.attrs['data-tooltip-html']
                pattern_total_rev = r'the\s+(\d[\d,]*)\s+user'
                match_total_rev = re.search(pattern_total_rev, tag)
                if match_total_rev:
                    number_total = match_total_rev.group(1).replace(',', '')
                    reviews.append(number_total)
                pattern_percent_rev = r'(\d[\d,]*)%'
                match_percent_rev = re.search(pattern_percent_rev, tag)
                if match_percent_rev:
                    number_percent = match_percent_rev.group(1).replace(',', '')
                    positive_rev.append(number_percent)
            except (AttributeError, TypeError):
                reviews.append(None)
                positive_rev.append(None)
        data_reviews = pd.DataFrame({
            'id_steam': self.appIDs,
            'total_reviews': reviews,
            'percent_positive_reviews': positive_rev
            })
        return data_reviews