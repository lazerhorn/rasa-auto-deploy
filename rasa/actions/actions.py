# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
import subprocess
import time
import logging
import re
import yaml
from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from datetime import datetime

# Set up Rasa logger
logger = logging.getLogger(__name__)

# Load configuration from YAML file
def load_config(config_path="deployment-config.yml"):
    try:
        with open(config_path, "r") as file:
            return yaml.safe_load(file)
    except Exception as e:
        logger.error(f"Failed to load config file: {e}")
        return {}

class ActionRunJupyterK8s(Action):
    def name(self) -> str:
        return "action_start_notebook"

    def run(self, dispatcher, tracker, domain):
        # Load config values
        config = load_config()
        deployment_file = config.get("jup_deployment_file", "jupyter_deployment.yaml")
        deployment_name = config.get("jup_deployment_name", "jupyter-notebook")
        service_name = config.get("jup_service_name", "jupyter-service")
        namespace = config.get("jup_namespace", "default")
        container_port = config.get("jup_container_port", 8888)
        
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {'-' * 15}")
        
        try:
            # Delete existing deployment and service (ignore errors if not exist)
            subprocess.run(f"kubectl delete deployment {deployment_name} --ignore-not-found=true -n {namespace}", 
                           shell=True, check=False)
            subprocess.run(f"kubectl delete service {service_name} --ignore-not-found=true -n {namespace}", 
                           shell=True, check=False)
    
            # Apply new Kubernetes deployment and service
            subprocess.run(f"kubectl apply -f {deployment_file}", shell=True, check=True)
            
            # Wait for the service to start
            time.sleep(15)

            # Get the exposed NodePort
            svc_result = subprocess.run(
                ["kubectl", "get", "svc", service_name, "-n", namespace, "-o", "jsonpath={.spec.ports[0].nodePort}"],
                capture_output=True, text=True, check=True
            )
            node_port = svc_result.stdout.strip()
            print(f'node_port: {node_port}')
            if not node_port:
                dispatcher.utter_message("Failed to retrieve Jupyter NodePort.")
                return []
            
            # Get the pod name
            pod_result = subprocess.run(
                ["kubectl", "get", "pods", "-l", f"app={deployment_name}", "-o", "jsonpath={.items[0].metadata.name}"],
                capture_output=True, text=True, check=True
            )
            pod_name = pod_result.stdout.strip()
            print(f'pod_name: {pod_name}')
            if not pod_name:
                dispatcher.utter_message("Failed to get Jupyter pod name.")
                return []

            # Fetch logs to extract the Jupyter token
            log_result = subprocess.run(
                ["kubectl", "logs", pod_name, "-n", namespace],
                capture_output=True, text=True
            )
            logs = log_result.stdout
            
            token = None
            for line in logs.split("\n"):
                match = re.search(r"token=([a-zA-Z0-9]+)", line)
                if match:
                    token = match.group(1)
                    break
        
            if not token:
                dispatcher.utter_message("Jupyter token not found in logs.")
                return []

            print(f'Token: {token}')

            # Construct the local URL
            jupyter_url = f"http://localhost:{node_port}/lab?token={token}"
            print(f'Jupyter URL: {jupyter_url}')
            
            dispatcher.utter_message(f"Jupyter Notebook is ready: {jupyter_url}")
            
            return [SlotSet("notebook_url", jupyter_url)]

        except subprocess.CalledProcessError as e:
            dispatcher.utter_message(f"Failed to start Jupyter in Kubernetes. Error: {e}")
            logger.error(f"Failed to start Jupyter in Kubernetes. Error: {e}")

        return []




