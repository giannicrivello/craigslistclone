from django.shortcuts import render
import requests
from requests.compat import quote_plus
from bs4 import BeautifulSoup

from . import models

BASE_CRAIGLIST_URL = 'https://portland.craigslist.org/d/services/search/bbb?query={}'

BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'



def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)  #creating search object #this writes to the database based off of user posts
    # print(quote_plus(search))
    final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
    # print(final_url)
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    post_title = soup.find_all('a', {'class' : 'result-title'}) # find all links where class is results-title
    # print(post_title.get('href'))
    post_lisitngs = soup.find_all('li', {'class' : 'result-row'})
    # # post_title = post_lisitngs.find('a', {'class' : 'result-title'}) # find all links where class is results-title
    # # post_url = post_lisitngs.find('a').get('href')
    # post_price = post_lisitngs.find(class_= 'result-price')
    # # post_text = new_soup.find(id='postingbody').text

    final_postings = []
    
    
    for post in post_lisitngs:
        post_title = post.find('a', {'class' : 'result-title'}).text
        post_url = post.find('a').get('href')
        post_price = post.find(class_= 'result-price')


        if post.find('a', {'class' : 'result-image'}).get('data-ids'):
            post_image_url = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1] #parsing the images in the URL 
            post_image_url = BASE_IMAGE_URL.format(post_image_url)
        print (post_image_url)
        # else:
        #     post_image_url = ''


        final_postings.append((post_title, post_url, post_price, post_image_url))

    
    
    # print(post_title)
    # print(post_url)
    # print(post_price)


    # print(data)
    # print(search)
    stuff_for_frontend = {
        'search' : search,
        'final_postings' : final_postings,
    }


    return render(request, 'myapp/new_search.html', stuff_for_frontend)
