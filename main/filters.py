from rest_framework.filters import BaseFilterBackend
import coreapi, coreschema


class CoursesMobileFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name='age_groups',
                location='query',
                required=False,
                schema=coreschema.Array()
            ),
            coreapi.Field(
                name='attendance_types',
                location='query',
                required=False,
                schema=coreschema.Array()
            ),
            coreapi.Field(
                name='grade_groups',
                location='query',
                required=False,
                schema=coreschema.Array()
            ),
            coreapi.Field(
                name='grade_types',
                location='query',
                required=False,
                schema=coreschema.Array()
            ),
            coreapi.Field(
                name='administrative_divisions',
                location='query',
                required=False,
                schema=coreschema.Array()
            ),
            coreapi.Field(
                name='time',
                location='query',
                required=False,
                schema=coreschema.String()
            ),
        ]
