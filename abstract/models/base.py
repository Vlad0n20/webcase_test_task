import logging

from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import connections, models
from django.db.models import ForeignKey
from django.db.models.query import QuerySet


logger = logging.getLogger(__name__)

class QuerySetExplainMixin:
    def explain(self, *args):
        extra_arguments = ''
        for item in args:
            extra_arguments = f'{extra_arguments} {item}' if isinstance(item, str) else extra_arguments
        cursor = connections[self.db].cursor()
        query, params = self.query.sql_with_params()
        cursor.execute('explain analyze verbose %s' % query, params)
        return '\n'.join(r[0] for r in cursor.fetchall())


QuerySet = type('QuerySet', (QuerySetExplainMixin, QuerySet), dict(QuerySet.__dict__))


class BaseModel(models.Model, QuerySetExplainMixin):
    migration_page_size = 50000

    objects = models.QuerySet.as_manager()

    class Meta:
        abstract = True

    def __unicode__(self):
        return f'{self.id}'

    def __str__(self):
        return f'{self.__class__.__name__} {self.id}'

    @classmethod
    def get_fk_field_names(cls):
        return [field.name for field in cls._meta.get_fields() if
                field.is_relation and not field.auto_created and (
                field.many_to_one or field.one_to_one) and not isinstance(field, GenericForeignKey)]

    @classmethod
    def get_m2m_field_names(cls):
        return [field.attname or field.name for field in
                cls._meta.get_fields() if
                field.is_relation and field.many_to_many and not hasattr(field, 'field')]

    def reload(self):
        return self.refresh_from_db()

    def clone(self):
        """Create a new, unsaved copy of this object."""
        copy = self.__class__.objects.get(pk=self.pk)
        copy.id = None

        # empty all the fks
        fk_field_names = [f.name for f in self._meta.model._meta.get_fields() if
                          isinstance(f, (ForeignKey, GenericForeignKey))]
        for field_name in fk_field_names:
            setattr(copy, field_name, None)

        try:
            copy._id = bson.ObjectId()
        except AttributeError:
            pass
        return copy


