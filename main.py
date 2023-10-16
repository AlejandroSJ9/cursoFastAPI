from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token

app = FastAPI()
app.title = "Mi primera app"
app.version = "0.0.1"

class User(BaseModel):
    email:str
    password:str

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5,max_length=15)
    overview: str = Field(min_length=15,max_length=50)
    year: int = Field(le=2022)
    rating: float = Field(ge=1,le=10)
    category: str = Field(min_length=5,max_length=15)
    
    class Config:
        schema_extra = {
            'example': {
                'id' : 1,
                'title' : 'Mi pelicula',
                'overview' : 'Descripcion de la peli',
                'year' : 2022,
                'rating' : 9.8,
                'category' : 'Non'
            }
        }

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

@app.get('/movies',tags=['movies'], response_model=List, status_code=200)
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)

@app.get('/movies/{id}', tags=['movies'], response_model=List, status_code=200)
def get_movie(id: int = Path(ge=1,le=2000)) -> List[Movie]:
    data = list(filter(lambda x:x['id']==id,movies))
    return JSONResponse(status_code=200, content=data)

@app.get('/movies/',tags=['movies'], response_model=List, status_code=200)
def get_movies_by_category(category:str = Query(min_length=5, max_length=15)) -> List[Movie]:
    data = [item for item in movies if item['category'] == category]
    return JSONResponse(status_code=200,content=data)

@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(status_code=201, content={'message':'Se registro la pelicula'})

@app.delete('/movies/{id}',tags=['movies'], response_model=dict, status_code=200)
def delete_by_id(id:int) -> dict:
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
    return JSONResponse(status_code=200, content={'message':'Se elimino la pelicula'})

@app.delete('/movies',tags=['movies'], response_model=dict, status_code=200)
def delete_all() -> dict:
    movies.clear()
    return JSONResponse(status_code=200, content={'message':'Se elimino todo'})

@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_by_id(id:int, movie: Movie) -> dict:
    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category        
    return JSONResponse(status_code=200, content={'message':'Se actualizo la pelicula'})

@app.post('/login', tags=['auth'])
def login(user: User):
    return user