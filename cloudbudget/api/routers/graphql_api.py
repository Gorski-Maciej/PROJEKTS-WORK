from fastapi import APIRouter
from strawberry.fastapi import GraphQLRouter
from api.graphql.schema import schema

router = APIRouter(tags=["graphql"])
graphql_app = GraphQLRouter(schema)
router.include_router(graphql_app, prefix="/graphql")
