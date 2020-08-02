from django.contrib import admin

from . import models

@admin.register(models.FoodGroup)
class FoodGroupAdmin(admin.ModelAdmin):
	list_display = ('code', 'name_en')

@admin.register(models.FoodSource)
class FoodSourceAdmin(admin.ModelAdmin):
	list_display = ('code', 'description_en')

class FoodNutrientsInline(admin.TabularInline):
	model = models.NutrientAmount
	fields = ('nutrient', 'value',)
	min_num = 0
	can_delete = True
	extra = 1

class FoodConstraintsInline(admin.TabularInline):
	model = models.FoodConstraint
	fields = ('min_qty', 'max_qty',)
	can_delete = False
	min_num = 0
	max_num = 1
	extra = 1

class NutrientConstraintsInline(admin.TabularInline):
	model = models.NutrientConstraint
	fields = ('weight_overconsumption', 'weight_underconsumption',)
	can_delete = False
	min_num = 0
	max_num = 1
	extra = 1

class FoodYieldAmountInline(admin.TabularInline):
	model = models.YieldAmount
	fields = ('amount',)
	can_delete = True
	min_num = 0
	extra = 1

class FoodRefuseAmountInline(admin.TabularInline):
	model = models.RefuseAmount
	fields = ('amount',)
	can_delete = True
	min_num = 0
	extra = 1

@admin.register(models.Food)
class FoodAdmin(admin.ModelAdmin):
	list_display = ('description_en', 'entry_date')
	search_fields = ('description_en', )
	inlines = (
		FoodNutrientsInline,
		FoodConstraintsInline,
		FoodYieldAmountInline,
		FoodRefuseAmountInline,)

@admin.register(models.Measure)
class MeasureAdmin(admin.ModelAdmin):
	list_display = ['description_en']
	search_fields = ('description_en', )

@admin.register(models.RefuseType)
class RefuseTypeAdmin(admin.ModelAdmin):
	list_display = ['description_en']
	search_fields = ('description_en', )

@admin.register(models.YieldType)
class YieldTypeAdmin(admin.ModelAdmin):
	list_display = ['description_en']
	search_fields = ('description_en', )

@admin.register(models.Nutrient)
class NutrientAdmin(admin.ModelAdmin):
	list_display = ('code', 'name_en', 'symbol', 'unit', 'tagname')
	search_fields = ('name_en', 'symbol', )
	inlines = (NutrientConstraintsInline,)

@admin.register(models.NutrientSource)
class NutrientSourceAdmin(admin.ModelAdmin):
	list_display = ('code', 'description_en')
	search_fields = ('code', 'description_en', )

@admin.register(models.IntakeProfile)
class IntakeProfileAdmin(admin.ModelAdmin):
	list_display = ('name', 'scope', 'age')
	search_fields = ('name', 'age' )

@admin.register(models.IntakeProfileScope)
class IntakeProfileScopeAdmin(admin.ModelAdmin):
	list_display = ('name', 'description')
	search_fields = ('name', 'descripton', )

@admin.register(models.FoodConstraint)
class FoodConstraintAdmin(admin.ModelAdmin):
	list_display = ('related_food', 'min_qty', 'max_qty')

	def related_food(self, obj):
	    return obj.food.description_en
	related_food.short_description = 'Food'

# Derived tables
class YieldAmountAdmin(admin.ModelAdmin):
	list_display = ('food', 'yield_type', 'amount')

class RefusedAmountAdmin(admin.ModelAdmin):
	list_display = ('food', 'refuse_type', 'amount')
