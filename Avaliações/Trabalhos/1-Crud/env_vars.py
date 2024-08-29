import os

API_SECRET_KEY = os.getenv('API_SECRET_KEY', 'cf8ec7f9-0384-45f7-a526-233b5105f577')

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'root')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'comprai')