from googleapiclient.discovery import build
from google.oauth2 import service_account

from config.config import SERVICE_ACCOUNT_FILE, SCOPES, logger


def get_cell_formatting(spreadsheet_id, range_):
    """Gets the formatting of cells in the specified range."""

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    service = build('sheets', 'v4', credentials=credentials)

    result = service.spreadsheets().get(spreadsheetId=spreadsheet_id,
                                   ranges=range_,
                                   fields='sheets(data(rowData(values(userEnteredFormat))))'
                                   ).execute()

    return result

def get_cell_values(spreadsheet_id, range_):
    """Retrieves the values ​​of cells in the specified range."""

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    service = build('sheets', 'v4', credentials=credentials)

    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                            range=range_
                                            ).execute()

    return result


def get_table_data(spreadsheet_id: str, ranges: list) -> dict:

    cell_formatting = get_cell_formatting(spreadsheet_id, f'Sheet1!{ranges[0]}:{ranges[1]}')

    cell_values = get_cell_values(spreadsheet_id, f'Sheet1!{ranges[0]}:{ranges[1]}')

    result_list = {}
    for i, row in enumerate(cell_values['values']):

        for j, value in enumerate(row):

            cell_name = chr(ord(f'{ranges[0][0]}') + j) + str(i + int(ranges[0][1:]))


            background_color = None
            text_color = None
            if i < len(cell_formatting['sheets'][0]['data'][0]['rowData']) and \
            j < len(cell_formatting['sheets'][0]['data'][0]['rowData'][i]['values']):
                cell_format = cell_formatting['sheets'][0]['data'][0]['rowData'][i]['values'][j]
                if 'userEnteredFormat' in cell_format:
                    background_color = cell_format['userEnteredFormat'].get('backgroundColor', None)
                    text_color = cell_format['userEnteredFormat'].get('foregroundColor', None)

            logger.info(f'Ячейка: {cell_name}, текст: {value}, цвет заливки: {background_color}, цвет текста: {text_color}')
            result_list[cell_name] = [value, background_color, text_color]
    return result_list

