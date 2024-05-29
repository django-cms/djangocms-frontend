
##############
 Grid plugins
##############

For details on how grids work, see, e.g. the `Bootstrap 5 documentation
<https://getbootstrap.com/docs/5.1/layout/grid/>`_.

.. index::
    single: Container

*********
Container
*********

A container is an invisible element that wraps other content. There are
in two types of containers:

Container
   All other containers restrict the width of their content depending on
   the used device.

Fluid container
   A fluid container occupies the full width available - no matter how
   wide the viewport (or containing) element is.

Full container
   A full container is like a fluid container and occupies the full width
   available. Additionally, it does not have a padding. Its content can
   therefore fill the entire area. Full containers are useful if you want
   to add a background color or shadow to another DOM element, like, e.g.,
   the contents of a column.


.. note::

    New feature:
        Containers can have a background color ("context"), opacity and shadow.


.. index::
    single: Row

.. _Grid plugins:

***
Row
***

A row contains one or more columns. By default columns are displayed
next to each other.

To automatically create not only a row but also some columns within that
row, enter the number of columns you will be using. You can always later
add more columns to the row or delete columns from the row.

Vertical aligned defines how columns of different height are
positioned against each other.

Horizontal alignment defines how columns **that do not fill an entire
row** are distributed horizontally.

.. note::

    New feature:

    The section "Row-cols settings" defines how many columns should be next
    to each other for a given display size. The "row-cols" entry defines the
    number of columns on mobile devices (and above if no other setting is
    given), the "row-cols-xl" entry the number of columns on a xl screen.

.. image:: screenshots/row.png


.. index::
    single: Column

******
Column
******

The column settings is largely about how much of the grid space the
column will use horizontally. To this end, the grid is divided in
(usually) 12 strips of equal width.

Auto sizing
   If no information on the column size is given, the column will be
   autosizing. This means that all autosizing columns of a row will
   occupy the same fraction of the space left, e.g. by sized columns.

Specifically sized columns
   If you enter a number the column for the specific screen size will
   exactly have the specified width. The unit of width is one twelfth of
   the surrounding's row width.

Natural width:
    If you need a column to take its natural width, enter ``0`` for its
    column size. This will display ``auto`` for columns size.

Also, you can adjust the vertical alignment of the specific column from
the row's default setting.

Finally, you can set the alignment of the content to left (right in a
rtl environment), center or right (left in a rtl environment). This
comes handy if, e.g., the column is supposed to contain centered
content.

.. image:: screenshots/col.png

.. note::

    Removed:
        The column type entry has been removed since it was a legacy from
        Bootstrap version 3.

***************************
Re-usable component example
***************************

**djangocms-frontend** plugins can be used as components. They can be
used in all your project's templates. Example (if key word arguments are
skipped they fall back to their defaults):

.. code-block::

    {% load frontend %}
    {% plugin "gridcontainer" container_type="container-fluid" %}
        {% plugin "row" vertical_alignment="align-items-center" %}
            {% plugin "gridcolumn" xs_col=12 md_col=6 text_alignment="center" %}
                This content is inside a column.
            {% endplugin %}
            {% plugin "gridcolumn" xs_col=12 md_col=6 text_alignment="center" %}
                This content is inside another column.
            {% endplugin %}
        {% endplugin %}
        This content still is inside a container.
    {% endplugin %}

Parameters for ``{% plugin "gridcontainer" %}`` are:

* ``container_type``: The type of container. Default is ``container``. Other
    options are ``container-fluid`` and ``container-full``.

Parameters for ``{% plugin "gridrow" %}`` are:

* ``vertical_alignment``: The vertical alignment of the row. Default is
    ``align-items-start``. Other options are ``align-items-center`` and
    ``align-items-end``.
* ``horizontal_alignment``: The horizontal alignment of the row. Default is
    ``justify-content-start``. Other options are ``justify-content-center``,
    ``justify-content-end`` and ``justify-content-around``.
* ``gutters``: Size of gutter between columns. Default is ``3``. Other
    options are ``0``, ``1``, ``2``, ``4``, ``5``.
* ``row_cols_xs``: Number of columns on mobile devices.
* ``row_cols{sm|md|lg|xl|xx}``: Number of columns on larger devices.


Parameters for ``{% plugin "gridcolumn" %}`` are:
* ``column_alignment``: The vertical alignment of the column. Default is
    ``align-self-start``. Other options are ``align-self-center`` and
    ``align-self-end``.
* ``text_alignment``: The text alignment of the column. Options are
    ``left``, ``center`` and ``right``.
* ``xs_col``: Number of columns on mobile devices.
* ``{sm|md|lg|xl|xx}_col``: Number of columns on larger devices.



