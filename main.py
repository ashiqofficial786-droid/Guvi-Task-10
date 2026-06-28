
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def login(driver, username, password):
    driver.get("https://www.saucedemo.com/")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )
    driver.find_element(By.ID, "user-name").clear()
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()


# ---------------- Positive Test Cases ----------------

def test_title_of_web_application(driver):
    """Positive: Title should be Swag Labs."""
    driver.get("https://www.saucedemo.com/")
    assert driver.title == "Swag Labs"


def test_url_of_homepage(driver):
    """Positive: Homepage URL should match saucedemo.com."""
    driver.get("https://www.saucedemo.com/")
    assert driver.current_url == "https://www.saucedemo.com/"


def test_url_of_dashboard_after_login(driver):
    """Positive: After valid login URL should contain inventory."""
    login(driver, "standard_user", "secret_sauce")
    WebDriverWait(driver, 10).until(
        EC.url_contains("inventory")
    )
    assert "inventory" in driver.current_url


# ---------------- Negative Test Cases ----------------

def test_title_should_not_be_empty(driver):
    """Negative: Title should NOT be empty."""
    driver.get("https://www.saucedemo.com/")
    assert driver.title != ""


def test_homepage_url_should_not_be_dashboard(driver):
    """Negative: Homepage URL should NOT contain inventory."""
    driver.get("https://www.saucedemo.com/")
    assert "inventory" not in driver.current_url


def test_wrong_credentials_should_not_login(driver):
    """Negative: Wrong credentials should NOT reach dashboard."""
    login(driver, "wrong_user", "wrong_pass")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']"))
    )
    assert "inventory" not in driver.current_url
