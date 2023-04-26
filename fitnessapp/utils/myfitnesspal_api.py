import aiohttp


async def search_food(food_name):
    async with aiohttp.ClientSession() as session:
        headers = {
            'x-app-id': '49eb582f',
            'x-app-key': '23a5af7be103248ab96b9817609e4607',
        }
        params = {
            'query': food_name,
            'detailed': 'false',
            'common': 'false',
            'branded': 'true'
        }
        try:
            async with session.get('https://trackapi.nutritionix.com/v2/search/instant', headers=headers, params=params) as resp:
                if resp.status == 200:
                    response_json = await resp.json()
                    return response_json['branded']
                else:
                    return None
        except Exception as ex:
            print(ex)
