import os
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import csv

load_dotenv()

csv_delimit = ';'
connection_url = ""  # url permettant d'acc. a la page de co.
login_id = 'login'  # id html du champ pour login/username
password_id = 'mdp'  # id html du champ pour mot de passe
submit_button_id = 'sbt_login'  # id html du btn pour soumettre le form. a remplir
form_url = ""  # url vers le formulaire a remplir une fois co
csv_url = ""  # chemin vers le fichier csv

driver = webdriver.Chrome(ChromeDriverManager().install())


def connect():
    driver.get(connection_url)
    mail_input = driver.find_element_by_id(login_id)
    password_input = driver.find_element_by_id(password_id)
    mail_input.send_keys(os.getenv('LOGIN'))
    time.sleep(1)
    password_input.send_keys(os.getenv('PASSWORD'))
    time.sleep(5)


def csv_to_list():
    with open(csv_url, encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=csv_delimit)
        line_count = 0
        result = []
        csv_reader = [i for i in csv_reader]
        for row in csv_reader:
            if line_count != 0:
                result.append({csv_reader[0][i]: row[i] for i in range(len(row))})
            line_count += 1
    return result


def fill(data):
    driver.get(form_url)
    for k in data:
        driver.find_element_by_id(k).send_keys(data[k])

    driver.find_element_by_id(submit_button_id).submit()

    time.sleep(5)


connect()
for element in csv_to_list():
    fill(element)
