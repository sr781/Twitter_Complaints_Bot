from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os

PROMISED_DOWN = 150  # The download speed that the ISP offered
PROMISED_UP = 10  # The upload speed that the ISP offered
chrome_driver_path = Service("C:\Development\chromedriver.exe")  # The location of the chrome driver
TWITTER_EMAIL = os.environ["TWITTER_EMAIL"]  # Email and password stored as environment variable locally
TWITTER_PASSWORD = os.environ["TWITTER_PASSWORD"]
TWITTER_USERNAME = "TwitSpeed"


class InternetSpeedTwitterBot:
    import time

    def __init__(self, chrome_driver_path):
        self.down = 0
        self.up = 0
        self.driver = webdriver.Chrome(service=chrome_driver_path)


    def get_internet_speed(self):  # This function is responsible for the speed test
        self.driver.get("https://www.speedtest.net/")  #The website is loaded
        self.time.sleep(1)
        self.driver.find_element(By.ID, "onetrust-accept-btn-handler").click()  # The website cookies are accepted
        self.driver.find_element(By.CLASS_NAME, "start-text").click()  # The "start" button is pressed
        self.time.sleep(45)  # Waits for the test to finish (takes 30 seconds)
        speed_up = self.driver.find_element(By.CLASS_NAME, "download-speed").text  # Obtains the speed located in the element
        speed_down = self.driver.find_element(By.CLASS_NAME, "upload-speed").text
        return float(speed_up), float(speed_down)  # Returns the speed up and speed down

    def tweet_at_provider(self, speed_up, speed_down):  # THis function is responsible for tweeting the ISP
        self.driver.get("https://twitter.com/i/flow/login")  # Opens up the twitter login page
        self.time.sleep(5)
        self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]'
                                           '/div/div/div/div[5]/label/div/div[2]/div/input').send_keys(TWITTER_EMAIL)  # Email address is entered
        self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]'
                                           '/div[2]/div/div/div/div[6]').click()  # Clicks "next"
        self.time.sleep(3)
        try:  # Sometimes if unusual activity is detected, the Twitter login asks to verify your username.
            # The try block ensures that if that prompt does not show, then the program won't crash
            self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/'
                                               'div[2]/div[1]/div/div[2]/label/div/div[2]/div/input').send_keys(TWITTER_USERNAME)
            self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/'
                                               'div[2]/div[2]/div/div/div/div/div').click()
        finally:
            self.time.sleep(5)
            self.driver.find_element(By.NAME, "password").send_keys(TWITTER_PASSWORD)
            self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/'
                                               'div[2]/div[2]/div/div[1]/div/div/div/div').click()  # Password is entered then "login" is pressed
            self.time.sleep(5)
            self.driver.find_element(By.CLASS_NAME, "public-DraftStyleDefault-block").send_keys(f"Internet Service Provider,"
            f" why is my download speed {speed_down} Mbps and upload {speed_up} when the speed advertised was, {PROMISED_DOWN} "
            f"Mbps download and {PROMISED_UP} Mbps upload?")  # The message is written in the text box. To prevent spam, the actual internet service provider is not mentioned
            self.time.sleep(2)
            self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/'
                                               'div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]').click()  # The message is uploaded


bot = InternetSpeedTwitterBot(chrome_driver_path)  # A new instance of the class "InternetSpeedTwitterBot" is created

speed = bot.get_internet_speed()  # First, the internet speed is obtained
if speed[0] <= PROMISED_UP or speed[1] <= PROMISED_DOWN:  # If the upload or download speed is lower than expected, then the Twitter bot is activated
    bot.tweet_at_provider(speed[0], speed[1])
else:
    print("Speed meets or exceeds expectations!")
# This program was written by Sulav Rai