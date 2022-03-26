from base64 import decode
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection,HashModel


#project config below defined
app = FastAPI()

app.add_middleware (
     CORSMiddleware,
     allow_origins = ['http://localhost:3000'],
     allow_methods = [ '*'],
     allow_headers  = ['* ']
)


REDIS_HOST  = 'redis-17991.c12.us-east-1-4.ec2.cloud.redislabs.com' #redis db endpoint
REDIS_PORT  = '17991'
REDIS_PASSWORD  = 'KJCe9NueoU3QD1JS1mCZTaj3QV1QRMtV'

redis  = get_redis_connection(
    host=REDIS_HOST, 
    port=REDIS_PORT, 
    password=REDIS_PASSWORD,
    decode_responses=True
)



#### *Redis database * model defiend below
class Product(HashModel):
    name : str
    price :float
    quantity : int
    
    class Meta:
        database = redis









### Def defiend below

@app.get('/products')
def all():
    return [format(x) for x in Product.all_pks()]


def format(pk : str):
    return Product.get(pk)

@app.post('/products')
def create(product: Product):
    return product.save()

@app.get('/products/{pk}')
def get(pk : str):
    return Product.get(pk)


@app.delete('/products/{pk}')
def delete(pk : str):
    return Product.delete(pk)