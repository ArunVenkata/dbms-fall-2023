from rest_framework.views import APIView
from rest_framework.response import Response
from userauth.utils import get_access_token
from userauth.serializers import UserLoginSerializer, UserModelSerializer



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
        )
        user = login_serializer.validated_data["user"]
        user_token_data = get_access_token(user)
        user_data = UserModelSerializer(user, fields=included_fields).data
        user_data["token_info"] = user_token_data
        return Response({"success": True, "data": user_data}, status=200)
