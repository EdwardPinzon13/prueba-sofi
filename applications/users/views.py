from django.contrib.sessions.models import Session
from datetime import datetime
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.generics import ListAPIView
from .models import User
from .authenticationmixins import Authentication
from .serializers import (
    UserTokenSerializer,
)


class UserToken(APIView):
    def get(self,request, *args, **kwargs):
        username = request.GET.get('username')
        try:
            user_token = Token.objects.get(
                user = UserTokenSerializer().Meta.model.objects.filter(username= username).first()
            )
            return Response(
                {'token' : user_token.key}
            )
        except:
            return Response(
                {'Error' : 'Credenciales enviadas incorrectas'}, status = status.HTTP_400_BAD_REQUEST
            )

class Login(ObtainAuthToken):#la clase ObtainAuthTOken no permite el method get, para trabajarlo toca con post, desde postman

    def post(self, request, *args, **kwargs): #capturamos el metodo post
        login_serializer = self.serializer_class(data = request.data, context = {'request':request}) # recuperamos el serializador
        # y le enviamos la data y el contexto que llegan por medio del request, de la peticion post
        print(login_serializer)
        if login_serializer.is_valid(): #si el login_serializer es valido
            user = login_serializer.validated_data['user'] #recupero el user enviado desde la peticion post
            if user.is_active: #validamos que el usuario este activo
                token,created = Token.objects.get_or_create(user = user) # retorna la instancia, es decir el token si existe, si no lo crea 
                print(created)
                #y devuelve un bool si fue creado o no
                user_serializer = UserTokenSerializer(user) #envio los campos del usuario para serializarlo
                if  created: # si no tenia token lo crea
                    return Response(
                        {
                            'token' : token.key,
                            'user': user_serializer.data,
                            'message' : 'Inicio de Sesión Exitoso'
                        }, status = status.HTTP_201_CREATED
                    )
                else: #si ya tenia uno lo elimina, si intenta iniciar sesion otra vez , y le creo uno nuevo
                    all_sessions = Session.objects.filter(expire_date__gte= datetime.now()) #recuperamos todas las sesiones que vayan a expirar
                    if all_sessions.exists(): #si existen sesiones
                        for session in all_sessions:
                            session_data = session.get_decoded() #decodificamos los datos de la session
                            if user.id == int(session_data.get('_auth_user_id')): #compramos los id de la session del usuario con su id
                                session.delete() #le eliminamos la session
                    token.delete()
                    token = Token.objects.create(user= user)
                    return Response(
                        {
                            'token' : token.key,
                            'user': user_serializer.data,
                            'message' : 'Inicio de Sesión Exitoso'
                        }, status = status.HTTP_201_CREATED
                    )
            else:# si el usuario no esta activo
                return Response({'Error':'Este usuario no puede iniciar sesión'}, status = status.HTTP_401_UNAUTHORIZED)
            print('paso validaci;on')
        else: # si no es valido el serializador
            return Response({'error':'Nombre de usuario o Contrasena incorrectos'},
                            status = status.HTTP_400_BAD_REQUEST)

        return Response({'mensaje':'Hola desde response'}, status =status.HTTP_200_OK)

class Logout(APIView):

    def post(self, request, *args, **kwargs):
        try:
            token = request.POST.get('token') # recupero el token enviado desde la petición
            print('token ;;',token)
            token = Token.objects.filter(key = token).first() #filtro el usuario buscando ese token en la lsita de tokens que tenga
            if token: #si existe el token
                user = token.user
                print(user)
                all_sessions = Session.objects.filter(expire_date__gte= datetime.now()) #recuperamos todas las sesiones que vayan a expirar
                if all_sessions.exists(): #si existen sesiones
                    for session in all_sessions:
                        session_data = session.get_decoded() #decodificamos los datos de la session
                        if user.id == int(session_data.get('_auth_user_id')): #compramos los id de la session del usuario con su id
                            session.delete() #le eliminamos la session

                token.delete()

                session_message = 'Sesiones de usuario eliminadas'
                token_message = 'Token eliminado'
                return Response({'token_message' : token_message , 'session_message' : session_message},
                            status = status.HTTP_200_OK)
            return Response({'Error' : 'No se ha encontrado un usuario con estas credenciales.'}, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({'error' : 'No se encontró  el token en la petición'} , status = status.HTTP_409_CONFLICT)

class RecovryPassword(APIView):

    def post(self, request, *args, **kwargs):
        try:
            email = request.data['email']
            password = request.data['password']
            print('password',password)
            user = User.objects.get(email=email)
            if user:
                user.set_password(password)
                user.save()
                return Response({'Accept' : 'Cambio de Contrasena Exitoso'} , status = status.HTTP_200_OK)
            else:
                return Response({'error' : 'El Email Digitado no Coincide con nuestros registros'},status = status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error' : 'No Se Encontró  el Usuario Registrado'} , status = status.HTTP_409_CONFLICT)






