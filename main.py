from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

import pandas as pd

url = 'https://www.drug-inspections.canada.ca/gmp/searchResult-en.html?estName=&ref=&site=&eType=&prov=+&rate=&lic=&licNum=&act=&actCat=actif&term=&startDate=&endDate='
inspectiondata = []

driver = webdriver.Chrome()
driver.get(url)

WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tbodyMain"]/tr[1]/td[2]/a')))

# Changes how many data row is visible on the page
driver.execute_script("""document.querySelector("select[name='wb-auto-4_length'] option").value="15";""") #change value to 3000 for final scrape
select = Select(driver.find_element(By.NAME, "wb-auto-4_length"))
select.select_by_index(2)
select.select_by_index(0)


# Extracts table data
table_id = driver.find_element(By.ID, 'tbodyMain')
rows = table_id.find_elements(By.TAG_NAME, "tr") # get all of the rows in the table
for row in rows:
    ref = row.find_elements(By.TAG_NAME, "td")[0].text  # Reference Number
    company = row.find_elements(By.TAG_NAME, "td")[1].text  # Company Name
    site = row.find_elements(By.TAG_NAME, "td")[2].text   # Site
    ins_date = row.find_elements(By.TAG_NAME, "td")[3].text   # Inspection Date
    rating = row.find_elements(By.TAG_NAME, "td")[4].text   # Rating
    clicense = row.find_elements(By.TAG_NAME, "td")[5].text   # Currently Licensed

    links = row.find_elements(By.XPATH, './/td[2]/a')
    for link in links:
        company_link = link.get_attribute('href')
    # print(ref,company,company_link,site,ins_date,rating,clicense)

    # Open a new window for each company data
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(company_link)
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="inspectionTable"]/tr[1]/td[1]')))
    location = driver.find_element(By.ID, 'address').text
    # print(location.text)

    driver.close()
    driver.switch_to.window(driver.window_handles[0])


    # Adds all data into dataframe for exporting
    insp_data = {
        'reference' : ref,
        'company': company,
        'site': site,
        'inspection_date': ins_date,
        'rating': rating,
        'currently_licensed': clicense,
        'address': location
    }
    inspectiondata.append(insp_data)

# Exports to CSV
df = pd.DataFrame(inspectiondata)
print(df)
df.to_csv('table.csv')