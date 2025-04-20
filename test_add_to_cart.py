from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup
driver = webdriver.Chrome()
driver.get("http://localhost:9000/")
driver.maximize_window()

# Wait for the page to load
time.sleep(3)

# Login
driver.find_element(By.NAME, "username").send_keys("admin")
driver.find_element(By.NAME, "password").send_keys("kjc")
driver.find_element(By.XPATH, "//button[@type='submit']").click()

# Handle alert (optional)
try:
    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert.accept()
    print("✅ Login alert accepted.")
except:
    print("ℹ️ No alert appeared.")

# Wait for page load
time.sleep(2)

# Scroll to categories
driver.execute_script("window.scrollBy(0, 500);")

# Wait for the 'Vegetables' category image to be clickable
try:
    veg_image = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//img[@alt='Vegetables']"))
    )
    veg_image.click()
    print("✅ Clicked on Vegetables category.")
except Exception as e:
    print(f"❌ Could not click Vegetables image: {e}")

# Wait for Vegetable products to appear
try:
    veg_products = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "product"))
    )
    count = len(veg_products)
    if count > 0:
        print(f"✅ {count} Vegetable products displayed.")
    else:
        print("❌ No Vegetable products found.")
except Exception as e:
    print(f"❌ Failed to load Vegetable products: {e}")

# Finish
time.sleep(2)
driver.quit()  