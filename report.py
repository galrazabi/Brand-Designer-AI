import os, requests
from googlerequest import *
from openairequests import *
from dotenv import load_dotenv
from embeddings import *
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Spacer
from io import BytesIO

load_dotenv()

api_key = os.getenv("STOCKS_API_KEY")


def get_cashflow_report(company: str):
    logging.info("Contacting Alpha Vantage API for cashflow")
    latest_data = {}

    try:
        url = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={company}&apikey={api_key}'
        r = requests.get(url)
        data = r.json()
        if "annualReports" in data.keys():
            latest_data = data["annualReports"][0]
        else:
            latest_data = {}
        logging.info("Contacted Alpha Vantage API for cashflow successfully")
    except:
        logging.error("Contacting Alpha Vantage API for cashflow failed")

    return latest_data

def get_company_overview(company: str):
    logging.info("Contacting Alpha Vantage API for overview")
    latest_data = {}
    try:
        url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={company}&apikey={api_key}'
        r = requests.get(url)
        data = r.json()
        if "Description" in data.keys():
            latest_data = data["Description"]
        else:
            latest_data = {}
        logging.info("Contacted Alpha Vantage API for overview successfully")
    except:
        logging.error("Contacting Alpha Vantage API for overview failed")

    return latest_data

def make_report(company: str, data: dict):
    prompt = f"""This is the annual report of the company {company}, and the description of the company logo: 
{data} 
WRITE ME A REPORT ON IT, relate to the annual report, add some key numbers and data from the annual report and relate to the logo description as well"""
    response = contact_openai(prompt)
    
    return response

def create_pdf(company, data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    story = []

    title = Paragraph(f"<b>{company}'s Similar Competitors Summary</b>", styles['Title'])
    story.append(title)

    lines = data.split('\n')
    
    for line in lines:
        if line.startswith('Company: '):
            story.append(Spacer(1, 7)) 
        data_paragraph = Paragraph(line, styles['Normal'])
        story.append(data_paragraph)
        story.append(Spacer(1, 2))  

    # Build the PDF
    doc.build(story)

    pdf_data = buffer.getvalue()
    buffer.close()

    return pdf_data


def create_report(name: str, description: str):
    companies = find_similar_companies(description)

    if companies is not None:
        buffer = BytesIO()
        
        with buffer:
            for i, company in enumerate(companies):
                overview = get_company_overview(company[2])
                cashflow_data = get_cashflow_report(company[2])
                logo_url_company = get_google_image(company[0]) 
                description_company = get_logo_description(logo_url_company)
                data = f"{overview}\n\n{cashflow_data}"
                if data != {}:
                    full_data = f"{data}\n\n{description_company}"
                    report = make_report(company[0], full_data)

                    if i != 0:
                        buffer.write(b"\n")  
                    buffer.write(f"Company: {company[0]}\n\n".encode())  
                    buffer.write(report.encode())  

            report_data = buffer.getvalue().decode('utf-8')

        if report_data.strip():
            db.update_report(name, report_data)
            logging.info("Report created successfully.")
            return report_data
        else:
            logging.error("Error creating report. No data found.")
            return None

