"""Code for the streamlit can be found here"""

import streamlit as st
from utils.wikipedia_functions import get_random_page, check_wikipedia_pages_existence
from wikirace_functions import full_wikirace

def generate_pages(mode:str) -> None:
    if mode == "easy":
        start_page = get_random_page(1)[0]
        st.session_state.start_page = start_page
        st.session_state.end_page = "United States"
    elif mode == "hard":
        start_page, end_page = get_random_page(2)
        st.session_state.start_page = start_page
        st.session_state.end_page = end_page

def prevent_solving() -> None:
    st.session_state.solve_enabled = False

def approve_solving() -> None:
    st.session_state.solve_enabled = True


st.title("Search Agent")

if "start_page" not in st.session_state:
    st.session_state.start_page = ""
if "end_page" not in st.session_state:
    st.session_state.end_page = ""
if "n_iterations" not in st.session_state:
    st.session_state.n_iterations = "10"
if '.solve_enabled' not in st.session_state:
    st.session_state.solve_enabled = False


easy_mode_button = st.button("(Easy Mode) Random Start, End = United States")
hard_mode_button = st.button("(Hard Mode) Random Start, Random End")
if easy_mode_button:
    generate_pages("easy")
if hard_mode_button:
    generate_pages("hard")

start_page_text = st.text_input("Start Page:", value=st.session_state.start_page, on_change=prevent_solving)
end_page_text = st.text_input("End Page:", value=st.session_state.end_page, on_change=prevent_solving)
n_iterations = int(st.text_input("Number of iterations:", value=st.session_state.n_iterations))
option = st.selectbox(
    "Model choice",
    ("haiku", "sonnet", "opus"))
check_button = st.button("Check if Pages are Valid")

if check_button:
    check_text = st.empty()
    check_pages = check_wikipedia_pages_existence([start_page_text, end_page_text])
    check_values = list(check_pages.values())
    if check_values[0] == True and check_values[1] == True:
        approve_solving()
        check_text.write("Pages are valid, solving can be launched!")
    else:
        check_text.write("Pages are invalid, solving can't be launched.")

solve_button = st.button("Launch Claude-3 Solving", disabled=not st.session_state.solve_enabled)
st_text = st.container()
if solve_button:
    full_wikirace(start_page_text, end_page_text, n_iterations, model_used=option, on_streamlit=True, st_text=st_text)