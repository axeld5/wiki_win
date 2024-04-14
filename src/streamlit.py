"""Code for the streamlit can be found here"""

import streamlit as st
from utils.wikipedia_functions import get_random_page
from wikirace_functions import full_wikirace

def generate_pages(mode:str):
    if mode == "easy":
        start_page = get_random_page(1)[0]
        st.session_state.start_page = start_page
        st.session_state.end_page = "United States"
    elif mode == "hard":
        start_page, end_page = get_random_page(2)
        st.session_state.start_page = start_page
        st.session_state.end_page = end_page


st.title("Search Agent")

if "start_page" not in st.session_state:
    st.session_state.start_page = ""

if "end_page" not in st.session_state:
    st.session_state.end_page = ""

if "n_iterations" not in st.session_state:
    st.session_state.n_iterations = "10"

easy_mode_button = st.button("(Easy Mode) Random Start, End = United States")
hard_mode_button = st.button("(Hard Mode) Random Start, Random End")

if easy_mode_button:
    generate_pages("easy")
if hard_mode_button:
    generate_pages("hard")

start_page_text = st.text_input("Start Page:", value=st.session_state.start_page)
end_page_text = st.text_input("End Page:", value=st.session_state.end_page)
n_iterations = int(st.text_input("Number of iterations:", value=st.session_state.n_iterations))

solve_button = st.button("Launch Claude-3 Solving")

st_text = st.container()
if solve_button:
    full_wikirace(start_page_text, end_page_text, n_iterations, on_streamlit=True, st_text=st_text)