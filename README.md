# pdf to csv

## Extract table and convert to csv

```
    # Works
    # ------------------------------
    # ./venv/Scripts/python ./pdf2csv.py ./pdf/table.pdf
    # ./venv/Scripts/python ./pdf2csv.py ./pdf/Audinate\ -\ DVS\ and\ Via\ Reseller\ Pricing\ -\ January\ 6\,\ 2020.pdf

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
```

## Working with asynchronous function

```
    ./venv/Scripts/python start_doc_analysis_for_table_extraction.py pdf/AF_Dealer_Pricelist_072020_w.pdf
    ./venv/Scripts/python get_doc_analysis_for_table_extraction.py c3704e90b1370a2cc5ae45ebfc96ae79d19b4fd369745c5c27abd7b1bc38e49d ./csv/AF_Dealer_Pricelist_072020_w.csv


    ./venv/Scripts/python start_doc_analysis_for_table_extraction.py pdf/Audinate\ -\ DVS\ and\ Via\ Reseller\ Pricing\ -\ January\ 6\,\ 2020.pdf
    ./venv/Scripts/python get_doc_analysis_for_table_extraction.py 9a53135474d199f2abff288d04c475649673edcb63a0aafd89e7a8e189b4e7d5 ./csv/Audinate\ -\ DVS\ and\ Via\ Reseller\ Pricing\ -\ January\ 6\,\ 2020.csv


    ./venv/Scripts/python start_doc_analysis_for_table_extraction.py pdf/af_test/AF_Dealer_Pricelist_072020_w-2.pdf
    ./venv/Scripts/python get_doc_analysis_for_table_extraction.py fb5357be2572e6b5abb1cc22aeea3c620b01722b66db3b28440f48633fa564fe ./csv/af_test/AF_Dealer_Pricelist_072020_w-2.pdf


    ./venv/Scripts/python start_doc_analysis_for_table_extraction.py pdf/af_test/AF_Dealer_Pricelist_072020_w-7.pdf
    ./venv/Scripts/python get_doc_analysis_for_table_extraction.py 7aede3bf044fd0a66c73ac2a721a547088a6cd5513d650566461255c5cfbfab3 ./csv/af_test/AF_Dealer_Pricelist_072020_w-7.pdf 

```

## Credential file format

./.aws/credentials
[default]
aws_access_key_id=xxxxxxxxxxxxxx
aws_secret_access_key=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
region_name=us-east-1
role_arn=arn:aws:iam::nnnnnnnnnnn:role/roleTopic

[s3]
bucket=bucketname

## Save new Package

```
    ./venv/Scripts/python -m pip freeze > requirements.txt

```

## Install Packages

```
    ./venv/Scripts/python  -m pip install -r requirements.txt

```
