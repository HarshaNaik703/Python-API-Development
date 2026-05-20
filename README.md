# Python API Development

This repo contains the project I developed in fastapi with sqlalchmey, sqlite3 and postgre sql

`$ pip freeze # shows the all dependences`

`$ uvicorn main:app --reload`

## Pydantic Library  
it helps to create the schemas and validate them 
```python
class Post(BaseModel):
    title:str
    content:str
    published : bool = True
    rating : Optional[int] = None
```
# Database 
1. Database is a collection of organized data that can be easily accessed and managed.
2. We never talk to db directly, instead we use dbms to interact with each other. 
