import httplib2
import googleapiclient.discovery
from google.oauth2.credentials import Credentials

CREDENTIALS_FILE = 'creds.json'
spreadsheet_id = '173habxrTzIwoQinsK03XLbBWYaGQLzuwV8AjIxYoaes'
credentials = Credentials.from_authorized_user_file(CREDENTIALS_FILE)
httpAuth = credentials.authorize(httplib2.Http())
service = googleapiclient.discovery.build('sheets', http=httpAuth)
#apiclient.discovery.build('sheets', 'v4', http=httpAuth)
# Пример чтения файла
values = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='A1:E10',
    majorDimension='COLUMNS'
).execute()
print(values)
