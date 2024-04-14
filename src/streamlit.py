import streamlit as st
import pandas as pd

import numpy as np
from utils.wikipedia_functions import get_random_page
from wikirace_functions import full_wikirace

def generate_pages():
    start_page = get_random_page(1)[0]
    st.session_state.start_page = start_page

st.title("Search Agent")

if "start_page" not in st.session_state:
    st.session_state.start_page = ""

if "end_page" not in st.session_state:
    st.session_state.end_page = "United States"

generate_button = st.button("Generate Pages")

if generate_button:
    generate_pages()

start_page_text = st.text_input("Start Page:", value=st.session_state.start_page)
end_page_text = st.text_input("End Page:", value=st.session_state.end_page)

solve_button = st.button("Launch Claude-3 Solving")

if solve_button:
    full_wikirace(start_page_text, end_page_text, on_streamlit=True)