from uuid import uuid4
from django.db.models import Model, DateTimeField, UUIDField
from rest_framework.serializers import Serializer, ModelSerializer

class BaseModel(Model):
    id = UUIDField(primary_key=True, default = uuid4)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        """Base Meta class"""
        abstract = True






class DynamicFieldsSerializer(Serializer):
    """
    A Serializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)
        exclude = kwargs.pop("exclude", None)
        include_fields = kwargs.pop("include_fields", None)
        # Instantiate the superclass normally
        super(DynamicFieldsSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
            return
        if include_fields is not None:
            for field_name, field_instance in include_fields:
                self.fields.update({f"{field_name}": field_instance})
        if exclude is not None:
            to_be_excluded = set(exclude)
            for field_name in to_be_excluded:
                self.fields.pop(field_name)


class DynamicFieldsModelSerializer(ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)
        exclude = kwargs.pop("exclude", None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
            return

        if exclude is not None:
            to_be_excluded = set(exclude)
            for field_name in to_be_excluded:
                self.fields.pop(field_name)

