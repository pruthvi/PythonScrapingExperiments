from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'https://www.drug-inspections.canada.ca/gmp/searchResult-en.html?estName=&ref=&site=&eType=&prov=+&rate=&lic=&licNum=&act=&actCat=actif&term=&startDate=&endDate='

driver = webdriver.Chrome()
driver.get(url)

WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tbodyMain"]/tr[1]/td[2]/a')))

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


    print(ref,company,company_link,site,ins_date,rating,clicense)





#    links = row.find_elements(By.XPATH, './/td[2]/a')  # Company Name
#   print(row.get_attribute('href')) #prints text from the element



# rowdatas = driver.findElements
# # //*[@id="tbodyMain"]/tr[1]/td[2]/a
#
# for row in rowdatas:
#     name = row.find_element_by_xpath('.//*[@id="tbodyMain"]/tr[1]/td[2]/a').text
#     print(name)
