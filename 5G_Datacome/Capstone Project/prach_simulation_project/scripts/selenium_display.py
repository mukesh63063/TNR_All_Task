from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import datetime


def display_results():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    log_file = "output/selenium_log.txt"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(log_file, "a") as f:
            f.write(f"\n[{timestamp}] Selenium started and opened http://localhost:5000\n")
    except Exception as e:
        print(f"Error writing Selenium log: {e}")

    driver.get("http://localhost:5000")
    time.sleep(5)  # Let user interact
    driver.quit()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(log_file, "a") as f:
            f.write(f"[{timestamp}] Selenium completed\n")
    except Exception as e:
        print(f"Error writing Selenium log: {e}")


if __name__ == "__main__":
    display_results()