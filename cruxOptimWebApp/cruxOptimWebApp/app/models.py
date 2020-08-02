# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

from django.utils.translation import ugettext_lazy as _


class ConversionFactor(models.Model):
    food = models.ForeignKey('Food', models.DO_NOTHING, blank=True, null=True)
    measure_id = models.IntegerField(blank=True, null=True)
    value = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    entry_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return ''

    def __unicode__(self):
        return self.__str__()

    class Meta:
        managed = True
        db_table = 'conversion_factor'


class DailyNutrientIntake(models.Model):
    intake_profile = models.ForeignKey('IntakeProfile', models.DO_NOTHING, blank=True, null=True)
    nutrient = models.ForeignKey('Nutrient', models.DO_NOTHING, blank=True, null=True)
    value = models.DecimalField(max_digits=10, decimal_places=5)

    def __str__(self):
        return ''

    def __unicode__(self):
        return self.__str__()

    class Meta:
        managed = True
        db_table = 'daily_nutrient_intake'


class Food(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.SmallIntegerField(blank=True, null=True)
    group_id = models.IntegerField(blank=True, null=True)
    source_id = models.IntegerField(blank=True, null=True)
    description_en = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_(u"Description"),
        help_text=_(u"Please enter a description for the food"))
    description_fr = models.CharField(max_length=255, blank=True, null=True)
    entry_date = models.DateField(blank=True, null=True)
    publication_date = models.DateField(blank=True, null=True)
    country_code = models.IntegerField(blank=True, null=True)
    scientific_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.description_en

    def __unicode__(self):
        return self.__str__()

    class Meta:
        managed = True
        db_table = 'food'


class FoodConstraint(models.Model):
    food = models.ForeignKey(Food, models.DO_NOTHING, blank=True, null=True)
    min_qty = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    max_qty = models.DecimalField(max_digits=10, decimal_places=5)

    def __str__(self):
        return ''

    def __unicode__(self):
        return self.__str__()

    class Meta:
        managed = True
        db_table = 'food_constraint'

class FoodGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.IntegerField(blank=True, null=True)
    name_en = models.CharField(max_length=200, blank=True, null=True)
    name_fr = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return ' - '.join( [self.code, self.name_en] )

    class Meta:
        managed = True
        db_table = 'food_group'


class FoodSource(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.IntegerField(blank=True, null=True)
    description_en = models.CharField(max_length=200, blank=True, null=True)
    description_fr = models.CharField(max_length=200, blank=True, null=True)


    def __str__(self):
        return ' - '.join( [self.code, self.description_en] )

    def __unicode__(self):
        return self.str()

    class Meta:
        managed = True
        db_table = 'food_source'


class IntakeProfile(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    scope = models.ForeignKey('IntakeProfileScope', models.DO_NOTHING, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.str()

    class Meta:
        managed = True
        db_table = 'intake_profile'


class IntakeProfileScope(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)


    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.str()

    class Meta:
        managed = True
        db_table = 'intake_profile_scope'


class Measure(models.Model):
    id = models.IntegerField(primary_key=True)
    description_en = models.CharField(max_length=200, blank=True, null=True)
    description_fr = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'measure'


class Nutrient(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    code = models.SmallIntegerField(blank=True, null=True)
    symbol = models.CharField(max_length=10, blank=True, null=True)
    unit = models.CharField(max_length=8, blank=True, null=True)
    name_en = models.CharField(max_length=200, blank=True, null=True)
    name_fr = models.CharField(max_length=200, blank=True, null=True)
    tagname = models.CharField(max_length=20, blank=True, null=True)
    num_decimals = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return ''.join( (self.name_en, ' (', self.symbol,')'))

    def __unicode__(self):
        return self.__str__()

    class Meta:
        managed = True
        db_table = 'nutrient'


class NutrientConstraint(models.Model):
    nutrient = models.ForeignKey(Nutrient, models.DO_NOTHING, blank=True, null=True)
    weight_overconsumption = models.DecimalField(max_digits=10, decimal_places=5)
    weight_underconsumption = models.DecimalField(max_digits=10, decimal_places=5)

    def __str__(self):
        return ''

    def __unicode__(self):
        return self.__str__()

    class Meta:
        managed = True
        db_table = 'nutrient_constraint'


class NutrientAmount(models.Model):
    food = models.ForeignKey(Food, models.DO_NOTHING, blank=True, null=True)
    nutrient = models.ForeignKey(Nutrient, models.DO_NOTHING, blank=True, null=True)
    value = models.DecimalField(max_digits=12, decimal_places=5, blank=True, null=True)
    standard_error = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    num_observations = models.SmallIntegerField(blank=True, null=True)
    nutrient_source_id = models.IntegerField(blank=True, null=True)
    entry_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return ''#.join( (self.food.description_en, self.nutrient.name_en ))
    
    def __unicode__(self):
        return self.__str__()

    class Meta:
        managed = True
        db_table = 'nutrient_amount'


class NutrientSource(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.IntegerField(blank=True, null=True)
    description_en = models.CharField(max_length=200, blank=True, null=True)
    description_fr = models.CharField(max_length=200, blank=True, null=True)


    def __str__(self):
        return ' - '.join([self.code, self.description_en])

    def __unicode__(self):
        return self.str()

    class Meta:
        managed = True
        db_table = 'nutrient_source'


class PlannerGoal(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=50, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    min_protein = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    max_protein = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    min_fat = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    max_fat = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    min_carb = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    max_carb = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)



    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.str()

    class Meta:
        managed = True
        db_table = 'planner_goal'


class PlannerNutrient(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    nutrient = models.ForeignKey(Nutrient, models.DO_NOTHING, blank=True, null=True)


    def __str__(self):
        return ''

    def __unicode__(self):
        return self.str()

    class Meta:
        managed = True
        db_table = 'planner_nutrient'


class RefuseAmount(models.Model):
    food = models.ForeignKey(Food, models.DO_NOTHING, blank=True, null=True)
    refuse_type = models.ForeignKey('RefuseType', models.DO_NOTHING, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    entry_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return ''

    def __unicode__(self):
        return self.str()

    class Meta:
        managed = True
        db_table = 'refuse_amount'


class RefuseType(models.Model):
    id = models.IntegerField(primary_key=True)
    description_en = models.CharField(max_length=200, blank=True, null=True)
    description_fr = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'refuse_type'


class YieldAmount(models.Model):
    food = models.ForeignKey(Food, models.DO_NOTHING, blank=True, null=True)
    yield_type = models.ForeignKey('YieldType', models.DO_NOTHING, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    entry_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return ''

    def __unicode__(self):
        return self.str()

    class Meta:
        managed = True
        db_table = 'yield_amount'


class YieldType(models.Model):
    id = models.IntegerField(primary_key=True)
    description_en = models.CharField(max_length=200, blank=True, null=True)
    description_fr = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'yield_type'
