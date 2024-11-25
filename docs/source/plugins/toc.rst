Table of Contents Plugin
=======================

The Table of Contents (TOC) plugin automatically generates a navigation list from heading plugins with defined anchor IDs.

Important Notes
-------------

* TOC entries are only generated from heading plugins that have a ``heading_id`` defined
* The TOC plugin must be placed **after** the headings it should include
* Use grid layouts to position the TOC above content while maintaining proper render order

Configuration Options
-------------------

* ``list_attributes`` - HTML attributes for the TOC list element
* ``link_attributes`` - HTML attributes for TOC link elements
* ``item_attributes`` - HTML attributes for TOC list item elements

Example Usage
------------

Basic TOC::

    # Will generate a list of all headings with IDs that appear before this TOC

Positioning TOC Above Content
---------------------------

To display the TOC at the top of a page while maintaining proper render order:

1. Create a two-column grid layout
2. Place headings in the main content column
3. Place TOC in the sidebar column
4. Use Bootstrap order classes to display sidebar first

Example grid structure::

    Grid Row
    ├── Column 1 (order-2)
    │   ├── Heading 1
    │   ├── Content...
    │   └── Heading 2
    └── Column 2 (order-1)
        └── TOC Plugin

This structure allows the TOC to render after the headings but display before them visually.

Customizing TOC Appearance
------------------------

Example with custom attributes::

    list_attributes:
        class: nav nav-pills flex-column
    
    link_attributes:
        class: nav-link
    
    item_attributes:
        class: nav-item

This will style the TOC using Bootstrap nav classes.
