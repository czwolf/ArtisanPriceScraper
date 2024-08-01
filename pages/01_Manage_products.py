from pages.modules.url_list import UrlList
import streamlit as st

st.set_page_config(layout="wide")

UrlList.check_file_exists()

tab1, tab2 = st.tabs(['Spravovat seznam produktů', 'Přidat produkt do seznamu sledovaných'])

with tab1:
    try:
        st.write("### Seznam sledovaných produktů")
        edit_products_table = st.toggle("Editovat produkty")
        data = UrlList.show_dataframe(UrlList.PATH)
        if edit_products_table:
            st.write("#### Mazání záznamů v tabulce je nevratné")
            st.write("- **produkt který chcete smazat označte v prvním sloupci zaškrtnutím**")
            st.write("- **zmáčkněte klávesu `del` na klávesnici nebo v kontextovém menu tabulky symbol `popelnice`**")
            st.write("- **tabulku uložte tlačítkem Uložit sledované produkty**")
            df = st.data_editor(data, num_rows="dynamic")
            save = st.button("Uložit změny")
            if save:
                df.to_csv(UrlList.PATH, index=False, sep=";")
        else:
            st.dataframe(data)

    except FileNotFoundError:
        st.error('Soubor nenalezen!')

with tab2:
    st.write("### Přidat produkt")
    name = st.text_input("Název produktu")
    url = st.text_input("URL")
    save = st.button("Uložit")

    if save:
        if name and url:
            try:
                UrlList.add_product_to_list(name, url)
                st.success("Uloženo...")
            except OSError:
                st.error("Produkt se nepovedl zapsat do seznamu.")
