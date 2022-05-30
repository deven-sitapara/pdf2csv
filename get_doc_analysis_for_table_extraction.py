import sys
import boto3
from pprint import pprint

from start_doc_analysis_for_table_extraction import load_aws_config


# reference :
# https://docs.aws.amazon.com/textract/latest/dg/examples-export-table-csv.html
#  https://github.com/aws-samples/amazon-textract-code-samples/blob/master/python/12-pdf-text.py#L59


# jobId = '9a1bf2b3a3a495a9a465e8c9bad6ca55d3a30d5fe07d4ec027e490a44481f1e4'
# # region_name = 'region-name'
# file_name = "output-file-name.csv"

jobId = sys.argv[1]
file_name = sys.argv[2]

config = load_aws_config()

# textract = boto3.client('textract', region_name=config["region_name"])

# jobId = '189ed0fab5f89cf889c78db66970a957ee90f8125bc775c28a4e37be5d0091eb'
# region_name = 'us-east-1'
# textract = boto3.client('textract', region_name=region_name)

# jobId = 'job-id'
# region_name = 'region-name'
# file_name = "output-file-name.csv"
# textract = boto3.client('textract', region_name=region_name)
textract = boto3.client('textract', region_name=config["region_name"])

# Display information about a block
def DisplayBlockInfo(block):
    print("Block Id: " + block['Id'])
    print("Type: " + block['BlockType'])
    if 'EntityTypes' in block:
        print('EntityTypes: {}'.format(block['EntityTypes']))

    if 'Text' in block:
        print("Text: " + block['Text'])

    if block['BlockType'] != 'PAGE':
        print("Confidence: " + "{:.2f}".format(block['Confidence']) + "%")

def GetResults(jobId, file_name):
    maxResults = 1000
    paginationToken = None
    finished = False

    # Mode	Description
    # 'r'	Open a file for reading. (default)
    # 'w'	Open a file for writing. Creates a new file if it does not exist or truncates the file if it exists.
    # 'x'	Open a file for exclusive creation. If the file already exists, the operation fails.
    # 'a'	Open for appending at the end of the file without truncating it. Creates a new file if it does not exist.
    # 't'	Open in text mode. (default)
    # 'b'	Open in binary mode.
    # '+'	Open a file for updating (reading and writing)

    # https://thepythonguru.com/python-how-to-read-and-write-csv-files/
    

    # clear content of a file 
    f = open(file_name,"w")
    f.close()

    f = open( file_name.replace("csv","json") , "wt")
    f.close()

    while finished == False:

        response = None

        if paginationToken == None:
            response = textract.get_document_analysis(JobId=jobId, MaxResults=maxResults)
        else:
            response = textract.get_document_analysis(JobId=jobId, MaxResults=maxResults,
                                                           NextToken=paginationToken)
 
        f = open( file_name.replace("csv","json") , "at")
        f.write(str(response['Blocks']))
        f.close()

        blocks = response['Blocks']
        table_csv = get_table_csv_results(blocks)
        output_file = file_name
        # replace content
        with open(output_file, "at") as fout:
            fout.write(table_csv)
        # show the results
        print('Detected Document Text')
        print('Pages: {}'.format(response['DocumentMetadata']['Pages']))
        print('OUTPUT TO CSV FILE: ', output_file)

        # Display block information
        # for block in blocks:
        #     DisplayBlockInfo(block)
        #     print()
        #     print()

        if 'NextToken' in response:
            paginationToken = response['NextToken']
        else:
            finished = True


def get_rows_columns_map(table_result, blocks_map):

    rows = {}
    for relationship in table_result['Relationships']:
        if relationship['Type'] == 'CHILD':
            for child_id in relationship['Ids']:
                try:
                    cell = blocks_map[child_id]
                    if cell['BlockType'] == 'CELL':
                        row_index = cell['RowIndex']
                        col_index = cell['ColumnIndex']
                        if row_index not in rows:
                            # create new row
                            rows[row_index] = {}

                        # get the text value
                        rows[row_index][col_index] = get_text(cell, blocks_map)
                except KeyError:
                    print("Error extracting Table data in col map - {}:".format(KeyError))
                    pass
    return rows


def get_text(result, blocks_map):
    text = ''
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    try:
                        word = blocks_map[child_id]
                        # if word['BlockType'] == 'WORD' : 
                        if 'Text' in word.keys(): 
                            text += word['Text'] + ' '
                        if word['BlockType'] == 'SELECTION_ELEMENT':
                            if word['SelectionStatus'] == 'SELECTED':
                                text += 'X '
                    except KeyError as e:
                        print("Page - {}".format(result["Page"]))
                        print(child_id)
                        print("Error extracting Table data in get text - {}:".format(e.args))

    return text


def get_table_csv_results(blocks):

    # pprint(blocks)

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
        # print(index + 1)
        csv += generate_table_csv(table, blocks_map, index + 1)
        csv += '\n\n'

    return csv


def generate_table_csv(table_result, blocks_map, table_index):
    rows = get_rows_columns_map(table_result, blocks_map)

    table_id = 'Table_' + str(table_index)

    # get cells.
    csv = 'Table: {0}\n\n'.format(table_id)

    for row_index, cols in rows.items():

        for col_index, text in cols.items():
            csv +=  '"{}"'.format(text.replace('"','""')) + ","
        csv += '\n'

    csv += '\n\n\n'
    return csv

response_blocks = GetResults(jobId, file_name)
