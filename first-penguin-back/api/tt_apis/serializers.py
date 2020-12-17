from rest_framework import serializers
import random
from . import models as tmodel

class SwpSerializer(serializers.ModelSerializer):
    class Meta:
        model = tmodel.TestMaster
        fields =("ques_id","ques_path1","ques_path2")

class PhSerializer(serializers.ModelSerializer):
    class Meta:
        model = tmodel.TestMaster
        fields = ("ques_id","ques_path1","ques_char")

class FocSerializer(serializers.ModelSerializer):
    class Meta:
        model = tmodel.TestMaster
        fields = ("ques_id","ques_path1","ques_int","ques_char","ques_level")

class ReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = tmodel.CureMaster
        fields=("cure_id","cure_level","cure_path","cure_tid","cure_text")

class CountSerializer(serializers.ModelSerializer):
    class Meta:
        model = tmodel.CureMaster
        fields = ("cure_id","cure_level","cure_path","cure_word")

class CommonSerializer(serializers.ModelSerializer):
    class Meta:
        model = tmodel.ComCure
        fields = '__all__'

class VowelsoundSerializer(serializers.ModelSerializer):
    answer = serializers.SerializerMethodField()

    class Meta:
        model = tmodel.CureMaster
        fields = ("cure_id","cure_level","cure_path","cure_path2","cure_word","cure_word2","answer")

    def get_answer(self,validated_data):
        x = random.randint(1,2)
        if x == 1:
            return 1
        else:
            return 2

class ConsomatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = tmodel.CureMaster
        fields = ("cure_id","cure_level","cure_path","cure_path2","cure_word","cure_tid")

class ConsocommonSerializer(serializers.ModelSerializer):
    class Meta:
        model = tmodel.CureMaster
        fields = ("cure_id","cure_level","cure_path","cure_word","cure_word2","cure_text")

class ConsosoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = tmodel.CureMaster
        fields = ("cure_id","cure_level","cure_path","cure_word","cure_word2")

class VoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = tmodel.Voice
        fields = ("voc_path","voc_script","voc_desc")

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = tmodel.Student
        fields = ("stu_id","stu_name","stu_gender","stu_birth","ic_id")