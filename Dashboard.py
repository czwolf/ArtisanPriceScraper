import streamlit as st
from Scraper import Scraper
from pages.modules.url_list import UrlList

st.set_page_config(layout="wide")

if __name__ == '__main__':
    st.write("## Sledované produkty")
    st.write("---")
    st.plotly_chart(Scraper.plot_scraped_data(Scraper.CSVPATH))
    st.write("---")
    st.write("#### Detail produktu")
    option = st.selectbox("Detail produktu", options=UrlList.get_product_list(UrlList.PATH),
                          placeholder="Vyberte produkt...", index=None)
    if option:
        st.metric("Nejvyšší cena", Scraper.get_max_product_price(Scraper.CSVPATH, option))
    st.write("---")
    if st.toggle("Ukázat tabulku dat"):
        st.write(Scraper.show_scraped_data(Scraper.CSVPATH))
