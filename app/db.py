import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL", "")

def get_db_connection():
    """
    Cria e retorna uma conexão com o Postgres.
    Railway vai fornecer 'DATABASE_URL' como variável de ambiente.
    """
    # Caso seu Postgres exija SSL, pode usar sslmode='require'.
    return psycopg2.connect(DATABASE_URL, sslmode='require')
