import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Sala, EstadoUsuario

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sala_id = self.scope['url_route']['kwargs']['sala_id']
        self.room_group_name = f'chat_{self.sala_id}'
        
        # Unirse al grupo de la sala
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Actualizar estado del usuario
        await self.actualizar_estado_usuario(True)
    
    async def disconnect(self, close_code):
        # Actualizar estado del usuario
        await self.actualizar_estado_usuario(False)
        
        # Salir del grupo de la sala
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        
        if data['type'] == 'message':
            # Enviar mensaje al grupo
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': data['message']
                }
            )
        elif data['type'] == 'typing':
            # Enviar estado de escritura al grupo
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_status',
                    'user': self.scope['user'].username,
                    'is_typing': data['is_typing']
                }
            )
    
    async def chat_message(self, event):
        # Enviar mensaje al WebSocket
        await self.send(text_data=json.dumps({
            'type': 'message',
            'html': event['message']
        }))
    
    async def typing_status(self, event):
        # Obtener lista de usuarios escribiendo
        typing_users = await self.get_typing_users()
        
        # Enviar estado de escritura al WebSocket
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'users': typing_users
        }))
    
    @database_sync_to_async
    def actualizar_estado_usuario(self, conectado):
        user = self.scope['user']
        if user.is_authenticated:
            estado, _ = EstadoUsuario.objects.get_or_create(usuario=user)
            estado.conectado = conectado
            estado.sala_actual_id = self.sala_id if conectado else None
            estado.save()
    
    @database_sync_to_async
    def get_typing_users(self):
        return list(EstadoUsuario.objects.filter(
            sala_actual_id=self.sala_id,
            esta_escribiendo=True
        ).values_list('usuario__username', flat=True)) 