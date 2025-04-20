from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup
driver = webdriver.Chrome()
driver.get("http://localhost:9000/")
driver.maximize_window()

# Wait for the page to load and log in
time.sleep(3)
driver.find_element(By.NAME, "username").send_keys("admin")
driver.find_element(By.NAME, "password").send_keys("kjc")
driver.find_element(By.XPATH, "//button[@type='submit']").click()

# Handle alert if any
try:
    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert.accept()
    print("✅ Login alert accepted.")
except:
    print("ℹ️ No alert appeared.")

# Wait for page load
time.sleep(2)

# Navigate to Vegetables category
driver.execute_script("window.scrollBy(0, 500);")
try:
    veg_image = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//img[@alt='Vegetables']"))
    )
    veg_image.click()
    print("✅ Clicked on Vegetables category.")
except Exception as e:
    print(f"❌ Could not click Vegetables image: {e}")

# Wait for Vegetable products to appear and add the first product to the cart
try:
    veg_products = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "product"))
    )
    first_product = veg_products[0]  # Select the first product
    add_to_cart_button = first_product.find_element(By.XPATH, ".//button[@class='add-to-cart']")
    add_to_cart_button.click()
    print("✅ Added first product to cart.")
    
    # Wait for success prompt to appear
    try:
        success_prompt = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
        )
        print("✅ Success prompt appeared.")
    except:
        print("❌ No success prompt appeared.")
except Exception as e:
    print(f"❌ Failed to add product to cart: {e}")

# Finish
time.sleep(2)
driver.quit()
