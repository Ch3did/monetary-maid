import os

os.environ(".env")

#Nubank Data 
TAX_ID=os.environ.get('TAX_ID')
PASSWORD=os.environ.get('PASSWORD')
FOLDER_PATH=os.environ.get('FOLDER_PATH')

# PLR
PERCENTAGE_OF_INVESTMENT=os.environ.get('PERCENTAGE_OF_INVESTMENT')
PERCENTAGE_OF_BIG_SAVE=os.environ.get('PERCENTAGE_OF_BIG_SAVE')