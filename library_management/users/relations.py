from collections import OrderedDict
from rest_framework.relations import PrimaryKeyRelatedField


class PresentablePrimaryKeyRelatedField(PrimaryKeyRelatedField):
    """
    Taken From:
    ** https://github.com/Hipo/drf-extra-fields/blob/
       462212c06f2f10113d7ab98a74c3aecc3deb26df/drf_extra_fields/relations.py **
    Apache License 2.0
    Override PrimaryKeyRelatedField to represent serializer data instead of a pk field of the object
    """

    def use_pk_only_optimization(self):
        """
        Instead of sending pk only object, return full object. The object already retrieved from db
        by drf. This doesn't cause an extra query.
        It even might save from making an extra query on serializer.to_representation method.
        Related source codes:
        - ** https://github.com/tomchristie/django-rest-framework/
             blob/master/rest_framework/relations.py#L41 **
        - ** https://github.com/tomchristie/django-rest-framework/
             blob/master/rest_framework/relations.py#L132 **
        """
        return False

    def __init__(self, **kwargs):
        self.presentation_serializer = kwargs.pop('presentation_serializer', None)
        assert self.presentation_serializer is not None, (
            'PresentablePrimaryKeyRelatedField must provide a `presentation_serializer` argument'
        )
        super(PresentablePrimaryKeyRelatedField, self).__init__(**kwargs)

    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            # Ensure that field.choices returns something sensible
            # even when accessed with a read-only field.
            return {}

        if cutoff is not None:
            queryset = queryset[:cutoff]

        return OrderedDict([(item.pk, self.display_value(item))
                            for item in queryset])

    def to_representation(self, data):
        return self.presentation_serializer(data, context=self.context).data
