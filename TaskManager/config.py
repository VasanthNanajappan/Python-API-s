 #Secret key that will be used by Flask for securely signing the session cookie
 # and can be used for other security related needs
SECRET_KEY = 'SECRET_KEY'
 #Webhook endpoint Mapping to the listener
WEBHOOK_RECEIVER_URL = 'http://localhost:5001/consumetasks'
 #Map to the REDIS Server Port
BROKER_URL = 'redis://localhost:6379'
MIN_NBR_TASKS=2
MAX_NBR_TASKS = 10
WAIT_TIME = 1
