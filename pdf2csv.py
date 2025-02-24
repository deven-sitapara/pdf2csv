# https://docs.aws.amazon.com/textract/latest/dg/examples-export-table-csv.html 

import configparser
from pathlib import Path
from pydoc import cli
from time import time
import webbrowser, os
import json
import boto3
import io
from io import BytesIO
import sys
from pprint import pprint
import base64


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
    
    # print('PDF loaded', file_name)
    # file_contents = Path(file_name).read_text()
    # bytes_test = file_contents # base64.b64encode(file_contents.encode("ascii"))
    # print(bytes_test)
    with open(file_name, 'rb') as file:
        img_test = file.read()
        bytes_test = bytearray(img_test)
        print('PDF loaded', file_name)

    # process using PDF bytes
    # get the results

    config = configparser.ConfigParser()
    config.read('./.aws/credentials')
    aws_access_key_id = config.get("default","aws_access_key_id")
    aws_secret_access_key = config.get("default","aws_secret_access_key")
    region_name = config.get("default","region_name")
    # print(aws_access_key_id , aws_secret_access_key , region_name)

    client = boto3.client('textract',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
     )
    

    # print(client)
    # response = client.analyze_document(Document={'Bytes': bytes_test}, FeatureTypes=['TABLES'])
    response = client.analyze_document(Document={'Bytes': bytes_test}, FeatureTypes=['TABLES'])
        # ErrorAWS Textract - UnsupportedDocumentException - PDF
        # https://stackoverflow.com/questions/60501332/aws-textract-unsupporteddocumentexception-pdf

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

    # print(os.path.basename(file_name))
    basename = os.path.basename(file_name)
    output_file = os.path.splitext(basename)[0] + ".csv"
    # print(csv_file_name)

    table_csv = get_table_csv_results(file_name)
 
    # output_file =  'output.csv'
 
    # replace content
    with open(output_file, "wt") as fout:
        fout.write(table_csv)

    # show the results
    # print('CSV OUTPUT FILE: ', output_file)


if __name__ == "__main__":
    file_name = sys.argv[1]
    main(file_name)



