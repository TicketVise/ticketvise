from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.generics import ListAPIView
from ticketvise.models.lti import LTIDomain, LTIClient, LTIDeployment
from ticketvise.views.api.security import UserIsSuperUserPermission


class LTIDeploymentSerializer(ModelSerializer):
    class Meta:
        model = LTIDeployment
        fields = ['deployment_id', 'name', 'description']


class LTIClientSerializer(ModelSerializer):
    deployments = SerializerMethodField()

    def get_deployments(self, obj):
        return LTIDeploymentSerializer(LTIDeployment.objects.filter(client_id=obj.id), many=True).data

    class Meta:
        model = LTIClient
        fields = ['client_id', 'name', 'auth_login_url', 'auth_token_url', 'auth_audience', 'key_set_url', 'key_set', 'default', 'deployments']


class LTIDomainSerializer(ModelSerializer):
    clients = SerializerMethodField()

    def get_clients(self, obj):
        return LTIClientSerializer(LTIClient.objects.filter(domain_id=obj.id), many=True).data

    class Meta:
        model = LTIDomain
        fields = ['domain', 'clients']


class LTIApiView(ListAPIView):
    permission_classes = [UserIsSuperUserPermission]
    queryset = LTIDomain.objects.all()
    serializer_class = LTIDomainSerializer

    def get_queryset(self):
        return LTIDomain.objects.all()
