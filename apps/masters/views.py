from __future__ import unicode_literals, absolute_import

from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .models import State, City, Country


# Create your views here.
@api_view()
@permission_classes((AllowAny,))
def get_countries(request):
    data = {
        'countries': [{'name': country.name, 'id': country.id} for country in Country.objects.all()] or []
    }
    return JsonResponse(data)


@api_view()
@permission_classes((AllowAny,))
def get_states(request):
    country_id = request.GET.get('country', None) or -1
    data = {
        'states': [{'name': state.name, 'id': state.id} for state in State.objects.filter(country=country_id)] or []
    }
    return JsonResponse(data)


@api_view()
@permission_classes((AllowAny,))
def get_cities(request):
    state_id = request.GET.get('state', None) or -1
    data = {
        'cities': [{'name': city.name, 'id': city.id} for city in City.objects.filter(state=state_id)] or []
    }

    return JsonResponse(data)
