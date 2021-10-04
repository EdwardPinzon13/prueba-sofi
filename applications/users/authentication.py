from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from datetime import timedelta
from django.utils import timezone
from django.conf import settings

class ExpiringTokenAuthentication(TokenAuthentication):
    expired= False
    def expires_in(self,token): #contabiliza en cuanto tiempo expirara el token
        time_elapsed = timezone.now() - token.created # mira cuanto tiempo ha pasado desde que el token fue creado y el tiempo actual,es 
        #decir el tiempo de vida del token
        left_time = timedelta(seconds= settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed #traemos desde el settings, la variable
        #que hemos definido y restamos el tiempo que le definimos de tiempo de vida y el tiempo que ha pasado
        return left_time #retornamos el tiempo de vida que le queda al token

    def is_token_expired(self,token): # compara si el tiempo que paso ya ha expirado el token
        return self.expires_in(token) < timedelta(seconds=0)

    def token_expire_handler(self,token): #
        is_expire= self.is_token_expired(token) #mira si ya expiro el token, llamando a un conjunto de secuencias que //arriba
        if is_expire:
            user = token.user
            token.delete()
            token = self.get_model().objects.create(user= user) #le refresco el token
            self.expired = True
        return is_expire,token

    def authenticate_credentials(self,key):
        message,token,user = None,None,None
        try:
            token = self.get_model().objects.select_related('user').get(key=key) #recupera el tokn de los registros de token en la BD
            user= token.user
        except self.get_model().DoesNotExist: #si el token no existe en la consulta de los tokens, en lso registros es invalido
            message = 'Token invalido'
            self.expired = True
        if token is not None:
            if not token.user.is_active:
                message = 'Usuario no activo o eliminado'
            is_expired = self.token_expire_handler(token)
            if is_expired:
                message = 'Su Token ha Expirado'
        return (user,token,message,self.expired)
