from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import VitalLog, SymptomLog, ClinicalNote
from .serializers import VitalLogSerializer, SymptomLogSerializer, ClinicalNoteSerializer
from accounts.permissions import IsPatientRole, IsStaffOrAdmin

class VitalLogView(APIView):
    permission_classes = [IsPatientRole]

    def get(self, request):
        logs = VitalLog.objects.filter(user=request.user).order_by('-created_at')
        serializer = VitalLogSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = VitalLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VitalLogDetailView(APIView):
    permission_classes = [IsPatientRole]

    def patch(self, request, pk):
        try:
            log = VitalLog.objects.get(pk=pk, user=request.user)
        except VitalLog.DoesNotExist:
            return Response({"detail": "Log not found or access denied."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = VitalLogSerializer(log, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SymptomLogView(APIView):
    permission_classes = [IsPatientRole]

    def get(self, request):
        logs = SymptomLog.objects.filter(user=request.user).order_by('-created_at')
        serializer = SymptomLogSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SymptomLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SymptomLogDetailView(APIView):
    permission_classes = [IsPatientRole]

    def patch(self, request, pk):
        try:
            log = SymptomLog.objects.get(pk=pk, user=request.user)
        except SymptomLog.DoesNotExist:
            return Response({"detail": "Record not found or access denied."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SymptomLogSerializer(log, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            log = SymptomLog.objects.get(pk=pk, user=request.user)
            log.delete()
            return Response({"detail": "Symptom log deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except SymptomLog.DoesNotExist:
            return Response({"detail": "Record not found or access denied."}, status=status.HTTP_404_NOT_FOUND)

class ClinicalNoteDetailView(APIView):
    permission_classes = [IsStaffOrAdmin]

    def patch(self, request, pk):
        try:
            note = ClinicalNote.objects.get(pk=pk)
        except ClinicalNote.DoesNotExist:
            return Response({"detail": "Clinical entry not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Ensure staff authors can only patch their own notes; admins can patch any note
        if request.user.role != 'ADMIN' and note.provider != request.user:
            return Response({"detail": "Permission denied. You did not author this note."}, status=status.HTTP_403_FORBIDDEN)
            
        serializer = ClinicalNoteSerializer(note, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)