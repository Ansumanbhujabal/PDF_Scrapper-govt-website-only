from selenium import webdriver
import streamlit as st
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from openpyxl import Workbook
import time

def get_search_results(keyword):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    results = []
    query = f'{keyword} site:.gov.in OR site:.nic.in filetype:pdf -site:pib.gov.in'

    driver.get('https://www.google.com')
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    
    wait = WebDriverWait(driver, 10)
    
    for page in range(10): 
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.g')))
        search_results = driver.find_elements(By.CSS_SELECTOR, 'div.g')
        
        for result in search_results:
            try:
                url = result.find_element(By.TAG_NAME, 'a').get_attribute('href')
                title_element = result.find_element(By.TAG_NAME, 'h3')
                title = title_element.text if title_element else 'N/A'
                language = "en"
                results.append((url, keyword, title, language))
            except Exception as e:
                print(f'Error extracting result: {e}')
        
        try:
            next_button = wait.until(EC.element_to_be_clickable((By.ID, 'pnnext')))
            next_button.click()
            time.sleep(3) 
        except Exception as e:
            print(f'Error navigating to next page: {e}')
            break  

    driver.quit()
    return results

def write_to_excel(results, filename):
    wb = Workbook()
    ws = wb.active
    ws.append(['URL', 'Keyword', 'Title', 'Language'])
    
    for result in results:
        ws.append(result)
    
    wb.save(filename)

st.title("PDF Scraper from all govt website")
st.write("Enter the Keyword you want to search and get PDF URLs and title in an Excel file.")

keyword = st.text_input("Keyword", "National Education Policy ")
file_name = st.text_input("Output Excel File Name", "Outputpdf_files.xlsx")

if st.button("Get PDF Links"):
    with st.spinner("Scraping pdf links..."):
        pdf_data = get_search_results(keyword)
        write_to_excel(pdf_data, file_name)
        st.success(f"Links added to {file_name} successfully.")
        st.download_button(label="Download Excel file", data=open(file_name, "rb").read(), file_name=f"{file_name}.xlsx")
st.markdown("[Github](https://github.com/Ansumanbhujabal) | [LinkedIn](https://www.linkedin.com/in/ansuman-simanta-sekhar-bhujabala-30851922b/) | © 2024 Ansuman Bhujabala")

