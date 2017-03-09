import json

from django.http import HttpResponse
from geonode.base.models import HierarchicalKeyword as hk
from geonode.api.api import FILTER_TYPES


def h_keywords(request):
    type_filter = FILTER_TYPES[request.GET.get('type')] if request.GET.get('type', None) in FILTER_TYPES.keys() \
        else None

    text_filter = request.GET.get('q', '')

    queryset = None
    if type_filter is not None:
        queryset = type_filter.objects.filter(title__icontains=text_filter)

    keywords = hk.objects.none()
    if queryset is not None:
        for element in queryset:
            keywords = keywords | element.keywords.all()

        keywords = keywords.distinct()
        dumped_kw = []
        for keyword in keywords:
            dumped_kw.append(hk.dump_bulk_tree(keyword)[0])
        keywords = json.dumps(dumped_kw)
    else:
        keywords = json.dumps(hk.dump_bulk_tree())


    return HttpResponse(content=keywords)
