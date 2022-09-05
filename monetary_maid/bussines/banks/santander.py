import json
from time import sleep

from loguru import logger
from selenium import webdriver


class Santanders:
    def __init__(self, cpf, senha):
        self.cpf = cpf
        self.senha = senha
        self.driver = webdriver.Chrome()

    def __repr__(self):
        return str(self.cpf)

    def logout(self):
        self.driver.switch_to.default_content()
        el = self.driver.find_element_by_xpath("//a[@title='Sair']")
        el.click()
        el = self.driver.find_element_by_xpath("//a[@id='closeMessageLogoutSim']")
        el.click()
        return False

    def login(self, SITE):
        self.driver.get(SITE)
        sleep(3)
        self.driver.set_window_size(1240, 981)

        el = self.driver.find_element_by_xpath("//input[@placeholder='Insira seu CPF']")
        el.click()
        el.clear()
        el.send_keys(self.cpf)

        el = self.driver.find_element_by_xpath(
            "//*[@id='appHeader']/header/login-field/div/form/div/div/div[1]/div/icon-circle-arrow/div"
        )
        el.click()
        sleep(3)
        el = self.driver.find_element_by_id("senha")
        el.click()
        el.clear()
        el.send_keys(self.senha)
        el = self.driver.find_element_by_id("Entrar")
        el.click()
        sleep(60)

        logger.info("Login com sucesso!")


# //*[@id="rejeiteTarjaLightboxHome"]/img     -

# el = self.driver.find_element_by_xpath(
#     "//input[@name='auxiliar.password']/../following-sibling::div[1]//input[@value='Acessar']"
# )
# el.click()

# logger("Aguardando Verificação manual com QR code")
# sleep(120)


# def get_balance(self):
#     if not wait_for_element_by_xpath(
#         self.driver,
#         "//div[text()='Saldo Disponível']/following-sibling::div[1]//span",
#     ):
#         return {
#             "status": False,
#             "msg": "Quadro com `Saldo Disponível` não encontrado!",
#             "block": False,
#         }
#     return {
#         "status": True,
#         "output": {
#             "balance": self.driver.find_element_by_xpath(
#                 "//div[text()='Saldo Disponível']/following-sibling::div[1]//span"
#             ).text
#         },
#     }


# def get_extrato(self):
#     end_date = datetime.now()
#     start_date = (end_date - timedelta(days=90)).strftime("%d/%m/%Y")

#     if not wait_for_element_by_xpath(
#         self.driver, '//span[text()="Conta Corrente"]/ancestor::a[1]'
#     ):
#         return {
#             "status": False,
#             "block": False,
#             "msg": "Conta sem acesso ao menu `Conta corrente`!",
#             "retry": False,
#         }

#     sleep(3)

#     el = self.driver.find_element_by_xpath(
#         '//span[text()="Conta Corrente"]/ancestor::a[1]'
#     )
#     el.click()

#     if not wait_for_element_by_xpath(
#         self.driver, '//a[contains(text(),"(Money)")]'
#     ):
#         return {
#             "status": False,
#             "block": True,
#             "msg": "Conta sem acesso ao menu `Exportar ofx (Money)`!",
#             "retry": False,
#         }

#     sleep(3)

#     el = self.driver.find_element_by_xpath('//a[contains(text(),"(Money)")]')
#     el.click()

#     self.driver.switch_to.default_content()
#     switch_to_frame_by_xpath_if_exists(self.driver, '//*[@id="Principal"]')
#     switch_to_frame_by_xpath_if_exists(self.driver, '//*[@id="frmSet"]/frame[3]')
#     switch_to_frame_by_xpath_if_exists(self.driver, '//*[@id="iframePrinc"]')

#     if not wait_for_element_by_xpath(
#         self.driver, '//input[@id="txtDataInicalPesquisa"]'
#     ):
#         return {
#             "status": False,
#             "block": False,
#             "msg": "Erro ao carregar página `Exportar ofx (Money)`!",
#         }

#     el = self.driver.find_element_by_xpath('//input[@id="txtDataInicalPesquisa"]')
#     el.send_keys(start_date)

#     el = self.driver.find_element_by_xpath('//input[@id="txtDataFinalPesquisa"]')
#     el.send_keys(end_date.strftime("%d/%m/%Y"))

#     el = self.driver.find_element_by_xpath('//a[text()="exportar"]')
#     el.click()

#     if not wait_for_clickable_element_by_xpath(
#         self.driver, "//input[@onclick=\"Seleciona('3');\"]"
#     ):
#         return {
#             "status": False,
#             "block": False,
#             "msg": "Erro ao selecionar formato `Money 2000 ou superior`!",
#         }
#     el = self.driver.find_element_by_xpath("//input[@onclick=\"Seleciona('3');\"]")
#     el.click()

#     el = self.driver.find_element_by_xpath('//a[text()="exibir"]')
#     el.click()

#     sleep(7.8)
#     if check_exists_by_xpath(
#         self.driver,
#         '//*[contains(text(),"Não há lançamentos desta conta corrente para o período solicitado")]',
#     ):
#         return {"status": True, "output": {"file": None}}
#     self.driver.execute_script("Seleciona('3'); SeleConf();")

#     wait_download_all_files(self.download_folder)
#     file_path = f"{self.download_folder}/extrato.ofx"
#     if not file_exists(file_path):
#         return {
#             "status": False,
#             "block": False,
#             "msg": "Ocorreu um erro ao baixar o OFX!",
#         }

#     return {"status": True, "output": {"file": file_path}}
