## Dynamic Tables

Builds out a table on a map in each output page of a data driven pages setup. Let's run through the setup and an example to see how this would work.

### The Setup

For any data driven pages setup you need an index layer. The index layer is a set of features that will be cycled through to produce multiple maps based on the extent of the feature or a scale defined in index layer's attribuet table.

Within your mxd you will need to enable data driven pages on a layer and set the "Name Field" parameter. This "Name Field" will be a key component later on in querying your table (i.e. dbf).

The next phase of setup all happens within the "Layout View" of your mxd. Once there, you need to establish where your table is going to go on your map and then construct the first row or header of your table.

First we start with our graphic elements. These would look like two boxes to make our header:

|           |           |
| --------- | --------- |

Then we add our text elements. These would be placed into the boxes as so:

| Building Name     | Square Feet   |
| :---------------: | :-----------: |

Now we have two elements for each column or field name. There will be a graphic element surrounding the Building Number and there will be a text element displaying the text "Building Number".

To read more about mxd elements see the [documentation](http://resources.arcgis.com/en/help/main/10.1/index.html#/ListLayoutElements/00s30000003w000000/)

Within the mxd you will need to then right click each element, go to "Properties" and under the tab "Size and Position" provide a name for the parameter "Element Name". The name would be identical for both the graphic and text elements of the same kind i.e. "Building_Name" for both the graphic and text elements that make up that box). If an element does not have a name, the script will pass over it.

Now what sort of name do you want for these elements? They key the name of these elements must match the field names in the attribute table where the data is stored. Let's look at an example to show you how everything gets connected.

### The Setup - Looking at Sectors

We have sectors in an unknown township. There are five of these sectors, and the aim is to produce five different maps listing all the buildings by their name and their square footage in a table on the map.

 So what we are working with is:

- A "Sectors" feature class with 5 sectors. Each sector has a name which is found in the feature "Sector_Name" within the attribute table

The attribute table looks like:

| Sector_Name            |
| :--------------------: |
| One                    |
| Two                    |
| Three                  |
| Four                   |
| Five                   |

- A "Buildings" feature class with a variable number of buildings within each sector. The attribute table has "Building_Name" and "Square_Feet" fields and the table looks like:

| Building_Name     | Square_Feet   |
| :---------------: | :-----------: |
| The Brown         | 20,000        |
| Pigeon Hole       | 200           |
| Aces              | 576           |
| Hull and Husk     | 10            |
| Dynamite Den      | 900           |
| Rubee Den         | 55            |
| Buyer's Remorse   | 10,000        |

The first task would be to setup a the "Sectors" feature class as an index layer in data driven pages and pass the "Sector_Name" to the parameter "Name Field." This means as we scroll through the data driven pages the name of each map will be associated with the Sector Name.

Then in an mxd under "Layout View" we set up the header of our table with building names and square feet and label the respective graphic and text elements "Building_Name" and "Square_Feet" as we have in the attribute table of the "Buildings" feature class.

From here, we run an intersect in GIS with the "Buildings" and "Sectors" feature class to generate a table of all buildings by sector.

This is our table which will look something like:

| Sector_Name | Building_Name     | Square_Feet   |
| :---------: | :---------------: | :-----------: |
| One         | The Brown         | 20,000        |
| One         | Pigeon Hole       | 200           |
| One         | Aces              | 576           |
| Two         | Hull and Husk     | 10            |
| Two         | Dynamite Den      | 900           |
| Two         | Rubee Den         | 55            |
| Two         | Buyer's Remorse   | 10,000        |

And so forth. What we want to show, then, is as data driven pages exports out each map, we all the rows of the table of the corresponding sector to be displayed on the map.

Sometihng to the likes of:

##### Sector 1 Map

| Building Name     | Square Feet   |
| :---------------: | :-----------: |
| The Brown         | 20,000        |
| Pigeon Hole       | 200           |
| Aces              | 576           |

##### Sector 2 Map

| Building Name     | Square Feet   |
| :---------------: | :-----------: |
| Hull and Husk     | 10            |
| Dynamite Den      | 900           |
| Rubee Den         | 55            |
| Buyer's Remorse   | 10,0000       |

### Putting it Together

When the script is executed, it will start on the first page of the data driven pages, look at 'Name Field' of the index layer and find the "Sector_Name" field and the current page we are on, Sector One.

It will then query the field "Sector_Name" in the table we passed to the script for all Sector One rows. With these rows, it will match up any fields in the table that match the names of elements in our mxd. So if a field is named "Building_Name" it will find these elements and start constructing the table. Then it will go to the next field 'Square_Feet', find any matching elements, and build construct that column.

Once the table is complete for Sector One a pdf will be exported, the mxd refreshed, and Sector Two will begin.

The key to the success of this script is maintaining the links between your data. If the index layer has a field "Sector_Names" while your table has a field "Sector_Name", the script won't run. If any of your elements have different names then the corresponding fields in the attribute table then they won't be displayed.

It's all about consistency.

### Behind the Scenes

How is this table being constructed? Let's dig in and take a look.

The first take is to get the elements on a map page. This can be done with a simple list of the layout elements such as:

```
map_doc = arcpy.mapping.MapDocument(path_to_mxd)
arcpy.mapping.ListLayoutElements(map_doc, element_type)
```

First we initialize and then use [ListLayoutElements](http://resources.arcgis.com/en/help/main/10.1/index.html#//00s30000003w000000) to list all elements of a given "element_type". There are a number of element types but the ones we would want to list are "GRAPHIC_ELEMENT" and "TEXT_ELEMENT."

This gives of a list of all objects associated with that element. In this way, with the help of some python shorthand, we can quickly make a list of tuples with the object name and the object via a list comprehension:

```
element_map = [(str(obj.name), obj) for obj in arcpy.mapping.ListLayoutElements(map_doc, element_type) if len(str(obj.name)) > 0]
```

What we are doing is looping through the layout elements and filtering out any elements that do not have a name (think back to above when we went through and named elements with corresponding field names from our attribute table). We then append to our list a tuple with the name of the object and the object.

In our example the list would look like

```
[
("Building_Name", <object>),
("Square_Feet", <object>)
]
```

With this list in hand, we can initiate a cursor on our table. If a field matches an element, their are properties and methods in an element we can ultilize to make a new cell in our table.

To Be Continued....

### Tool Parameters

1. MXD_PATH = The pathname to a mxd with data driven pages enabled
2. TABLE = The pathname to a table with field names that match the graphic and text elements and the index layer
3. DESTINATION = Where to send all the pdfs on export

### TODO

1. Support rectangle text box graphics
2. Add python toolbox
3. More testing
