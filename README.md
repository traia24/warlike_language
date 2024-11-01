# warlike_language
Repository containing materials created and used for the methodological proposal in the empirical study of warlike language (analysis of war-related language in cancer discourse within journalistic contexts).

This paper presents a methodological proposal for analyzing the use of war-related language in media coverage of cancer, adaptable to other disciplines and the specific-project needs. It emphasizes automation through chatbots employing large language models (LLMs) and prompt engineering, tools that enable linguistic researchers to conduct quantitative studies with automated but flexible processes. This study demonstrates how technology can enhance interdisciplinary research and broaden the opportunities for researching and applying language in different professional contexts with the assistance of natural language processing and LLM-based conversational assistants.

IMPORTANT: Before running the main code procesar_archivos.py, the user must install the following (either in the terminal or in Google Colab):

bash
Copiar código
pip install spacy
pip install pandas
pip install six
pip install --upgrade six
python -m spacy download es_core_news_lg


In the main directory, the user will find:

- Folder "corpus_prueba": Contains three sample texts used for testing the lexicological extraction and frequency analysis code.

- Workflow diagrams: Provides summaries of both the creation of the reference war vocabulary and the main code for the methodological process.

- File "procesar_archivos.py": The main script for installing and importing all libraries needed to run the code; it includes a function to clean punctuation and typographic errors from the corpus texts, a function to tokenize and lemmatize words in each corpus text, a function to create the variable Vocabulario_referencia, and the main function to process text files.

- Folder "resultados_pruebas": Contains two files generated by the code with frequency analyses, saved as .txt (per corpus and per file: number of lexical and war-related lemmas and corresponding percentage of war lemmas) and as .xls (war-related lemmas identified in each file and their frequency).

- Folder "textos_lematizados": Contains the three sample texts after executing the first steps of the main code, covering cleaning (punctuation, typographic corrections, and lemmatization). These files have no practical purpose for reproducing the proposed methodological process in the study; they are only included to allow the user to see the results of applying text cleaning and lemmatization in Python.
File "vocabulario_belico_lematizado_v3.txt": Text file with the war vocabulary created as a reference, with the assistance of ChatGPT, to be used by the main code as a reference to identify and analyze these lemmas in the corpus processed by the code.
