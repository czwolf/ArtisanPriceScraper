import streamlit as st
from Scraper import Scraper
from pages.modules.url_list import UrlList

st.set_page_config(layout="wide")

if __name__ == '__main__':
    st.write("## Přehled")
    st.write("---")
    if Scraper.check_data_length(Scraper.CSVPATH) != 0:
        st.plotly_chart(Scraper.plot_scraped_data(Scraper.CSVPATH))
    else:
        st.warning("Soubor scraped_data.csv neobsahuje žádná data.")
    st.write("---")
    st.write("#### Detail produktu")
    option = st.selectbox("Detail produktu", options=UrlList.get_product_list(UrlList.PATH),
                          placeholder="Vyberte produkt...", index=None)
    if option:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Aktuální cena", Scraper.get_current_product_price(Scraper.CSVPATH, option), Scraper.get_delta_product_price(Scraper.CSVPATH, option))
            if Scraper.get_delta_product_price(Scraper.CSVPATH, option) < 0:
                st.write(f"Aktuální cena se snížila o {abs(Scraper.get_delta_product_price(Scraper.CSVPATH, option))}Kč")
            elif Scraper.get_delta_product_price(Scraper.CSVPATH, option) > 0:
                st.write(f"Aktuální cena se zvýšila o {Scraper.get_delta_product_price(Scraper.CSVPATH, option)}Kč")
            else:
                st.write(f"Aktuální cena se od minule nezměnila.")
        with col2:
            st.metric("Nejvyšší cena", Scraper.get_max_product_price(Scraper.CSVPATH, option))
        with col3:
            st.metric("Nejnižší cena", Scraper.get_min_product_price(Scraper.CSVPATH, option))
        with col4:
            st.metric("Průměrná cena", Scraper.get_average_product_price(Scraper.CSVPATH, option))

    st.write("---")
    if st.toggle("Ukázat tabulku dat"):
        st.write(Scraper.show_scraped_data(Scraper.CSVPATH))
