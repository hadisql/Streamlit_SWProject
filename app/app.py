import pandas as pd
import requests
import streamlit as st
import re

st.title("Star Wars Interface")

st.subheader("what type of data are you looking for young Padawan ?")
sw_selection = st.selectbox('select a data',['People','Starships','Vehicles','Planets','Films'])

@st.cache
def get_data_names(choice):
    '''
    returns
    '''
    r = requests.get(f"https://swapi.dev/api/{choice.lower()}/")
    namelist = []
    for item in r.json().get('results'):
        if choice == 'Films':
            namelist.append(item['title'])
        else:
            namelist.append(item['name'])
    return namelist

def req_sw_list(url_list):

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

def req_sw_url(url):

        if re.search('https',url) and re.search('\/films\/',url):
            return requests.get(url).json()['title']
        elif re.search('https',url):
            return requests.get(url).json()['name']
        else:
            return url

@st.experimental_memo
def update_url_infos_regex(df):

    return df.iloc[:,0].apply(lambda x: ", ".join(req_sw_list(x)) if type(x)==list else req_sw_url(str(x)))


st.write(f"Which one ?")

name_selection = st.selectbox(f'select one of the {sw_selection}', get_data_names(sw_selection))

name_info = requests.get(f"https://swapi.dev/api/{sw_selection.lower()}/?search={name_selection}")

name_info_res = name_info.json().get('results')[0]

data1 = pd.DataFrame(data=name_info_res.values(),
                     index=name_info_res.keys()).rename({0:f"{name_selection}"},axis='columns')


update_with_names = st.checkbox('update url info with names')

if update_with_names :
    st.table(update_url_infos_regex(data1))
else:
    st.table(data1)
