from rest_framework import viewsets
from .models import Students
from .serializers import StudentsSerializers


class StudentView(viewsets.ModelViewSet):
    serializer_class = StudentsSerializers
    queryset = Students.objects.all()