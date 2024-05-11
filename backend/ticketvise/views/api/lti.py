from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.generics import ListAPIView, RetrieveAPIView
from ticketvise.models.user import UserInbox
from ticketvise.models.ticket import Ticket
from ticketvise.models.inbox import Inbox
from ticketvise.models.lti import LTIDomain, LTIClient, LTIDeployment
from ticketvise.views.api.inbox import InboxSerializer
from ticketvise.views.api.security import UserIsSuperUserPermission


class LTIDeploymentSerializer(ModelSerializer):
    class Meta:
        model = LTIDeployment
        fields = '__all__'
        
        
class LTIDeploymentWithInboxesSerializer(ModelSerializer):
    inboxes = SerializerMethodField()
    statistics = SerializerMethodField()
    
    def get_inboxes(self, obj):
        return InboxSerializer(Inbox.objects.filter(deployment_id=obj.id), many=True).data
    
    def get_statistics(self, obj):
        stats = {}

        stats['tickets'] = sum(Ticket.objects.filter(inbox=inbox['id']).count() for inbox in self.get_inboxes(obj))
        stats['users'] = sum(UserInbox.objects.filter(inbox=inbox['id']).count() for inbox in self.get_inboxes(obj))
        return stats
    
    class Meta:
        model = LTIDeployment
        fields = ['id', 'client_id', 'deployment_id', 'name', 'description', 'inboxes', 'statistics']


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


class LTIDeploymentApiView(RetrieveAPIView):
    permission_classes = [UserIsSuperUserPermission]
    serializer_class = LTIDeploymentWithInboxesSerializer
    queryset = LTIDeployment.objects.all()
