import pandas as pd

class DataResolver:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)

    def get_unique_values(self, column_name) -> pd.DataFrame:
        """Returns a DataFrame of unique values for a specified column."""
        return pd.DataFrame(self.df[column_name].unique(), columns=[column_name])