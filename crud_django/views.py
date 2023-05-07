# from rest_framework import viewsets
# from .models import Students
# from .serializers import StudentsSerializers

import torch
torch.__version__

from transformers import pipeline
import pandas as pd

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def process_text(request):
    tqa = pipeline(task="table-question-answering",model="google/tapas-base-finetuned-wtq")
    table=pd.read_csv("data.csv")
    table = table.astype(str)
    table
    input_text = request.data.get('text')
    query = input_text.upper() 
    processed_text = tqa(table=table,query=query)["answer"]
    print(processed_text)

    return Response({'processed_text': processed_text})


# class StudentView(viewsets.ModelViewSet):
    # tqa = pipeline(task="table-question-answering",model="google/tapas-base-finetuned-wtq")
    # table=pd.read_csv("data.csv")
    # table = table.astype(str)

    # table
    # for x in range(0,1):
    #     print("Ask a Question?")
    #     query = input()
    #     print(tqa(table=table,query=query)["answer"])

    # print("Your Five Questions are over")
    # serializer_class = StudentsSerializers
    # queryset = Students.objects.all()



    