import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class TestSanity:
    @pytest.fixture(autouse=True)
    def setup(self):
        global driver

        node_url = "http://localhost:4444"
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Remote(command_executor=node_url, desired_capabilities=webdriver.DesiredCapabilities.CHROME, options=options)

        driver.set_window_size(1920, 1080)
        driver.set_window_position(620, 0)
        driver.get("https://www.saucedemo.com/")
        driver.implicitly_wait(3)
        self.login("standard_user", "secret_sauce")

    def test_01_count_items(self):
        self.select_all_items()
        self.verify_number_of_items_cart("6")

    def login(self, username, password):
        driver.find_element(By.ID, "user-name").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "login-button").click()

    def select_all_items(self):
        num_items = len(driver.find_elements(By.CLASS_NAME, "inventory_item_name"))
        for i in range(num_items):
            driver.find_elements(By.CLASS_NAME, "inventory_item_name")[i].click()
            driver.find_element(By.CSS_SELECTOR, "button[class='btn btn_primary btn_small btn_inventory").click()
            driver.find_element(By.ID, "back-to-products").click()

    def verify_number_of_items_cart(self, expected):
        actual = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
        assert actual == expected, f"Expected number of items in cart: {expected}, but got {actual}"

    def teardown_method(self):
        driver.quit()
