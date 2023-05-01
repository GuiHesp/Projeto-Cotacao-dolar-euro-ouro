#!/usr/bin/env python
# coding: utf-8

# # Automação Web e Busca de Informações com Python
# 
# #### Desafio: 
# 
# Trabalhamos em uma importadora e o preço dos nossos produtos é vinculado a cotação de:
# - Dólar
# - Euro
# - Ouro
# 
# Precisamos pegar na internet, de forma automática, a cotação desses 3 itens e saber quanto devemos cobrar pelos nossos produtos, considerando uma margem de contribuição que temos na nossa base de dados.
# 
# Base de Dados: https://drive.google.com/drive/folders/1KmAdo593nD8J9QBaZxPOG1yxHZua4Rtv?usp=sharing
# 
# Para isso, vamos criar uma automação web:
# 
# - Usaremos o selenium
# - Importante: baixar o webdriver

# In[24]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

navegador = webdriver.Chrome()

#cotacao dólar
navegador.get('https://www.google.com.br/')
navegador.find_element(By.XPATH, '//*[@id="APjFqb"]').send_keys('cotação dólar')
navegador.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[4]/center/input[1]').click()
cotacao_dolar = navegador.find_element(By.XPATH, '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')
print(cotacao_dolar)

#cotacao euro
navegador.get('https://www.google.com.br/')
navegador.find_element(By.XPATH, '//*[@id="APjFqb"]').send_keys('cotação euro')
navegador.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[4]/center/input[1]').click()
cotacao_euro = navegador.find_element(By.XPATH, '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')
print(cotacao_euro)

#cotacao ouro
navegador.get('https://dolarhoje.com/ouro-hoje/')
cotacao_ouro = navegador.find_element(By.XPATH, '//*[@id="nacional"]').get_attribute('value')
cotacao_ouro = cotacao_ouro.replace(",", ".")
print(cotacao_ouro)

cotacao_dolar = float(cotacao_dolar)
cotacao_dolar = f'{cotacao_dolar:.2f}'

cotacao_euro = float(cotacao_euro)
cotacao_euro = f'{cotacao_euro:.2f}'

print(f'Nova cotação do Euro:{cotacao_euro}')
print(f'Nova cotação do Euro:{cotacao_dolar}')


# ### Agora vamos atualiza a nossa base de preços com as novas cotações

# - Importando a base de dados

# In[25]:


import pandas as pd

tabela_produtos = pd.read_excel(r'Produtos.xlsx')
display(tabela_produtos)


# - Atualizando os preços e o cálculo do Preço Final

# In[26]:


#atualizar coluna de cotação
tabela_produtos.loc[tabela_produtos["Moeda"] == "Dólar", "Cotação"] = float(cotacao_dolar)

#atualizar a coluna de preço de compra = preço original * cotação
tabela_produtos.loc[tabela_produtos["Moeda"] == "Euro", "Cotação"] = float(cotacao_euro)

#atualizar a coluna de preço de venda = preço de compra * margem
tabela_produtos.loc[tabela_produtos["Moeda"] == "Ouro", "Cotação"] = float(cotacao_ouro)

#preço compra e venda
tabela_produtos["Preço de Compra"] = tabela_produtos["Preço Original"] * tabela_produtos["Cotação"]
tabela_produtos["Preço de Venda"] = tabela_produtos["Preço de Compra"] * tabela_produtos["Margem"]

display(tabela_produtos)


# ### Agora vamos exportar a nova base de preços atualizada

# In[27]:


#formatar os valores
tabela_produtos["Preço Original"] = tabela_produtos["Preço Original"].map("R$ {:,.2f}".format)
tabela_produtos["Preço de Compra"] = tabela_produtos["Preço de Compra"].map("R$ {:,.2f}".format)
tabela_produtos["Preço de Venda"] = tabela_produtos["Preço de Venda"].map("R$ {:,.2f}".format)

display(tabela_produtos)


# In[28]:


tabela_produtos.to_excel("Produtos Novo.xlsx", index=False)

