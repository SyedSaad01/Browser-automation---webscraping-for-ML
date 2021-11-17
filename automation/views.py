from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from bs4 import BeautifulSoup
import requests
import pandas as pd
# Create your views here.
def automation(request):
    driver=webdriver.Chrome(executable_path= 'C:/Users/syeds/Downloads/chromedriver_win32/chromedriver.exe')
    driver.get('https://imdb.com')
    driver.maximize_window()
    time.sleep(1)

    dropdown=driver.find_element_by_class_name('ipc-icon--arrow-drop-down')
    dropdown.click()
    time.sleep(1)

    advanced_search=driver.find_element_by_link_text('Advanced Search')
    advanced_search.click()

    advanced_title_search=driver.find_element_by_link_text('Advanced Title Search')
    advanced_title_search.click()


    feature_film=driver.find_element_by_id('title_type-1')
    feature_film.click()

    TV_Movie=driver.find_element_by_id('title_type-2')
    TV_Movie.click()

    time.sleep(0.5)
    release_date_from=driver.find_element_by_name('release_date-min')
    release_date_from.click()
    release_date_from.send_keys('1990')

    release_date_to=driver.find_element_by_name('release_date-max')
    release_date_to.click()
    release_date_to.send_keys('2020')

    time.sleep(0.5)
    rating_from=driver.find_element_by_name('user_rating-min')
    rating_from.click()
    rating_from=Select(rating_from)
    rating_from.select_by_visible_text('2.0')

    rating_to=driver.find_element_by_name('user_rating-max')
    rating_to.click()
    rating_to=Select(rating_to)
    rating_to.select_by_visible_text('9.9')

    # time.sleep(0.5)
    # genres=driver.find_element_by_id('genres-14')
    # genres.click()

    # adventure=driver.find_element_by_id('genres-2')
    # adventure.click()

    time.sleep(0.5)


    oscar_nominated=driver.find_element_by_id('groups-7')
    oscar_nominated.click()

    time.sleep(0.5)
    color_info=driver.find_element_by_id('colors-1')
    color_info.click()

    time.sleep(0.5)
    languages=driver.find_element_by_name('languages')
    languages=Select(languages)
    languages.select_by_visible_text('English')


    time.sleep(0.5)
    pages=driver.find_element_by_id('search-count')
    pages.click()
    pages=Select(pages)
    pages.select_by_index(2)


    time.sleep(0.5)
    button=driver.find_element_by_xpath('(//button[@type="submit"])[2]')
    button.click()


    current_url = driver.current_url
    # current_url='https://www.imdb.com/search/title/?title_type=feature,tv_movie&release_date=1990-01-01,2020-12-31&user_rating=1.3,9.9&languages=en&count=250'

    #Beautiful soup
    response = requests.get(current_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    all_movies_list=soup.find_all('div',{'class':'lister-item'})


    movie_names=[]
    movie_duration=[]
    movie_rating=[]
    movie_genres=[]
    movie_year=[]

    for count in range(len(all_movies_list)):
        name=all_movies_list[count].find('h3').find('a').get_text()
        year=all_movies_list[count].find('h3').find('span',{'class':'lister-item-year'}).get_text().replace('(','').replace(')','')
        genres=all_movies_list[count].find('p',{'class':'text-muted'}).find('span',{'class':'genre'}).get_text().strip()
        rating=all_movies_list[count].find('div',{'class':'ratings-bar'}).find('strong').get_text().strip()
        duration=all_movies_list[count].find('p',{'class':'text-muted'}).find('span',{'class':'runtime'}).get_text()
        movie_names.append(name)
        movie_duration.append(duration)
        movie_genres.append(genres)
        movie_rating.append(rating)
        movie_year.append(year)

    movies_df = pd.DataFrame({'Movie Title': movie_names, 'Year': movie_year, 'Duration':movie_duration,
                        'Genre': movie_genres, 'Rating':movie_rating})
    return render(request,'automation.html')

def home(request):
    return render(request,'home.html')