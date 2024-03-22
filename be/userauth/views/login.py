from rest_framework.views import APIView
from rest_framework.response import Response
from userauth.models import SalesUser
from userauth.enums import USER_TYPES
from shop.models.region import Region
from userauth.utils import get_access_token
from userauth.serializers import UserLoginSerializer, UserModelLoginSerializer



class UserLogin(APIView):
    http_method_names = ["post"]

    def post(self, request):
        login_serializer = UserLoginSerializer(data=request.data)
        if not login_serializer.is_valid(raise_exception=False):
            return Response(
                {
                    "success": False,
                    "message": "Invalid Request",
                    "errors": login_serializer.errors,
                },
                status=403,
            )
        included_fields = (
            "id",
            "email",
            "created_at",
            "first_name",
            "last_name",
            "user_type",
            "current_region",
            "is_superuser"
        )
        user = login_serializer.validated_data["user"]
        print(user, user.current_region, "REGION")
        if user and not user.current_region:
            region = None
            if user.user_type == USER_TYPES.salesperson:
                sales_user = SalesUser.objects.filter(user_id=user.id).first()
                if sales_user and sales_user.store_assigned:
                    region = sales_user.store_assigned.region
            if not region:
                region = Region.objects.first()
            user.current_region = region
            user.save()
        user_token_data = get_access_token(user)
        user_data = UserModelLoginSerializer(user, fields=included_fields).data
        user_data["token_info"] = user_token_data

        return Response({"success": True, "data": user_data}, status=200)
