from selenium import webdriver
from selenium.webdriver.chrome.options import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType

import time

co = webdriver.ChromeOptions()

co.add_argument("log-level=3")
co.add_argument("--disable-blink-features=AutomationaControlled")
#co.add_argument("--headless")

def get_proxies(co=co):
   
    driver = webdriver.Chrome(executable_path='I:\Scalper\chromedriver.exe', chrome_options=co)
    
    driver.get("")

    PROXIES = []
    proxies = driver.find_elements_by_css_selector("tr[role='row']")
    for p in proxies:
        result = p.text.split(" ")

        if result[-1] == "yes":
            PROXIES.append(result[0]+":"+result[1])

    driver.close()
    return PROXIES


ALL_PROXIES = get_proxies()
print(ALL_PROXIES)

def proxy_driver(PROXIES, co=co):
    prox = Proxy()

    if len(PROXIES) < 1:
        print("--- Proxies used up (%s)" % len(PROXIES))
        PROXIES = get_proxies()
        
    pxy = PROXIES[-1]

    prox.proxy_type = ProxyType.MANUAL
    prox.http_proxy = pxy
    
    prox.ssl_proxy = pxy

    capabilities = webdriver.DesiredCapabilities.CHROME
    prox.add_to_capabilities(capabilities)

    driver = webdriver.Chrome(executable_path='I:\Scalper\chromedriver.exe', chrome_options=co, desired_capabilities=capabilities)
    print(driver)
    return driver

# --- YOU ONLY NEED TO CARE FROM THIS LINE ---
# creating new driver to use proxy
pd = proxy_driver(ALL_PROXIES)

# code must be in a while loop with a try to keep trying with different proxies
running = True
driver = webdriver.Chrome(executable_path='I:\Scalper\chromedriver.exe', chrome_options=co)

    
while running:
    try:
         
        addToCartBtn = driver.find_element_by_xpath("//form[@id='test']/button")
        #Button isn't open, restart the script
        print("Button isn't ready yet.")
        #Refresh page after a delay
        time.sleep(1)
        driver.refresh()
    
    except:
        new = ALL_PROXIES.pop()
        
        # reassign driver if fail to switch proxy
        pd = proxy_driver(ALL_PROXIES)
        print("--- Switched proxy to: %s" % new)
        time.sleep(1)

        #Find & Click the button
        
        driver.find_element_by_xpath("//form[@id='test']/button").click()
        print("Found & Clicked Add to Cart")
        time.sleep(1)
        #go to cart
        driver.get("")
        time.sleep(5)
        driver.find_element_by_xpath("//a[@data-automation='continue-to-checkout']").click()
        print("Found & Clicked Continue to Checkout")
        time.sleep(5)
        #click continue as guest
        driver.find_element_by_xpath("//a[@target='_self']/span").click()
        print("Found & Clicked Continue to Checkout as Guest")
        time.sleep(5)
        
        #input information
        driver.finde_elements_by_xpath("//input[@id='email']").click().send_keys(data[0])
        time.sleep(1)
        driver.finde_elements_by_xpath("//input[@id='firstName']").click().send_keys(data[1])
        time.sleep(1)
        driver.finde_elements_by_xpath("//input[@id='lastName']").click().send_keys(data[2])
        time.sleep(1)
        driver.finde_elements_by_xpath("//input[@id='addressLine']").click().send_keys(data[3])
        time.sleep(1)
        driver.finde_elements_by_xpath("//input[@id='city']").click().send_keys(data[4])
        time.sleep(1)
        driver.finde_elements_by_xpath("//input[@id='postalCode']").click().send_keys(data[5])      
        time.sleep(1)
        driver.finde_elements_by_xpath("//input[@id='phone']").click().send_keys(data[6])
        time.sleep(1)
        driver.find_element_by_xpath("//select[@name='regionCode']/option[text()='Ontario']").click()
        #wait 1 second after inputting
        time.sleep(2)
        driver.find_element_by_xpath("//section[@class='cost-sum-section']/button").click()
        time.sleep(5)
        print("Input Information for delivery")
        
        #payment page
        driver.finde_elements_by_xpath("//div[@class='false']/select[@name='shownCardNumber']").click().send_keys("1234-1234-1234-1234") #input card num
        time.sleep(1)        
        driver.find_element_by_xpath("//select[@name='expirationMonth']/option[text()='12']").click()
        time.sleep(1)        
        driver.find_element_by_xpath("//select[@name='expirationYear']/option[text()='1234']").click()
        time.sleep(1)        
        driver.finde_elements_by_xpath("//div[@class='false']/input[@name='cvv']").click().send_keys("123") #input cvv
        time.sleep(2)
        driver.find_element_by_xpath("//section[@class='cost-sum-section']/button").click()
        time.sleep(4)
        
        driver.find_element_by_xpath("//section[@class='cost-sum-section']/button").click()
        print("Order placed.")
        running = False