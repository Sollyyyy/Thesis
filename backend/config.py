import os
# should be env variables
SECRET_KEY = 'cf1c7f5f8500ce42346b06f2abb815e18409f787e1e69c3209816e7daa241792'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
FLIGHT_API_KEY = os.getenv('FLIGHT_API_KEY', '69efaa78b2bcf0b803ec6fb9')
#  69f0e637276f54b7f4206a3f

MYSQL_HOST = os.getenv('MYSQL_HOST', '127.0.0.1')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', '3306'))
MYSQL_USER = os.getenv('MYSQL_USER', 'tripplanner')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'tripplanner123')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'tripplanner')
