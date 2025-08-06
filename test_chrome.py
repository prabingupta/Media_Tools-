from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

chromedriver_path = "/Users/prabinkumargupta/Downloads/chromedriver-mac-arm64/chromedriver"

options = Options()
options.add_argument("--headless")  # comment this line to see browser window

service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.google.com")
print("Page title is:", driver.title)

driver.quit()
