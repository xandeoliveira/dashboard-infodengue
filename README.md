# Dashboard de Análise de Casos de Dengue

Este projeto implementa um dashboard interativo utilizando **Streamlit** para análise de dados relacionados aos casos de dengue nas cidades de **Acarape** e **Redenção**. O dashboard permite ao usuário selecionar um ano e um mês específicos para visualizar os dados de casos de dengue em formato de tabela.

## Funcionalidades
- O usuário pode selecionar entre duas cidades: **Acarape** ou **Redenção**.
- Ao escolher a cidade, o dashboard exibe um conjunto de opções para selecionar o **ano** e o **mês**.
- O dashboard filtra e exibe os dados correspondentes ao ano e mês selecionados, permitindo a visualização de tendências sazonais de dengue. (ainda não implementado)
- Os dados são carregados a partir de arquivos CSV, cujos dados coletados são provenientes do **Infodengue** ([https://info.dengue.mat.br](https://info.dengue.mat.br)), com a possibilidade de visualização interativa dos mesmos.

## Tecnologias
- **Python**
- **Streamlit** (para criação do dashboard)
- **Pandas** (para manipulação de dados)
