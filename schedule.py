from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.common.by import By
import re

with open(".env.local", "r") as file:
    env = dict([(line[:line.index("=")], line[line.index("=") + 1:]) for line in file.read().strip().split("\n")])

def get_calendar():
    browser = webdriver.Chrome()

    # Sign in
    browser.get("https://worksmart.michaels.com/etm/")

    loginField = browser.find_element(By.ID, "loginField")
    passwordField = browser.find_element(By.ID, "passwordField")
    loginButton = browser.find_element(By.ID, "loginButton")

    loginField.send_keys(env["LOGIN"])
    passwordField.send_keys(env["PASSWORD"])
    loginButton.click()

    # Scrape schedule
    browser.execute_script("setLocationAndClearFrame('', '/etm/time/timesheet/etmTnsMonth.jsp?selectedTocID=181&parentID=10')")

    current_month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"].index(browser.find_element(By.CLASS_NAME, "pageTitle").text.split(" ")[0]) + 1
    current_year = browser.find_element(By.CLASS_NAME, "pageTitle").text.split(" ")[1]
    table = browser.find_elements(By.CSS_SELECTOR, ".calTD-NoShift, .calendarCellRegularPast, .calendarCellRegularCurrent, .calendarCellRegularFuture")
    current_month_schedule = [cell.text for cell in table]

    browser.find_elements(By.CLASS_NAME, "imageButton")[4].click()


    next_month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"].index(browser.find_element(By.CLASS_NAME, "pageTitle").text.split(" ")[0]) + 1
    next_year = browser.find_element(By.CLASS_NAME, "pageTitle").text.split(" ")[1]
    table = browser.find_elements(By.CSS_SELECTOR, ".calTD-NoShift, .calendarCellRegularPast, .calendarCellRegularCurrent, .calendarCellRegularFuture")
    next_month_schedule = [cell.text for cell in table]

    # Parse schedule
    calendar = {}
    output = ""
    for day in current_month_schedule:
        if re.match("^\d\d(?!:).*", day) and not "NOT SCHEDULED" in day:
            lines = day.split("\n")
            calendar[str(current_month) + "/" + lines[0] + "/" + current_year] = lines[1]
    for day in next_month_schedule:
        if re.match("^\d\d(?!:).*", day) and not "NOT SCHEDULED" in day:
            lines = day.split("\n")
            calendar[str(next_month) + "/" + lines[0] + "/" + next_year] = lines[1]
    browser.close()
    return calendar