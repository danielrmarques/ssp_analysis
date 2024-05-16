# ssp_analysis
Projeto usado para analisar os dados de veículos e celulares subtraídos em São Paulo, divulgados pela Secretaria de Segurança Pública de São Paulo (SSP SP).

Este projeto nasceu de uma curisidade com relação a violência em São Paulo e para que eu possa transformar um dado em informação e com isso, tomar decisões e precauções com relação a comportamento em determinadas regiões.

## Disclaimer

Este conteúdo é fornecido apenas para fins informativos e educacionais. Não deve ser interpretado como aconselhamento profissional ou utilizado para fins comerciais. Todas as informações apresentadas são fornecidas de boa fé e são baseadas em fontes consideradas confiáveis, fornecidas pelo portal da transparência da Secretaria de  Segurança Pública de São Paulo. No entanto, não garanto a precisão, integridade ou atualidade dessas informações. Os usuários são incentivados a realizar suas próprias pesquisas e consultar profissionais qualificados para obter orientação específica para suas necessidades. Não me responsabilizo por quaisquer perdas ou danos decorrentes do uso ou confiança nas informações fornecidas neste conteúdo.

## Fontes de Dados

As informações informações utilizadas nesse projeto foram obtidas através do portal da transparêncoa da Secretaria de Segurança Pública de São Paulo.

Link [text](https://www.ssp.sp.gov.br/estatistica/consultas)

Para reduzir o tamanho do arquivo e deixá-lo com menos de 50MB e em formato CSV, separado por ";", foi feita a importação do arquivo original no formato "xlsx" e deixado com as seguintes colunas:

Arquivo: CelularesSubtraidos_2023.csv

    #   Column                
    --  -------------------                
    0   NUM_BO                
    1   DATA_OCORRENCIA_BO    
    2   HORA_OCORRENCIA       
    3   DATAHORA_REGISTRO_BO  
    4   DESCR_TIPOLOCAL       
    5   CIDADE                
    6   BAIRRO                
    7   LOGRADOURO            
    8   LATITUDE              
    9   LONGITUDE             
    10  QUANTIDADE_OBJETO     
    11  MARCA_OBJETO          

Arquivo: VeiculosSubtraidos_2023.csv

    #   Column                
    --  --------------------               
    0   NUM_BO               
    1   DATA_OCORRENCIA_BO   
    2   HORA_OCORRENCIA      
    3   DATAHORA_REGISTRO_BO 
    4   DESCR_TIPOLOCAL      
    5   CIDADE               
    6   BAIRRO               
    7   LOGRADOURO           
    8   LATITUDE             
    9   LONGITUDE            
    10  DESCR_TIPO_VEICULO   
    11  DESCR_MARCA_VEICULO  

**Nota**: Não foi feita nenhuma manipulação e/ou tratamento de dados, somente exclusão de colunas. Existem bairros como números, duplicados devido a acentuação. Este projeto não tem o intuito de ser o estado da arte, somente servir de exemplo de usabilidade do que daria para ser feito com informações públicas e transformar dados em informações, além de ter tido como motivador minha curiosidade sobre o comportamento da violência em São Paulo.

Sinta-se a vontade para baixar os arquivos de outros anos e substituir e fazer suas analises. Não se esqueça de manter a mesma estrutura!

Aproveite!

Um grande abraço,

Daniel Marques (dnmarques@gmail.com)