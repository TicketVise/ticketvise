from django.db import models

class Automation(models.Model):
    name = models.CharField(max_length=255)
    inbox = models.ForeignKey("Inbox", on_delete=models.CASCADE, related_name="automation_condition")
    assign_to = models.ForeignKey("User", on_delete=models.CASCADE)

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
        return getattr(self, self.evaluation_func)()

    def equals(self):
        print(self.__dict__.values())
        pass