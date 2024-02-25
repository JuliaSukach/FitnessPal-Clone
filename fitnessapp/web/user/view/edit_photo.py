import os

from aiohttp import web
from aiohttp_jinja2 import template

from fitnessapp.utils.myfitnesspal_api import search_food
from fitnessapp.web.user.models import User
from fitnessapp.web.user.views import BaseView


class EditPhoto(BaseView):
    @template('edit_photo.html')
    async def get(self):
        user_id = await self.get_current_user()
        if not user_id:
            return web.HTTPFound(location='/register')
        user = await User.get(id=user_id)
        filename = user.image_name
        photo_url = None
        if filename:
            photo_url = f'/dynamic/img/{filename}'

        return {
            'photo_url': photo_url,
            'user': user,
            'current_url': str(self.request.rel_url)
        }

    async def post(self):
        user_id = await self.get_current_user()
        if not user_id:
            return web.HTTPFound(location='/register')

        reader = await self.request.multipart()
        field = await reader.next()

        if field.name == 'photo':
            filename = field.filename

            # Check if the filename is not None and not an empty string
            if filename and filename.strip():
                # Construct the file path to the 'img' directory
                img_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dynamic', 'img')
                photo_path = os.path.join(img_directory, filename)

                with open(photo_path, 'wb') as f:
                    while True:
                        chunk = await field.read_chunk()  # Read the photo data in chunks
                        if not chunk:
                            break
                        f.write(chunk)

                # Pass the filename or relative URL of the uploaded photo to the template
                photo_url = f'/dynamic/img/{filename}'  # Change this based on your server setup

                # Update the user's image_name field in the database (if you want to save it)
                user = await User.get(id=user_id)
                user.image_name = filename
                await user.save(update_fields=['image_name'])
                return web.HTTPFound(location='/photos/edit')
            else:
                return web.Response(text='Please select a valid photo to upload.')
        elif field.name == 'delete':
            print('delete')
            # Handle image deletion here
            user = await User.get(id=user_id)

            if user.image_name:
                # Delete the image file from the server
                img_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dynamic', 'img')
                photo_path = os.path.join(img_directory, user.image_name)
                if os.path.exists(photo_path):
                    os.remove(photo_path)

                # Set the user's image_name to None
                user.image_name = None
                await user.save(update_fields=['image_name'])

            # Redirect the user back to the edit photo page
            return web.HTTPFound(location='/photos/edit')
        else:
            return web.Response(text='Invalid field name for photo upload.')


