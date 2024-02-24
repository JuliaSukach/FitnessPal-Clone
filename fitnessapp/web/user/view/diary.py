import json
from datetime import datetime

import aiohttp
from aiohttp import web
from aiohttp.web_response import json_response
from aiohttp_jinja2 import template
from tortoise.transactions import in_transaction

from fitnessapp.utils.myfitnesspal_api import search_food
from fitnessapp.utils.serializer import Serializer
from fitnessapp.web.user.models import User, Meal, MealType
from fitnessapp.web.user.views import BaseView


class UserDiary(BaseView):
    @template('diary.html')
    async def get(self):
        user_id = await self.get_current_user()
        if not user_id:
            return web.HTTPFound(location='/register')
        user = await User.get(id=user_id)

        # Get all meals for the user
        meals = await Meal.filter(user=user).order_by('-created_at').all()

        breakfast_meals = [meal for meal in meals if meal.meal_type == MealType.BREAKFAST]
        lunch_meals = [meal for meal in meals if meal.meal_type == MealType.LUNCH]
        dinner_meals = [meal for meal in meals if meal.meal_type == MealType.DINNER]
        snacks_meals = [meal for meal in meals if meal.meal_type == MealType.SNACKS]

        return {
            'user': user,
            'breakfast_meals': breakfast_meals,
            'lunch_meals': lunch_meals,
            'dinner_meals': dinner_meals,
            'snacks_meals': snacks_meals
        }

    async def post(self):
        return web.HTTPFound(location='/food/search')

    async def delete(self):
        meal_id = None
        try:
            data = await self.request.json()
            meal_id = data.get('meal_id')
        except Exception as e:
            return web.json_response({'success': False, 'error': 'Invalid request body'}, status=400)

        if not meal_id:
            return web.json_response({'success': False, 'error': 'Meal ID not provided'}, status=400)

        try:
            meal = await Meal.get(id=meal_id)
            await meal.delete()
            return web.json_response({'success': True})
        except Meal.DoesNotExist:
            return web.json_response({'success': False, 'error': 'Meal not found'}, status=404)


class AddMeal(BaseView):
    @template('add_meal.html')
    async def get(self):
        user_id = await self.get_current_user()
        if not user_id:
            return web.HTTPFound(location='/register')
        user = await User.get(id=user_id)
        return {'user': user}

    async def post(self):
        # Get the search query from the form data
        data = await self.request.post()
        search_query = data.get('search')
        return web.HTTPFound(location=f'/food/search?search={search_query}')


class SearchMeal(BaseView):
    @template('search.html')
    async def get(self):
        user_id = await self.get_current_user()
        if not user_id:
            return web.HTTPFound(location='/register')
        user = await User.get(id=user_id)

        search_query = self.request.query.get('search')
        food_results = await search_food(search_query)
        return {'user': user, 'food_data': food_results, 'search': search_query}


    async def post(self):
        user_id = await self.get_current_user()
        data = await self.request.post()
        meal_name = data.get('food-description')
        meal_calories = data.getall('food_entry')[1]
        meal_type_id = int(data.get('food_entry_meal_id'))
        meal_type = MealType(meal_type_id)
        await Meal.create(user_id=user_id, name=meal_name, calories=meal_calories, meal_type=meal_type)
        return web.HTTPFound(location='/food/diary')

