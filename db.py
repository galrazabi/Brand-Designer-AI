import base64
import sqlite3
import logging


logging.basicConfig(level=logging.INFO, format='%(message)s')
connection = sqlite3.connect('companies.db')
cursor = connection.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS icons (icon_id INTEGER PRIMARY KEY, icon BLOB, company_name TEXT, number INTEGER, FOREIGN KEY(company_name) REFERENCES companies(name))')
cursor.execute('CREATE TABLE IF NOT EXISTS slogans (slogan_id INTEGER PRIMARY KEY, slogan TEXT, company_name TEXT, number INTEGER, FOREIGN KEY(company_name) REFERENCES companies(name))')
cursor.execute('CREATE TABLE IF NOT EXISTS products (product_id INTEGER PRIMARY KEY, product BLOB, company_name TEXT, number INTEGER, FOREIGN KEY(company_name) REFERENCES companies(name))')
cursor.execute('CREATE TABLE IF NOT EXISTS companies (name TEXT PRIMARY KEY, description TEXT, logo BLOB, colors TEXT, shape TEXT, mood_board BLOB)')
cursor.execute('CREATE TABLE IF NOT EXISTS logo (id INTEGER PRIMARY KEY, logo BLOB, logo_number INTEGER)')
cursor.execute('CREATE TABLE IF NOT EXISTS reports (company_name TEXT PRIMARY KEY, report TEXT, FOREIGN KEY(company_name) REFERENCES companies(name))')

def get_all_logo_candidates():
    try:
        connection = sqlite3.connect('companies.db')
        cursor = connection.cursor()
        cursor.execute(f"SELECT logo FROM logo")    
        result = cursor.fetchall()
        connection.close()
        
        candidates = [base64.b64encode(logo[0]).decode('utf-8') for logo in result]
        logging.info("Contacting DB succeeded")
        if result:
            return candidates
        else:
            return None
    except:
        logging.error("Error connecting to DB")
        status = "ERROR"


def check_if_company_exists(name):
    
    exist = False

    connection = sqlite3.connect('companies.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM companies WHERE name=?", (name,))    
    result = cursor.fetchone()
    connection.close()
    
    if result:
        exist = True

    return exist

def insert_company_with_logo(name, description, logo, colors, shape):

    status = None

    try:            
        connection = sqlite3.connect('companies.db')
        cursor = connection.cursor()
        cursor.execute('INSERT OR REPLACE INTO companies (name, description, logo, colors, shape) VALUES (?, ?, ?, ?, ?)', (name, description, logo, colors, shape))
        connection.commit()
        connection.close()
        status = "OK"
        logging.info("insertion to DB succeeded")
    except:
        logging.error("Error inserting to DB")
        status = "ERROR"

    return status


def update_slogan(name, slogan, number):

    status = None
    
    try:
        connection = sqlite3.connect('companies.db')
        cursor = connection.cursor()
        cursor.execute(f'INSERT OR REPLACE INTO slogans (slogan_id, slogan, company_name, number) VALUES ((SELECT slogan_id FROM slogans WHERE company_name = ? AND number = ?), ?, ?, ?)', (name, number, slogan, name, number))
        connection.commit()
        connection.close()
        status = "OK"
        logging.info("insertion to DB succeeded")
    except:
        logging.error("Error inserting to DB")
        status = "ERROR"

    return status


def update_report(name, report):
    
    status = None
    
    try:
        connection = sqlite3.connect('companies.db')
        cursor = connection.cursor()
        cursor.execute(f'INSERT OR REPLACE INTO reports (company_name, report) VALUES (?, ?)', (name, report))
        connection.commit()
        connection.close()
        status = "OK"
        logging.info("insertion to DB succeeded")
    except:
        logging.error("Error inserting to DB")
        status = "ERROR"

    return status


def update_product(name, product, number):

    status = None

    try:
        connection = sqlite3.connect('companies.db')
        cursor = connection.cursor()
        cursor.execute(f'INSERT OR REPLACE INTO products (product_id, product, company_name, number) VALUES ((SELECT product_id FROM products WHERE company_name = ? AND number = ?), ?, ?, ?)', (name, number, product, name, number))
        connection.commit()
        connection.close()
        status = "OK"
        logging.info("insertion to DB succeeded")
    except:
        logging.error("Error inserting to DB")
        status = "ERROR"

    return status


def update_mood_board(name, mood_board):

    status = None

    try:
        connection = sqlite3.connect('companies.db')
        cursor = connection.cursor()
        cursor.execute('UPDATE companies SET mood_board = ? WHERE name = ?', (mood_board, name))
        connection.commit()
        connection.close()
        status = "OK"
        logging.info("insertion to DB succeeded")
    except:
        logging.error("Error inserting to DB")
        status = "ERROR"

    return status


def get_company_by_name(name):
    try:
        connection = sqlite3.connect('companies.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM companies WHERE name = ?', (name, ))
        connection.commit() 
        data = cursor.fetchall()
        connection.close()
        logging.info("contacting DB succeeded")

        return data
    except:
        logging.error("Error contacting DB")
        return None


def get_company_logo(name):
    try:
        connection = sqlite3.connect('companies.db')
        cursor = connection.cursor()
        cursor.execute('SELECT logo FROM companies WHERE name = ?', (name, ))
        result = cursor.fetchone()
        connection.close()
        logging.info("contacting DB succeeded")
        if result:
            return base64.b64encode(result[0]).decode('utf-8')
        else:
            return None

    except:
        logging.error("Error contacting DB")
        return None


def get_company_description(name):
    try:
        connection = sqlite3.connect('companies.db')
        cursor = connection.cursor()
        cursor.execute('SELECT description FROM companies WHERE name = ?', (name, ))
        result = cursor.fetchone()
        connection.close()
        logging.info("contacting DB succeeded")
        if result:
            return result[0]
        else:
            return None
    except:
        logging.error("Error contacting DB")
        return None
        

def insert_or_replace_logo(logo_number, logo_blob):

    status = None

    try:
        connection = sqlite3.connect('companies.db')
        cursor = connection.cursor()
        cursor.execute('INSERT OR REPLACE INTO logo (id, logo, logo_number) VALUES ((SELECT id FROM logo WHERE logo_number = ?), ?, ?)', (logo_number, logo_blob, logo_number))
        connection.commit()
        connection.close()
        status = "OK"
        logging.info("insertion to DB succeeded")
    except:
        logging.error("Error inserting to DB")
        status = "ERROR"

    return status

    
def get_logo_from_logos(logo_number):
    try:
        connection = sqlite3.connect('companies.db')
        cursor = connection.cursor()
        cursor.execute('SELECT logo FROM logo WHERE logo_number = ?', (logo_number,))
        result = cursor.fetchone()
        connection.close()
        logging.info("Contacting DB succeeded")
        return result[0] if result else "not implemented"
    
    except:
        logging.error("Error contacting DB")
        return None
        

def get_company_shape_name(name):
    try:
        connection = sqlite3.connect('companies.db')
        cursor = connection.cursor()
        cursor.execute('SELECT shape FROM companies WHERE name = ?', (name,))
        result = cursor.fetchone()
        connection.close()
        logging.info("Contacting DB succeeded")
        if result:
            return result[0] 
        else:
            return None
        
    except:
        logging.error("Error contacting DB")
        return None
        

def get_company_colors(name):
    try:
        connection = sqlite3.connect('companies.db')
        cursor = connection.cursor()
        cursor.execute('SELECT colors FROM companies WHERE name = ?', (name,))
        result = cursor.fetchone()
        connection.close()
        logging.info("Contacting DB succeeded")
        if result:
            return result[0] 
        else:
            return None
        
    except:
        logging.error("Error contacting DB")
        return None
        

def get_company_moodboard(name):
    try:
        connection = sqlite3.connect('companies.db')
        cursor = connection.cursor()
        cursor.execute('SELECT mood_board FROM companies WHERE name = ?', (name,))
        result = cursor.fetchone()
        connection.close()
        logging.info("Contacting DB succeeded")
        if result:
            return base64.b64encode(result[0]).decode('utf-8')
        else:
            return None
    
    except:
        logging.error("Error contacting DB")
        return None
        

def delete_all_data_from_all_tables():
    connection = sqlite3.connect('companies.db')
    cursor = connection.cursor()
    # List of table names
    tables = ['products']
    for table_name in tables:
        cursor.execute(f'DELETE FROM {table_name}')
    connection.commit()
    connection.close()


def get_slogan(name, number):
    try:
        connection = sqlite3.connect('companies.db')
        cursor = connection.cursor()
        cursor.execute('SELECT slogan FROM slogans WHERE company_name = ? AND number = ?', (name, number))
        result = cursor.fetchone()
        connection.close()
        logging.info("Contacting DB succeeded")
        return result[0] if result else None
    
    except:
        logging.error("Error contacting DB")
        

def get_product(name, number):
    try:
        connection = sqlite3.connect('companies.db')
        cursor = connection.cursor()
        cursor.execute('SELECT product FROM products WHERE company_name = ? AND number = ?', (name, number))
        result = cursor.fetchone()
        connection.close()
        logging.info("Contacting DB succeeded")
        return base64.b64encode(result[0]).decode('utf-8') if result else None
    except:
        logging.error("Error contacting DB")
        

def get_report(name):
    try:
        connection = sqlite3.connect('companies.db')
        cursor = connection.cursor()
        cursor.execute('SELECT report FROM reports WHERE company_name = ?', (name, ))
        result = cursor.fetchone()
        connection.close()
        logging.info("Contacting DB succeeded")
        return result[0] if result else None
    except:
        logging.error("Error contacting DB")


def get_company_products(name): 
    try:
        connection = sqlite3.connect('companies.db')
        cursor = connection.cursor()
        cursor.execute('SELECT product FROM products WHERE company_name = ?', (name, ))
        result = cursor.fetchall()
        connection.close()
        products_list = [base64.b64encode(product[0]).decode('utf-8') for product in result]
        logging.info("Contacting DB succeeded")
        if result:
            return products_list
        else:
            return None
    except:
        logging.error("Error contacting DB")
