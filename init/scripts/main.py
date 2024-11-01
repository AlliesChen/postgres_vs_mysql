import pandas as pd
import os
from db.postgres import PostgresDatabase
from db.mysql import MysqlDatabase
from data.data_resolver import DataResolver

# Retrieve environment variables
pg_host = os.getenv('PG_HOST', 'localhost')
pg_port = os.getenv('PG_PORT', 5432)
pg_name = os.getenv('PG_NAME')
pg_user = os.getenv('PG_USER')
pg_password = os.getenv('PG_PASSWORD')
pg_connection_str = f"postgresql+psycopg2://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_name}"

mysql_host = os.getenv('MYSQL_HOST', 'localhost')
mysql_port = os.getenv('MYSQL_PORT', 3306)
mysql_name = os.getenv('MYSQL_NAME')
mysql_user = os.getenv('MYSQL_USER')
mysql_password = os.getenv('MYSQL_PASSWORD')
mysql_connection_str = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_name}"

# Step 0: Initialize database
pg_db = PostgresDatabase(pg_connection_str)
mysql_db = MysqlDatabase(mysql_connection_str)
resolver = DataResolver('hotel_reservations.csv')

# Step 1: Create tables
pg_db.create_tables()
mysql_db.create_tables()

# Step 2: Populate lookup tables
meal_plans_data = resolver.get_unique_values('type_of_meal_plan')
meal_plans_data.rename(columns={'type_of_meal_plan': 'meal_plan_name'}, inplace=True)
room_types_data = resolver.get_unique_values('room_type_reserved')
room_types_data.rename(columns={'room_type_reserved': 'room_type_name'}, inplace=True)
market_segments_data = resolver.get_unique_values('market_segment_type')
market_segments_data.rename(columns={'market_segment_type': 'market_segment_name'}, inplace=True)
unique_booking_statuses_data = resolver.get_unique_values('booking_status')
unique_booking_statuses_data.rename(columns={'booking_status': 'booking_status_name'}, inplace=True)

pg_db.insert_data("meal_plans", meal_plans_data)
pg_db.insert_data("room_types", room_types_data)
pg_db.insert_data("market_segments", market_segments_data)
pg_db.insert_data("booking_statuses", unique_booking_statuses_data)
pg_db.insert_data("bookings", resolver.df)

mysql_db.insert_data("meal_plans", meal_plans_data)
mysql_db.insert_data("room_types", room_types_data)
mysql_db.insert_data("market_segments", market_segments_data)
mysql_db.insert_data("booking_statuses", unique_booking_statuses_data)
mysql_db.insert_data("bookings", resolver.df)
