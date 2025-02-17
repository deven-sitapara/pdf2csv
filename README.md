# pdf to csv

![Header](./pdf2csv-github-header-image.png)

A Python script to convert PDF files to CSV format.

## Description

This script uses the `PyPDF2` and `pandas` libraries to extract tabular data from PDF files and convert it into a CSV file. It's designed to handle PDFs that contain tables, attempting to identify and parse them effectively.

## Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/deven-sitapara/pdf2csv.git
    cd pdf2csv
    ```

2.  Create a virtual environment (recommended):

    ```bash
    python3 -m venv .venv  # or python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4 AWS integration - Credential 

```bash
    ./.aws/credentials
    [default]
    aws_access_key_id=xxxxxxxxxxxxxx
    aws_secret_access_key=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    region_name=us-east-1
    role_arn=arn:aws:iam::nnnnnnnnnnn:role/roleTopic

    [s3]
    bucket=bucketname
```
 
## Usage

```bash
python pdf2csv.py <input_pdf_file> <output_csv_file>
