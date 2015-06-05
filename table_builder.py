import arcpy
import os


##
##### Helper Functions
##
def map_elements(map_doc, element_type):
    ''' Takes an Element Type i.e. "GRAPHIC_ELEMENT", "TEXT_ELEMENT" and
        builds a dictionary with the name of the element as the key and the
        object as the value. Excludes all elements not given a name '''
    element_map = sorted([(str(obj.name), obj)
        for obj in arcpy.mapping.ListLayoutElements(map_doc, element_type)
                   if len(str(obj.name)) > 0], key = lambda name: name[0])
    return {element[0]:element[1] for element in element_map}


def get_element_dimensions(element_object):
    ''' return tuple with element dimensions '''
    return element_object.elementHeight, element_object.elementWidth


def get_element_coordinates(element_object):
    ''' return tuple of element coordinates '''
    return element_object.elementPositionY, element_object.elementPositionX


def make_rectangle_text_cell(text_object, text_content, row_depth):
    text_height, text_width = get_element_dimensions(text_object)
    if row_depth != 0:
        text_object = text_object.clone()
        text_object.elementPositionY -= (text_height * row_depth)
    text_object.text = text_content


def to_pdf(map_doc, destination, page_id, page_index):
    ''' moves through data driven pages, exporting pdf '''
    map_doc.dataDrivenPages.currentPageID = page_id
    print "Exporting to PDF: {}".format(page_index)
    export_name = os.path.join(destination, "{}.pdf".format(page_index))
    map_doc.dataDrivenPages.exportToPDF(export_name, "CURRENT", resolution=300, picture_symbol="VECTORIZE_BITMAP")


##
##### MISC Functions
##
def move_arrow(map_doc, position_x, position_y):
    ''' adjust the north arrow as needed dependent on whether north arrow
        obstructs a view in ddp '''
    north_arrow = map_elements(map_doc, "MAPSURROUND_ELEMENT")["North Arrow"]
    north_arrow.elementPositionY = position_x
    north_arrow.elementPositionX = position_y


##
##### Application
##
class GenerateTable(object):
    ''' To cycle through a ddp setup in an mxd and export out a unique table
        on each map, field names must match exactly between graphic and text
        elements in an mxd and the table passed into the class. Further, the
        ddp index name must also match a field in the table '''
    def __init__(self, **params):
        self.__dict__.update(params)
        self.ddp_field = arcpy.mapping.MapDocument(self.mxd).dataDrivenPages.pageNameField.name

    def initialize(self):
        ''' A temporary MXD is created to find the datasource of the ddp in
            the mxd, and then a cursor loops through the mxd wherein each loop
            translates to one map constructed and exported '''
        temp_map_doc = arcpy.mapping.MapDocument(self.mxd)
        ddp_layer = arcpy.mapping.ListLayers(temp_map_doc, temp_map_doc.dataDrivenPages.indexLayer)[0].dataSource
        cursor = arcpy.SearchCursor(ddp_layer)
        for page_id, map_page in enumerate(cursor, start=1):
            self.construct_table(page_id, map_page)
        del cursor

    def construct_table(self, page_id, map_page):
        ''' A new mxd is stfarted to purge any previous tables that may have
            been constructed beforehand '''
        map_doc = arcpy.mapping.MapDocument(self.mxd)
        page_index = map_page.getValue(self.ddp_field)
        self.build_rows(map_doc, page_index)
        self.message.addMessage("Exporting to PDF: {}".format(page_index))
        to_pdf(map_doc, self.destination, page_id, page_index)

    def build_rows(self, map_doc, page_index):
        ''' If you build it, they will come '''
        text_map = map_elements(map_doc, "TEXT_ELEMENT")
        table_cursor = arcpy.SearchCursor(self.data)
        row_depth = 0
        for row in table_cursor:
            if row.getValue(self.ddp_field) == page_index:
                for field in text_map.keys():
                    make_rectangle_text_cell(text_map[field], row.getValue(field), row_depth)
                row_depth += 1
        del table_cursor


##
##### Application initialization
##
if __name__ == '__main__':
    MXD_PATH = r''
    TABLE = r''
    DESTINATION = r''
    input_values = dict(
        mxd=MXD_PATH,
        data=TABLE,
        destination=DESTINATION
    )
    APP = GenerateTable(**input_values)
    APP.initialize()
