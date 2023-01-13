import pandas as pd
import streamlit as st
import re
from app_functions import get_data_names, update_url_infos_regex

#------------------- STYLING (test)---------------------------------------
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)

local_css("style.css")
#remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

#original_title = '<p style="font-family:Courier; color:LightGrey; font-size: 40px;">Original image</p>'
#st.markdown(original_title, unsafe_allow_html=True)
#----------------------------------------------------------

# - Sidebar - #
with st.sidebar:
    st.markdown('![Wookiee image](https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Ficons.iconarchive.com%2Ficons%2Fgoodstuff-no-nonsense%2Ffree-space%2F128%2Fchewbacca-icon.png&f=1&nofb=1&ipt=31860093d9e36704bdc26dddac54b3183fe0ab02913267d78fe9135bc2e1a38a&ipo=images)')
    wookie_mode = st.radio('Wookiee mode ?:', ['No', 'Yes'])
# ----- Logo ------ #
col1, col2, col3 = st.columns([0.4,1,0.6])

r2d2_gif_url = "https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.pekegifs.com%2Fimgotros%2Fstarwars%2F004.gif&f=1&nofb=1&ipt=77ab2a866b0854d4ee6bc1d46e6bea5c1528cb05863a27a308f6f03a4b70f4e6&ipo=images"
wookiee_gif_url = 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmedia.giphy.com%2Fmedia%2FLGFDEOFY7XAxq%2Fgiphy.gif&f=1&nofb=1&ipt=6a4acd52b078097d94e20ab03ebde0af934eb6c07d12a4a67d0672ecb2c95a17&ipo=images'
sw_logo_url = 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2F1000marcas.net%2Fwp-content%2Fuploads%2F2019%2F12%2Flogo-StarWars-320x137.png&f=1&nofb=1&ipt=3b322aaaa7f955796fc146c5b170607e50e72b4773e6a800d508af478f9867fc&ipo=images'
sw_gif_url = 'https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.civfanatics.net%2Fuploads2%2FAT-AT_Death.gif&f=1&nofb=1&ipt=24facfd7fca7e944ee363e9dc77de5a7edf51e928fd8028495a34751ea829d17&ipo=images'
##########
if wookie_mode=='Yes':
    col2.image(wookiee_gif_url,use_column_width=True)
else:
    col1.image(r2d2_gif_url, use_column_width=True)
    col2.image(sw_logo_url,use_column_width=True)
    col3.image(sw_gif_url)
##########
# ----- Title ------ #
st.markdown(' ')
st.markdown(' ')

if wookie_mode == 'Yes':
    st.title("WWOOAARDDSFGR NNNNNNROAR")
#else:
#    st.title("Star Wars Interface")

st.subheader("what type of data are you looking for young Padawan ?")

# ----- Selectbox ------ #
sw_selection = st.selectbox('select a data',['Films','People','Starships','Vehicles','Species','Planets'])

n_results,name_list, all_list = get_data_names(sw_selection)

st.write(f"number of {sw_selection} found: {n_results}")

st.write(f"Which one ?")

# ----- Input Form ----- #
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
