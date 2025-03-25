##############################
Headings and table of contents
##############################

*********
 Heading
*********

The Heading plugin allows you to add headings (h1-h6) to your content with optional styling and anchors for navigation.

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
---------------

To make a heading appear in a Table of Contents:

1. The heading **must** have an ID set
2. The TOC plugin must be placed **after** the heading in the content flow
3. Only headings with IDs will appear in the TOC

*******************
 Table of Contents
*******************

The Table of Contents (TOC) plugin automatically generates a navigation list from headings in your content.

**Important**: The TOC plugin must be placed **after** the headings it references in the content flow.

How it Works
============

The TOC plugin:

1. Scans for Heading plugins that appear before it in the content
2. Collects headings that have an ID set
3. Generates a nested list of links to those headings

Basic Usage
===========

To create a table of contents:

1. Add your Heading plugins with IDs set
2. Add the TOC plugin after the headings
3. The TOC will automatically generate when the page renders

Positioning at Top of Page
==========================

Table of contents at the top Example
------------------------------------

Since the TOC must be placed after headings to collect them, use grid layouts to display it at the top:

1. Create a container
2. Add a row with two columns
3. In the first (bottom) column: Add your content with Heading plugins
4. In the second (top) column: Add the TOC plugin
5. Set the column width and order: Both columns should cover full width (typically 12/12),
   the second columns should be shown before (i.e., at the top) the first (then at the bottom)

Two Column Layout Example
-------------------------

1. Create a container
2. Add a row with two columns
3. In the first (left) column: Add your content with Heading plugins
4. In the second (right) column: Add the TOC plugin
5. Set column widths appropriately (e.g., 3/9 split)

Example Structure::

    Container
    └── Row
        ├── Column (col-9)
        │   ├── Heading Plugin
        │   ├── Content...
        │   ├── Heading Plugin
        │   └── More content...
        └── Column (col-3)
            └── TOC Plugin

This creates a sidebar layout with the TOC always visible while scrolling through content.

Best Practices
==============

1. Always set IDs on headings that should appear in the TOC
2. Use consistent heading levels for proper hierarchy
3. Keep heading IDs unique across the page
4. Consider using the grid layout pattern for better UX
5. Test navigation on both desktop and mobile views
