Official website link : https://fastapi.tiangolo.com/

To run it : 
```console
uvicorn main:app --reload
```

Exemple de route : 
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

Auto documentation : http://127.0.0.1:8000/docs