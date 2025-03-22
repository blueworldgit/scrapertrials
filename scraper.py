from selenium import webdriver
import pickle
import time

# Open browser
driver = webdriver.Chrome()

# Navigate to the site
driver.get('https://rypc.co.uk/crm/index.php')

# Wait for manual login
print("Please log in manually in the browser window...")
input("Press Enter when you've logged in successfully...")

# Save cookies after manual login
cookies = driver.get_cookies()
pickle.dump(cookies, open("cookies.pkl", "wb"))

# Close browser
driver.quit()

# Later, in your scraping script:
import requests
import pickle

session = requests.Session()
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])

# Use session for requests
response = session.get('https://rypc.co.uk/crm/dashboard/admin.php')

# Output the response for debugging
print("Response Status Code:", response.status_code)
print("Response Headers:", response.headers)
print("Response Text:", response.text)