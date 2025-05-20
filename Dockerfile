# Usa un'immagine base ufficiale di Python
FROM python:3.12.7-slim

# Imposta la directory di lavoro nel container
WORKDIR /app

# Copia script Python e le librerie personalizzate nella directory di lavoro
COPY Blue_Deploy_Working.py /app/
COPY caldera_api.py /app/
COPY wazuh_api.py /app/

# Installa le dipendenze Python necessarie
RUN pip install requests prettytable pytz

# Imposta una variabile d'ambiente 
ENV SLEEP_TIME=10



# Comando che viene eseguito quando il container viene avviato con log level DEBUG
CMD ["python", "Blue_Deploy_Working.py", "--debug"]


# Se si vuole dare in input l'argomento SLEEP_TIME, puoi farlo con il comando:




