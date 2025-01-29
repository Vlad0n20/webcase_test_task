from drf_yasg import openapi

swagger_schema_fields_dict = {
    'fields': openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=openapi.Schema(type=openapi.TYPE_STRING),
    )
}
