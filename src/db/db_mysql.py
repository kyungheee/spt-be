from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.dialects.mysql import insert
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")

# connection_string = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
# db = create_engine(connection_string)
# conn = db.connect()

# conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, db=MYSQL_DB)
# curs = conn.cursor(pymysql.cursors.DictCursor)

# def save_to_mysql(df, table_name):
#     df.to_sql(con=db, name=table_name,if_exists='append', index=False)

DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=MYSQL_USER,
    password=MYSQL_PASSWORD,
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    database=MYSQL_DB,
    query={"charset": "utf8mb4"}
)

engine = create_engine(
    DATABASE_URL,
    pool_recycle=3600,
    pool_pre_ping=True,
)

def create_tracks_table():
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS tracks (
        track_id VARCHAR(50) PRIMARY KEY,
        track_name VARCHAR(255) NOT NULL,
        track_uri VARCHAR(255),

        artist_id VARCHAR(50),
        artist_name VARCHAR(255),
        artist_uri VARCHAR(255),

        duration_ms INT,
        popularity INT,
        release_date DATE,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ON UPDATE CURRENT_TIMESTAMP,

        INDEX idx_popularity (popularity),
        INDEX idx_release_date (release_date),
        INDEX idx_artist_id (artist_id)
    ) CHARACTER SET utf8mb4;
    """

    with engine.begin() as conn:
        conn.execute(create_table_sql)

    print("✅ tracks 테이블 생성 완료")

def save_to_mysql(df: pd.DataFrame, table_name: str):
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=1000
    )



# from sqlalchemy.dialects.mysql import insert

# def save_tracks_ignore_duplicates(df: pd.DataFrame, table_name: str):
#     with engine.begin() as conn:
#         for _, row in df.iterrows():
#             stmt = insert(engine.table_names())
#             stmt = insert_stmt = insert(
#                 pd.io.sql.SQLTable(
#                     table_name,
#                     engine,
#                     index=False,
#                     if_exists="append"
#                 ).table
#             ).values(**row.to_dict())

#             stmt = stmt.prefix_with("IGNORE")
#             conn.execute(stmt)
