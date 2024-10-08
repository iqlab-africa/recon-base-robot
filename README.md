# Reference Robot

This repository contains code for a Robot that is meant as a reference for the FNB Bank Recon project. The Robot integrates with the Azure Cloud Platform to download files and to interact with a serverless backend provided via Azure Functions. The functions provide the API that the Recon robots will need.

The Recon robots will be deployed to Robocorp Control Room or can be executed via a Python script that simulates the processes in the Control Room. Once the files have been uploaded to Azure Storage the robot can run completely un-attended.

The robots interact with the serverless Azure Functions that live in https://github.com/iqlab-africa/recon-base-functions

## Technologies

* Azure Functions
* Azure Storage
* Azure Key Vault
* Azure Postgres Database
* Python
* Typescript

## Robocorp Control Room 
![robocorp2](https://github.com/user-attachments/assets/ea4e99eb-5701-40ff-b274-3e6b5a55fa4d) 

Screenshots from the deployment:

<img width="2339" alt="Control Room Activity" src="https://github.com/user-attachments/assets/53f7cfce-9946-4c49-b18a-df027012a82b">

<img width="2376" alt="Process Running" src="https://github.com/user-attachments/assets/b526bdc5-0cbc-49f3-849e-54250fe03037">
  

## Demo
Assuming that you have cloned the repository you can run the 3 steps of the Robot using run.py. See the script at: https://github.com/iqlab-africa/recon-base-robot/blob/main/run.py

This simulates a Process defined in the Control Room. Each step passes on work item data to the next step. The script reads the Azure Postgres database to display data created by the Robot runs.

This reference Robot, PlayerRobot, simulates a task that downloads a file of famous football players, passes a list to the next task that simulates voting for the best player. This player is passed on to task 3. When the run.py is executed, the last step reads the postgres data that was created by the robots.  

### Screenshots from run.py script:  
<img width="1396" alt="Screenshot 2024-08-19 at 01 57 48" src="https://github.com/user-attachments/assets/34cc3430-aae1-416e-8c67-626296bdc1d4">  
<img width="783" alt="Screenshot 2024-08-19 at 01 57 04" src="https://github.com/user-attachments/assets/cd861e54-204a-4cbe-9627-38d125fb3f95">  
<img width="750" alt="Screenshot 2024-08-19 at 01 56 20" src="https://github.com/user-attachments/assets/bf066b31-2f8d-4ce2-9728-6dc47a97dce5">  
