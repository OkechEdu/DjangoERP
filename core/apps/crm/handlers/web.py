from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView

from core.apps.crm.handlers.factories import get_repository_for_lead_creation
from core.apps.crm.logic.lead import create_lead
from core.apps.crm.repo.exceptions import LeadExistException


class LeadAPIView(APIView):
    def post(self, request):
        data = request.data
        lead_repo = get_repository_for_lead_creation(use_case_type="internal")
        try:
            lead = create_lead(lead_data=data, lead_repo=lead_repo)
        except LeadExistException:
            return HttpResponse(
                error="Lead with that Email Ecist", status=status.HTTP_400_BAD_REQUEST
            )
        return HttpResponse(lead.json(), status=status.HTTP_201_CREATED)
