import undetected_chromedriver as uc
options = uc.ChromeOptions()
options.arguments.extend(["--no-sandbox", "--disable-setuid-sandbox"])     # << this
driver = uc.Chrome(options)
print("open")
driver.get("https://nowsecure.nl/")
driver.save_screenshot("/app/flac/hi.png")
print("hi")