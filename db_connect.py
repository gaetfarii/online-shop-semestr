import psycopg2
from psycopg2.extras import DictCursor


def connect_to_db():
    conn = psycopg2.connect(database="online_sneaker_shop",
                            user="postgres",
                            password="rdy127wc",
                            host="localhost",
                            port=5432)

    return conn


def choose_model(art):
    cur = connect_to_db().cursor(cursor_factory=DictCursor)
    req = f"SELECT * FROM public.products WHERE products.product_articul = {art}"
    cur.execute(req)
    sn_models = cur.fetchone()
    return sn_models


