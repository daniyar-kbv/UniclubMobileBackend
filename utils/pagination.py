from rest_framework.response import Response
from rest_framework import pagination, status


class CustomPagination(pagination.PageNumberPagination):
    page_size = 15

    def get_paginated_response(self, data):
        data = {
            'results': data,
            'page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
        }
        return Response(data, status=status.HTTP_200_OK)
