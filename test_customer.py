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

# Handle alert if any (login alert)
try:
    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert.accept()
    print("✅ Login alert accepted.")
except:
    print("ℹ️ No login alert appeared.")

# Wait for dashboard
time.sleep(2)

# Click Vegetables category (scroll if needed)
driver.execute_script("window.scrollBy(0, 500);")
try:
    veg_image = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//img[@alt='Vegetables']"))
    )
    veg_image.click()
    print("✅ Clicked on Vegetables category.")
except Exception as e:
    print(f"❌ Could not click Vegetables image: {e}")

# Add first product to cart
try:
    veg_products = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "product"))
    )
    first_product = veg_products[0]
    add_to_cart_button = first_product.find_element(By.XPATH, ".//button[@class='add-to-cart']")
    add_to_cart_button.click()
    print("✅ Added first product to cart.")

    try:
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert.accept()
        print("✅ Product added alert accepted.")
    except:
        print("ℹ️ No product added alert appeared.")

    view_cart_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "view-cart-btn"))
    )
    driver.execute_script("arguments[0].style.display = 'inline-block';", view_cart_button)
    view_cart_button.click()
    print("✅ View Cart button clicked. Cart opened.")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "cart-container"))
    )
    print("✅ Cart is displayed.")
except Exception as e:
    print(f"❌ Failed to add product to cart or view cart: {e}")

# Proceed to checkout
try:
    checkout_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "checkout-btn"))
    )
    checkout_button.click()
    print("✅ Proceeded to Checkout.")

    # Wait for customer form to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "customerForm"))
    )

    # Fill customer details (update fields as per your latest HTML)
    driver.find_element(By.ID, "fullName").send_keys("John Doe")
    driver.find_element(By.ID, "email").send_keys("john@example.com")
    driver.find_element(By.ID, "phone").send_keys("9876543210")
    driver.find_element(By.ID, "address").send_keys("123 Main Street, Cityville")

    # Select payment method (Cash or Card)
    payment_method = "Cash"  # change to "Credit Card" or "Debit Card" to test card input
    driver.find_element(By.XPATH, f"//input[@type='radio' and @value='{payment_method}']").click()
    print(f"✅ Selected Payment Method: {payment_method}")

    # If card payment, enter card details
    if payment_method != "Cash":
        driver.find_element(By.ID, "cardNumber").send_keys("4111111111111111")
        driver.find_element(By.ID, "cardName").send_keys("John Doe")
        driver.find_element(By.ID, "expiryDate").send_keys("12/26")
        driver.find_element(By.ID, "cvv").send_keys("123")
        print("✅ Filled Card Details.")

    # Submit order
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    print("✅ Submitted Customer Form.")

    # Success message or alert
    try:
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        print("✅ Order Confirmation Alert:", alert.text)
        alert.accept()
    except:
        print("ℹ️ No order alert appeared after submission.")
except Exception as e:
    print(f"❌ Error during customer form submission: {e}")

# Cleanup
time.sleep(2)
driver.quit()
