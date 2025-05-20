import json
import os
from datetime import datetime
import caldera_api as api
import wazuh_api as wazuh
import requests
import time
import threading
import json
import base64


# Configurazione delle credenziali e degli endpoint API
CALDERA_API_ENDPOINT = "http://localhost:8888"
CALDERA_API_KEY_BLUE = "n1Pzbva6skp7MbZGm7aWF4hH-XgdJR__c5HjOPRsmSo"
CALDERA_API_KEY_RED = "PoikrnUdtkDIPMScFmHqDWnGoNWS8f_m2QDkunraZc0"
date_format = "%b %d %H:%M:%S" 


def get_required_response(adversary_id):
    # Uso un dizionario per mappare le abilità che mi servono per rispondere all'attacco red
    abilities_mapping = {
    #Linux_Profile_cronjob : [Task-Hunter]
    "T1053.003": "169cdc73-8fea-49cf-9021-d0b3c24e2b17",
    "T1136": "169cdc73-8fea-49cf-9021-d0b3c24e2b17"
    }
    return abilities_mapping.get(adversary_id, [])

def auto_deploy_blue_agent(sleep_time:int):
    old = datetime.now().strftime(date_format)
    #old = "Mar 27 12:43:19"
    number = 1
    while(True):
        wazuh.get_alerts_file()
        with open('syscheck_events.json', 'r') as f:
            data = json.load(f)
            # Se esiste il campo predecoder e timestamp
            if 'predecoder' not in data['hits']['hits'][0]['_source']:
                print("No predecoder field found")
                time.sleep(sleep_time)
                continue
            timestamp = data['hits']['hits'][0]['_source']['predecoder']['timestamp']
            # Se la data è più recente di quella salvata allora è stato rilevato un nuovo attacco
            now = datetime.strptime(timestamp, date_format)
            old = datetime.strptime(old, date_format)
            if now > old:
                old = timestamp
                print(f"🔴 Red agent detected an attack")
                #Identifico l'avversario
                id = data['hits']['hits'][0]['_source']['rule']['mitre']['id']
                print(f"Attack Tactic ID: {id[0]}")

                # Identifico le abilità di cui ho bisogno per rispondere all'attacco red
                adversary_blue = get_required_response(id[0])

                # Mi autentico come utente blue
                print(f"🔵 Authenticating as blue agent")
                print(f"⏳ Deploying blue agent")
                blue_agent = Agent(group = "blue", key = CALDERA_API_KEY_BLUE)
                blue_agent.start_beaconing()
                print(f"✅ Blue agent deployed")
                # Faccio partire l'operazione di risposta
                print(f"⏳ Starting blue operation")
                op_name = f"Blue Response {number}"
                operation = blue_agent.caldera.add_operation(name=op_name,group="blue",adversary_id=adversary_blue)
                print(f"✅ Blue operation started")
                number+=1
            else:
                old = timestamp
                print(f"⏳ No new attacks detected")
        time.sleep(sleep_time)
                

class Agent:
    def __init__(self, group: str, key: str, paw: str | None = None, beaconing_interval: int = 5, caldera_instance: api.Caldera | None = None):
        self.beaconing: bool = False
        self.beaconing_interval: int = beaconing_interval
        self.caldera: api.Caldera = api.Caldera(key, debug=True, print_banner=False) if not caldera_instance else caldera_instance
        self.paw: str = paw if paw else self.caldera.add_agent(name="sandcat.go-linux",group=group)
        self.group: str = group

    def start_beaconing(self) -> None:
        if self.beaconing:
            print("Beaconing already started")
            return
        self.beaconing = True
        self.beaconing_thread = threading.Thread(target=self.beacon, daemon=True)
        self.beaconing_thread.start()
    
    def beacon(self) -> None:
        while self.beaconing:
            # Invia un beacon al server
            response = self.send_beacon()
            if response.status_code != 200:
                raise Exception(f"Failed to send beacon: {response.text}")
            time.sleep(self.beaconing_interval)

    def stop_beaconing(self) -> None:
        if not self.beaconing:
            print("Beaconing already stopped")
            return
        self.beaconing = False

    def send_beacon(self) -> requests.Response:
        data_dict = {
            "paw": self.paw,
            "server": self.caldera.caldera_URL,
            "pid": os.getpid(),
        }
        
        # Converto il dizionario in JSON e lo codifico in base64
        json_data = json.dumps(data_dict)
        base64_data = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')
        
        # Invio il beacon al server
        response = requests.post(self.caldera.caldera_URL + '/beacon', data=base64_data)
        
        return response

    def __str__(self):
        return f"Agent(name={self.paw}, group={self.group}, platform={self.platform})"

    def __repr__(self):
        return self.__str__()
    
if __name__ == "__main__":
    debug = True
    sleep_time = int(os.getenv("SLEEP_TIME", 10))
    auto_deploy_blue_agent(sleep_time)
    #auto_deploy_blue_agent(10)