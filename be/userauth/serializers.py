from utilities import DynamicFieldsModelSerializer, DynamicFieldsSerializer
from rest_framework.serializers import (
    CharField,
    EmailField,
    IntegerField,
    ValidationError as SerializerValidationError,
    ChoiceField,
    DecimalField,
    UUIDField,
)


from userauth.models import User, Address
from userauth.enums import USER_TYPES, MARITAL_STATUSES


class UserModelSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
class UserViewsetSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "user_type", "email", "created_at")

class UserLoginSerializer(DynamicFieldsSerializer):
    email = EmailField()
    password = CharField()

    def validate(self, data):
        # if user valid, allow else raise error
        email = data["email"]
        passwd = data["password"]

        user = User.objects.filter(email=email).first()
        if not user:
            raise SerializerValidationError("User Does not exist. Please Sign Up.")
        if not user.check_password(passwd):
            raise SerializerValidationError("Incorrect Password. Try Again")
        data["user"] = user
        return data


class AddressModelSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class UserSignUpSerialzier(DynamicFieldsSerializer):
    email = EmailField(required=True)
    password = CharField(min_length=8)
    first_name = CharField(required=True)
    last_name = CharField(required=True)
    user_type = ChoiceField(choices=list(map(lambda x: (x.name, x.value), USER_TYPES)))
    # address = AddressModelSerializer(exclude=("id", ))

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise SerializerValidationError(
                "User Already Exists. Please use Different Email"
            )
        return email


class BusinessUserSignUpSerializer(DynamicFieldsSerializer):
    business_category = CharField(required=True)
    gross_annual_income = DecimalField(max_digits=20, decimal_places=2, required=True)


class HomeUserSignUpSerializer(DynamicFieldsSerializer):
    marital_status = ChoiceField(
        choices=list(map(lambda x: (x.name, x.value), MARITAL_STATUSES))
    )
    gender = CharField()
    age = IntegerField()
    income = DecimalField(max_digits=20, decimal_places=2)


class SalesUserSignUpSerializer(DynamicFieldsSerializer):
    job_title = CharField(max_length=150)
    store_assigned = UUIDField(allow_null=True, required=False)
    income = DecimalField(max_digits=20, decimal_places=2)
