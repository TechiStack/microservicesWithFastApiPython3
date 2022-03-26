from base64 import decode
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection,HashModel
from starlette.requests import Request
import requests

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






class Order(HashModel):
    product_id  : str
    price : float
    fee : float 
    total : float
    quantity : int
    status  : str
    
    class Meta:
        database  =  redis 
        


@app.post('/orders')
async def create(request : Request):
    body = await request.json()
    
    req = requests.get('https:localhost:8000/products/%s'%body['id'])
    
    return req.json()