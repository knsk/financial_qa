import os

username = os.environ.get('KANPO_DATABASE_USERNAME', 'kanpo')
password = os.environ.get('KANPO_DATABASE_PASSWORD', 'kanpo')
host = os.environ.get('KANPO_DATABASE_HOST', 'localhost')
environment = os.environ.get('KANPO_APP_ENVIRONMENT', 'development')

DATABASE = {
  'drivername': 'postgresql',
  'username': username,
  'password': password,
  'host': host,
  'port': 5432,
  'database': f"kanpo_{environment}",
  'query': {}
}
