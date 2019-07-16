"""Script to gather content from IMDB"""
import sys
import csv
from bs4 import BeautifulSoup
import requests
import config


URL = config.URL


def first_test():
    """
    Main entry point for the script.
    :return:
    """
    movies = get_top_movie_link(URL)
    with open('output.csv', 'w') as output:
        writer = csv.writer(output)
        for title, url in movies:
            keywords = get_keywords_for_movie('http://www.imdb.com{}keywords/'.format(url))
            writer.writerow([title, keywords])


def get_top_movie_link(url):
    """
    Return a list of tuple containing the top grossing movies of 2019 and link to their IMDB page.
    :param url:
    :return top_movie_list:
    """
    response = requests.get(url)
    movies_list = []
    for each_url in BeautifulSoup(response.text, 'html.parser').select('a[href*="title"]'):
        movie_title = each_url.text
        movies_list.append((movie_title, each_url['href']))
    return movies_list


def get_keywords_for_movie(url):
    """
    return of keywords associated with 'movie'.
    :param url:
    :return keywords_list:
    """
    keywords = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table', class_='dataTable')
    table = tables[0]
    return [td.text for tr in table.find_all('tr') for td in tr.find_all('td')]


print(get_top_movie_link(URL))
