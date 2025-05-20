## A component for automating the deployment of Caldera Blue Agents triggered by Wazuh events

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