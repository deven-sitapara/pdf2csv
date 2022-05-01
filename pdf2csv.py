# https://docs.aws.amazon.com/textract/latest/dg/examples-export-table-csv.html 

from pydoc import cli
import webbrowser, os
import json
import boto3
import io
from io import BytesIO
import sys
from pprint import pprint


def get_rows_columns_map(table_result, blocks_map):
    rows = {}
    for relationship in table_result['Relationships']:
        if relationship['Type'] == 'CHILD':
            for child_id in relationship['Ids']:
                cell = blocks_map[child_id]
                if cell['BlockType'] == 'CELL':
                    row_index = cell['RowIndex']
                    col_index = cell['ColumnIndex']
                    if row_index not in rows:
                        # create new row
                        rows[row_index] = {}
                        
                    # get the text value
                    rows[row_index][col_index] = get_text(cell, blocks_map)
    return rows


def get_text(result, blocks_map):
    text = ''
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    word = blocks_map[child_id]
                    if word['BlockType'] == 'WORD':
                        text += word['Text'] + ' '
                    if word['BlockType'] == 'SELECTION_ELEMENT':
                        if word['SelectionStatus'] =='SELECTED':
                            text +=  'X '    
    return text


def get_table_csv_results(file_name):

    with open(file_name, 'rb') as file:
        img_test = file.read()
        bytes_test = bytearray(img_test)
        print('PDF loaded', file_name)

    # process using PDF bytes
    # get the results
    client = boto3.client('textract',
        aws_access_key_id='AKIASGQTMRYOSSJB4DK7',
        aws_secret_access_key='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',
        region_name='us-east-1'
     )
    

    # print(client)
    response = client.analyze_document(Document={'Bytes': bytes_test}, FeatureTypes=['TABLES'])

    # Get the text blocks
    blocks=response['Blocks']
    pprint(blocks)

    blocks_map = {}
    table_blocks = []
    for block in blocks:
        blocks_map[block['Id']] = block
        if block['BlockType'] == "TABLE":
            table_blocks.append(block)

    if len(table_blocks) <= 0:
        return "<b> NO Table FOUND </b>"

    csv = ''
    for index, table in enumerate(table_blocks):
        csv += generate_table_csv(table, blocks_map, index +1)
        csv += '\n\n'

    return csv

def generate_table_csv(table_result, blocks_map, table_index):
    rows = get_rows_columns_map(table_result, blocks_map)

    table_id = 'Table_' + str(table_index)
    
    # get cells.
    csv = 'Table: {0}\n\n'.format(table_id)

    for row_index, cols in rows.items():
        
        for col_index, text in cols.items():
            csv += '{}'.format(text) + ","
        csv += '\n'
        
    csv += '\n\n\n'
    return csv

def main(file_name):
    table_csv = get_table_csv_results(file_name)

    output_file = 'output.csv'

    # replace content
    with open(output_file, "wt") as fout:
        fout.write(table_csv)

    # show the results
    print('CSV OUTPUT FILE: ', output_file)


if __name__ == "__main__":
    file_name = sys.argv[1]
    main(file_name)



# Works 
# ------------------------------
# ./venv/Scripts/python ./pdf2csv.py ./pdf/table.pdf 


# NOT WORKING 
# ------------------------------
# ./venv/Scripts/python ./pdf2csv.py ./pdf/Roland\ Pro\ Reseller\ \(AVR\)\ Price\ List\ -\ April\ 1\,\ 2020.pdf
# Image loaded ./pdf/Roland Pro Reseller (AVR) Price List - April 1, 2020.pdf
# Traceback (most recent call last):
#   File "D:\laragon\www\gkb_req\pricedonkey\pdf2csv\pdf2csv.py", line 118, in <module>
#     main(file_name)
#   File "D:\laragon\www\gkb_req\pricedonkey\pdf2csv\pdf2csv.py", line 104, in main
#     table_csv = get_table_csv_results(file_name)
#   File "D:\laragon\www\gkb_req\pricedonkey\pdf2csv\pdf2csv.py", line 63, in get_table_csv_results
#     response = client.analyze_document(Document={'Bytes': bytes_test}, FeatureTypes=['TABLES'])
#   File "D:\laragon\www\gkb_req\pricedonkey\pdf2csv\venv\lib\site-packages\botocore\client.py", line 415, in _api_call
#     return self._make_api_call(operation_name, kwargs)
#   File "D:\laragon\www\gkb_req\pricedonkey\pdf2csv\venv\lib\site-packages\botocore\client.py", line 745, in _make_api_call
#     raise error_class(parsed_response, operation_name)
# botocore.errorfactory.UnsupportedDocumentException: An error occurred (UnsupportedDocumentException) when calling the AnalyzeDocument operation: Request has unsupported document format       