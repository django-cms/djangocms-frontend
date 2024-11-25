Heading Plugin
=============

The Heading plugin allows you to create HTML headings (h1-h6) with optional styling and anchors that can be referenced by the Table of Contents plugin.

Configuration Options
-------------------

* ``heading_level`` - The heading level (h1-h6)
* ``heading`` - The heading text content
* ``heading_id`` - The HTML ID attribute for the heading (required for TOC entries)
* ``heading_context`` - Bootstrap contextual class for styling (primary, secondary, success, etc.)
* ``heading_alignment`` - Text alignment (left, center, right)

Example Usage
------------

Basic heading::

    heading_level: h2
    heading: My Section Title
    heading_id: section-1

Styled heading with custom alignment::

    heading_level: h3
    heading: Important Section
    heading_id: important
    heading_context: primary
    heading_alignment: center

Table of Contents Integration
---------------------------

To make a heading appear in a table of contents:

1. Always set a unique ``heading_id`` for the heading
2. Place the heading before any TOC plugins that should reference it
3. Use semantic heading levels (h1 > h2 > h3) for proper hierarchy

Example with TOC integration::

    heading_level: h2
    heading: First Section
    heading_id: first-section

    heading_level: h3
    heading: Subsection
    heading_id: first-section-sub

The above headings will appear in any TOC plugin placed after them in the content flow.
