from django.views.generic import FormView
from django import forms
from django.conf import settings
from .jsonrpc import JsonRpcClient
import json

class JsonRpcForm(forms.Form):
    method = forms.CharField(label="Метод JSON-RPC", max_length=100)
    params = forms.CharField(label="Параметры (JSON)", widget=forms.Textarea, required=False)

class JsonRpcView(FormView):
    template_name = "api/jsonrpc_form.html"
    form_class = JsonRpcForm

    def form_valid(self, form):
        method = form.cleaned_data["method"]
        params = form.cleaned_data["params"]

        try:
            params_dict = json.loads(params) if params else {}
        except json.JSONDecodeError:
            return self.render_to_response(self.get_context_data(
                form=form, error="Ошибка: Параметры должны быть в формате JSON"
            ))

        client = JsonRpcClient(
            endpoint=settings.JSONRPC_ENDPOINT,
            certificate=settings.CERTIFICATE_CONTENT,
            key=settings.KEY_CONTENT,
        )
        response = client.call_method(method, params_dict)
        return self.render_to_response(self.get_context_data(
            form=form, response=response
        ))
