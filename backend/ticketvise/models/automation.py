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
    index = models.IntegerField() #TODO: auto increment this value?
    field_name = models.CharField(max_length=50)
    evaluation_func = models.CharField(max_length=50)
    evaluation_value = models.CharField(max_length=50)
    negation = models.BooleanField(default=False)

    class Meta:
        unique_together = ["automation", "index"]

    def __call__(self, ticket):
        field = ticket._meta.get_field(self.field_name)
        value = self.evaluation_value
        if isinstance(field, models.ForeignKey):
            value = field.related_model.objects.get(pk=value)
            field = getattr(ticket, self.field_name)
        elif isinstance(field, models.ManyToManyField):
            # Convert to list to be able to make comparisons, Querysets cannot be compared.
            value = list(field.related_model.objects.filter(pk=value).values("pk"))
            field = list(getattr(ticket, self.field_name).all().values("pk"))
        else:
            field = str(getattr(ticket, self.field_name))
            value = str(value)

        return getattr(self, self.evaluation_func)(field, value)

    def eq(self, field, value):
        return field == value

    def contains(self, field, value):
        return value in field

    def gt(self, field, value):
        return field > value

    def ge(self, field, value):
        return field >= value

    def lt(self, field, value):
        return field < value

    def le(self, field, value):
        return field <= value
