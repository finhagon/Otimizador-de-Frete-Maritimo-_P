Otimizador de Fretes Marítimos
Este projeto é uma ferramenta interativa desenvolvida em Python e Streamlit para auxiliar na tomada de decisão logística. O objetivo é comparar diferentes opções de frete marítimo utilizando múltiplos critérios, gerando um ranking (score) baseado nas prioridades do usuário.
  Funcionalidades
Filtro em Cascata: Seleção dinâmica por Porto de Origem e Porto de Destino.

Análise Multicritério: Avalia simultaneamente Frete, Transit Time e Free Time.

Pesos Personalizáveis: O sistema utiliza pesos configurados no código (60% Preço, 30% Transit Time, 10% Free Time) para calcular a melhor opção. *Os pesos devem ser alterados conforme necessidade do usuario.

Ranking Top 3: Exibição clara das três melhores opções com destaque visual para a vencedora.

Segurança de Dados: Os dados são processados em memória através do upload de ficheiros CSV, garantindo que as informações não fiquem armazenadas permanentemente no servidor.

   Lógica de Cálculo (Score)
Para comparar grandezas diferentes (Moeda vs. Dias), o sistema utiliza a técnica de Normalização Min-Max, transformando os valores em notas de 0 a 100:

Frete: Menor valor = Nota mais alta.

Transit Time: Menor tempo = Nota mais alta.

Free Time: Maior tempo = Nota mais alta.

O Score final é a média ponderada destas notas.

  Como usar
Prepare uma planilha com as colunas exatamente com estes nomes: Porto Origem, Porto de Destino, Armador, Frete, Transittime, Fretime.

Faça o upload do ficheiro .csv na barra lateral.

Selecione a Origem e o Destino desejados.

O sistema apresentará automaticamente a melhor opção técnica.

 Tecnologias Utilizadas
Python

Streamlit (Interface Web)

Pandas (Manipulação de dados)

Scikit-learn (Normalização Min-Max)
