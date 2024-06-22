import streamlit as st
from streamlit_option_menu import option_menu
import pags.logs, pags.requests, pags.profileSpider, pags.collectionSpider

st.set_page_config(
    page_title="Logs"
)

class MultiApp:
    def __init__(self) -> None:
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run():
        with st.sidebar:
            app = option_menu(
                menu_title="DiscoData",
                options=[
                    'Bot Logs',
                    # "Requests",
                    # "Profile Spider",
                    # "Collection Spider"
                ],
                default_index=1,
                styles={
                "container": {"padding": "4!important","background-color":'black'},
                "icon": {"color": "white", "font-size": "23px"}, 
                "nav-link": {"color":"white","font-size": "18px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
                "nav-link-selected": {"background-color": "#02ab21", "font-size": "18px"},
                }
            )
        if app == "Bot Logs":
            pags.logs.app()
        # if app == "Requests":
        #     pags.requests.app()  
        # if app == "Profile Spider":
        #     pags.profileSpider.app()  
        # if app == "Collection Spider":
        #     pags.collectionSpider.app()

    run()      