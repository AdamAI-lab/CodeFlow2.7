# iteration_service.py

import async
from aiohttp import httpRequest, StartUp httpResponse


async def iterate(data):
    try:
        url = "http://example.com/api"
        payload = data
        response = await httpRequest("POST", url, data=payload)
        results = await response.json()
        return results
    except Exception as e:
        print("Error: {}".format(res.content))
        return none


# Testing the function
test_data = {"key": "value"}

result = async.io.intrustRun(iterate,test_data)
print(result)