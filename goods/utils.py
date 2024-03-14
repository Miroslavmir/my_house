from goods.models import Products
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline


def q_search(query):
    if query.isdigit() and len(query) <= 5:
        return Products.objects.filter(id=int(query))

    vector = SearchVector("name", "description")
    search_query = SearchQuery(query)

    search_headline_params = {
        "field_name": "",
        "query": search_query,
        "start_sel": '<span style="background-color: yellow;">',
        "stop_sel": "</span>",
    }

    headline_params = {**search_headline_params, "field_name": "name"}
    bodyline_params = {**search_headline_params, "field_name": "description"}

    result = (
        Products.objects.annotate(rank=SearchRank(vector, search_query))
        .filter(rank__gt=0)
        .order_by("-rank")
        .annotate(headline=SearchHeadline(**headline_params))
        .annotate(bodyline=SearchHeadline(**bodyline_params))
    )

    return result