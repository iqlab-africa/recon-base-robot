# Reference Robot

This repository contains code for a Robot that is meant as a reference for the FNB Bank Recon project. The Robot integrates with the Azure Cloud Platform to download files and to interact with a serverless backend provided via Azure Functions. The functions provide the API that the Recon robots will need.

The Recon robots will be deployed to Robocorp Control Room or can be executed via a Python script that simulates the processes in the Control Room. Once the files have been uploaded to Azure Storage the robot can run completely un-attended.

The robots interact with the serverless Azure Functions that live in https://github.com/iqlab-africa/recon-base-functions

## Technologies

Azure Functions
Azure Storage
Azure Key Vault
Azure Postgres Database
Python
Typescript

## Robocorp Control Room

Screenshots from the deployment:

