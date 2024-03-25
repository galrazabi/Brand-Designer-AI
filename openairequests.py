import os
import logging
from openai import OpenAI
import requests
import db
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
logging.basicConfig(level=logging.INFO, format='%(message)s')
client = OpenAI(api_key=api_key, )

def contact_openai(prompt: str):
    logging.info("Contacting gpt-3.5-turbo")
    response = None

    try:
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user",
                "content": prompt}
            ], )
        
        response = chat_completion.choices[0].message.content
        logging.info("Contacted gpt-3.5-turbo successfully")
    except:
        logging.error("Contacting gpt-3.5-turbo Failed")

    return response


def contact_dalle(prompt: str):
    logging.info("Contacting dall-e-3")
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1, )
        image_url = response.data[0].url
        response = requests.get(image_url)
        response = response.content
        logging.info("Contacted dall-e-3 successfully")
    except:
        logging.error("Contacting dall-e-3 Failed")
        image_url, response = None, None
        
    return image_url, response


def contact_gpt4vision(prompt: str, image_url: str):
    logging.info("Contacting gpt-4-vision")
    response = None

    try:
        response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
            "role": "user",
            "content": [
                {"type": "text", "text": f"{prompt}"},
                {
                "type": "image_url",
                "image_url": {
                    "url": f"{image_url}",
                },
                },
            ],
            }
        ],
        max_tokens=300,
        )
        response = response.choices[0].message.content
        logging.info("Contacted gpt-4-vision successfully")

    except:
        logging.error("Contacting gpt-4-vision Failed")

    return response


def create_slogans(name : str, description : str):
    prompt = f"Write 5 catchy slogan for a companny name: {name}.Base your slogans on the name of the company and her description:{description}. Write only the 5 slogans and number them. Try to be short and concise."
    slogan = generate_slogans(prompt) # list of slogans

    for index, slogan in enumerate(slogan):
        db.update_slogan(name, slogan, index+1)


def generate_slogans(prompt: str):
    response = contact_openai(prompt)
    generated_list = []
    lines = response.split("\n")

    for line in lines:
        line = line.split(" ", 1)[1]
        generated_list.append(line.strip())

    return generated_list
    

def generate_new_product(prompt, number):
    _, response = contact_dalle(prompt)
        
    return response


def generate_new_logo(name : str, description : str , color: list, shape: str):

    prompt = f"Create a {shape} shaped logo for a company named {name} that {description}.Make sure to be inspired by the description. The logo is abstract and has clean lines and based only on the colors: {color}. Make the logo on white background. Create only the logo and nothing but it, and make sure to mention the company's name."
    best_logo = create_and_find_best_logo(prompt, name, description)   
    return best_logo

def generate_new_logo_by_existing_company(name : str, description : str , description_existing_company: str, color: list, shape: str):
    another_company_description = description_existing_company
    prompt = f"Create a {shape} shaped logo for a company named {name} that {description}. Try to be a bit inspired by this description as well: {another_company_description} The logo is abstract and has clean lines and based only on the colors: {color}. Make the logo on white background. Create only the logo and nothing but it, and make sure to mention the company's name."
    best_logo = create_and_find_best_logo(prompt, name, description)
    return best_logo

def create_and_find_best_logo(prompt: str, name: str, description: str):
    ratings = []
    i_max_rate = 0
    max_rate = 0

    for i in range(3):
        image_url, response = contact_dalle(prompt)
        db.insert_or_replace_logo(i, response)
        rate = get_logo_rate(description, name, image_url)
        ratings.append(rate)

    for i in range(3):
        if ratings[i] >= max_rate:
            max_rate = ratings[i]
            i_max_rate = i
        
    return db.get_logo_from_logos(i_max_rate)


def get_logo_rate(description : str ,name: str, image_url : str):
    rate = 0
    questions = [ f"Is the logo answer the description: {description}?", "There is only one object in the image with no additional objects around?", f"Is the name: {name} accuratly appears in the logo?", "Is the logo on white background?", "Is the logo has effective use of color, shape, and typography?", "Is the logo visually appealing and aesthetically pleasing?", f"Is the logo appropriate for our target market and industry where the description of the company is: {description}?", "Is logo simple and easy to understand at a glance?"]
    questions_to_show = [f"Is the logo answer the description ?", "There is only one logo in the image?", f"Is the name: {name} accuratly appears in the image?", "Does the logo have a white background?", "Is the logo has effective use of color, shape, and typography?", "Is the logo visually appealing and aesthetically pleasing?", "Is logo appropriate for our target market and industry?", "Is logo simple and easy to understand at a glance?"]
    weight = [1.5, 1.2, 1, 1.3, 1, 0.5, 0.7, 1]
    add_to_prompt =". please rate it from 1 to 10, where 1 is the lowest and 10 is the highest, try to get creative when rating the image based on my question. Dont write anything but the rate. example: 'rate: number'"

    for index, question in enumerate(questions):
        question = question + add_to_prompt
        response = contact_gpt4vision(question,image_url)
        logging.info(f"{questions_to_show[index]} - {response}")
        try:
            response = response.split(":")[1].strip()
            rate += weight[index]*int(response)
        except:
            rate += 0
    
    return rate

    
def get_logo_description(image_url : str):
    question = "describe the logo, analyze every detail in the image. Be short and concise."
    response = contact_gpt4vision(question,image_url)
    return response


def get_logo_colors(image_url : str):
    question = "What are the colors in the logo? write only the colors and nothing but it. For example: 'red, blue, green'"
    response = contact_gpt4vision(question,image_url)
    return response
    

def generate_moodboard_dalle(prompt):
    image_url, response = contact_dalle(prompt)
    
    return response



