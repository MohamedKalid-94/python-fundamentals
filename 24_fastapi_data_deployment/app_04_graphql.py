import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

# GRAPHQL: one endpoint, and the CLIENT chooses which fields it wants.
#   REST    many URLs, the server decides the shape of each answer
#   GraphQL one URL (POST /graphql), a typed SCHEMA, the client sends a QUERY:
#           { sensors { name unit } }       -> only name and unit come back
#   QUERY (read)   MUTATION (change data)   SUBSCRIPTION (live updates over WebSocket)
# Strawberry builds the schema from Python type hints (like FastAPI does for REST).
# Python names are snake_case, GraphQL names are camelCase: add_sensor becomes addSensor.
# Open http://127.0.0.1:8000/graphql in a browser for the GraphiQL playground.
# REST remains the common choice for AI back ends; GraphQL fits clients that need flexible, nested data.
# Errors do not use HTTP status codes: the answer has an "errors" list next to "data".


@strawberry.type
class Sensor:
    id: int
    name: str
    unit: str


SENSORS = [Sensor(id=1, name="temp", unit="C"), Sensor(id=2, name="humidity", unit="%")]


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello from GraphQL"

    @strawberry.field
    def sensors(self) -> list[Sensor]:
        return SENSORS

    @strawberry.field
    def sensor(self, id: int) -> Sensor | None:         # None is allowed: an unknown id gives null
        return next((sensor for sensor in SENSORS if sensor.id == id), None)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_sensor(self, name: str, unit: str = "C") -> Sensor:
        sensor = Sensor(id=len(SENSORS) + 1, name=name, unit=unit)
        SENSORS.append(sensor)
        return sensor


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")      # a GraphQL router is a normal FastAPI router


@app.get("/health")                                     # REST and GraphQL live side by side
def health():
    return {"status": "ok"}