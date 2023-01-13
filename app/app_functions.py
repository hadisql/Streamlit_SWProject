import pandas as pd
import requests
import streamlit as st
import re

@st.cache
def get_data_names(choice):
    '''
    returns
    '''
    r = requests.get(f"https://swapi.dev/api/{choice.lower()}/")
    namelist = []
    number_of_results = r.json()["count"]
    dict_of_results = {}
    for i in range(number_of_results):
        try:
            r_i = requests.get(f"https://swapi.dev/api/{choice.lower()}/{i+1}/")
            if choice == 'Films':
                print(r_i.json()['title'])
                namelist.append(r_i.json()['title'])
                dict_of_results[r_i.json()['title']] = r_i.json()
            else:
                namelist.append(r_i.json()['name'])
                dict_of_results[r_i.json()['name']] = r_i.json()
        except:
            pass
    return number_of_results,namelist, dict_of_results


def request_list(url_list):

    if url_list == []:
        return url_list
    try:
        requested_info = []
        for url in url_list:
            if re.search('\/films\/',url):
                requested_info.append(requests.get(url).json()['title'])
            else:
                requested_info.append(requests.get(url).json()['name'])
        print(requested_info)
        return requested_info
    except:
        return url_list

def request_url(url):
        if re.search('https',url) and re.search('\/films\/',url):
            try:
                result = requests.get(url).json()['title']
                return result
            except:
                pass
        elif re.search('https',url):
            try:
                result = requests.get(url).json()['name']
                return result
            except:
                pass
        else:
            return url

@st.experimental_memo
def update_url_infos_regex(df):

    return df.iloc[:,0].apply(lambda x: ", ".join(request_list(x)) if type(x)==list else request_url(str(x)))
