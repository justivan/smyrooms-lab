from datetime import date, datetime

from sqlalchemy import MetaData, Table, and_, create_engine, func, or_, select
from sqlalchemy.orm import Session

from config import Config


class Database:
    TABLES = [
        "reports_bookingsfinancialdata",
        "reports_bookingsinitialvalues",
        "reports_specificstopsalesrules",
        "reports_hotelsfinancials",
        "reports_clientsrules",
        "clients_credential",
        "hotel_hotel",
        "hotel_chain",
        "hotel_provider",
    ]

    def __init__(self):
        self.engine = create_engine(Config.DB_CCENTER)
        self.metadata = MetaData()

        self.load_tables()

    def load_tables(self):
        for table_name in self.TABLES:
            setattr(
                self,
                table_name,
                Table(
                    table_name,
                    self.metadata,
                    autoload_with=self.engine,
                ),
            )