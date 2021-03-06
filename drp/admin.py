from django.contrib import admin
from models import *  # import database models from models.py
from django.forms import TextInput, Textarea  # import custom form widgets
from django.http import HttpResponse
import unicodecsv
from django.core.exceptions import ObjectDoesNotExist
from olwidget.admin import GeoModelAdmin


#################
## Media Admin ##
#################


class imagesInline(admin.TabularInline):
    model = Image
    extra = 0
    readonly_fields = ("id",)


class filesInline(admin.TabularInline):
    model = File
    extra = 0
    readonly_fields = ("id",)

###################
## Biology Admin ##
###################

occurrence_fieldsets =(
('Curatorial', {
'fields': (('barcode','catalognumber'),
           ("id", 'fieldnumber', 'yearcollected', 'datelastmodified'),
           ("collectioncode", "paleolocalitynumber", "itemnumber", "itempart"))
}),

('Occurrence Details', {
'fields': (('basisofrecord','itemtype','disposition','preparationstatus'),
           ('itemdescription','itemscientificname'),
           ('remarks'))
}),
('Provenience', {
'fields': (("strat_upper", "distancefromupper"),
           ("strat_lower", "distancefromlower"),
           ("strat_found", "distancefromfound"),
           ("strat_likely", "distancefromlikely"),
           ("analyticalunit", "analyticalunit2", "analyticalunit3"),
           ("insitu", "ranked"),
           ("stratigraphicmember",),
           ("point_X", "point_Y"),
           ('geom'))
}),
)


biology_fieldsets = (
    ('Taxonomy', {'fields':
                      (('taxon',),
                       ('id')
                      )
    }),
)


class biologyInline(admin.TabularInline):
    model = Biology
    extra = 0
    readonly_fields = ("id",)
    fieldsets = biology_fieldsets


class biologyAdmin(admin.ModelAdmin):
    list_display = ("id", "collectioncode","paleolocalitynumber","itemnumber","itempart",
                    'stratigraphicmember',"barcode", 'basisofrecord', 'itemtype', 'taxon', )
    list_filter = ("family",)
    readonly_fields = ("id",)
    fieldsets = biology_fieldsets

    #note: autonumber fields like id are not editable, and can't be added to fieldsets unless specified as read only.
    #also, any dynamically created fields (e.g. point_X) in models.py must be declared as read only to be included in fieldset or fields
    readonly_fields = ("id","fieldnumber", "point_X", "point_Y", "catalognumber", "datelastmodified")

    list_filter = ["basisofrecord", "yearcollected", "stratigraphicmember", "collectioncode", "itemtype"]
    search_fields = ("id", "itemscientificname", "barcode", "catalognumber")
    inlines = (biologyInline, imagesInline, filesInline)
    fieldsets = occurrence_fieldsets
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'25'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }
    list_per_page = 500  # show 500 records per page
    #change_form_template = "occurrence_change_form.html"
    actions = ["move_selected", "get_nearest_locality"]  # TODO clarify actions
    actions = ["get_nearest_locality", "create_data_csv"]


#####################
## Hydrology Admin ##
#####################

class hydrologyAdmin(GeoModelAdmin):
    list_display = ("id", "size")
    search_fields = ("id",)
    list_filter = ("size",)

    options = {
        'layers': ['google.terrain']
    }


#####################
## Locality Admin ##
#####################

class localityAdmin(GeoModelAdmin):
    list_display = ("collectioncode", "paleolocalitynumber", "paleosublocality")
    list_filter = ("collectioncode",)
    search_fields = ("paleolocalitynumber",)

    options = {
        'layers': ['google.terrain']
    }

######################
## Occurrence Admin ##
######################



class occurrenceAdmin(GeoModelAdmin):
    list_display = ("id", "collectioncode","paleolocalitynumber","itemnumber","itempart",'stratigraphicmember',"barcode", 'basisofrecord', 'itemtype',
                    "itemscientificname", "itemdescription", "yearcollected")


    #note: autonumber fields like id are not editable, and can't be added to fieldsets unless specified as read only.
    #also, any dynamically created fields (e.g. point_X) in models.py must be declared as read only to be included in fieldset or fields
    readonly_fields = ("id","fieldnumber", "point_X", "point_Y", "catalognumber", "datelastmodified")

    list_filter = ["basisofrecord", "yearcollected", "stratigraphicmember", "collectioncode", "itemtype"]
    search_fields = ("id", "itemscientificname", "barcode", "catalognumber")
    inlines = (biologyInline, imagesInline, filesInline)
    fieldsets = occurrence_fieldsets
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'25'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }
    list_per_page = 500  # show 500 records per page
    #change_form_template = "occurrence_change_form.html"
    actions = ["move_selected", "get_nearest_locality"]  # TODO clarify actions
    actions = ["get_nearest_locality", "create_data_csv"]

    options = {
        'layers': ['google.terrain']
    }

    def create_data_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')  # declare the response type
        response['Content-Disposition'] = 'attachment; filename="DRP_data.csv"'  # declare the file name
        writer = unicodecsv.writer(response)  # open a .csv writer
        o = Occurrence()  # create an empty instance of an occurrence object
        b = Biology()  # create an empty instance of a biology object

        occurrence_field_list = o.__dict__.keys()  # fetch the fields names from the instance dictionary
        try:  # try removing the state field from the list
            occurrence_field_list.remove('_state')  # remove the _state field
        except ValueError:  # raised if _state field is not in the dictionary list
            pass
        try:  # try removing the geom field from the list
            occurrence_field_list.remove('geom')
        except ValueError:  # raised if geom field is not in the dictionary list
            pass
        # Replace the geom field with two new fields
        occurrence_field_list.append("point_x")  # add new fields for coordinates of the geom object
        occurrence_field_list.append("point_y")

        biology_field_list = b.__dict__.keys()  # get biology fields
        try:  # try removing the state field
            biology_field_list.remove('_state')
        except ValueError:  # raised if _state field is not in the dictionary list
            pass

        #################################################################
        # For now this method handles all occurrences and corresponding #
        # data from the biology table for faunal occurrences.           #
        #################################################################
        writer.writerow(occurrence_field_list+biology_field_list)  # write column headers

        for occurrence in queryset:  # iterate through the occurrence instances selected in the admin
            # The next line uses string comprehension to build a list of values for each field
            occurrence_dict = occurrence.__dict__
            occurrence_dict['point_x'] = occurrence.geom.get_x()  # translate the occurrence geom object
            occurrence_dict['point_y'] = occurrence.geom.get_y()

            # Next we use the field list to fetch the values from the dictionary.
            # Dictionaries do not have a reliable ordering. This code insures we get the values
            # in the same order as the field list.
            try:  # Try writing values for all keys listed in both the occurrence and biology tables
                writer.writerow([occurrence.__dict__.get(k) for k in occurrence_field_list] +
                                [occurrence.Biology.__dict__.get(k) for k in biology_field_list])
            except ObjectDoesNotExist:  # Django specific exception
                writer.writerow([occurrence.__dict__.get(k) for k in occurrence_field_list])
            except AttributeError:  # Django specific exception
                writer.writerow([occurrence.__dict__.get(k) for k in occurrence_field_list])

        return response

    create_data_csv.short_description = "Download Selected to .csv"

    #admin action to get nearest locality
    def get_nearest_locality(self,request, queryset):
        #first make sure we are only dealing with one point
        if queryset.count()>1:
            self.message_user(request,"You can't get the nearest locality for multiple points at once. Please select a single point.",level='error')
            return
        #check if point is within any localities
        matching_localities = []
        for locality in Locality.objects.all():
            if locality.geom.contains(queryset[0].geom):
                matching_localities.append(str(locality.collectioncode) + "-" + str(locality.paleolocalitynumber))
        if matching_localities:
            #warning to user if the point is within multiple localities
            if len(matching_localities)>1:
                self.message_user(request,"The point falls within multiple localities (localities %s). Please consider redifining your localities so they don't overlap."% str(matching_localities).replace("[",""))
                return
            #Message user with the nearest locality
            self.message_user(request,"The point is in %s" %(matching_localities[0]))

        #if the point is not within any locality, get the nearest locality
        distances={}#dictionary which will contain {<localityString>:key} entries
        for locality in Locality.objects.all():
            locality_name=str(locality.collectioncode) + "-" + str(locality.paleolocalitynumber)
            #how are units being dealt with here?
            locality_distance_from_point = locality.geom.distance(queryset[0].geom)
            distances.update({locality_name:locality_distance_from_point})
            closest_locality_key=min(distances,key=distances.get)
        self.message_user(request,"The point is %d meters from locality %s" %(distances.get(closest_locality_key),closest_locality_key))


    #admin action to move points to specified x and y coordinates
    # TODO test and implement. Not currently active.
    def move_selected(self,request,queryset):
        returnURL="/admin/drp/occurrence/"
        def render_move_form():
            t=loader.get_template("move_points.html")
            c = RequestContext(request, {'returnURL': returnURL, 'selectedPoints': queryset, 'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,})
            return HttpResponse(t.render(c))

        if "apply" in request.POST:#if move form has been completed
            if request.POST["NewX"]:
                if request.POST["NewY"]:
                    for point in queryset:
                        point.geom.x=float(request.POST["NewX"])
                        point.geom.y=float(request.POST["NewY"])
                        point.save()
                        self.message_user(request,"Point Succesfully Moved")
                else:
                    return render_move_form()
            else:
                return render_move_form()
        else:#if move form has NOT been completed
            return render_move_form()
    move_selected.short_description = "Move the selected points."


#####################
## Taxonomy Admin  ##
#####################

class taxonomyAdmin(admin.ModelAdmin):
    list_display = ("id", "rank", "taxon")
    search_fields = ("taxon",)
    list_filter = ("rank",)


############################
## Register Admin Classes ##
############################

admin.site.register(Biology, biologyAdmin)
admin.site.register(Hydrology, hydrologyAdmin)
admin.site.register(Locality, localityAdmin)
admin.site.register(Occurrence, occurrenceAdmin)

