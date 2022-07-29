import aiohttp
import string
import secrets

#[{"key":"X-AUTH-TOKEN","value":"TEST123456789","description":"","type":"default","enabled":true}]

class SensibullApis():
    x_auth_token = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(12))
    
    @staticmethod
    async def create(symbol,quantity,order_tag):
      try:
        async with aiohttp.ClientSession() as session:
              api_url = 'https://prototype.sbulltech.com/api/order/place'
              async with session.post(api_url,
                                      json={ "symbol": symbol, "quantity": quantity, "order_tag": order_tag },
                                      headers={'X-AUTH-TOKEN':SensibullApis.x_auth_token}) as resp:
                  response = await resp.json()
                  return response
      except Exception as e:
        return e
    
    @staticmethod
    async def modify(order_id,quantity):
      try:
        async with aiohttp.ClientSession() as session:
              api_url = f'https://prototype.sbulltech.com/api/order/{order_id}'
              async with session.put(api_url,
                                      json={ "quantity": quantity},
                                      headers={'X-AUTH-TOKEN':SensibullApis.x_auth_token}) as resp:
                  response = await resp.json()
                  return response
      except Exception as e:
        return e
    
    @staticmethod
    async def cancel(order_id):
      try:
        async with aiohttp.ClientSession() as session:
              api_url = 'https://prototype.sbulltech.com/api/order/{order_id}'
              async with session.delete(api_url,
                                      headers={'X-AUTH-TOKEN':SensibullApis.x_auth_token}) as resp:
                  response = await resp.json()
                  return response
      except Exception as e:
        return e
    
    @staticmethod
    async def status(order_ids):
      try:
        async with aiohttp.ClientSession() as session:
              api_url = 'https://prototype.sbulltech.com/api/order/status-for-ids'
              async with session.post(api_url,
                                      json={ "order_ids": order_ids },
                                      headers={'X-AUTH-TOKEN':SensibullApis.x_auth_token}) as resp:
                  response = await resp.json()
                  return response
      except Exception as e:
        return e