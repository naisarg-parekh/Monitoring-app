import boto3

ecr_client = boto3.client('ecr')

repository_name = "devops-project"
response = ecr_client.create_repository(repositoryName=repository_name)

repository_uri = response ['repository']['repositoryUri']
print(repository_uri)

with open('repository_uri.txt', 'w') as file:
    file.write(repository_uri)
