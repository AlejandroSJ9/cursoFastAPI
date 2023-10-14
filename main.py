from fastapi import FastAPI
from fastapi.responses import HTMLResponse
app = FastAPI()
app.title = "Mi primera app"
app.version = "0.0.1"

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 2,
        'title': 'Avatar 2',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Aventura'    
    }
]

@app.get('/',tags=['home'])
def message():
    return HTMLResponse('<h1>Hola mundo</h1>')

@app.get('/movies',tags=['movies'])
def get_movies():
    return movies

@app.get('/movies/{id}', tags=['movies'])
def get_movie(id: int):
    return list(filter(lambda x:x['id']==id,movies))

@app.get('/movies/',tags=['movies'])
def get_movies_by_category(category:str):
    return [item for item in movies if item['category'] == category]