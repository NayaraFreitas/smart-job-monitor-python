import os
import time 
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def rodar_automacao_scraper():
    chrome_options = Options() 
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)

    lista_vagas = []
    titulos_desejados = ['analista de dados','python' , 'rpa']

    try:
        url_base = "https://www.geekhunter.com.br/vagas?page="
        pagina_do_site_atual = 1
        maximo_de_paginas = 5

       
        #Acessando a url base
        while pagina_do_site_atual <= maximo_de_paginas:
            print(f"Acessando a página {pagina_do_site_atual}")
            driver.get(f"{url_base}{pagina_do_site_atual}")
            time.sleep(4)

           

            #Navegando por cada das 5 paginas do site e coletando os dados
            print("Realizando scroll da pagina intera")
            ultima_altura = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(2)
                nova_altura = driver.execute_script("return document.body.scrollHeight")
                if nova_altura == ultima_altura:
                    break
                ultima_altura = nova_altura


            #Coletando Dados
            elementos_vagas = driver.find_elements(By.TAG_NAME, "a")

            if not elementos_vagas:
                elementos_vagas = driver.find_elements(By.TAG_NAME, "p")

            for item in elementos_vagas:
                texto_vaga = item.text.strip()

                if texto_vaga and len(texto_vaga) > 10:
                    if any(termo in texto_vaga.lower() for termo in titulos_desejados):
                        if{'titulo': texto_vaga} not in lista_vagas:
                            lista_vagas.append({'titulo':texto_vaga})

            pagina_do_site_atual += 1
            time.sleep(2)

            
            #Salvando as vagas encontradas em um csv todas de uma vez
            if lista_vagas:
                df = pd.DataFrame(lista_vagas)

                diretorio_destino = "../data/raw"
                os.makedirs(diretorio_destino, exist_ok=True)

                caminho_final = os.path.join(diretorio_destino, "vagas_geekhunter.csv")
                df.to_csv(caminho_final, index=False, encoding='utf-8')

                print(f"\n[Sucesso] Monitoramento concluipd! {len(lista_vagas)} vagas  salvas em: {caminho_final} ")
            else:
                print(f"\n[Eviso] Nenhuma vaga correpondente aos filtro foi encontrada.")

    except Exception as e:
        print(f"[Erro] Falha na execução: {e}")

    finally:
        print("[INFO] Finalizando o webdriver...")
        driver.quit()

if __name__ == '__main__':
    rodar_automacao_scraper()