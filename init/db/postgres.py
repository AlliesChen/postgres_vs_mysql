from sqlalchemy import Table, Column, Integer, String, ForeignKey
from .base import BaseDatabase

class PostgresDatabase(BaseDatabase):
    def use_foreign_keys(self) -> list[Column]:
        type_of_meal_plan = Column(
            'type_of_meal_plan', String(50),
            ForeignKey('meal_plans.meal_plan_name'), nullable=False)
        room_type_reserved = Column('room_type_reserved', String(50),
            ForeignKey('room_types.room_type_name'), nullable=False)
        market_segment_type = Column('market_segment_type', String(50),
            ForeignKey('market_segments.market_segment_name'), nullable=False)
        booking_status = Column('booking_status', String(50),
            ForeignKey('booking_statuses.booking_status_name'), nullable=False)

        return type_of_meal_plan, room_type_reserved, market_segment_type, booking_status
    def use_associate_cols(self) -> list[Column]:
        type_of_meal_plan = Column('type_of_meal_plan', String(50), nullable=False)
        room_type_reserved = Column('room_type_reserved', String(50), nullable=False)
        market_segment_type = Column('market_segment_type', String(50), nullable=False)
        booking_status = Column('booking_status', String(50), nullable=False) 

        return type_of_meal_plan, room_type_reserved, market_segment_type, booking_status

    """Define and create table specific to PostgreSQL."""
    def create_tables(self, use_foreign_keys=False) -> ValueError | None:
        if (self.engine is None):
            raise ValueError("No engine assigned")
        
        # Define lookup table for meal plans
        meal_plans = Table(
            'meal_plans', self.metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('meal_plan_name', String(50), unique=True, nullable=False),
        )

        # Define lookup table for room types
        room_types = Table(
            'room_types', self.metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('room_type_name', String(50), unique=True, nullable=False),
        )

        # Define lookup table for market segments
        market_segments = Table(
            'market_segments', self.metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('market_segment_name', String(
                50), unique=True, nullable=False),
        )

        # Define lookup table for booking statuses
        booking_statuses = Table(
            'booking_statuses', self.metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('booking_status_name', String(
                50), unique=True, nullable=False),
        )

        # Define the main bookings table with foreign keys
        bookings = Table(
            'bookings', self.metadata,
            Column('booking_id', String(10), primary_key=True),
            Column('no_of_adults', Integer, nullable=False),
            Column('no_of_children', Integer, nullable=False),
            Column('no_of_weekend_nights', Integer, nullable=False),
            Column('no_of_week_nights', Integer, nullable=False),
            Column('required_car_parking_space', Integer, nullable=False),
            Column('lead_time', Integer, nullable=False),
            Column('arrival_year', Integer, nullable=False),
            Column('arrival_month', Integer, nullable=False),
            Column('arrival_date', Integer, nullable=False),
            Column('repeated_guest', Integer, nullable=False),
            Column('no_of_previous_cancellations', Integer, nullable=False),
            Column('no_of_previous_bookings_not_canceled', Integer, nullable=False),
            Column('avg_price_per_room', Integer, nullable=False),
            Column('no_of_special_requests', Integer, nullable=False),
        )

        associated_fields = self.use_foreign_keys() if use_foreign_keys else self.use_associate_cols()
        for col in associated_fields:
            bookings.append_column(col)

        # Create all tables in the database
        self.metadata.create_all(self.engine) 
