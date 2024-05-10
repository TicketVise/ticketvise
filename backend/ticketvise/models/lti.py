from django.db import models

from ticketvise.models.inbox import Inbox


class LTIDomain(models.Model):
    id = models.UUIDField(primary_key=True, null=False)
    domain = models.TextField(null=False)
    

class LTIClient(models.Model):
    id = models.UUIDField(primary_key=True, null=False)
    domain_id = models.ForeignKey(LTIDomain, on_delete=models.CASCADE, null=False)
    client_id = models.TextField(null=False)
    name = models.TextField(null=False)
    auth_login_url = models.TextField(null=False)
    auth_token_url = models.TextField(null=False)
    auth_audience = models.TextField(null=True)
    key_set_url = models.TextField(null=True)
    key_set = models.TextField(null=True)
    default = models.BooleanField(null=False, default=False)
    
    class Meta:
        unique_together = ('domain_id', 'client_id')
    

class LTIDeployment(models.Model):
    id = models.UUIDField(primary_key=True, null=False)
    client_id = models.ForeignKey(LTIClient, on_delete=models.CASCADE, null=False)
    deployment_id = models.TextField(null=False)
    name = models.TextField(null=False)
    description = models.TextField(null=True)
    
    class Meta:
        unique_together = ('client_id', 'deployment_id')
          
    def get_inboxes(self):
        return Inbox.objects.filter(deployment_id=self.id)


# class LTIKeySet(models.Model):
#     id = models.UUIDField(primary_key=True, null=False)
    
    
# class LTIKey(models.Model):
#     id = models.UUIDField(primary_key=True, null=False)
#     key_set_id = models.ForeignKey(LTIKeySet, on_delete=models.CASCADE, null=False)
#     private_key = models.TextField(null=False)
#     alg = models.TextField(null=False)
    

# class LTIRegistration(models.Model):
#     id = models.UUIDField(primary_key=True, null=False)
#     issuer = models.TextField(null=False)
#     client_id = models.TextField(null=False)
#     platform_login_auth_endpoint = models.TextField(null=False)
#     platform_service_auth_endpoint = models.TextField(null=False)
#     platform_jwts_endpoint = models.TextField(null=False)
#     platform_auth_provider = models.TextField()
#     key_set_id = models.ForeignKey(LTIKeySet, on_delete=models.CASCADE, null=False)
    
#     class Meta:
#         unique_together = ('issuer', 'client_id')


# class LTIDeployment(models.Model):
#     deployment_id = models.TextField(null=False)
#     registration_id = models.ForeignKey(LTIRegistration, on_delete=models.CASCADE, null=False)
#     customer_id = models.TextField(null=False)
    
#     class Meta:
#         unique_together = ('deployment_id', 'registration_id')
