import json

from django.http import HttpResponse
from geonode.base.models import HierarchicalKeyword as hk
from geonode.api.api import FILTER_TYPES
from geonode.base.models import ResourceBase


def h_keywords(request):
    type_filter = FILTER_TYPES[request.GET.get('type')] if request.GET.get('type', None) in FILTER_TYPES.keys() \
        else ResourceBase

    text_filter = request.GET.get('q', '')
    category_filter = request.GET.getlist('category', None)
    initial_keyword =request.GET.get('keyword', None)

    queryset = type_filter.objects.filter(title__icontains=text_filter)
    if len(category_filter) > 0:
        queryset = queryset.filter(category__identifier__in=category_filter)
    if initial_keyword is not None:
        queryset = queryset.filter(keywords__slug=initial_keyword)

    kw_ids = []
    if queryset is not None:
        for element in queryset:
            for kw in element.keywords.all():
                if kw.is_root():
                    kw_ids.append(kw.id)
                else:
                    kw_ids.append(hk.get_ancestors(kw)[0].id)

        keywords = hk.objects.filter(id__in=kw_ids).distinct()
        dumped_kw = []
        for keyword in keywords:
            dumped_kw.append(hk.dump_bulk_tree(keyword)[0])
        keywords = json.dumps(dumped_kw)
    else:
        keywords = json.dumps(hk.dump_bulk_tree())


    return HttpResponse(content=keywords)
