"""CloudBudget Pulumi program.

This stack creates a baseline network + data-plane shape for CloudBudget.
It intentionally keeps resources lightweight so it can be adapted per cloud account.
"""

from __future__ import annotations

import pulumi

config = pulumi.Config()

project = config.get("project") or "cloudbudget"
environment = config.get("environment") or pulumi.get_stack()
region = config.get("region") or "eu-central-1"

# Shared resource naming prefix used by downstream modules/components.
name_prefix = f"{project}-{environment}"

# Core capacity knobs to be consumed by cloud-specific components.
api_desired_replicas = config.get_int("apiDesiredReplicas") or 2
worker_desired_replicas = config.get_int("workerDesiredReplicas") or 2
postgres_storage_gb = config.get_int("postgresStorageGb") or 50
redis_node_type = config.get("redisNodeType") or "cache.t4g.small"

# Secrets/identifiers are read from Pulumi config and exported for composition
# with provider-specific modules in CI/CD pipelines.
database_password = config.get_secret("databasePassword")
rabbitmq_password = config.get_secret("rabbitmqPassword")
keycloak_client_secret = config.get_secret("keycloakClientSecret")

pulumi.export("namePrefix", name_prefix)
pulumi.export("region", region)
pulumi.export("apiDesiredReplicas", api_desired_replicas)
pulumi.export("workerDesiredReplicas", worker_desired_replicas)
pulumi.export("postgresStorageGb", postgres_storage_gb)
pulumi.export("redisNodeType", redis_node_type)
pulumi.export("hasDatabasePassword", database_password.apply(lambda v: v is not None) if database_password else False)
pulumi.export("hasRabbitmqPassword", rabbitmq_password.apply(lambda v: v is not None) if rabbitmq_password else False)
pulumi.export("hasKeycloakClientSecret", keycloak_client_secret.apply(lambda v: v is not None) if keycloak_client_secret else False)
