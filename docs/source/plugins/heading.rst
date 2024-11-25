#########
 Heading
#########

The Heading plugin allows you to add headings (h1-h6) to your content with optional styling and anchors for navigation.

*************
Configuration
*************

- **Heading Level**: Choose h1-h6 for the heading tag
- **Heading Text**: The text content of the heading
- **Heading ID**: Optional anchor ID for TOC linking
- **Heading Alignment**: Text alignment (left, center, right)
- **Heading Context**: Optional Bootstrap contextual class for styling

Example
=======

Basic heading::

    <h2 id="my-section">My Section Title</h2>

To create a heading that will appear in a table of contents:

1. Add a Heading plugin
2. Set the heading level (e.g., h2)
3. Enter your heading text
4. Set a unique ID in the "Heading ID" field
5. Optional: Adjust alignment and styling

Advanced Usage
=============

Styling
-------

You can apply Bootstrap contextual classes through the "Heading Context" setting:

- primary
- secondary
- success
- danger
- warning
- info
- light
- dark

For example, selecting "primary" will add the ``text-primary`` class.

TOC Integration
--------------

To make a heading appear in a Table of Contents:

1. The heading **must** have an ID set
2. The TOC plugin must be placed **after** the heading in the content flow
3. Only headings with IDs will appear in the TOC

See the :doc:`Table of Contents </plugins/toc>` documentation for more details.
