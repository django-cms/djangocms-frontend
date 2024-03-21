from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import View

from .helpers import get_link_choices


class AutocompleteJsonView(LoginRequiredMixin, View):
    """Handle AutocompleteWidget's AJAX requests for data."""

    paginate_by = 20
    admin_site = None

    def get(self, request, *args, **kwargs):
        """
        Return a JsonResponse with search results of the form:
        {
            results: [{id: "123" text: "foo"}],
            pagination: {more: true}
        }
        """

        # TODO Check permissions
        # ======================
        self.term = kwargs.get("term", request.GET.get("term", "")).strip()
        results = get_link_choices(request, self.term)
        return JsonResponse(
            {
                "results": results,
                "pagination": {"more": False},
            }
        )
