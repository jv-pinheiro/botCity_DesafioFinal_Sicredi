from selenium.webdriver.common.keys import Keys
from botcity.web import WebBot, Browser, By
from dotenv import load_dotenv
from botcity.maestro import *
import pandas as pd
import os

#Carrega variáveis do .env
load_dotenv()

class AlterarSLA(WebBot):
    def action(self, execution=None):
        #Conecta ao Orquestrador
        maestro = BotMaestroSDK.from_sys_args()
        execution = maestro.get_execution()

        #Credenciais no arquivo .env
        USER = os.getenv("SESUITE_USER")
        PASSWORD = os.getenv("SESUITE_PASS")
        URL = os.getenv("SESUITE_URL")

        self.headless = False
        self.browser = Browser.EDGE
        self.driver_path = r"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedgedriver.exe"

        #Abre site do SeSuite
        self.browse(URL)

        #Preenche login e senha, e clica em entrar
        self.find_element('user', By.ID).send_keys(USER)
        self.find_element('password', By.ID).send_keys(PASSWORD)
        self.find_element('//*[@id="loginButton"]/span/div', By.XPATH).click()

        #Fecha alerta, se ocorrer
        alert_btn = self.find_element('button#alertConfirm > span > div > span', By.CSS_SELECTOR)
        if alert_btn:
            alert_btn.click()

        #Ler planilha de chamados
        chamados = pd.read_excel("chamados.xlsx")

        resultados = []
        #Varre os chamados
        for _, row in chamados.iterrows():
            chamado_id = str(row["chamado_id"])
            nova_data = str(row["nova_data"])
            justificativa = row["justificativa"]
            try:
                #Abre gestão de workflows
                self.browse("https://sesuite.sicredi.com.br/softexpert/workspace?page=tracking,104,2")

                #Entra no iframe da barra de pesquisa
                iframe = self.find_element("iframe", By.TAG_NAME)
                self.enter_iframe(iframe)

                #Pesquisa pelo chamado
                search = self.find_element('//*[@id="bc_quick_filter"]', By.XPATH)
                search.send_keys(chamado_id)
                search.send_keys(Keys.ENTER)

                #Aguarda carregamento e clica no chamado
                self.wait(2000)
                self.find_element('//*[@id="t_content_gridframe"]/tbody/tr/td[10]', By.XPATH).click()

                #Clica em "Redefinir prazo"
                self.wait(2000)
                self.find_element('//*[contains(text(), "Redefinir prazo")]', By.XPATH).click()

                #Confirma alert
                self.driver.switch_to.alert.accept()

                #Troca para iframe do modal (campos de mudança de prazo e justificativa)
                self.leave_iframe()
                modal = self.find_element('cardModalFrame', By.ID)
                self.enter_iframe(modal)

                #Preenche data
                self.find_element('//*[@id="dateActivityTerm"]', By.XPATH).send_keys(nova_data)

                # Preenche justificativa
                self.find_element('//*[@id="justifActivityTerm"]', By.XPATH).send_keys(justificativa)

                #Confirma alteração
                self.find_element('//*[@id="modal_activityTerm"]/div/button[1]', By.XPATH).click()

                resultados.append([chamado_id, "OK"])
            except Exception as e:
                resultados.append([chamado_id, f"ERRO: {e}"])

        #Salva log da execução como planilha (.xlsx)
        pd.DataFrame(resultados, columns=["Chamado", "Status"]).to_excel("resultado_execucao.xlsx", index=False)

        #Reporta ao Orquestrador
        maestro.post_artifact(
            task_id=execution.task_id,
            artifact_name="resultado_execucao.xlsx",
            filepath="resultado_execucao.xlsx"
        )
        #Finaliza execução
        maestro.finish_execution(execution.execution_id)
if __name__ == '__main__':
    AlterarSLA().action()