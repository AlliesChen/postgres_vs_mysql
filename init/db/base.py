import time
from sqlalchemy import MetaData, create_engine, Engine
from sqlalchemy.exc import OperationalError

class BaseDatabase:
    def __init__(self, db_url):
        self.engine = self.create_conn(db_url, retry=5, wait_time=5)
        self.metadata = MetaData()
    
    def create_tables(self):
        """Method to be overridden by subclasses to define specific tables."""
        raise NotImplementedError("Subclasses should implement create_tables")

    def insert_data(self, table, data):
        """Generic data insertion method."""
        data.to_sql(table, self.engine, if_exists='append', index=False)
    
    def create_conn(self, db_url, retry=1, wait_time=5) -> None | Engine:
        print(f"create engine for url: {db_url}")
        engine = create_engine(db_url)
        conn = None
        while not conn and retry > 0:
            retry -= 1
            try:
                conn = engine.connect()
                print("Database connection successful!")
            except OperationalError as e:
                print(f"Database connection failed: {e}\n {retry} times left")
                time.sleep(wait_time)

        return engine
