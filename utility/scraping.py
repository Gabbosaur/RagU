import requests
from bs4 import BeautifulSoup
import re

base_url = 'https://www.sace.it/mappe/dettaglio/'

def remove_space(text):
    return re.sub(r'\s+', ' ', text)

def scrape_full_html(country, response):
    f = open("..\\countries_html\\" + country + ".html", "w", encoding="utf-8")
    f.write(response.text)
    f.close()

def remove_from_line(text, line_number):
    lines = text.splitlines()  # Split the text into lines
    if 0 <= line_number < len(lines):  # Ensure the line_number is valid
        lines = lines[:line_number]  # Keep lines up to (but not including) line_number
    return "\n".join(lines)  # Join the remaining lines back into a string


# Open the file in read mode
with open('countries.txt', 'r') as file:
#with open('utility\prova.txt', 'r') as file:
    # Iterate over each line in the file
    for line in file:
        # Strip leading/trailing whitespaces (including newlines) and print
        country = line.strip()

        refactored_country = country.replace(" ", "-").replace(",", "-").replace("(", "-").replace(")", "-").replace(".", "-").replace("'", "-")
        # Form the full URL (assuming the API takes the country name as a query parameter)
        url = f'{base_url}/{refactored_country}'
        # Send GET request
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            print(f'Success for {country}')
            final_text = ''
            # Crea un oggetto BeautifulSoup per il parsing dell'HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            final_text += country + "\n\n"

            # Trova tutti i tag con la classe "col-12 col-md-6 text-center"
            elements = soup.find_all(class_="col-12 col-md-6 text-center")
            # Itera su ogni elemento e stampa il testo contenuto
            full_text = ''
            for element in elements:
                if element.get_text():
                    full_text += element.get_text().strip()
            final_text += remove_space(full_text) + "\n"


            elements = soup.find_all(class_="pr-break-inside-avoid d-none d-md-block")
            # Itera su ogni elemento e stampa il testo contenuto
            full_text = ''

            for element in elements:
                values = element.find_all("div", class_="c100")
                titles = element.find_all("div", class_="my-2")
                filtered_titles = [title for title in titles if "graphValue" not in title.get("class", [])]

                for i in range(len(values)):
                    full_text += remove_space(titles[i].get_text()) + ": " + remove_space(values[i].get_text()) + "\n" 
            final_text += full_text + "\n"


            elements = soup.find_all(class_="row justify-content-md-center")

            # Itera su ogni elemento e stampa il testo contenuto
            full_text = ''
            try:
                elements.pop()
                elements.pop()
            except:
                pass
            for element in elements:

                values = element.find_all("div", class_="c100")
                titles = element.find_all("div", class_="my-2")
                filtered_titles = [title for title in titles if "graphValue" not in title.get("class", [])]

                for i in range(len(values)):
                    full_text += remove_space(titles[i].get_text()) + ": " + remove_space(values[i].get_text()) + "\n" 
            final_text += full_text.replace("Score 0-100", "/100") + "\n"


            elements = soup.find_all(class_="showPremiumLoggedIn")
            # Itera su ogni elemento e stampa il testo contenuto
            full_text = ''
            try:
                elements.pop()
                elements.pop()
            except:
                pass
        
            for element in elements[3:]:
                couples = element.find_all("div", class_="py-4")
                for couple in couples:
                    if "Contesto di benessere" in couple.get_text():
                        full_text += "Contesto di benessere" + "\n"
                    elif "Transizione energetica" in couple.get_text():
                        full_text += "Transizione energetica" + "\n"
                    else:
                        full_text += remove_space(couple.get_text()).replace(" i ", " ").replace(" Score 0-100", "/100") + "\n"
                
            final_text += remove_from_line(full_text, 23) + "\n"
            
            # items = elements[1].find_all("div", class_="row")
            # for item in items:
            #     print(remove_space(item.get_text()))
            final_text += remove_space(elements[1].get_text().replace("- euro", "")) + "\n"
            
            f = open("..\\countries_data\\" + country + ".txt", "w", encoding="utf-8")
            f.write(final_text)
            f.close()

        else:
            print(f'Failed for {country}: Status Code {response.status_code}')