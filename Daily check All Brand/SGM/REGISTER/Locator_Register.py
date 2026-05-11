class RegisterSGM:
    #def __init__(self, browser):
     #   self.browser = browser
      #  self.page = browser.new_page()
    def __init__(self, page):
        self.page = page
        self.url = "https://www.generasimaju.co.id/klub-generasi-maju/register?referral=https://www.generasimaju.co.id/klub-generasi-maju"  # ← tambah self.
        page.goto(self.url)
        self.clickButtonLogin = page.locator("/html/body/nav/div/div[2]/div[2]/div[1]/div[3]/a[1]/span")
        self.clickButtonChookiesActive2 =page.locator("//button[@id='footer_tc_privacy_button']")
        self.InputMsisdn = page.locator("//input[@name='msisdn']")
        self.password = page.locator("//input[@name='password']")
        self.buttonMasuk = page.locator("//button[@id='handphone-submit']")
        self.buttonOTPclick = page.locator("//a[@class='btn btn-secondary full-width font-capitalize color-red font-bold font-underline']")
        self.kollomNomordiotp = page.locator("//input[@name='msisdn']")
        self.buttonMasukOTP = page.locator("//button[@id='handphone-otp-submit']")
        self.inputMasukinNomorOTP = page.locator("//input[@class='form-control text-center otp__box--inline']")
        self.otp_boxes = page.locator("//input[contains(@class,'otp__box--inline')]")
        self.buttonClickOTP = page.locator("//button[@id='kirim-otp']")
        self.InputFirstnamae = page.locator("//input[@name='firstname']")
        self.InputNoHpReg = page.locator("//input[@id='handphone']")
        self.InputPassword = page.locator("//input[@name='password']")
        self.clickKondisi = page.locator("//div[@id='kondisi-bunda']")
        self.optionHamil = page.locator("//div[contains(@class,'show-kondisi__all') and @data-pregnant='Y' and @data-child='N']")
        self.checkboxSetuju = page.locator("//input[@id='sayasetuju']")
        self.buttonDaftar = page.locator("//button[@id='register-new-kgm']")
        self.pesanBerhasil = page.locator("//div[contains(text(),'Selamat Berhasil')]")
        self.pesanSudahTerdaftar = page.locator("//div[contains(text(),'Sudah Terdaftar dan Terverifikasi')]")
        self.warningNama = page.locator("//input[@id='namalengkap']/following-sibling::div[contains(@class,'warning')]")
        self.warningPassword = page.locator("//div[contains(@class,'password-form')]")
        self.warningPhone = page.locator("//div[@id='phone_number-error']")
        self.radioKodeReferal = page.locator("//input[@name='is_code_refferal_event_code' and @value='refferal_code']")
        self.inputKodeReferalField = page.locator("//input[@id='kode_referal_kode_event']")

    #def clickButtonLogin(self):
#        self.ClickButtonLogin.click()

    #def clickButtonChookiesActive(self):
        #self.clickButtonChookiesActive2.click()
    #Login Bener
    def noHP(self,text):
        self.InputMsisdn.fill(text)
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
    def inputNamaPertama(self,text):
        self.InputFirstnamae.fill(text)
    def InputnoHP(self,text):
        self.InputNoHpReg.fill(text)
    def Inputpassword(self,text):
        self.InputPassword.fill(text)
    def ClickKondisi(self):
        self.clickKondisi.click()
    def ClickKondisiHamil(self):
        self.optionHamil.click()
    def PilihMinggu(self, week):
        # Select2 widget hides the native <select>; use jQuery trigger to set value
        self.page.evaluate(f"$('.usia-kehamilan').val('{week}').trigger('change')")
        self.page.locator("//input[@name='pregnancyweek']").evaluate(f"el => el.value = '{week}'")
    def ClickSetuju(self):
        self.checkboxSetuju.check()
    def ClickDaftar(self):
        self.buttonDaftar.click()
    def verifyWarningPhone(self, expected_text):
        actual = self.warningPhone.inner_text()
        assert actual == expected_text, f"✗ Warning phone: expected '{expected_text}', got '{actual}'"
        print(f"✓ Warning phone muncul: '{actual}'")
    def ClickKodeReferalRadio(self):
        self.radioKodeReferal.click()
    def IsiKodeReferal(self, kode):
        self.inputKodeReferalField.fill(kode)
    def verifyWarningPassword(self, expected_text):
        actual = self.warningPassword.inner_text()
        assert actual == expected_text, f"✗ Warning password: expected '{expected_text}', got '{actual}'"
        print(f"✓ Warning password muncul: '{actual}'")
    def verifyNoPasswordWarning(self):
        # Jika form diterima, halaman redirect ke login (password tanpa kapital dianggap valid)
        if "/login" in self.page.url:
            print("✓ Tidak ada warning password — form diterima dan redirect ke login")
            print("  Site tidak mensyaratkan huruf kapital pada password")
        else:
            actual = self.warningPassword.inner_text()
            assert actual == "", f"✗ Harusnya tidak ada warning password, tapi muncul: '{actual}'"
            print("✓ Tidak ada warning password — site tidak mensyaratkan huruf kapital")
    def verifyWarningNama(self, expected_text):
        actual = self.warningNama.inner_text()
        assert actual == expected_text, f"✗ Warning nama: expected '{expected_text}', got '{actual}'"
        print(f"✓ Warning nama muncul: '{actual}'")
    def verifyElementPresent(self):
        current_url = self.page.url
        assert "/login" in current_url, f"✗ URL tidak mengarah ke halaman login. URL sekarang: {current_url}"
        print(f"✓ URL redirect ke login: {current_url}")

        berhasil_visible = self.pesanBerhasil.is_visible()
        terdaftar_visible = self.pesanSudahTerdaftar.is_visible()

        assert berhasil_visible or terdaftar_visible, "✗ Tidak ada pesan konfirmasi yang muncul setelah klik Daftar"

        if berhasil_visible:
            print("✓ Registrasi berhasil: 'Selamat Berhasil, kini Bunda dapat melakukan Login Akun'")
        elif terdaftar_visible:
            print("✓ Akun sudah terdaftar: 'Akun Bunda Sudah Terdaftar dan Terverifikasi'")


