from rest_framework.views import APIView
from django.db import transaction
from rest_framework.response import Response
from userauth.models import Address, User, USER_TYPES, BusinessUser, SalesUser, HomeUser
from userauth.serializers import (
    UserModelSerializer,
    UserSignUpSerialzier,
    HomeUserSignUpSerializer,
    SalesUserSignUpSerializer,
    BusinessUserSignUpSerializer,
)
from django.contrib.auth.hashers import make_password


class UserSignUp(APIView):
    http_method_names = ["post"]

    def post(self, request):
        signup_serializer = UserSignUpSerialzier(data=request.data)
        if not signup_serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "message": "Invalid Request",
                    "errors": signup_serializer.errors,
                },
                status=403,
            )
        signup_validated_data = signup_serializer.validated_data
        validated_data = {
            **signup_serializer.initial_data,
            **signup_validated_data,
        }
        if validated_data["user_type"] == USER_TYPES.home:
            signup_serializer = HomeUserSignUpSerializer(data=validated_data)
        elif validated_data["user_type"] == USER_TYPES.business:
            signup_serializer = BusinessUserSignUpSerializer(data=validated_data)
        elif validated_data["user_type"] == USER_TYPES.salesperson:
            signup_serializer = SalesUserSignUpSerializer(data=validated_data)

        if not signup_serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "message": "Invalid Request",
                    "errors": signup_serializer.errors,
                }
            )
        validated_data = {
            **signup_serializer.initial_data,
            **signup_serializer.validated_data,
        }
        with transaction.atomic():
            user = User.objects.create(
                email=validated_data["email"],
                first_name=validated_data["first_name"],
                last_name=validated_data.get("last_name"),
                user_type=validated_data["user_type"],
                password=make_password(validated_data["password"]),
            )

            sales_user, business_user = None, None
            validated_data["id"] = str(user.id)
            if validated_data.get("address"):
                Address.objects.create(user=user, **validated_data["address"])
            if validated_data["user_type"] == USER_TYPES.business:
                business_user = BusinessUser.objects.create(
                    user=user,
                    business_category=validated_data["business_category"],
                    gross_annual_income=validated_data["gross_annual_income"],
                )
            elif validated_data["user_type"] == USER_TYPES.salesperson:
                sales_user = SalesUser.objects.create(
                    user=user,
                    job_title=validated_data["job_title"],
                    income=validated_data["income"],
                )
                if store_id := validated_data["store_assigned"]:
                    sales_user.store_assigned = store_id
                    sales_user.save()
            elif validated_data["user_type"] == USER_TYPES.home:
                home_user = HomeUser.objects.create(
                    user=user,
                    marital_status=validated_data["marital_status"],
                    age=validated_data["age"],
                    gender=validated_data["gender"],
                    income=validated_data["income"],
                )

        return Response(
            {"success": True, "message": "Created User", "data": validated_data}
        )
