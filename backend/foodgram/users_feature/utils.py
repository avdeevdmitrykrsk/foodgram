def add_recipe_to_list(self, obj):
    return self.Meta.model.objects.create(
        user=self.context.get('request').user,
        recipe=obj.objects.get(
            id=self.context.get('request').parser_context['kwargs']['pk']
        )
    )
