# Python Flask RESTful API Server on Azure App Service
This is a proof of concept (POC) project for building and deploying a Python Flask RESTful API server to Azure App Service through Azure DevOps.

## Prerequisites
- Azure subscription and resource group.
- Azure App Service resource (Linux with Python runtime stack).  In this POC project, the App Service is called BillTestVmssServer.
- Azure System Assigned Managed Identity of the above Azure App Service is turned on.
- Azure Virtual Machine Scale Set (VMSS).
- Azure Key Vault.
- Azure Storage Account (Blob for application logging).
- Azure DevOps Account with organization, project, pipeline, and service connection configured.
- GitHub action configured.
  
## Azure Role-Based Access Control (RBAC)
Following RBAC roles are needed at the minumum for the System Assigned Managed Identity of the Azure App Service:
- Virtual Machine Scale Set (VMSS)
  - Virtual Machine Contributor
- Key Vault
  - Key Vault Secrets User
- Storage Account
  - Storage Blob Data Contributor

## Accessing the Flask RESTful API Server
The Flask RESTful API Server can be accessed via the following URL after deployment:

http://BillTestVmssServer.azurewebsites.net

## Examples
- http://BillTestVmssServer.azurewebsites.net/status
  - Get the running status of all the virtual machines in the scale set.

- http://BillTestVmssServer.azurewebsites.net/turnon
  - Turn on all the virtual machines in the scale set.

- http://BillTestVmssServer.azurewebsites.net/turnoff
  - Turn off all the virtual machines in the scale set.