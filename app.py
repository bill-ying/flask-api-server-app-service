import time
from datetime import datetime   

from flask import Flask, jsonify
from flask_cors import CORS
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.storage.blob import BlobServiceClient
from azure.keyvault.secrets import SecretClient


app = Flask(__name__)
CORS(app)

key_vault_name='BillTestKeyVault'
key_valut_uri = f"https://{key_vault_name}.vault.azure.net"
subscription_id_key = "subscriptionId"
resource_group_name_key = "resourceGroupName"
vmss_name = 'BillTestA'
account_url = "https://billteststorage238.blob.core.windows.net/"

credential=DefaultAzureCredential()
secret_client = SecretClient(vault_url=key_valut_uri, credential=credential)

blob_service_client = BlobServiceClient(account_url=account_url, credential=credential)
container_client = blob_service_client.get_container_client("ssms-server")

def __azure_values():
    subscription_id = secret_client.get_secret(subscription_id_key).value
    computer_client = ComputeManagementClient(credential=credential, subscription_id=subscription_id)
    resource_group_name = secret_client.get_secret(resource_group_name_key).value
    
    return computer_client, resource_group_name

def log(message):
    blob_client = container_client.get_blob_client(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}: ' +
                                                   'Information')
    blob_client.upload_blob(message)

@app.route('/')
def index():
    log('Request for index page received')
    return 'VMSS Server Works'

@app.route('/status', methods=['GET'])
def status():
    instances = __azure_values()[0].virtual_machine_scale_set_vms.list(__azure_values()[1], vmss_name)

    status = {}
    instance_list = list(instances)
    print(f'instances list length: {len(instance_list)}')

    for instance in instance_list:
        print('instance' + str(instance))

        instance_view = __azure_values()[0].virtual_machine_scale_set_vms.get_instance_view(
            resource_group_name=__azure_values()[1],
            vm_scale_set_name=vmss_name,
            instance_id=instance.instance_id
        )

        print('instance_view' + str(instance_view))

        status[instance.name] = instance_view.statuses[1].display_status

    return jsonify(status)

@app.route('/turnon', methods=['GET'])
def turn_on():
    print('Request for turn on received')
    __azure_values()[0].virtual_machine_scale_sets.begin_start(__azure_values()[1], vmss_name)
    time.sleep(6)

    return status()

@app.route('/turnoff', methods=['GET'])
def turn_off():
    print('Request for turn off received')
    __azure_values()[0].virtual_machine_scale_sets.begin_deallocate(__azure_values()[1], vmss_name)
    time.sleep(6)

    return status()


if __name__ == '__main__':
   app.run()
