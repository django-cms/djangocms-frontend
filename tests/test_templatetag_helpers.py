from cms.test_utils.testcases import CMSTestCase
from django.contrib.sessions.backends.db import SessionStore
from django.template import Context
from django.test import RequestFactory

from djangocms_frontend.templatetags.frontend import is_inline_editing_active


class IsInlineEditingActiveTestCase(CMSTestCase):
    """Test cases for the is_inline_editing_active template tag helper function."""

    def setUp(self):
        self.factory = RequestFactory()

    def test_returns_false_when_request_not_in_context(self):
        """Test that the function returns False when request is not in context."""
        context = Context({})
        result = is_inline_editing_active(context)
        self.assertFalse(result)

    def test_returns_false_when_request_has_no_session(self):
        """Test that the function returns False when request object doesn't contain a session object."""
        request = self.factory.get("/")
        # Ensure the request doesn't have a session attribute
        if hasattr(request, "session"):
            delattr(request, "session")

        context = Context({"request": request})
        result = is_inline_editing_active(context)
        self.assertFalse(result)

    def test_returns_true_when_inline_editing_enabled(self):
        """Test that the function returns True when inline_editing is enabled in session."""
        request = self.factory.get("/")
        # RequestFactory doesn't include session by default, so add it
        session = SessionStore()
        session["inline_editing"] = True
        request.session = session

        context = Context({"request": request})
        result = is_inline_editing_active(context)
        self.assertTrue(result)

    def test_returns_false_when_inline_editing_disabled(self):
        """Test that the function returns False when inline_editing is explicitly disabled in session."""
        request = self.factory.get("/")
        session = SessionStore()
        session["inline_editing"] = False
        request.session = session

        context = Context({"request": request})
        result = is_inline_editing_active(context)
        self.assertFalse(result)

    def test_returns_true_by_default_when_session_exists(self):
        """Test that the function returns True by default when session exists but inline_editing key is not set."""
        request = self.factory.get("/")
        session = SessionStore()
        # Don't set the inline_editing key, so it defaults to True
        request.session = session

        context = Context({"request": request})
        result = is_inline_editing_active(context)
        self.assertTrue(result)
