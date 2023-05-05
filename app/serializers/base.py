from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):
    def get_extra_kwargs(self):
        extra_kwargs_for_edit = super().get_extra_kwargs()
        for key in self.Meta.create_only_fields:
            self.add_create_only_constraint_to_field(key, extra_kwargs_for_edit)
        return extra_kwargs_for_edit

    def add_create_only_constraint_to_field(self, key: str, extra_kwargs: dict):
        if not self.context.get("view"):
            return
        action = self.context["view"].action
        if action in ["create"]:
            kwargs = extra_kwargs.get(key, {})
            kwargs["read_only"] = False
            extra_kwargs[key] = kwargs
        elif action in ["update", "partial_update"]:
            kwargs = extra_kwargs.get(key, {})
            kwargs["read_only"] = True
            extra_kwargs[key] = kwargs
