# Thirdparty imports
from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class PaginateByPageLimit(PageNumberPagination):
    page_size = settings.PAGINATE_PAGE_SIZE
    page_size_query_param = 'limit'
