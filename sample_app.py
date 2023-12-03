from fastapi import FastAPI, Request, Depends

from fastapi_di_decorator import inject

app = FastAPI()


@inject()
def validate_name(request: Request):
    # do something with request
    return "asd"


@inject(validate_name=Depends(validate_name))
def hello_world(name, validate_name):
    return {"Hello": validate_name(name)}


@app.get("/")
def get_hello_world(name: str, hello_world=Depends(hello_world)):
    return hello_world(name)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
