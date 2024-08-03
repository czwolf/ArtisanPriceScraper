import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import csv
from pages.modules.url_list import UrlList
import plotly.express as px


class Scraper:
    """
    Price scraper for artisan.cz website
    """

    CSVPATH = "scraped_data.csv"
    COLUMNS = ["date", "product", "price"]

    @classmethod
    def check_csv_exists(cls):
        """
        Check if the file for saving scraped data exists.
        If not, it creates csv file with header row.
        :return: csv file
        """
        try:
            pd.read_csv(cls.CSVPATH, sep=";")
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSVPATH, sep=";", index=False)

    @classmethod
    def scrape_data(cls, product_name: str, url: str) -> dict:
        """
        It scrapes prices from artisan.cz for selected product
        :param product_name: you choose product name manualy
        :param url: url from artisan.cz
        :return: dict with date, product name and price
        """
        r = requests.get(url)
        html_data = BeautifulSoup(r.text, "html.parser")
        price_text = html_data.find("span", id="product_price_with_tax").text
        price_text = price_text.replace(",", ".")
        price = round(float(price_text), 2)
        today = datetime.today().strftime("%d.%m.%Y")
        return {"date": today, "product": product_name, "price": price}

    @classmethod
    def save_scraped_data_to_csv(cls, scraped_data_csv: str) -> None:
        """
        It iterate over csv file with products for which you want scrape data
        :param scraped_data_csv: str - file name of csv file with product names and urls
        """
        with open(scraped_data_csv, 'r', encoding='utf-8') as csv_file:
            data = csv.reader(csv_file, delimiter=';', dialect='excel')
            data = iter(data)
            next(data)
            for row in data:
                name = row[0]
                url = row[1]
                scraped_data = Scraper.scrape_data(name, url)
                with open(cls.CSVPATH, 'a', encoding='utf-8', newline='') as scraped_data_file:
                    writer = csv.DictWriter(scraped_data_file, Scraper.COLUMNS, delimiter=';')
                    file_empty = scraped_data_file.tell() == 0
                    if file_empty:
                        writer.writeheader()
                    writer.writerow(scraped_data)
                    print(f"{scraped_data}: row saved")

    @classmethod
    def remove_duplicity_from_scraped_data(cls, scraped_data_csv: str):
        """
        Method removes duplicity data from csv file with scraped data.
        :param scraped_data_csv: str
        :return: pd.Dataframe or str
        """
        try:
            df = pd.read_csv(scraped_data_csv, sep=";")
            df.drop_duplicates(subset=["date", "product"], inplace=True)
            df.to_csv(cls.CSVPATH, sep=";", index=False)
        except FileNotFoundError:
            return "File not found"

    @classmethod
    def show_scraped_data(cls, scraped_data_csv: str):
        """
        Method returns dataframe with scraped data.
        :param scraped_data_csv: str
        :return: pd.Dataframe or str
        """
        try:
            df = pd.read_csv(scraped_data_csv, sep=";")
            pivot = pd.pivot_table(data=df, index="date", columns="product", values="price", fill_value=0)
            return pivot
        except FileNotFoundError:
            return "File not found"


    @classmethod
    def delete_unwanted_scraped_data(cls, product_name: str, scraped_data_csv: str):
        """
        Method delete unwanted product from scraped data.
        :param scraped_data_csv: str
        :param product_name: str
        :return: pd.Dataframe or str
        """
        try:
            df = pd.read_csv(scraped_data_csv, sep=";")
            product_df = df.loc[df["product"] != product_name]
            product_df.to_csv(Scraper.CSVPATH, sep=";")
        except FileNotFoundError:
            return "File not found"


    @classmethod
    def check_data_length(cls, scraped_data_csv: str):
        """
        Check if scraped_data.csv contains data
        """
        try:
            df = pd.read_csv(scraped_data_csv, sep=";")
            return len(df)
        except FileNotFoundError:
            return "File not found"

    @classmethod
    def plot_scraped_data(cls, scraped_data_csv: str):
        """
        Method prepares graph for drawing on the streamlit site.
        :param scraped_data_csv: str
        :return: plot or str
        """
        try:
            df = pd.read_csv(scraped_data_csv, sep=";")
            df['date'] = pd.to_datetime(df['date'], dayfirst=True)
            pivot = df.pivot_table(index='date', columns='product', values='price', aggfunc='last')
            cols = pivot.columns.tolist()
            fig = px.line(pivot, x=pivot.index, y=cols, title='Vývoj ceny produktů v čase')
            fig.update_layout(
                xaxis_title="Datum",
                yaxis_title="Cena"
            )
            return fig
        except FileNotFoundError:
            return "File not found"

    @classmethod
    def get_max_product_price(cls, csv_file: str, product_name: str) -> float:
        """
        Get historically maximal product's price
        :param csv_file: str
        :param product_name: str
        :return: float
        """
        try:
            df = pd.read_csv(csv_file, sep=";")
            product = df.loc[df["product"] == product_name]
            max_price = float(product.price.max())
            return max_price
        except FileNotFoundError:
            return "File not found."

    @classmethod
    def get_min_product_price(cls, csv_file: str, product_name: str) -> float:
        """
        Get historically minimal product's price
        :param csv_file: str
        :param product_name: str
        :return: float
        """
        try:
            df = pd.read_csv(csv_file, sep=";")
            product = df.loc[df["product"] == product_name]
            min_price = float(product.price.min())
            return min_price
        except FileNotFoundError:
            return "File not found."

    @classmethod
    def get_average_product_price(cls, csv_file: str, product_name: str) -> float:
        """
        Get historically average product's price
        :param csv_file: str
        :param product_name: str
        :return: float
        """
        try:
            df = pd.read_csv(csv_file, sep=";")
            product = df.loc[df["product"] == product_name]
            avg_price = float(product.price.mean())
            return round(avg_price, 2)
        except FileNotFoundError:
            return "File not found."

    @classmethod
    def get_current_product_price(cls, csv_file: str, product_name: str) -> float:
        """
        Get current product's price
        :param csv_file: str
        :param product_name: str
        :return: float
        """
        try:
            df = pd.read_csv(csv_file, sep=";")
            product = df.loc[df["product"] == product_name]
            current_price = float(product["price"].tail(1))
            return current_price
        except FileNotFoundError:
            return "File not found."

    @classmethod
    def get_delta_product_price(cls, csv_file: str, product_name: str) -> float:
        """
        Get product's price difference between current price and previous price.
        :param csv_file: str
        :param product_name: str
        :return: float
        """
        try:
            df = pd.read_csv(csv_file, sep=";")
            product = df.loc[df["product"] == product_name]
            previous_price = product["price"].iloc[-2]
            current_price = product["price"].tail(1)
            delta = current_price - previous_price
            return float(delta)
        except FileNotFoundError:
            return "File not found."

    @classmethod
    def check_data_length(cls, csv_file: str) -> int:
        """
        Get length of dataframe
        :param csv_file: str
        :return: int
        """
        try:
            df = pd.read_csv(csv_file, sep=";")
            return len(df)
        except FileNotFoundError:
            return "File not found."


if __name__ == '__main__':
    Scraper.check_csv_exists()
    if Scraper.check_data_length(UrlList.PATH) != 0:
        Scraper.save_scraped_data_to_csv(UrlList.PATH)
        Scraper.remove_duplicity_from_scraped_data(Scraper.CSVPATH)
        Scraper.plot_scraped_data(Scraper.CSVPATH)
    else:
        print("Soubor url.csv neobsahuje žádné produkty ke sledování.")
