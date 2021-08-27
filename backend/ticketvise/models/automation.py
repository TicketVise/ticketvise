from django.db import models

class Automation(models.Model):
    name = models.CharField(max_length=255)
    inbox = models.ForeignKey("Inbox", on_delete=models.CASCADE, related_name="automation_condition")
    # assign_to = models.ForeignKey("User", on_delete=models.CASCADE)

    def get_condtions(self):
        return AutomationCondition.objects.filter(automation=self)\
            .order_by("index")

    def execute(self, ticket):
        if all(condition(ticket) for condition in self.get_condtions()):
            ticket.assign_to(self.assign_to)


class AutomationCondition(models.Model):
    automation = models.ForeignKey("Automation", on_delete=models.CASCADE)
    index = models.IntegerField()
    field_name = models.CharField(max_length=50)
    evaluation_func = models.CharField(max_length=50)
    evaluation_value = models.CharField(max_length=50)
    negation = models.BooleanField(default=False)

    class Meta:
        unique_together = ["automation", "index"]

    def __call__(self, ticket):
        # field_type = type(ticket._meta.get_field(self.field_name))
        # parsed_evaluation_value = field_type(self.evaluation_value)
        return getattr(self, self.evaluation_func)(ticket, self.field_name, self.evaluation_value)

    def equals(self, ticket, field_name, value):
        test = str(getattr(ticket, field_name))
        return str(getattr(ticket, field_name)) == value

    def contains(self, ticket, field_name, value):
        pass

    def gt(self, ticket, field_name, value):
        return str(getattr(ticket, field_name)) > value

    def gte(self, ticket, field_name, value):
        pass

    def lt(self, ticket, field_name, value):
        pass

    def lte(self, ticket, field_name, value):
        pass

