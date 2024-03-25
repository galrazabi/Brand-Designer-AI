import io
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import uvicorn
from typing import List, Optional
from openairequests import *
import db
from productlogo import *
from tools import *
from report import *
from googlerequest import *
import base64
import zipfile


app = FastAPI()

class NewLogo(BaseModel):
    name: str
    description: str
    color: Optional[List[str]] = None

class NewLogoByExisting(BaseModel):
    name: str
    description: str
    name_existing_company: str

class CompanyName(BaseModel):
    name: str

@app.get("/")
def index():
    return {"Message": "Welcome to the Brand Designer !!!!"}
    

@app.post("/createlogo")
def create_logo(logo : NewLogo):
    color_list = logo.color
    if color_list == None: 
        color_list = get_random_colors()
    colors = ", ".join(color_list)
    shape = get_random_shapes()
    generated_logo = generate_new_logo(logo.name, logo.description, colors, shape) 
    db.insert_company_with_logo(logo.name, logo.description, generated_logo, colors, shape)

    return "Success"


@app.post("/createlogoinspiredbyexisting")
def create_logo(logo : NewLogoByExisting):
    logo_url_existing_company = get_google_image(logo.name_existing_company) 
    description_existing_company = get_logo_description(logo_url_existing_company)
    color_existing_company = get_logo_colors(logo_url_existing_company)
    shape = get_random_shapes()
    generated_logo = generate_new_logo_by_existing_company(logo.name, logo.description, description_existing_company, color_existing_company, shape) 
    db.insert_company_with_logo(logo.name, logo.description, generated_logo, color_existing_company, shape)

    logos = db.get_all_logo_candidates()

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        if logos:
            for i, logo in enumerate(logos):
                binary_data = base64.b64decode(logo)
                zip_file.writestr(f"logo{i}.png", binary_data)

    if zip_buffer.tell() > 0:
        zip_buffer.seek(0)
        return StreamingResponse(zip_buffer, media_type="application/zip", headers={"Content-Disposition": f"attachment; filename=logo_selection.zip"})

    return "Success"


@app.post("/createmoodboard")
def create_mood_board(company : CompanyName):

    output = "No such company"

    description = db.get_company_description(company.name)
    colors = db.get_company_colors(company.name)
    if colors and description:
        generated_mood_board = generate_moodboard_dalle(f"a mood board for a company that {description}. Use mainly the colors: {colors}")
        db.update_mood_board(company.name, generated_mood_board)
        output = "Success"
    
    return output

@app.post("/createreport")
def create_compatitors_report(company : CompanyName):

    output = "No such company"

    description = db.get_company_description(company.name)
    if description is not None:
        create_report(company.name, description)
        output = "Success"
    
    return output


@app.post("/createproducts")
def create_product(company : CompanyName):

    output = "No such company"

    description = db.get_company_description(company.name)
    if description is not None:
        create_slogans(company.name, description) 
        shape = db.get_company_shape_name(company.name)
        colors = db.get_company_colors(company.name)

        for i, product in enumerate(products):
            slogan = db.get_slogan(company.name, i+1)
            prompt = f"Create a cream colored {product} with the slogan: {slogan} on it.make sure to write the slogan, and mention the name: {company.name}. In the print on the {product} you can use only the shape {shape}. Use only the colors: {colors}. do it on white background"
            product_file = generate_new_product(prompt, i+1)
            db.update_product(company.name, product_file, i+1)
        
        tshirt_product = make_logo_shirt(company.name)
        db.update_product(company.name, tshirt_product, len(products)+1)   
        output = "Success"
    
    return output

    
@app.get("/extractoutputs/{company_name}")
def download_files(company_name: str):
    if not check_if_company_exists(company_name):
        return "No such company"

    moodboard = get_company_moodboard(company_name)
    logo = get_company_logo(company_name)
    products = get_company_products(company_name)
    report = get_report(company_name)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        if moodboard:
            binary_data = base64.b64decode(moodboard)
            zip_file.writestr("moodboard.png", binary_data)

        if logo:
            binary_data = base64.b64decode(logo)
            zip_file.writestr("selectedlogo.png", binary_data)

        if products:
            for index, product in enumerate(products):
                number = index + 1
                binary_data = base64.b64decode(product)
                zip_file.writestr(f"product{number}.png", binary_data)

        if report:
            pdf_data = create_pdf(company_name, report)
            zip_file.writestr(f"report_{company_name}.pdf", pdf_data)

    if zip_buffer.tell() > 0:
        zip_buffer.seek(0)
        return StreamingResponse(zip_buffer, media_type="application/zip", headers={"Content-Disposition": f"attachment; filename={company_name}_files.zip"})
    else:
        return "No files to download"
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)