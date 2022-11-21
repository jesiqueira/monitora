# `Monitora`: Controle de estoque e monitoramento de equipamento on site
---
> STATUS: Em desenvolvimento
----
## - Descrição do Projeto
- O Sistema Monitora é uma aplicação Web voltado para:
  > 1. Controle dos Desktop que estão alocado no site 
  > 2. Controlar o estoque da empresa
---
## Funcionalidade
- `Monitora` é um sistema para controlar o estoque, facilitar o controle de mudanças dos equipamento entre estoque para empresas que tem mais de um estoque.
- `Monitora` tem como  principal objetivo facilitar o monitoramento dos Desktop que estão no site e evitar problema com armazenamento de informações do estoque em planilhas, será um facilitador no trabalho dos analistas de suporte com as seguintes funcionalidades:
  > 1. Cadastrar e atualizar estoque.
  > 1. Irá integrar os estoque caso a empresa tenha mais de um.
  > 1. Monitorar os equipamentos/Desktop que estão configurado no AD e instalado no site/operação.

## Sobre o monitoramento
- O sitema irá realizar scanner em uma rede de computadores local onde dependendo da resposta o sistema irá atualizar o Banco de Dados alterando o Status dos equipamento para `TRUE` ou `FALSE` ou seja está ok ou com falha. 
- A partir dessa resposta o sistema erá mostrar em uma tela os seguintes `STATUS`:
  > 1. Aprovado
  > 1. Atenção;
  > 1. Fora de conformida;
- A partir desses status o analista será capaz de identificar de forma fácil qual é o equipamento que requer correção e atuar protualmente, evitando que computador deixe de receber atualização de segurança e falha no controle.

## Tecnologias usadas para esse desenvolvimeno
- Python
- SQLAlchemy
- Flask
- HTML
- CSS
- javaScript
- Bootstrap
- Banco de Dados relacional de escolha no momento do desenvolvimento estou usando `SQLITE` por ser leve e não precisar de um SGBD instalado no equipamento para desenvolver aplicação.







