import yaml
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    with open("src/docs/openapi.yaml") as file:
        openapi = yaml.load(file, Loader=yaml.FullLoader)
    return openapi
