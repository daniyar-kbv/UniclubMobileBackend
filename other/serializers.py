from rest_framework import serializers

from.models import AgeGroup, AttendanceType, AdministrativeDivision, GradeType, GradeTypeGroup


class AgeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgeGroup
        fields = ['id', 'from_age', 'to_age']


class AttendanceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceType
        fields = '__all__'


class GradeTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeType
        exclude = ['group']


class GradeTypeGroupWithTypesSerializer(serializers.ModelSerializer):
    types = GradeTypeListSerializer(many=True)

    class Meta:
        model = GradeTypeGroup
        fields = ['id', 'name', 'types']


class GradeTypeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeTypeGroup
        fields = ['id', 'name']


class AdministrativeDivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdministrativeDivision
        fields = '__all__'


class FilterDataSerializer(serializers.Serializer):
    age_groups = AgeGroupSerializer(many=True)
    attendance_types = AttendanceTypeSerializer(many=True)
    administrative_divisions = AdministrativeDivisionSerializer(many=True)
    grade_groups = GradeTypeGroupWithTypesSerializer(many=True)
    time_types = serializers.ListField(child=serializers.CharField())
