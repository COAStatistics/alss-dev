# Data Migrations

from django.db import migrations
from itertools import chain


def assign_new_type(apps, schema):
    Product = apps.get_model('surveys20', 'Product')
    Loss = apps.get_model('surveys20', 'Loss')
    Unit = apps.get_model('surveys20', 'Unit')
    for obj in list(chain(Product.objects.all(), Loss.objects.all(), Unit.objects.all())):
        if obj.type:
            obj.new_type = obj.type.id
            obj.save()


def revert_new_type(apps, schema):
    Product = apps.get_model('surveys20', 'Product')
    Loss = apps.get_model('surveys20', 'Loss')
    Unit = apps.get_model('surveys20', 'Unit')
    ProductType = apps.get_model('surveys20', 'ProductType')
    for obj in list(chain(Product.objects.all(), Loss.objects.all(), Unit.objects.all())):
        if obj.new_type:
            obj.type = ProductType.objects.get(id=obj.new_type)
            obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('surveys20', '0004_product_new_type'),
    ]

    operations = [
        migrations.RunPython(assign_new_type, revert_new_type)
    ]
