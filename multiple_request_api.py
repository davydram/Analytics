##Executar direto no terminal pois irá precisar destas bibliotecas para consumir a API
#pip install requests
#pip install requests-toolbelt
#pip install pandas
#pip install pyautogui

import requests
import json
import pandas as pd
import numpy as np
import os, zipfile
import urllib

for ano in range(2016, 2017):

    ano = str(ano)

    print('baixando grupo de receitas: ')

    listarequests = {"listarunidade":"listaUnidade" ,
                    "listarsubunidade": "listaSubunidade",
                    "listargrupofonte":"listaGrupoFonte",
                    "listarfonterecurso":"listaFonte"}

    diretorio_raiz = 'C:/DataMartBase/Input/'

    if not os.path.exists(diretorio_raiz):
        os.makedirs(diretorio_raiz)
        print("Directory " , diretorio_raiz ,  " Created ")
    else:    
        print("Directory " , diretorio_raiz ,  " already exists")


    
    for k, v in listarequests.items():
        print(f'inciando solicitação de {k} ')

        solicitacao = k #a que se refere os dados no portal
        schemmalevel = v
        endpoint = "ws/receitas/" + solicitacao

        url = "http://www.transparencia.pr.gov.br/pte/"+endpoint+"?exercicio="+ano
        print(url)

        response = requests.get(url) 
        response = response.json()
        json_string = json.dumps(response[schemmalevel])
        nome_arquivo = 'receita_'+solicitacao+'_'+ano

        diretorio = diretorio_raiz+'/'+endpoint+'/'+ano+'/'

        if not os.path.exists(diretorio):
            os.makedirs(diretorio)
            print("Directory " , diretorio ,  " Created ")
        else:    
            print("Directory " , diretorio ,  " already exists")

        #salvar o JSON
        with open(diretorio+nome_arquivo+'.json', 'w') as outfile:
            outfile.write(json_string) 
            
        #transformar o JSON em CSV
        with open(diretorio+nome_arquivo+'.json', encoding='utf-8') as inputfile:
            df = pd.read_json(inputfile)    
            df.to_csv(diretorio+nome_arquivo+'.csv', encoding='utf-8', index=False)

        
        print(f'{k} baixada com sucesso')


    print('baixando grupo de despesas: ')

    listarequests = {'listardespesa':'listaDespesa',
                    'listarelementodespesa':'listaElemento'}


    for k, v in listarequests.items():
        print(f'inciando solicitação de {k} ')


        solicitacao = k #a que se refere os dados no portal
        schemmalevel = v
        mes = False
        endpoint = "ws/despesas/" + solicitacao
    
        if solicitacao == 'listardespesa': 

            mes = True 
            diretorio = diretorio_raiz+'/'+endpoint+'/'+ano+'/'
            
            if not os.path.exists(diretorio):
                os.makedirs(diretorio)
                print("Directory " , diretorio ,  " Created ")
            else:    
                print("Directory " , diretorio ,  " already exists")

            if mes == True:        
                for m in range(1, 13):
                    url = "http://www.transparencia.pr.gov.br/pte/"+endpoint+"?exercicio="+ano+"&mes="+str(m)
                    response = requests.get(url) 
                    response = response.json()
                    json_string = json.dumps(response[schemmalevel])
                    nome_arquivo = 'desp-'+solicitacao+'-'+ano+'-'+str(m)

                    #salvar o JSON
                    with open(diretorio+nome_arquivo+'.json', 'w') as outfile:
                        outfile.write(json_string) 
                        
                    #transformar o JSON em CSV            
                    with open(diretorio+nome_arquivo+'.json', encoding='utf-8') as inputfile:
                        df = pd.read_json(inputfile)    
                        df.to_csv(diretorio+nome_arquivo+'.csv', encoding='utf-8', index=False)
                    
                    print(f'{k} ano: {ano} - mes: {str(m)} baixada com sucesso')

    
        else:
            solicitacao = solicitacao #a que se refere os dados no portal
            endpoint = "ws/despesas/" + solicitacao
            diretorio = diretorio_raiz+'/'+endpoint+'/'+ano+'/'
            mes = False
            
            if not os.path.exists(diretorio):
                os.makedirs(diretorio)
                print("Directory " , diretorio ,  " Created ")
            else:    
                print("Directory " , diretorio ,  " already exists")
    
            url = "http://www.transparencia.pr.gov.br/pte/"+endpoint+"?exercicio="+ano
            print(url)

            response = requests.get(url) 
            response = response.json()
            json_string = json.dumps(response[schemmalevel])
            nome_arquivo = 'despesa_'+solicitacao+'_'+ano

            #salvar o JSON
            with open(diretorio+nome_arquivo+'.json', 'w') as outfile:
                outfile.write(json_string) 
                
            #transformar o JSON em CSV
            with open(diretorio+nome_arquivo+'.json', encoding='utf-8') as inputfile:
                df = pd.read_json(inputfile)    
                df.to_csv(diretorio+nome_arquivo+'.csv', encoding='utf-8', index=False)
            
            print(f'{k} baixada com sucesso')

    #outras bases que nao puderam ser baixadas por API:


    #VIAGENS:

    url='http://www.transparencia.download.pr.gov.br/exportacao/VIAGENS/VIAGENS-'+ano+'.zip?windowId=6eb'

    diretorio = 'C:/DataMartBase/Input/outras_fontes/viagens/'+ano+'/'
    nome_arquivo = url.split('/')[-1].replace(" ", "_").split('?')[0]
    print(nome_arquivo)
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
        print("Directory " , diretorio ,  " Created ")
    else:    
        print("Directory " , diretorio ,  " already exists")

    urllib.request.urlretrieve(url, diretorio+nome_arquivo)


    dir_name = diretorio 
    extension = ".zip"

    os.chdir(dir_name) # change directory from working dir to dir with files

    for item in os.listdir(dir_name): # loop through items in dir
        if item.endswith(extension): # check for ".zip" extension
            file_name = os.path.abspath(item) # get full path of files
            zip_ref = zipfile.ZipFile(file_name) # create zipfile object
            zip_ref.extractall(dir_name) # extract file to dir
            zip_ref.close() # close file
            os.remove(file_name) # delete zipped file




    #RENUMERACOES

    url='http://www.transparencia.download.pr.gov.br/exportacao/REMUNERACAO_RH/REMUNERACAO_RH.zip?windowId=3f7'

    diretorio = 'C:/DataMartBase/Input/outras_fontes/remuneracao_rh/'
    nome_arquivo = url.split('/')[-1].replace(" ", "_").split('?')[0]
    print(nome_arquivo)
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
        print("Directory " , diretorio ,  " Created ")
    else:    
        print("Directory " , diretorio ,  " already exists")

    urllib.request.urlretrieve(url, diretorio+nome_arquivo)

    dir_name = diretorio 
    extension = ".zip"

    os.chdir(dir_name) # change directory from working dir to dir with files

    for item in os.listdir(dir_name): # loop through items in dir
        if item.endswith(extension): # check for ".zip" extension
            file_name = os.path.abspath(item) # get full path of files
            zip_ref = zipfile.ZipFile(file_name) # create zipfile object
            zip_ref.extractall(dir_name) # extract file to dir
            zip_ref.close() # close file
            os.remove(file_name) # delete zipped file


    #RECEITAS PQ A API NAO FUNCIONOU


    url='http://www.transparencia.download.pr.gov.br/exportacao/RECEITAS/RECEITAS-'+ano+'.zip?windowId=554'

    diretorio = 'C:/DataMartBase/Input/outras_fontes/receitas/'+ano+'/'
    nome_arquivo = url.split('/')[-1].replace(" ", "_").split('?')[0]
    print(nome_arquivo)
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
        print("Directory " , diretorio ,  " Created ")
    else:    
        print("Directory " , diretorio ,  " already exists")

    urllib.request.urlretrieve(url, diretorio+nome_arquivo)

    dir_name = diretorio 
    extension = ".zip"

    os.chdir(dir_name) # change directory from working dir to dir with files

    for item in os.listdir(dir_name): # loop through items in dir
        if item.endswith(extension): # check for ".zip" extension
            file_name = os.path.abspath(item) # get full path of files
            zip_ref = zipfile.ZipFile(file_name) # create zipfile object
            zip_ref.extractall(dir_name) # extract file to dir
            zip_ref.close() # close file
            os.remove(file_name) # delete zipped file
print('finalizado')


