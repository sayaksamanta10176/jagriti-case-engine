import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import requests
from datetime import datetime, timezone
from sqlalchemy import text
from config import get_engine

# Getting SQLAlchemy engine
engine = get_engine()

# Getting the connection object
conn = engine.connect()

complainant_name = input("Enter the compalinant name: ")
filing_date_start = input("Enter the filing start date (yyyy-mm-dd): ")
filing_date_end = input("Enter the filing end date (yyyy-mm-dd): ")

api_url = f"https://e-jagriti.gov.in/services/report/report/getCauseTitleListByCompany?commissionTypeId=1&commissionId=11000000&filingDate1={filing_date_start}&filingDate2={filing_date_end}&complainant_respondent_name_en={complainant_name}"
headers = {
    'Referer' : 'https://e-jagriti.gov.in/',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
}
try:
    resp = requests.get(api_url, headers=headers, timeout=5)
    data = json.loads(resp.text)
except requests.exceptions.ConnectionError as e:
    print(f"Error: A connection error occurred (e.g., DNS failure, refused connection) - {e}")
    sys.exit()
except requests.exceptions.Timeout as e:
    print(f"Error: The request timed out after 5 seconds - {e}")
    sys.exit()
except requests.exceptions.HTTPError as e:
    print(f"Error: An HTTP error occurred (e.g., 404 Not Found, 500 Server Error) - {e}")
    sys.exit()
except requests.exceptions.RequestException as e:
    print(f"Error: An unexpected requests error occurred - {e}")
    sys.exit()
except ValueError as e:
    print(f"Error: Could not decode JSON from the response - {e}")
    sys.exit()

if data:
    # print(json.dumps(data, indent=4))

    # List for inserting a row
    insert_data = []

    # List for updating an existing row
    update_data = []

    # Query to check already existing case number
    select_query = text("SELECT case_no FROM e_jagriti_cases WHERE case_no = :value")

    # Cleaning multiline texts
    def clean_multiline_text(text: str)->str:
        if text:
            cleaned_lines = [line.strip() for line in text.splitlines() if line.strip()] 
            cleaned_text = ' '.join(cleaned_lines)
            return cleaned_text
        else:
            return text
        

    for case_info in data:
        # Creating timestamp of when the record was processed
        scraped_at = datetime.now(timezone.utc)

        # Handling upsert
        result = conn.execute(select_query, {"value" : case_info.get('case_number')})
        if result.fetchone():
            case_data = {
                "respondent" : clean_multiline_text(case_info.get('respondent_name')),
                "filing_date" : case_info.get('case_filing_date'),
                "first_hearing" : case_info.get('date_of_hearing'),
                "next_hearing" : case_info.get('date_of_next_hearing'),
                "stage" : case_info.get('case_stage_name'),
                "scraped_at" : scraped_at.strftime('%Y-%m-%d %H:%M:%S+00'),
                "case_no" : case_info.get('case_number'),
            }
            update_data.append(case_data)
        else:
            case_data = {
                "case_no" : case_info.get('case_number'),
                "complainant" : clean_multiline_text(case_info.get('complainant_name')),
                "respondent" : clean_multiline_text(case_info.get('respondent_name')),
                "filing_date" : case_info.get('case_filing_date'),
                "first_hearing" : case_info.get('date_of_hearing'),
                "next_hearing" : case_info.get('date_of_next_hearing'),
                "stage" : case_info.get('case_stage_name'),
                "scraped_at" : scraped_at.strftime('%Y-%m-%d %H:%M:%S+00')
            }
            insert_data.append(case_data)

    # print("Insert Data:")
    # print(json.dumps(insert_data, indent=4))
    # print("Update Data:")
    # print(json.dumps(update_data, indent=4))

    def execute_query(query, data):
        try:
            conn.execute(query, data)
            conn.commit()
            print("Query executed and committed successfully!")
        except Exception as e:
            conn.rollback()
            print(f"Error executing query: {e}")
            sys.exit()
    
    if insert_data:
        insert_query = text("""
        INSERT INTO e_jagriti_cases (case_no, complainant, respondent, filing_date, first_hearing, next_hearing, stage, scraped_at)
        VALUES (:case_no, :complainant, :respondent, :filing_date, :first_hearing, :next_hearing, :stage, :scraped_at)
        """)
        execute_query(insert_query, insert_data)
        print(f"Successfully inserted {len(insert_data)} records")

    if update_data:
        update_query = text("""
        UPDATE e_jagriti_cases 
        SET respondent = :respondent, filing_date = :filing_date, 
        first_hearing = :first_hearing, next_hearing = :next_hearing, 
        stage = :stage, scraped_at = :scraped_at
        WHERE case_no = :case_no
        """)
        execute_query(update_query, update_data)
        print(f"Successfully updated {len(update_data)} records")

    conn.close()
else:
    print(f"No data found for complaint text :{complainant_name}")