### Requirements:
- Linux host machine
- Docker

## Install Katharange

Prima di tutto si deve installare KathaRange Cyber Lab
Repository Katharange: https://github.com/g4br-i/KathaRange
  
## Getting Started
Eseguire lo script nella cartella radice di Katharange.
```
 ./init.sh
```

Quando l'installazione è completata, andare nella cartella:
```
cd lab
kathara lstart
```
⚠️ Attendi che tutti i terminali carichino completamente gli script di avvio, dopodiché potrai accedere a tutti i servizi.


## 🐳 Build & Run
Per costruire l'immagine Docker e avviare il contenitore:

```bash
sudo docker build -t blue_deploy .
sudo docker run -it --network host blue_deploy 
```

## ⏱️ Esecuzione con variabile d'ambiente

È possibile specificare un valore per SLEEP_TIME tramite variabile d'ambiente:

```bash
sudo docker run -it --network host -e SLEEP_TIME=15 blue_deploy
```