from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from yaml import serialize
from .models import InfoRequest,InfoAppeal
from .serializers import InfoAppealSerializer,InfoRequestSerializer

class ListInfoRequestApiView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):

        if(request.query_params.get('status')):
            info_requests = InfoRequest.objects.filter(status = request.query_params['status'])
        else:
            info_requests = InfoRequest.objects.all()
        
        serializer = InfoRequestSerializer(info_requests, many = True)

        return Response(serializer.data, status = status.HTTP_200_OK)


class InfoRequestApiView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    #Função que retorna um pedido de informação, caso ele exista
    def get(self, request, *args, **kwargs):

        if(request.query_params.get('id')):
            info_request = InfoRequest.objects.get(pk = request.query_params.get('id'))
            serializer = InfoRequestSerializer(info_request)
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    #Função que abre uma novo pedido de informação
    def post(self, request, *args, **kwargs):

        data = {
            'demander': request.user.id,
            'content': request.data.get('content')
        }

        serializer = InfoRequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #Função que atualiza a situação da demanda. para atualizar a situação para respondida é necessário enviar junto a resposta
    def put(self, request, *args, **kwargs):

        if(not request.data.get('id')):
            return Response(status=status.HTTP_400_BAD_REQUEST) 
        info_request = InfoRequest.objects.get(pk = request.data.get('id'))


        if(request.data.get('status') == 'respondida' and request.data.get('answer')):
            info_request.answer_request(request.data.get('answer'))
        elif(request.data.get('status') == 'finalizada'):
            info_request.finalize_request()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST) 

        serializer = InfoRequestSerializer(info_request)
        return Response(serializer.data, status=status.HTTP_200_OK) 

        
class InfoAppealApiView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    #Função que retorna um recurso de pedido de informação, caso ele exista
    def get(self, request, *args, **kwargs):

        if(not request.query_params.get('id')):
            return Response(status=status.HTTP_400_BAD_REQUEST) 

        # if(request.query_params.get('id')):
        info_appeal = InfoRequest.objects.get(pk = request.query_params.get('id')).appeal
        if(info_appeal):
            serializer = InfoAppealSerializer(info_appeal)
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    #Função que abre uma novo pedido de informação
    def post(self, request, *args, **kwargs):

        if(not request.data.get('id') or not request.data.get('content')):
            return Response(status=status.HTTP_400_BAD_REQUEST) 
        info_request = InfoRequest.objects.get(pk = request.data.get('id'))

        appeal = info_request.open_appeal(request.data.get('content'))
        serializer = InfoAppealSerializer(appeal)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
