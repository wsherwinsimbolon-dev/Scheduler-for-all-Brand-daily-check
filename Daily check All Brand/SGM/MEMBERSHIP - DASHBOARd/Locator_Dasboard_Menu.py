class MembershipDashboard:
    #def __init__(self, browser):
     #   self.browser = browser
      #  self.page = browser.new_page()
    def __init__(self, page):
        self.page = page
        self.url = "https://www.generasimaju.co.id/klub-generasi-maju/login"  # ← tambah self.
        page.goto(self.url)
        self.clickButtonLogin = page.locator("/html/body/nav/div/div[2]/div[2]/div[1]/div[3]/a[1]/span")
        self.clickButtonChookiesActive2 =page.locator("//button[@id='footer_tc_privacy_button']")
        self.InputnoHP = page.locator("//input[@name='msisdn']")
        self.password = page.locator("//input[@name='password']")
        self.buttonMasuk = page.locator("//button[@id='handphone-submit']")
        self.buttonOTPclick = page.locator("//a[@class='btn btn-secondary full-width font-capitalize color-red font-bold font-underline']")
        self.kollomNomordiotp = page.locator("//input[@name='msisdn']")
        self.buttonMasukOTP = page.locator("//button[@id='handphone-otp-submit']")
        self.inputMasukinNomorOTP = page.locator("//input[@class='form-control text-center otp__box--inline']")
        self.otp_boxes = page.locator("//input[contains(@class,'otp__box--inline')]")
        self.buttonClickOTP = page.locator("//button[@id='kirim-otp']")
        self.ClickProfileDashboard = page.locator("//span[@class='motherName']")
        self.clickXbutton = page.locator("//button[@onclick='closepopupthankyou()']")

    #def clickButtonLogin(self):
#        self.ClickButtonLogin.click()

    #def clickButtonChookiesActive(self):
        #self.clickButtonChookiesActive2.click()
    #Login Bener
    def noHP(self,text):
        self.InputnoHP.fill(text)
    def pasWort(self,text):
        self.password.fill(text)
    def tombolMasuk(self):
        self.buttonMasuk.click()
    def tombolOTPclick(self):
        self.buttonOTPclick.click()
    def kolomHP(self,text):
        self.kollomNomordiotp.fill(text)
    def buttonClickMasukOTP(self):
        self.buttonMasukOTP.click()
    def inputMasukinOTP(self,text):
        self.inputMasukinNomorOTP.fill(text)
    def inputMasukinOTPboxes(self, otp_code):
        for i, digit in enumerate(str(otp_code)):
            self.otp_boxes.nth(i).fill(digit)
    def buttonClickOTPSekarang(self):
        self.buttonClickOTP.click()
    def ClickProfileDashboardmember(self):
        self.ClickProfileDashboard.click()
    def clickXbuttonprofile(self):
        self.clickXbutton.dblclick()


