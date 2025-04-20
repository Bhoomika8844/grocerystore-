from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("http://localhost:9000/")


# --- Step 1: Login ---
time.sleep(2)
driver.find_element(By.NAME, "username").send_keys("admin")
driver.find_element(By.NAME, "password").send_keys("kjc")
driver.find_element(By.XPATH, "//button[@type='submit']").click()
time.sleep(2)

# --- Step 2: Scroll to category section ---
driver.execute_script("window.scrollBy(0, 500);")
time.sleep(1)

# --- Step 3: Click "Vegetables" button ---
driver.find_element(By.XPATH, "//button[text()='Vegetables']").click()
time.sleep(2)

# --- Step 4: Verify vegetable products are visible ---
vegetable_products = driver.find_elements(By.CLASS_NAME, "product-card")

if len(vegetable_products) > 0:
    print("✅ Vegetable products are displayed correctly.")
else:
    print("❌ No vegetable products found after filter.")

# --- End Test ---
driver.quit()
