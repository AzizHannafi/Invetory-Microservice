from  fastapi import  FastAPI
from fastapi.middleware.cors import  CORSMiddleware
from redis_om import get_redis_connection, HashModel

app= FastAPI()

#Database connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*'],
)

redis = get_redis_connection(
    host="redis-12345.c135.eu-central-1-1.ec2.cloud.redislabs.com",
    port="12345",
    password="LLoaxgTe47xMTh7wxFzn3Mlog2o9SaOF",
    decode_responses=True

)

#Product Model
class Product(HashModel):
    name:str
    price: float
    quantity: int
    class Meta:
        database = redis


#Api
@app.get("/Product")
def all():
    return (format(pk) for pk in Product.all_pks())

def format(pk:str):
    product=Product.get(pk)

    return {
        "id":product.pk,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity
    }

@app.get('/GetSingleProduct/{pk}')
def getOne(pk:str):
    return Product.get(pk)

@app.post('/AddProduct')
def create(product: Product):
    return product.save()

@app.delete('/DeleteProduct/{pk}')
def deleteOne(pk:str):
    product = Product.get(pk)
    Product.delete(pk)
    return {"product": product,"Message":"deleted"}

@app.patch('/UpdateProduct/{pk}')
def UpdateOne(pk:str, prod: Product):
    product = Product.get(pk)
    prod.pk=pk
    Product.update(prod)
    return  {"product": prod,"Message":"updated"}
