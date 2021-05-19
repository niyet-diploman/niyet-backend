from django_filters import rest_framework as filters
from app.donations.models import *
from app.utility.models import *


def get_filter_by_id_function(model, param_name):
    def filter_function(request):
        if request is None:
            return model.objects.none()
        id = request.query_params.get(param_name, None)
        if id is not None:
            return model.objects.filter(id=id)
        return model.objects.all()

    return filter_function


class BeneficiaryFilter(filters.FilterSet):
    city = filters.ModelChoiceFilter(queryset=get_filter_by_id_function(City, 'city'))
    age = filters.NumberFilter(lookup_expr='gt')
    program = filters.ModelChoiceFilter(queryset=get_filter_by_id_function(Program, 'program'))

    class Meta:
        model = Beneficary
        fields = ['city', 'age', 'program']
