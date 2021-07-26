from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Burger(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    weight = fields.FloatField()
    commanditor = fields.CharField(max_length=250)

    class PydanticMeta:
        pass


burger_pydantic = pydantic_model_creator(Burger, name="burger")
burger_in_pydantic = pydantic_model_creator(
    Burger, name="burger_in", exclude_readonly=True)
