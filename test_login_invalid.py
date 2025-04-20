from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import time

# Initialize the WebDriver
driver = webdriver.Chrome()
driver.get("http://localhost:9000/")
  # URL of the login page

# Wait for the page to load
time.sleep(2)

# Enter invalid credentials
driver.find_element(By.NAME, "username").send_keys("wrongusername")
driver.find_element(By.NAME, "password").send_keys("wrongpassword")

# Click the submit button
driver.find_element(By.XPATH, "//button[@type='submit']").click()

# Wait for the alert to appear
time.sleep(2)

# Handle the alert and get the text
alert = Alert(driver)
alert_text = alert.text
print(alert_text)  # This will print the alert message: "❌ Invalid Login! Try Again."

# Assert that the alert message is as expected
assert "Invalid Login! Try Again" in alert_text

# Accept the alert (close the alert box)
alert.accept()

# Close the browser
driver.quit()
