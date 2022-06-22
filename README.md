# pdf to csv

## Extract table and convert to csv

```
    # Works
    # ------------------------------
    # ./venv/Scripts/python ./pdf2csv.py ./pdf/table.pdf
    # ./venv/Scripts/python ./pdf2csv.py ./pdf/Audinate\ -\ DVS\ and\ Via\ Reseller\ Pricing\ -\ January\ 6\,\ 2020.pdf

    # Synchronous call - NOT WORKING
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
    ./venv/Scripts/python process_pdf.py ./pdf/AF_Dealer_Pricelist_072020_w.pdf ./csv/AF_Dealer_Pricelist_072020_w.csv


    ./venv/Scripts/python start_doc_analysis_for_table_extraction.py pdf/AF_Dealer_Pricelist_072020_w.pdf
    ./venv/Scripts/python get_doc_analysis_for_table_extraction.py dfa0c5cee58367aed71003fffa0a3be2d93176befe67422a890ad8c8ba57fad4 ./csv/AF_Dealer_Pricelist_072020_w.csv


    ./venv/Scripts/python start_doc_analysis_for_table_extraction.py pdf/Audinate\ -\ DVS\ and\ Via\ Reseller\ Pricing\ -\ January\ 6\,\ 2020.pdf
    ./venv/Scripts/python get_doc_analysis_for_table_extraction.py 06dbdee7cc03cfa2239a8c7e6b49da595574d9d4f86956b74ee2445496ac3a80 ./csv/Audinate\ -\ DVS\ and\ Via\ Reseller\ Pricing\ -\ January\ 6\,\ 2020.csv

    ./venv/Scripts/python start_doc_analysis_for_table_extraction.py pdf/AVR\ Pricelist\ -\ Roland\ Jan\ 24th\ 2022.pdf
    ./venv/Scripts/python get_doc_analysis_for_table_extraction.py 325a21718a35edff81b2374eb7b8a5b15ba591d6f3c250c6333e03527eed70b1 ./csv/AVR\ Pricelist\ -\ Roland\ Jan\ 24th\ 2022.csv

    ./venv/Scripts/python start_doc_analysis_for_table_extraction.py pdf/Commercial_Price_List_10-20_Dlr.pdf
    ./venv/Scripts/python get_doc_analysis_for_table_extraction.py 8a498a40407ad9c01843f185dfd81ecfcbf487604b91f2b501c433d89eb1de35 csv/Commercial_Price_List_10-20_Dlr.csv

    ./venv/Scripts/python start_doc_analysis_for_table_extraction.py pdf/Danley\ -\ Jericho\ Dealer\ Price\ List\ -\ June\ 21\,\ 2019.pdf
    ./venv/Scripts/python get_doc_analysis_for_table_extraction.py 6a06646ef95250115ab0a328e204129aa0c9254372113c7a30d7eac2175389b1 csv/Danley\ -\ Jericho\ Dealer\ Price\ List\ -\ June\ 21\,\ 2019.csv

    ./venv/Scripts/python start_doc_analysis_for_table_extraction.py pdf/Dante\ Domain\ Manager\ Aug\ 2021.pdf
    ./venv/Scripts/python get_doc_analysis_for_table_extraction.py 01f2cebc158c0ae08100d22fd0657be2f02a4108691ded3b35eb22d7a3849fda csv/Dante\ Domain\ Manager\ Aug\ 2021.csv

    ./venv/Scripts/python start_doc_analysis_for_table_extraction.py pdf/DenonPro_USDealer_April_1_2022.pdf
    ./venv/Scripts/python get_doc_analysis_for_table_extraction.py 52d0187e0133aa2b2c4218b5ccd78a12b5eaadda3b91366bbcd9f885222339a7 csv/DenonPro_USDealer_April_1_2022.csv

    ...

    ./venv/Scripts/python start_doc_analysis_for_table_extraction.py pdf/DiGiCo\ Dealer\ Price\ 12-1-2021-v2\ .pdf
    ./venv/Scripts/python get_doc_analysis_for_table_extraction.py ad92100a32af1188d1c2314d9f5142b3909d16f43ea5675b78201398d057bc89 csv/DiGiCo\ Dealer\ Price\ 12-1-2021-v2\ .csv

    ./venv/Scripts/python start_doc_analysis_for_table_extraction.py pdf/DPI\ Master\ Price\ List\ -\ CAV\ DEALER\ -\ FINAL\ -\ CLEAN\ -\ August\ 16\,\ 2021\ -\ FOR\ DISTRIBUTION.pdf

    ./venv/Scripts/python get_doc_analysis_for_table_extraction.py c19ee256e11c934a82dcbe4804a1648ef1aea39ab0c33caf33b357af16065d12 csv/DPI\ Master\ Price\ List\ -\ CAV\ DEALER\ -\ FINAL\ -\ CLEAN\ -\ August\ 16\,\ 2021\ -\ FOR\ DISTRIBUTION.csv



```

## Testing AF Dealer

```
    ./venv/Scripts/python start_doc_analysis_for_table_extraction.py pdf/AVR\ Pricelist\ -\ Roland\ Jan\ 24th\ 2022.pdf
    ./venv/Scripts/python get_doc_analysis_for_table_extraction.py 325a21718a35edff81b2374eb7b8a5b15ba591d6f3c250c6333e03527eed70b1 ./csv/AVR\ Pricelist\ -\ Roland\ Jan\ 24th\ 2022.csv


    ./venv/Scripts/python start_doc_analysis_for_table_extraction.py pdf/AF_Dealer_Pricelist_072020_w.pdf
    ./venv/Scripts/python get_doc_analysis_for_table_extraction.py 57354ddb40af9c0b7ae48d8af078bbeb7e209c2f5fd738171f47ad0f6d9b453b ./csv/AF_Dealer_Pricelist_072020_w.csv

    ./venv/Scripts/python start_doc_analysis_for_table_extraction.py pdf/af_test/AF_Dealer_Pricelist_072020_w-2.pdf
    ./venv/Scripts/python get_doc_analysis_for_table_extraction.py ae782a828a744404a76fd2555231fe6aaf71b06b444f5a5d1cac221bed2e9a70 ./csv/af_test/AF_Dealer_Pricelist_072020_w-2.pdf


    ./venv/Scripts/python start_doc_analysis_for_table_extraction.py pdf/af_test/AF_Dealer_Pricelist_072020_w-7.pdf
    ./venv/Scripts/python get_doc_analysis_for_table_extraction.py c8ccabde3e4e88f6642500ed9b4accf7685a13eb00d3ba5ba10f2cb9d897d67a ./csv/af_test/AF_Dealer_Pricelist_072020_w-7.csv


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

## Activate venv

```
    source ./venv/Scripts/activate

```

## Save new Package

```
    ./venv/Scripts/python -m pip freeze > requirements.txt

```

## Install / Uninstall Packages

```
    chmod -R 0775 /opt/bitnami/apache/htdocs_dev/pdf2csv/
    pip install -r ./requirements.txt
    ./venv/Scripts/pip install -r requirements.txt
    rm -rf ./venv/Lib/site-packages/*
    ./venv/Scripts/python  -m pip uninstall -r  requirements.txt -y

```

## Test case

```
    ./venv/Scripts/python  -m  unittest -v ./test/sample_test.py

```
