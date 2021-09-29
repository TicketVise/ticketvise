from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class Automation(models.Model):
    name = models.CharField(max_length=255)
    inbox = models.ForeignKey("Inbox", on_delete=models.CASCADE, related_name="automation_condition")
    action_func = models.CharField(max_length=50)
    action_value = models.CharField(max_length=50)

    def get_condtions(self):
        return AutomationCondition.objects.filter(automation=self) \
            .order_by("index")

    def execute(self, ticket):
        if all(condition(ticket) for condition in self.get_condtions()):
            getattr(ticket, self.action_func)(self.action_value)


class AutomationCondition(models.Model):
    automation = models.ForeignKey("Automation", on_delete=models.CASCADE)
    index = models.IntegerField()  # TODO: auto increment this value?
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
            try:
                value = field.related_model.objects.get(pk=value)
            except ObjectDoesNotExist:
                value = None
            field = getattr(ticket, self.field_name)
        elif isinstance(field, models.ManyToManyField):
            try:
                value = field.related_model.objects.get(pk=value).pk
            except ObjectDoesNotExist:
                value = None
            field = list(getattr(ticket, self.field_name).all().values_list("pk", flat=True))
            # If the evaluation function is equals, put value in a list so the lists can be compared to be equal.
            if self.evaluation_func == "eq":
                value = [value]
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
