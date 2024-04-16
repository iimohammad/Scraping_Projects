import requests
from bs4 import BeautifulSoup
import csv


def scrape(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    body = soup.find('body')

    h2_tags = body.find_all('h2')
    print("H2 Tags within the body:")
    for tag in h2_tags:
        print(tag.tex)

    h5_tags = body.find_all('h5')
    for tag in h5_tags:
        location_text = tag.get_text(separator='\n').strip()
        if '\n' in location_text:
            city_state, phone_number = location_text.split('\n')
            city_state_parts = city_state.split(', ')
            if len(city_state_parts) == 2:
                city, state = city_state_parts
            else:
                city = city_state
                state = ""
            phone_number = phone_number.split(': ')[1]
            print("City:", city)
            print("State:", state)
            print("Phone number:", phone_number)
        else:
            print("City and State:", location_text)




def scrape_save_to_csv(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    body = soup.find('body')

    with open('scraped_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['h2', 'City', 'State', 'Phone number'])

        h2_tags = body.find_all('h2')
        for tag in h2_tags:
            h2_text = tag.text.strip()

            h5_tag = tag.find_next_sibling('h5')
            if h5_tag:
                location_text = h5_tag.get_text(separator='\n').strip()
                if '\n' in location_text:
                    city_state, phone_number = location_text.split('\n')
                    city_state_parts = city_state.split(', ')
                    if len(city_state_parts) == 2:
                        city, state = city_state_parts
                    else:
                        city = city_state
                        state = ""
                    phone_number = phone_number.split(': ')[1]
                else:
                    city = state = phone_number = ""

                writer.writerow([h2_text, city, state, phone_number])
            else:
                writer.writerow([h2_text, "", "", ""])  
                
                  
if __name__ == "__main__":
    url = 'https://ipta.org.au/?post_type=ipta_attorney&s=&state=&specialty=pa'
    scrape_save_to_csv(url)
    scrape(url)
