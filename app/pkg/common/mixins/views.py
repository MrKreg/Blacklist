from rest_framework.response import Response


class ActionMixin:

    def run_action(self, save_kwargs=None, **kwargs):
        instance = self.get_object()
        sz = self.get_serializer(instance=instance, data=self.request.data)
        sz.is_valid(raise_exception=True)
        sz.save(**save_kwargs or {})
        return Response(sz.data, **kwargs)
