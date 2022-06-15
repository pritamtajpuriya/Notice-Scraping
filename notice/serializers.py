from rest_framework import serializers
from .models import *


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ('title', 'belongs', 'date', 'file', 'category',)
