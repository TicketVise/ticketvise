from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.utils import dateparse

from ticketvise.models.label import Label
from ticketvise.models.ticket import Ticket
from ticketvise.models.user import User


class Automation(models.Model):
    name = models.CharField(max_length=255)
    inbox = models.ForeignKey("Inbox", on_delete=models.CASCADE, related_name="automations")
    action_func = models.CharField(max_length=50)
    action_value = models.CharField(max_length=50)

    def get_conditions(self):
        return AutomationCondition.objects.filter(automation=self)

    def execute(self, ticket):
        conditions = self.get_conditions()
        if conditions and all(condition(ticket) for condition in conditions):
            value = None
            # TODO: Wat gebeurd er als een user of label verwijderd wordt, maar de automation nog bestaat.
            if self.action_func == "assign_to":
                try:
                    value = User.objects.get(pk=self.action_value)
                except ObjectDoesNotExist:
                    value = None
            elif self.action_func == "add_label":
                try:
                    value = Label.objects.get(pk=self.action_value)
                except ObjectDoesNotExist:
                    value = None

            getattr(ticket, self.action_func)(value)


class AutomationCondition(models.Model):
    EVALUATION_FUNC_CHOICES = [
        ("eq", "equals"),
        ("contains", "contains"),
        ("contains_not", "contains not"),
        ("gt", "greater than"),
        ("ge", "greater than or equals"),
        ("lt", "less than"),
        ("le", "less than or equal"),
        ("is_set", "is set"),
    ]

    automation = models.ForeignKey("Automation", on_delete=models.CASCADE)
    field_name = models.CharField(max_length=50)
    evaluation_func = models.CharField(max_length=50, choices=EVALUATION_FUNC_CHOICES)
    evaluation_value = models.CharField(max_length=50)
    negation = models.BooleanField(default=False)

    def parse_iso(self, value):
        try:
            try:
                return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f%z')
            except ValueError:
                return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S%z')
        except ValueError as e:
            raise ValidationError(f"Field 'evaluation_value' expected a date in combination with field_name '{self.field_name}', but got '{self.evaluation_value}'.") from e



    def clean(self):
        super().clean()
        # Checks if the field is a ticket field and uses the field for further cleaning
        field = Ticket._meta.get_field(self.field_name)

        # Check if foreign keys and manytomany fields have an int as evaluation value.
        if (isinstance(field, models.ForeignKey) or isinstance(field, models.ManyToManyField)) \
                and not self.evaluation_value.isdigit():
            raise ValidationError(
                f"Field 'evaluation_value' expected a number in combination with field_name '{self.field_name}', but got '{self.evaluation_value}'.")


        # Parse ISO 8601 date format
        if self.evaluation_func != "is_set" and isinstance(field, models.DateField):
            self.parse_iso(self.evaluation_value)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.full_clean()
        super().save(force_insert, force_update, using, update_fields)

    def __call__(self, ticket):
        field = ticket._meta.get_field(self.field_name)
        # does this do anything?
        value = self.evaluation_value

        if self.evaluation_func == "is_set":
            value = "True" if getattr(ticket, self.field_name) else "False"
            return value == self.evaluation_value

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
            if self.evaluation_func == "eq":
                value = [value]
        elif isinstance(field, models.DateTimeField):
            value = dateparse.parse_datetime(self.evaluation_value)
            attr = dateparse.parse_datetime(str(getattr(ticket, self.field_name)))

            field = datetime.fromisoformat(str(attr))
            value = datetime.fromisoformat(str(value))
        else:
            field = str(getattr(ticket, self.field_name)).lower()
            value = str(value).lower()

        evaluation = getattr(self, self.evaluation_func)(field, value)

        if self.negation:
            return not evaluation
        else:
            return evaluation

    def eq(self, field, value):
        return field == value

    def contains(self, field, value):
        return value in field

    def contains_not(self, field, value):
        return value not in field

    def gt(self, field, value):
        return field > value

    def ge(self, field, value):
        return field >= value

    def lt(self, field, value):
        return field < value

    def le(self, field, value):
        return field <= value

    def is_set(self, field, value):
        return str(field is not None and field != "None") == value
