

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import csv

url = "https://www.bcregistry.org.in/iba/home/HomeAction.do?doBCPortal=yes"

options = webdriver.ChromeOptions()

# options.add_argument('--headless') 
options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-extensions")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument("--disable-features=SameSiteByDefaultCookies,CookiesWithoutSameSiteMustBeSecure")

# service = Service('chromedriver.exe')

driver = webdriver.Chrome(options=options)

driver.get(url)

time.sleep(2)

state_dropdown = driver.find_element(By.ID, "stateId")

# Get all available states (assuming it's a dropdown)
state_options = Select(state_dropdown).options

with open('bcregistry.csv', 'a', newline='',encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Name of BC','Contact Number','Gender','Bank Name','State','District','Block','Pincode','Corporate','Gram Panchayat(GP)','Village Name','Corporate BC Name'])
    # Loop through each state
    for i in range(1,len(state_options)):
        # Select the current state

        # state = state_options[i].text

        state_options[i].click()
        # Find the district dropdown element (might need adjustment based on HTML structure)

        time.sleep(2)

        district_dropdown = driver.find_element(By.ID, "districtId")

        # Get all available districts for the current state (assuming it's a dropdown)
        district_options = Select(district_dropdown).options

        # Loop through each district in the current state
        for j in range(1,len(district_options)):
            # Select the current district

            # district = district_options[j].text
            district_options[j].click()

            # Find the button element
            button = driver.find_elements(By.CLASS_NAME, "search_btn")[-2]

            driver.execute_script("arguments[0].click();", button)

            time.sleep(2)

            captcha = driver.find_element(By.ID,"txtCaptcha_search")
            captcha_text = captcha.get_attribute("value")
            # remove space
            captcha_text = captcha_text.replace(" ","")

            captcha_input = driver.find_element(By.ID,"cap_search")
            captcha_input.send_keys(captcha_text)

            button_xpath = "//a[@type='submit' and text()='Verify']"

            button = driver.find_element(By.XPATH, button_xpath)
            
            driver.execute_script("arguments[0].click();", button)

            time.sleep(5)

            table = driver.find_element(By.TAG_NAME, "table")

            # Find all table body rows (<tr> elements within <tbody>)
            table_body = table.find_element(By.TAG_NAME, "tbody")  
            rows = table_body.find_elements(By.TAG_NAME, "tr")


            # mention state and district in csv
            # writer.writerow([state,district])

            # Loop through each row
            for row in rows:
            # Get the second table data (cell) - assuming zero-based indexing
                second_cell = row.find_elements(By.TAG_NAME, "td")[1]

                # Find the only anchor tag within the cell (assuming there's only one)
                anchor_tag = second_cell.find_element(By.TAG_NAME, "a")

                # clicke the anchor tag
                driver.execute_script("arguments[0].click();", anchor_tag)

                time.sleep(2)

                captcha = driver.find_element(By.ID,"txtCaptcha_detail")
                captcha_text = captcha.get_attribute("value")
                # remove space
                captcha_text = captcha_text.replace(" ","")

                captcha_input = driver.find_element(By.ID,"cap_detail")
                captcha_input.send_keys(captcha_text)

                button_xpath = "//a[@type='submit' and text()='Verify']"

                button = driver.find_element(By.XPATH, button_xpath)
                driver.execute_script("arguments[0].click();", button)

                time.sleep(2)

                modal = driver.find_element(By.ID,"modelcontentDiv")
                modal_table = modal.find_element(By.TAG_NAME, "tbody")

                modal_rows = modal_table.find_elements(By.TAG_NAME, "tr")

                data=[]
                for modal_row in modal_rows:
                    
                    # for each td in the row get the text
                    modal_cells = modal_row.find_elements(By.TAG_NAME, "td")
                    # data = [cell.text for cell in modal_cells]
                    data.append(modal_cells[1].text)
      
                writer.writerow(data)        

                # print a blank line to separate each record
                # writer.writerow([])
                
            # Go back to the previous page
            driver.back()

            time.sleep(4)

            state_dropdown = driver.find_element(By.ID, "stateId")
            state_options = Select(state_dropdown).options

            state_options[i].click()

            time.sleep(2)
            district_dropdown = driver.find_element(By.ID, "districtId")
            district_options = Select(district_dropdown).options

        time.sleep(2)
        state_dropdown = driver.find_element(By.ID, "stateId")
        state_options = Select(state_dropdown).options

driver.quit()
# Find the state dropdown element


