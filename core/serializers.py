from rest_framework import serializers
from core.models import *

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Textbook
        fields = ('name', 'author', 'sku', 'new_price', 'used_price', 'is_required')
