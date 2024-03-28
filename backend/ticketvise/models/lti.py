from django.db import models

class LTIKeySet(models.Model):
    id = models.UUIDField(primary_key=True, null=False)
    
    
class LTIKey(models.Model):
    id = models.UUIDField(primary_key=True, null=False)
    key_set_id = models.ForeignKey(LTIKeySet, on_delete=models.CASCADE, null=False)
    private_key = models.TextField(null=False)
    alg = models.TextField(null=False)
    

class LTIRegistration(models.Model):
    id = models.UUIDField(primary_key=True, null=False)
    issuer = models.TextField(null=False)
    client_id = models.TextField(null=False)
    platform_login_auth_endpoint = models.TextField(null=False)
    platform_service_auth_endpoint = models.TextField(null=False)
    platform_jwts_endpoint = models.TextField(null=False)
    platform_auth_provider = models.TextField()
    key_set_id = models.ForeignKey(LTIKeySet, on_delete=models.CASCADE, null=False)
    
    class Meta:
        unique_together = ('issuer', 'client_id')


class LTIDeployment(models.Model):
    deployment_id = models.TextField(null=False)
    registration_id = models.ForeignKey(LTIRegistration, on_delete=models.CASCADE, null=False)
    customer_id = models.TextField(null=False)
    
    class Meta:
        unique_together = ('deployment_id', 'registration_id')
