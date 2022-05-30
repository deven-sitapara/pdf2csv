import json
import sys
import boto3
from pprint import pprint
import pandas as pd
from start_doc_analysis_for_table_extraction import load_aws_config


# reference :
# https://docs.aws.amazon.com/textract/latest/dg/examples-export-table-csv.html
# https://github.com/aws-samples/amazon-textract-code-samples/blob/master/python/12-pdf-text.py#L59


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
# response_blocks = GetResults(jobId, file_name)

def main():
    print(jobId)
    page_lines = process_response(jobId)

    csv_key_name = f"{jobId}.csv"
    df = pd.DataFrame(page_lines.items())
    df.columns = ["PageNo", "Text"]
    # df.to_csv(f"./csv/{csv_key_name}", index=False)
    df.to_csv(file_name, index=False)
    print(df)
    return {"statusCode": 200, "body": json.dumps("File converted successfully!")}


# def upload_to_s3(filename, bucket, key):
#     s3 = boto3.client("s3")
#     s3.upload_file(Filename=filename, Bucket=bucket, Key=key)


def process_response(job_id):

    textract = boto3.client('textract', region_name=config["region_name"])

    maxResults = 1000
    paginationToken = None
    finished = False

    response = {}
    pages = []

    # response = textract.get_document_text_detection(JobId=job_id)
    response = textract.get_document_analysis(JobId=jobId, MaxResults=maxResults)
    pages.append(response)

    nextToken = None
    if "NextToken" in response:
        nextToken = response["NextToken"]

    while nextToken:
        response = textract.get_document_analysis(JobId=jobId, MaxResults=maxResults,
                                                           NextToken=nextToken)
        # response = textract.get_document_text_detection(
        #     JobId=job_id, NextToken=nextToken
        # )
        pages.append(response)
        nextToken = None
        if "NextToken" in response:
            nextToken = response["NextToken"]

    page_lines = {}
    for page in pages:
        for item in page["Blocks"]:
            if item["BlockType"] == "TABLE":
                if item["Page"] in page_lines.keys():
                    page_lines[item["Page"]].append(item["Text"])
                else:
                    page_lines[item["Page"]] = []
    return page_lines

if __name__ == "__main__":
    main()
