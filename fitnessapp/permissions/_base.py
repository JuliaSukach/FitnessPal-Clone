import jwt
from aiohttp import web
from typing import Type
from functools import wraps

from fitnessapp.api.user.models import User
from fitnessapp.utils.crypto import Enigma

Request: Type[web.Request] = web.Request
View: Type[web.View] = web.View


class AnonymousUser:
    username = None
    is_anonymous = True


class AbstractPermission:
    perms: list = None

    def __call__(self, handler):
        for method_name in ('get', 'post', 'put', 'delete'):
            method = getattr(handler, method_name)
            if method is not None:
                # method decoration
                setattr(handler, method_name, self.subpermission(method))
        return handler

    @classmethod
    def get_token(cls, request: Request):
        try:
            schema, token = request.headers['Authorization'].split(' ')
        except KeyError:
            raise PermissionError('Required "Authorization" header.')
        except ValueError:
            raise PermissionError('Required token schema.')
        if schema != 'Bearer':
            raise PermissionError('Invalid token schema.')
        return token

    async def process_token(self, request: web.Request):
        if self.perms is not None:
            token = self.get_token(request)
            token_headers = jwt.get_unverified_header(token)
            try:
                info = jwt.decode(
                    token,
                    Enigma.public_key,
                    algorithms=[token_headers.get('alg')],
                    issuer='access',
                    audience=self.perms
                )
            except jwt.exceptions.InvalidAudienceError:
                raise PermissionError('Permission denied')
            except jwt.exceptions.InvalidIssuerError:
                raise PermissionError('Invalid token. Required "access" type.')
            except jwt.exceptions.ExpiredSignatureError:
                raise PermissionError('Invalid token. Old token.')
            return await User.get(username=info['username'])
        return AnonymousUser()

    @classmethod
    def subpermission(cls, func):
        @wraps(func)
        async def _wrap(view: View):
            view.user = await cls.process_token(cls, view.request)
            return await func(view)

        return _wrap
