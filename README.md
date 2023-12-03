# FastAPI-DI-Decorator
This decorator allows you to
1. specify functions in `Depends` and calling them manually
2. retain the possibility of sup-dependencies beeing resolved correctly
## Usage
```
@inject()
def validate_name(request: Request, name: str):
    # do something the injected request instance
    return name.upper()

@inject(
    validate=Depends(validate_name)
)
def hello_world(name: str, validate):
    return {"Hello": validate(name)}

@app.get("/")
def get_hello_world(name: str, hello_world=Depends(hello_world)):
    return hello_world(name)
```