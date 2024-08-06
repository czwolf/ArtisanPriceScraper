import pandas as pd
import csv
import os


class UrlList:
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    CSV = "url.csv"
    PATH = os.path.join(PROJECT_ROOT, CSV)
    COLUMNS = ["name", "url"]

    @classmethod
    def check_file_exists(cls):
        try:
            pd.read_csv(cls.PATH, sep=';')
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.PATH, sep=';', index=False)

    @classmethod
    def add_product_to_list(cls, name, url):
        product = {'name': name,
                   'url': url}

        with open(cls.PATH, 'a', newline='', encoding='utf-8') as csv_writer:
            writer = csv.DictWriter(csv_writer, fieldnames=cls.COLUMNS, delimiter=';')
            file_empty = csv_writer.tell() == 0
            if file_empty:
                writer.writeheader()
            writer.writerow(product)

    @classmethod
    def show_dataframe(cls, csv_file: str):
        try:
            df = pd.read_csv(csv_file, sep=";")
            return df
        except FileNotFoundError:
            return "File not found."

    @classmethod
    def get_product_list(cls, csv_file: str) -> list:
        try:
            df = pd.read_csv(csv_file, sep=";")
            products = df["name"].tolist()
            return set(products)
        except FileNotFoundError:
            return "File not found."
