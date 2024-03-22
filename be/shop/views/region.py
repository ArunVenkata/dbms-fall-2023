from rest_framework.viewsets import ModelViewSet
from shop.models.region import Region
from shop.serializers import RegionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class RegionModelViewSet(ModelViewSet):
    serializer_class = RegionSerializer
    queryset = Region.objects.all()
    permission_classes = [IsAuthenticated]
    

class ChangeRegionView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        new_region = request.data.get("region")
        verified_region = Region.objects.filter(name__iexact=new_region).first()
        if not verified_region:
            return Response({"success": False, "message": "Invalid Region/Region Does not Exist"}, status=400)

        request.user.current_region = verified_region
        request.user.save()
        
        return Response({"success": True, "message": "Region Changed Successfully", "data": RegionSerializer(request.user.current_region).data})