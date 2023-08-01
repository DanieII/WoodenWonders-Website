from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import urlencode


class ProhibitLoggedUsersMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)


class HandleQueryParamsFromLoginRequiredFormsMixin:
    def get_form_fields_from_request(self, request_method):
        request_method_instance = getattr(self.request, request_method)
        login_required_form_fields = request_method_instance.get(
            "login_required_form_fields"
        )

        if login_required_form_fields:
            fields_with_values = {
                field: request_method_instance.get(field)
                for field in request_method_instance
                if field in login_required_form_fields
            }
        else:
            fields_with_values = {}

        return login_required_form_fields, fields_with_values

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        (
            login_required_form_fields,
            fields_with_values,
        ) = self.get_form_fields_from_request("GET")

        context["login_required_form_fields"] = login_required_form_fields
        context["fields_with_values"] = fields_with_values

        return context

    def form_valid(self, form):
        response = super().form_valid(form)

        (
            login_required_form_fields,
            fields_with_values,
        ) = self.get_form_fields_from_request("POST")

        if login_required_form_fields:
            return redirect(response.url + "?" + urlencode(fields_with_values))

        return response


class HandleSendLoginRequiredFormInformationMixin:
    mixin_form = None
    fields = []
    additional_fields = {}

    def get_query_string(self, form_instance):
        fields_with_values = {}
        next_url = self.request.get_full_path()

        for field in self.fields:
            fields_with_values[field] = form_instance.cleaned_data.get(field)

        parameters_in_query_format = urlencode(fields_with_values)
        fields_list = ",".join(self.fields)

        query_string = f"?next={next_url}&{parameters_in_query_format}&login_required_form_fields={fields_list}"

        return query_string

    def get_additional_fields(self):
        return {}

    def post(self, request, *args, **kwargs):
        form_instance = self.mixin_form(request.POST)
        if form_instance.is_valid():
            if not request.user.is_authenticated:
                query_string = self.get_query_string(form_instance)
                login_url = reverse("login") + query_string

                return redirect(login_url)

            form_instance = form_instance.save(commit=False)

            additional_fields = self.additional_fields or self.get_additional_fields()
            for field, value in additional_fields.items():
                setattr(form_instance, field, value)

            for field in self.fields:
                field_value = request.POST.get(field)
                setattr(form_instance, field, field_value)

            form_instance.save()

        return redirect(self.get_success_url())
