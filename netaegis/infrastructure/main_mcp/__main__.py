import pulumi
from pulumi_docker import Container, ContainerPortArgs

container = Container("main-mcp", image="netaegis-main:latest", ports=[ContainerPortArgs(internal=8000, external=8000)])
pulumi.export("container_id", container.id)
