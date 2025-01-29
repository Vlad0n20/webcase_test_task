import requests
import json
import xml.etree.ElementTree as ET


def fetch_data_from_source(url):
    response = requests.get(url)
    content_type = response.headers.get('Content-Type')

    if 'application/json' in content_type:
        return 'json', response.json()
    elif 'application/xml' in content_type or 'text/xml' in content_type:
        return 'xml', ET.fromstring(response.content)
    else:
        raise ValueError('Unsupported content type')

from .models import MainObject, RelatedObject1, RelatedObject2, RelatedObject3

def process_data(data_format, data):
    if data_format == 'json':
        process_json_data(data)
    elif data_format == 'xml':
        process_xml_data(data)

def process_json_data(data):
    for item in data:
        _id = item.pop('id')
        main_object, created = MainObject.objects.update_or_create(
            external_id=item['id'],
            defaults={**item}
        )
        process_related_objects(main_object, item)

def process_xml_data(data):
    for item in data.findall('item'):
        main_object, created = MainObject.objects.update_or_create(
            external_id=item.find('id').text,
            defaults={
                'field1': item.find('field1').text,
                'field2': item.find('field2').text,
            }
        )
        process_related_objects(main_object, item)

def process_related_objects(main_object, item):
    related1_data = item['related1'] if isinstance(item, dict) else item.find('related1')
    for related1 in related1_data:
        RelatedObject1.objects.update_or_create(
            main_object=main_object,
            external_id=related1['id'] if isinstance(related1, dict) else related1.find('id').text,
            defaults={
                'field1': related1['field1'] if isinstance(related1, dict) else related1.find('field1').text,
            }
        )

def load_data_from_source(url):
    data_format, data = fetch_data_from_source(url)
    process_data(data_format, data)