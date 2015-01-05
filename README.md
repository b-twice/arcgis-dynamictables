## Dynamic Tables

Builds out a table in each output page of a data driven pages setup. Examples pending. Let's run through the setup and an example to see how this would work.

### The Setup

For any data driven pages setup you need an index layer. The index layer is a set of features that will be cycled through to produce multiple output pages.

Within your mxd you will need to enable data driven pages on a layer and set the "Name Field" parameter. This "Name Field" will be a key component later on in querying your table (i.e. dbf).

The next phase of setup all happens within the "Layout View" of your mxd. Once there, you need to establish where your table is going to go on your page and then construct the first row or header of your table. This would look something like:

| Building Number   | Square Feet   |
| :---------------: | :-----------: |

Here we will have two elements for each field name. There will be a graphic element surrounding the Building Number and there will be a text element displaying the text "Building Number". The same goes for "Square Feet" heading.

To read more about elements in a mxd see the [documentation!](http://resources.arcgis.com/en/help/main/10.1/index.html#/ListLayoutElements/00s30000003w000000/)

Within the mxd you will need to then right click each element, go to "Properties" and under the tab "Size and Position" provide a name for the parameter "Element Name". The name would be identical for both the graphic and text elements. If an element does not have a name, the script will pass over it.

Now what sort of name do you want for these elements? They key is in a table, so let's look at an example to show you how everything gets connected.

### The Setup - Looking at Sectors

Let's work with some made up sectors in an unknown township. There are ten of these sectors, and the aim is to produce 10 different maps listing all the buildings by their name and their square footage in a table on the map.

 So what we are working with is:

- A "Sectors" feature class with 10 sectors. Each sector has a name which is found in the feature "Sector_Name" within the attribute table
- A "Buildings" feature class with a variable number of buildings within each sector. Each building as a name and square footage in the fields, respectively, "Building_Name" and "Square_Feet"

The first task would be to setup a the "Sectors" feature class as an index layer in data driven pages and pass the "Sector_Name" to the parameter "Name Field".

Then in an mxd under "Layout View" we set up the header of our table with for building numbers and square feet and name the respective graphic and text elements "Building_Name" and "Square_Feet" as we have in the attribute table of the "Buildings" feature class.

From here, we run an intersect in GIS with the "Buildings" and "Sectors" feature class to generate a table of all buildings by sector.

This is our table.

### Putting it Together

When the script is executed, it will start on the first page of the data driven pages, look at the "Field Name" of the index layer and query the table for a field with that name and all the elements within the table that the current page of the index layer (i.e. give me all "Sector One" buildings).

Then it will look through the map for all graphic and text elements. From our example, it would then start with "Building Number" and look in the table for a field with the element name "Building_Number" and gather all the building numbers within "Sector One" and add them to the table. It would then move on and do the same for the "Square Feet" element.

Once the table is complete for "Sector One" a pdf will be exported, the mxd refreshed, and "Sector Two" will begin.

### Tool Parameters

1. MXD_PATH = The pathname to a mxd with data driven pages enabled
2. TABLE = The pathname to a table with field names that match the graphic and text elements and the index layer
3. DESTINATION = Where to send all the pdfs on export


