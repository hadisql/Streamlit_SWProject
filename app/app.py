import pandas as pd
import requests
import streamlit as st
import re

#----------------------------------------------------------
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)

local_css("style.css")
#remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

#icon("search")
#selected = st.text_input("", "Search...")
#button_clicked = st.button("OK")
original_title = '<p style="font-family:Courier; color:LightGrey; font-size: 40px;">Original image</p>'
#st.markdown(original_title, unsafe_allow_html=True)
#----------------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')

with col2:
    st.markdown('![SW logo](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftoppng.com%2Fpublic%2Fuploads%2Fthumbnail%2Fstar-wars-gold-vector-logo-free-115740376030qixhwp63f.png&f=1&nofb=1&ipt=7ceb09a8de4e4f640ae0707180d6348274e5fa91ce4023ad7319e3e451b89160&ipo=images)')

with col3:
    st.write(' ')

st.title("Star Wars Interface")

st.subheader("what type of data are you looking for young Padawan ?")
# - Sidebar - #
with st.sidebar:
    st.markdown('![Wookiee image](https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Ficons.iconarchive.com%2Ficons%2Fgoodstuff-no-nonsense%2Ffree-space%2F128%2Fchewbacca-icon.png&f=1&nofb=1&ipt=31860093d9e36704bdc26dddac54b3183fe0ab02913267d78fe9135bc2e1a38a&ipo=images)')
    wookie_mode = st.radio('Wookiee mode ?:', ['No', 'Yes'])
# ----------- #
sw_selection = st.selectbox('select a data',['Films','People','Starships','Vehicles','Species','Planets'])

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


n_results,name_list, all_list = get_data_names(sw_selection)

st.write(f"number of {sw_selection} found: {n_results}")

st.write(f"Which one ?")

with st.form("Input"):
    input = st.text_input('For what you are looking for, you may type :', max_chars=30)
    update_with_names = st.checkbox('update url info with names (takes more time to run)')
    btnResult = st.form_submit_button('Search',)

def search_name(input):
    display_result_names = []
    for name in name_list:
        if re.search(f'{input.lower()}|{input.upper()}|{input.capitalize()}',name):
            display_result_names.append(name)
    return display_result_names

if st.session_state['FormSubmitter:Input-Search']:

    st.markdown(f'##### **Here are your results :** \n ***{", ".join(search_name(input))}***')
    name_selection = st.selectbox(f'Which {sw_selection} result do you want to get more informations about ?',search_name(input))

    data1 = pd.DataFrame(data=all_list[name_selection].values(),
                        index=all_list[name_selection].keys()).rename({0:f"{name_selection}"},axis='columns')

    if update_with_names :
        st.table(update_url_infos_regex(data1))
    else:
        st.table(data1)

    ##############################################
#st.write(st.session_state)
