from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from userauth.models import SalesUser
from shop.models import Store
from rest_framework.response import Response
from userauth.serializers import SalesUserModelSerializer


class SalesPersonsStoreView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # get all unassigned Sales persons
        qs = SalesUser.objects.all()
        store_id = request.query_params.get("store_id")
        if store_id and Store.objects.filter(id=store_id).exists():
            qs = qs.filter(store_assigned_id=store_id)
        
        return Response(SalesUserModelSerializer(qs, many=True).data)
