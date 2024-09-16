from selenium import webdriver
from selenium.webdriver.common.by import By

def test_google_search():
    # Selenium Remote WebDriver ile Chrome'u başlat
    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
        command_executor="http://localhost:4444/wd/hub",
        options=options
    )

    # Google'ı aç ve test yap
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("Selenium")
    search_box.submit()

    assert "Selenium" in driver.title

    driver.quit()
