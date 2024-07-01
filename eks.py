import argparse
from kubernetes import client, config

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Create Kubernetes deployment and service.')
parser.add_argument('--image', required=True, help='Docker image URI')
args = parser.parse_args()

# Load Kubernetes configuration
config.load_kube_config()

# Create a Kubernetes API client
api_client = client.ApiClient()

# Define the deployment
deployment = client.V1Deployment(
    metadata=client.V1ObjectMeta(name="devops-project"),
    spec=client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(
            match_labels={"app": "devops-project"}
        ),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(
                labels={"app": "devops-project"}
            ),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name="live-demo",
                        image=args.image,
                        ports=[client.V1ContainerPort(container_port=5000)]
                    )
                ]
            )
        )
    )
)

# Create the deployment
api_instance = client.AppsV1Api(api_client)
api_instance.create_namespaced_deployment(
    namespace="default",
    body=deployment
)

# Define the service
service = client.V1Service(
    metadata=client.V1ObjectMeta(name="devops-project-service"),
    spec=client.V1ServiceSpec(
        selector={"app": "devops-project"},
        ports=[client.V1ServicePort(port=5000, target_port=5000, node_port=30007)],  # Change node_port if needed
        type="NodePort"  # Set the service type to NodePort
    )
)

# Create the service
api_instance = client.CoreV1Api(api_client)
api_instance.create_namespaced_service(
    namespace="default",
    body=service
)
