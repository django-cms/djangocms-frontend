###################
 Table of Contents
###################

The Table of Contents (TOC) plugin automatically generates a navigation list from headings in your content.

**Important**: The TOC plugin must be placed **after** the headings it references in the content flow.

*************
 How it Works
*************

The TOC plugin:

1. Scans for Heading plugins that appear before it in the content
2. Collects headings that have an ID set
3. Generates a nested list of links to those headings

Basic Usage
==========

To create a table of contents:

1. Add your Heading plugins with IDs set
2. Add the TOC plugin after the headings
3. The TOC will automatically generate when the page renders

Positioning at Top of Page
=========================

Since the TOC must be placed after headings to collect them, use grid layouts to display it at the top:

Two Column Layout Example
------------------------

1. Create a container
2. Add a row with two columns
3. In the first (left) column:
   - Add the TOC plugin
4. In the second (right) column:
   - Add your content with Heading plugins
5. Set column widths appropriately (e.g., 3/9 split)

Example Structure::

    Container
    └── Row
        ├── Column (col-3)
        │   └── TOC Plugin
        └── Column (col-9)
            ├── Heading Plugin
            ├── Content...
            ├── Heading Plugin
            └── More content...

This creates a sidebar layout with the TOC always visible while scrolling through content.

Best Practices
=============

1. Always set IDs on headings that should appear in the TOC
2. Use consistent heading levels for proper hierarchy
3. Keep heading IDs unique across the page
4. Consider using the grid layout pattern for better UX
5. Test navigation on both desktop and mobile views
