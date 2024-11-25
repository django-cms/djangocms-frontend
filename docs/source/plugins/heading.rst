#########
 Heading
#########

The Heading plugin allows you to add HTML headings (h1-h6) to your content with optional styling and anchors for table of contents integration.

************
 Basic Usage
************

The Heading plugin provides the following key features:

- Choose heading level (h1-h6)
- Set heading text
- Add custom ID/anchor for table of contents linking
- Apply text alignment
- Set text color using contextual classes

Example usage:

.. code-block:: html

    <h2 id="my-section">My Section Heading</h2>

***********
 Settings
***********

Heading Level
============

Select the appropriate heading level (h1-h6) based on your content hierarchy. Use consistent heading levels for proper document structure.

Heading ID
=========

The heading ID field sets the HTML id attribute and is crucial for table of contents functionality:

- Must be unique within the page
- Used by the Table of Contents plugin to generate navigation links
- Should be URL-friendly (e.g., "my-section-name")

Example with ID:

.. code-block:: html

    <h2 id="installation">Installation Guide</h2>

Text Alignment
============

Control heading alignment:

- Left (default)
- Center
- Right

Text Color
=========

Apply Bootstrap contextual colors:

- Primary
- Secondary
- Success
- Danger
- Warning
- Info
- Light
- Dark

********************
 TOC Integration
********************

To include a heading in the table of contents:

1. Add a unique ID to the heading
2. Place a Table of Contents plugin where you want the navigation to appear
3. Ensure the Table of Contents plugin is rendered after all headings

.. note::
    Headings without IDs will not appear in the table of contents.

See the :doc:`Table of Contents </plugins/toc>` documentation for more details.
