from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Message
from .serializers import MessageSerializer
from django.shortcuts import  get_list_or_404

class MyAPIView(APIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.all()

    def get(self, request):
        fmt = request.GET.get('FMT')
        msg = request.GET.get('msg')
        if fmt == 'true':
            if msg:
                # Serialize the msg data and return it in JSON format
                serializer = MessageSerializer(data={"msg": msg})
                if serializer.is_valid():
                    return Response(serializer.data, status=200)
                return Response(serializer.errors, status=400)
            else:
                # Get a list of all messages from the database
                # messages=self.get_queryset()
                # Serialize the messages and return them in JSON format
                serializer = MessageSerializer(self.get_queryset(), many=True)
                return Response(serializer.data, status=200)
        elif fmt == 'false':
            if msg:
                # Return the msg data as CSV
                return HttpResponse(f'msg\n{msg}', content_type='text/csv')
            else:
                # Get a list of all messages from the database
                messages = self.get_queryset()
                # Format the messages as CSV and return them in the response
                csv = 'msg\n'
                for message in messages:
                    csv += f'{message.msg}\n'
                return HttpResponse(csv, content_type='text/csv')
        # Return an empty response for other request methods
        return HttpResponse()

    def post(self):
        pass

# @csrf_exempt
# def MyAPIView(request):
#     if request.method == 'GET':
#         fmt = request.GET.get('FMT')
#         msg = request.GET.get('msg')
#         if fmt == 'true':
#             if msg:
#                 serializer = MessageSerializer(data={"msg": msg})
#                 if serializer.is_valid():
#                     return JsonResponse(serializer.data, status=200)
#                 return JsonResponse(serializer.errors, status=400)
#             else:
#                 # Get a list of all messages from the database
#                 messages = get_list_or_404(Message)
#                 # Serialize the messages and return them in JSON format
#                 serializer = MessageSerializer(messages, many=True)
#                 return JsonResponse(serializer.data, safe=False, status=200)

#         elif fmt == 'false':
#             if msg:
#                 return HttpResponse(msg, content_type='text/csv')
#             else:
#                 # Get a list of all messages from the database
#                 messages = get_list_or_404(Message)
#                 # Format the messages as CSV and return them in the response
#                 csv = 'msg\n'
#                 for message in messages:
#                     csv += f'{message.msg}\n'
#                 return HttpResponse(csv, content_type='text/csv')

#     # Return an empty response for other request methods
#     return HttpResponse()