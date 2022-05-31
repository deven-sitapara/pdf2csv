import json
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
    

    # clear content of csv_file
    f = open(file_name,"w")
    f.close()
    
    output_csv_file = file_name

    # Just for debugging use json file
    # output_json_file = file_name.replace("csv","json") 
    # print(output_json_file)

    # csv_file = file_name.replace("csv","json") 
    # # f = open( csv_file , "wt")
    # # f.write("[")
    # # f.close()
    # output_file = file_name

    # f = open('./json/AF_Dealer_Pricelist_072020_w copy.json')
    # blocks = json.load(f)
    # print(type(blocks))
    # table_csv = get_table_csv_results(blocks)
    # print(table_csv)



    # print(csv_file)
    # # Opening JSON file
    # f = open(csv_file)
    # # returns JSON object as 
    # # a dictionary
    # blocks = json.load(f)
    # table_csv = get_table_csv_results(blocks)
    # print(table_csv)
    # with open(output_file, "at") as fout:
    #     fout.write(table_csv)
    # exit()

    response_block_list = []

    while finished == False:

        response = None

        if paginationToken == None:
            response = textract.get_document_analysis(JobId=jobId)
        else:
            response = textract.get_document_analysis(JobId=jobId,NextToken=paginationToken)
 
        response_blocks = response['Blocks']    # list 

        # remove Geometry field from response_blocks
        for json_res in response_blocks:
            del json_res['Geometry']

        # if response_block_list == []:    
        #     response_block_list = response_blocks
        # else:
        #     response_block_list.append(response_blocks) 

        response_block_list.append(response_blocks) 


        # show the results
        # print('Detected Document Text')
        # print('Pages: {}'.format(response['DocumentMetadata']['Pages']))
        # print('OUTPUT TO CSV FILE: ', output_file)

        # Display block information
        # for block in blocks:
        #     DisplayBlockInfo(block)
        #     print()
        #     print()

        if 'NextToken' in response:
            paginationToken = response['NextToken']
        else:
            finished = True    

    # Convert list to json and write in json file 
    # f = open(output_json_file , "wt")
    # response_block_json_serialized = json.dumps(response_block_list,indent=4)
    # f.write(response_block_json_serialized)
    # f.close()
    # response_block_json = json.loads(response_block_json_serialized)    # obj now contains a dict of the data
    # print(type(response_block_list))
    # exit()
    converted_table_csv = get_table_csv_results( response_block_list)
    with open(output_csv_file, "at") as csv:
        csv.write(converted_table_csv)



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
                except KeyError as e:
                    print("Error extracting Table data in col map - {}:".format(e.args))
                    pass
    return rows

def get_text(result, blocks_map):
    text = ''
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    if child_id not in blocks_map:
                        print("Page:",  result["Page"] , ", Error extracting Table data in get text - {}:".format(child_id))
                        # print("blocks_map:",  blocks_map)
                        # print("result:",  result)
                        # exit()
                    else:
                        word = blocks_map[child_id]
                        if word['BlockType'] == 'WORD':
                            text += word['Text'] + ' '
                        if word['BlockType'] == 'SELECTION_ELEMENT':
                            if word['SelectionStatus'] =='SELECTED':
                                text +=  'X '    
    return text

def get_text__(result, blocks_map):
    text = ''
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    try:

                        if child_id not in blocks_map:
                            print("Page - {}".format(result["Page"]))
                            print("Error extracting Table data in get text - {}:".format(child_id))
                        else:
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


def get_table_csv_results(response_block_list):

    # pprint(blocks)

    blocks_map = {}
    table_blocks = []
    csv = ''
    for blocks in response_block_list:
        for block in blocks:
            blocks_map[block['Id']] = block
            if block['BlockType'] == "TABLE":
                table_blocks.append(block)

        if len(table_blocks) <= 0:
            return "<b> NO Table FOUND </b>"

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
