# Chatbot for Automated Deployment

This application is a chatbot that automates the deployment of applications. Currently, it only supports Jupyter Notebook with Kubernetes, but it is designed to be extended for other applications in the future.


## Prerequisites

Ensure you have the following installed:
- **Python 3.10 or above**
- **Docker and Kubernetes** (Preferably DockerHub v43.7.1 or any recent version)

---

## How It Works

### 1. Create and Activate a Virtual Environment
Run the following commands:
```sh
python -m venv venv  # Create virtual environment
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

### 2. Install Required Packages
```sh
pip install -r requirements.txt
```

### 3. Train the Model
Before starting the application, you'll need to train the Rasa model to understand the intents and actions.
```sh
rasa train
```
This command will process the NLU training data, as well as the rules and stories, to create a model that will be used to handle the chatbot's responses and interactions.

### 4. Start the Application
```sh
python app.py
```
After launching, click the provided link to access the chatbot.

### 5. Open Two New Terminals and Activate the Virtual Environment
```sh
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

### 6. Run Rasa Services
In one terminal, start the Rasa server:
```sh
rasa run
```
In the second terminal, start the Rasa action server:
```sh
rasa run actions
```

### 7. Wait for Model to Load (1-2 Minutes)
Once the model is ready, type your prompt to interact with the chatbot.

---

## Automating Deployment for Other Applications

To extend this chatbot to deploy additional applications, follow these steps:

### 1. Modify Rasa Custom Actions
Edit `rasa/actions.py` to add new custom actions related to deploying your application.

### 2. Update NLU, Rules, and Stories
Modify the following files to include intents, rules, and conversation flows for your new deployment:
- `rasa/data/nlu.yml`
- `rasa/data/rules.yml`
- `rasa/data/stories.yml`

### 3. Register Entities and Parameters
Update `rasa/domain.yml` to define new entities and parameters required for deployment.

### 4. Configure Deployment Settings
Edit `rasa/deployment-config.yml`, which is linked to `rasa/actions/actions.py`, to change configurations like paths, parameters, and settings—allowing you to avoid retraining and restarting the Rasa server.

### 5. Add Deployment and Docker Files
- Place any Kubernetes deployment YAML files inside the `deployment-fol/` directory.
- Store Dockerfiles for additional applications inside the `docker-fol/` directory.

---

Following these steps will allow you to automate the deployment of any application using this chatbot framework.

