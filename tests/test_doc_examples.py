"""Render every runnable ``{% plugin %}`` example in the documentation.

Examples that are meant to be copy-and-paste runnable are marked in the docs
with ``.. code-block:: template``. This test extracts every such block and
renders it, making sure that

* every plugin slug used actually resolves to a registered component (otherwise
  the tag renders a ``"... add its plugin class to the CMS_COMPONENT_PLUGINS
  setting"`` comment), and
* every keyword argument is a valid field (an unknown field raises while the
  dummy instance is being built).

This keeps the documentation honest: a renamed plugin or field, or a typo in a
marked example, makes this test fail. Illustrative snippets that cannot be
rendered standalone (e.g. carousel slides, which require a saved parent) simply
use a plain ``.. code-block::`` and are not collected here.
"""

import re
from pathlib import Path

from cms.test_utils.testcases import CMSTestCase
from django.template import engines
from django.test import override_settings

from tests.fixtures import TestFixture

django_engine = engines["django"]

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs" / "source"

# Substring of the comment emitted (in DEBUG) when a slug is not a component.
UNREGISTERED_MARKER = "add its plugin class to the"

# Marks a code block as a runnable template example to be verified here.
TEMPLATE_BLOCK_RE = re.compile(r"^(?P<indent>\s*)\.\.\s+code-block::\s*template\s*$")


def _iter_template_blocks(path):
    """Yield ``(line_number, dedented_source)`` for each ``.. code-block:: template``."""
    lines = path.read_text().splitlines()
    i = 0
    n = len(lines)
    while i < n:
        match = TEMPLATE_BLOCK_RE.match(lines[i])
        if not match:
            i += 1
            continue
        directive_indent = len(match.group("indent"))
        block_start = i + 1
        j = block_start
        # Skip directive options (":linenos:" etc.) and blank lines.
        while j < n and (not lines[j].strip() or lines[j].lstrip().startswith(":")):
            j += 1
        # Collect the indented block body.
        body = []
        block_indent = None
        while j < n:
            cur = lines[j]
            if not cur.strip():
                body.append("")
                j += 1
                continue
            indent = len(cur) - len(cur.lstrip())
            if indent <= directive_indent:
                break
            if block_indent is None:
                block_indent = indent
            body.append(cur[block_indent:])
            j += 1
        yield block_start + 1, "\n".join(body).strip("\n")
        i = max(j, i + 1)


def _collect_examples():
    examples = []
    for path in sorted(DOCS_DIR.rglob("*.rst")):
        for line_number, source in _iter_template_blocks(path):
            examples.append((path.relative_to(DOCS_DIR), line_number, source))
    return examples


EXAMPLES = _collect_examples()


@override_settings(DEBUG=True)
class DocPluginExamplesTest(TestFixture, CMSTestCase):
    def test_examples_were_found(self):
        """Guard against the parser silently finding nothing."""
        self.assertTrue(
            EXAMPLES,
            "No `.. code-block:: template` examples found in the docs.",
        )

    def _render(self, source):
        template = django_engine.from_string(source)
        return template.render({"request": None})


def _make_test(doc, line_number, source):
    location = f"{doc}:{line_number}"

    def test(self):
        try:
            result = self._render(source)
        except Exception as exc:  # noqa: BLE001 - re-raised with doc context
            raise AssertionError(f"{location} failed to render:\n{exc.__class__.__name__}: {exc}\n\n{source}") from exc
        self.assertNotIn(
            UNREGISTERED_MARKER,
            result,
            msg=f"{location} uses a plugin slug that is not a registered component:\n{source}",
        )
        self.assertTrue(
            result.strip(),
            msg=f"{location} rendered empty output:\n{source}",
        )

    return test


for _doc, _line_number, _source in EXAMPLES:
    _slug = str(_doc).replace("/", "_").replace(".", "_").replace("-", "_")
    _name = f"test_example_{_slug}_line_{_line_number}"
    setattr(DocPluginExamplesTest, _name, _make_test(_doc, _line_number, _source))
