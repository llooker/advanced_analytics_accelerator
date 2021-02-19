
import base64
from googleapiclient import discovery
import pytz
import datetime

#-------------------- Configurations --------------------
GCP_PROJECT = "advanced_analytics_accelerator"
GCS_BUCKET_PATH = "gs://notebooks_bucket_looker"
STARTUP_SCRIPT_URL = "https://storage.cloud.google.com/advanced-analytics-accelerator.appspot.com/notebook_executor.sh"

PROJECT_NAME = "project-name-1"
NOTEBOOK_NAME = "CLV_predict-basic.ipynb.ipynb"
DLVM_IMAGE_PROJECT = "deeplearning-platform-release"
DLVM_IMAGE_FAMILY = "tf2-2-0-cu100"
ZONE = "us-west1-b"
MACHINE_TYPE = "n1-highmem-8"
MACHINE_NAME = PROJECT_NAME
BOOT_DISK_SIZE = "200GB"
GPU_TYPE = "nvidia-tesla-k80"
GPU_COUNT = 1
INSTALL_NVIDIA_DRIVER = True


def create_instance():

    # Create the Cloud Compute Engine service object
    compute = discovery.build('compute', 'v1')
    
    image_response = compute.images().getFromFamily(
        project=DLVM_IMAGE_PROJECT, family=DLVM_IMAGE_FAMILY).execute()
    source_disk_image = image_response['selfLink']

    # Configure the machine
    machine_type_with_zone = "zones/%s/machineTypes/%s" % (ZONE,MACHINE_TYPE)
    
    today_date = datetime.datetime.now(pytz.timezone('America/Los_Angeles'))

    gcs_input_notebook = "%s/notebooks/%s/current/%s" % (GCS_BUCKET_PATH,PROJECT_NAME,NOTEBOOK_NAME)
    gcs_output_folder = "%s/outputs/%s/%s/%s/%s/" % (GCS_BUCKET_PATH,PROJECT_NAME,today_date.year,today_date.month,today_date.day)
    gcs_parameters_file= "%s/notebooks/%s/current/%s" % (GCS_BUCKET_PATH,PROJECT_NAME,"params.yaml")
    gcs_requirements_txt= "%s/notebooks/%s/current/%s" % (GCS_BUCKET_PATH,PROJECT_NAME,"requirements.txt")

    accelerator_type = "projects/%s/zones/%s/acceleratorTypes/%s" % (GCP_PROJECT,ZONE,GPU_TYPE)

    config = {
        'name': MACHINE_NAME,
        'machineType': machine_type_with_zone,

        # Specify the boot disk and the image to use as a source.
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': source_disk_image,
                },
                'boot-disk-size': BOOT_DISK_SIZE
            }
        ],
        
        # Specify a network interface with NAT to access the public
        # internet.
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],

        'guestAccelerators': [{
            'acceleratorType':accelerator_type,
            'acceleratorCount':GPU_COUNT
        }],

        'scheduling': {
            'onHostMaintenance': 'TERMINATE'
        },

        # Allow the instance to access cloud storage and logging.
        'serviceAccounts': [{
            'email': 'default',
            'scopes': [
                'https://www.googleapis.com/auth/cloud-platform'
            ]
        }],

        # Metadata is readable from the instance and allows you to
        # pass configuration from deployment scripts to instances.
        'metadata': {
            'items': [{
                # Startup script is automatically executed by the
                # instance upon startup.
                'key': 'startup-script-url',
                'value': STARTUP_SCRIPT_URL
            }, {
                'key': 'input_notebook',
                'value': gcs_input_notebook
            }, {
                'key': 'output_notebook',
                'value': gcs_output_folder
            }, {
                'key': 'requirements_txt',
                'value': gcs_requirements_txt 
            }, {
                'key': 'parameters_file',
                'value': gcs_parameters_file
            }, {
                'key': 'install-nvidia-driver',
                'value': INSTALL_NVIDIA_DRIVER
            }]
        }
    }

    return compute.instances().insert(
        project=GCP_PROJECT,
        zone=ZONE,
        body=config).execute()
        
        
def execute(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    
    # We don't really need the content of pubsub message
    # pubsub_message = base64.b64decode(event['data']).decode('utf-8')

    resp = create_instance()
    return str(resp)
