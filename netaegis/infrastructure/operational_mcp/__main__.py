import pulumi
from pulumi_docker import Container, ContainerPortArgs

container = Container("op-mcp", image="netaegis-op:latest", ports=[ContainerPortArgs(internal=8001, external=8001)])
pulumi.export("container_id", container.id)
