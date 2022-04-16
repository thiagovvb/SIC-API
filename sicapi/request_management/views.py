from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from yaml import serialize
from .models import InfoRequest,InfoAppeal
from .serializers import InfoAppealSerializer,InfoRequestSerializer

class ListInfoRequestApiView(APIView):

    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):

        info_requests = None

        # if(request.status):
        #     info_requests = InfoRequest.objects.filter(status = request.status)
        # else:
        info_requests = InfoRequest.objects.all()

        serializer = InfoRequestSerializer(info_requests, many = True)

        print(serializer.data)

        return Response(serializer.data, status = status.HTTP_200_OK)


