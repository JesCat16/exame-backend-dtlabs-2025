# exame-backend-dtlabs-2025
## Setup the env
Windows
```
...\exame-backend-dtlabs-2025> python -m venv env
```
```
...\exame-backend-dtlabs-2025\env\Scripts> ./activate.ps1
```
```
...\exame-backend-dtlabs-2025> pip install -r requirements.txt
```
## Docker-compose
### Starting compose
```
...\exame-backend-dtlabs-2025\Docker_Components> docker-compose up
```
## Code
### Follow in order!
Start main
```
...\exame-backend-dtlabs-2025> uvicorn main:app --reload 
```
Start Workers
```
...\exame-backend-dtlabs-2025\Workers> python .\ActivateServer.py
```
```
...\exame-backend-dtlabs-2025\Workers> python .\ServerStatus.py
```
Start Servers and Consumer
```
...\exame-backend-dtlabs-2025> python .\server_03.py
```
```
...\exame-backend-dtlabs-2025> python .\server_02.py
```
```
...\exame-backend-dtlabs-2025> python .\server_03.py
```
```
...\exame-backend-dtlabs-2025> python .\consumer.py
```
## Test
```
...\exame-backend-dtlabs-2025> pytest .\Test.py
```
