###################
 Table of Contents
###################

The Table of Contents (TOC) plugin automatically generates a navigation list from headings with IDs in your content.

************
 How It Works
************

The TOC plugin:

1. Scans the page for heading plugins with defined IDs
2. Creates a nested list of links to those headings
3. Must be rendered after the headings it references

.. warning::
    The TOC plugin can only reference headings that are rendered before it in the page flow.

*********************
 Positioning the TOC
*********************

Since the TOC must be rendered after headings to include them, use these strategies to position it at the top of the page:

Using Grid Layout
===============

1. Create a two-column grid layout
2. Place TOC in the first column
3. Place content with headings in the second column

Example structure:

.. code-block:: html

    <div class="row">
        <!-- TOC Column -->
        <div class="col-md-3">
            <!-- TOC Plugin -->
        </div>
        
        <!-- Content Column -->
        <div class="col-md-9">
            <!-- Heading Plugins -->
            <h2 id="section-1">Section 1</h2>
            <p>Content...</p>
            
            <h2 id="section-2">Section 2</h2>
            <p>Content...</p>
        </div>
    </div>

Using CSS
========

Alternatively, use CSS positioning:

1. Place the TOC plugin after your content
2. Use CSS to position it at the top:

.. code-block:: css

    .toc-wrapper {
        position: fixed;
        top: 20px;
        left: 20px;
        max-width: 250px;
    }

***********
 Settings
***********

The TOC plugin offers several customization options:

List Style
=========

- Ordered list (numbers)
- Unordered list (bullets)
- Custom classes for styling

Link Attributes
=============

- Add custom classes to TOC links
- Set active link styling
- Configure hover effects

***********
 Examples
***********

Basic TOC
========

.. code-block:: html

    <!-- Content -->
    <h2 id="install">Installation</h2>
    <p>Installation content...</p>

    <h2 id="config">Configuration</h2>
    <p>Configuration content...</p>

    <!-- TOC Plugin will generate: -->
    <ul class="toc">
        <li><a href="#install">Installation</a></li>
        <li><a href="#config">Configuration</a></li>
    </ul>

Styled TOC with Grid
==================

.. code-block:: html

    <div class="row">
        <div class="col-md-3">
            <!-- TOC Plugin with Bootstrap styling -->
            <nav class="sticky-top">
                <ul class="nav flex-column">
                    <li><a href="#install">Installation</a></li>
                    <li><a href="#config">Configuration</a></li>
                </ul>
            </nav>
        </div>
        
        <div class="col-md-9">
            <h2 id="install">Installation</h2>
            <p>Installation content...</p>

            <h2 id="config">Configuration</h2>
            <p>Configuration content...</p>
        </div>
    </div>
