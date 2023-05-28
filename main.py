import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

from fake_useragent import UserAgent
import time
import random


def get_source_html(url):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={UserAgent.random}")
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        # Убеждаемся, что сайт откроется в десктопной версии и переходим по ссылке
        driver.maximize_window()
        driver.get(url=url)
        # Вход в личный кабинет
        login_to_personal_account(driver)
        with open("index.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def search_proxy_and_time():
    with open("index.html", encoding="utf-8") as file:
        src = file.read()

    proxy = []
    soup = BeautifulSoup(src, "lxml")
    # Поиск информации и вывод на экран
    items_divs_proxy = soup.find_all("div", class_="right clickselect")
    for item in items_divs_proxy:
        if len(item.text) > 14:
            proxy.append(item.text[:-1])
    items_divs_time = soup.find_all("div", class_="right color-warning")
    for i, item in enumerate(items_divs_time):
        print(f"{proxy[i]} - {item.text}".encode("utf-8"))


def login_to_personal_account(driver):
    # Клик по кнопке Войти
    enter_button = driver.find_element(
        By.CSS_SELECTOR,
        "body > div.layout > header > div > ul.nav.pull-right > li:nth-child(2) > a",
    ).click()
    time.sleep(2)

    # Поиск поля для ввода email и ввод email пользователя
    email_input = driver.find_element(
        By.CSS_SELECTOR, "#form-login > div:nth-child(1) > div > input[type=email]"
    )
    email_input.clear()
    email_input.send_keys("demo-tt1@inet-yar.ru")

    # Поиск поля для ввода password и ввод password пользователя
    password_input = driver.find_element(By.ID, "login-password")
    password_input.clear()
    password_input.send_keys("rNCV14la")

    # Ввод капчи
    time.sleep(30)

    # Клик по кнопке Войти
    enter_button = driver.find_element(
        By.CSS_SELECTOR, "#form-login > div:nth-child(7) > button"
    ).click()
    time.sleep(10)


def main():
    get_source_html(url="https://proxy6.net/")
    search_proxy_and_time()


if __name__ == "__main__":
    main()
