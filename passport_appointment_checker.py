from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import inspect
import logging
import os


class PassportAppointmentChecker(object):

    def __init__(self, screenshots_dir, number_of_days = 7):
        self.driver = None
        self.screenshots_dir = screenshots_dir
        self.number_of_days = number_of_days

    def check_available_slots_for_spanish_passport_issuance(self):
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        option.add_argument("disable-infobars")
        option.add_argument("--disable-extensions")
        option.add_argument("--disable-dev-shm-usage")
        option.add_argument("--no-sandbox")   
        self.driver = webdriver.Chrome(os.environ['CHROMEDRIVER_PATH'], options=option)
        #self.driver = webdriver.Chrome(options=option)
        try:
            result = self._try_to_scrap_availability_info_fron_site_(self.number_of_days)
            logging.info(f"Availability {vars(result)}")
        except Exception as e:
            logging.error(e)
            result = AvailabilityCheckResult(is_slot_available=False)
        self.driver.save_screenshot(f"{self.screenshots_dir}/{datetime.now()}.png")
        self.driver.quit()
        return result

    def _try_to_scrap_availability_info_fron_site_(self, number_of_days):
        # Enter spanish consulate page
        spanish_consulate_website='http://www.exteriores.gob.es/Consulados/MONTEVIDEO/es/ServiciosConsulares/Pasaporte_y_Matricula_Uruguay/Paginas/default.aspx'
        self.driver.get(spanish_consulate_website)

        # Click on appointments icon.
        get_appointment_image_name='/Consulados/MONTEVIDEO/es/PublishingImages/CitaPrevia.png'
        self.driver.find_element_by_xpath(f"//a[img/@src='{get_appointment_image_name}']").click()

        # A new window will open for that appointment, switch to that window.
        new_appointments_window = self.driver.window_handles[-1]
        self.driver.switch_to.window(new_appointments_window)

        # Wait for page to be loaded.
        self._wait_for_loader_to_disappear_("clsBktWidgetDefaultLoading")
        self._wait_for_passport_appointment_link_()

        # Go to appointments link.
        self._click_on_make_appointment_link_()

        # Wait for page to be loaded.
        self._wait_for_loader_to_disappear_("clsDivBktWidgetDefaultLoading")

        # Check the calendar for the next days, determined by the parameter
        availability_check_result = self._check_availability_for_n_days_(number_of_days)

        return availability_check_result

    def _click_on_make_appointment_link_(self):
        try:
            link = self.driver.find_element(By.CSS_SELECTOR, "a[href*='bkt218867']")
            link.click()
        except Exception as e:
            raise self._scraping_exception_(e)

    def _wait_for_passport_appointment_link_(self):
        try:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Pasaportes y Alta Consular')]")))
        except TimeoutException as e:
            raise self._scraping_exception_(e)

    def _check_availability_for_n_days_(self,n):
        for i in range(n):
            available_today = self._today_has_any_availability_slots_()
            if available_today:
                date_found = self.driver.find_element_by_id("idDivBktDatetimeSelectedDate").text
                image_path = f"{self.screenshots_dir}/suspicious_screen.png"
                self.driver.save_screenshot(image_path)
                return AvailabilityCheckResult(is_slot_available=True, available_day=date_found, image_path=image_path)
            self.driver.find_element_by_id("idDivBktDatetimeSelectedDateRight").click()
        return AvailabilityCheckResult(is_slot_available=False)

    def _today_has_any_availability_slots_(self):
        try:
            not_available_slots_message = self.driver.find_element_by_id("idDivNotAvailableSlotsTextTop")
            return not_available_slots_message is None
        except Exception:
            return True ## Not available dates message, we need to announce it

    def _wait_for_loader_to_disappear_(self, loaderName, timeout = 20):
        try:
            WebDriverWait(self.driver, timeout).until_not(EC.presence_of_element_located((By.CLASS_NAME, loaderName)))
        except TimeoutException as e:
            raise self._scraping_exception_(e)

    def _scraping_exception_(self, exception):
        raise AvailabilityCheckingException(f"[{inspect.stack()[1][3]}] {str(exception)}")

class AvailabilityCheckResult(object):
    def __init__(self, is_slot_available, image_path=None, available_day=None):
        self.is_slot_available = is_slot_available
        self.available_day = available_day
        self.image_path = image_path

class AvailabilityCheckingException(Exception):
    pass




