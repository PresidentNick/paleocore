from django.db import models
from mysite.ontologies import BASIS_OF_RECORD_VOCABULARY, ITEM_TYPE_VOCABULARY, COLLECTING_METHOD_VOCABULARY, \
    COLLECTOR_CHOICES, SIDE_VOCABULARY


class Occurrence(models.Model):
    specimen_number = models.IntegerField(primary_key=True)  # NOT NULL
    cm_specimen_number = models.IntegerField(null=True, blank=True)  # CM SPec #
    locality = models.ForeignKey("Locality", to_field="locality_number")
    date_collected = models.DateField(blank=True, null=True, editable=True)
    time_collected = models.CharField(null=True, blank=True, max_length=50)
    date_last_modified = models.DateTimeField("Date Last Modified", auto_now_add=True, auto_now=True)
    basis_of_record = models.CharField("Basis of Record", max_length=50, blank=True, null=False,
                                       choices=BASIS_OF_RECORD_VOCABULARY)  # NOT NULL
    item_scientific_name = models.CharField("Scientific Name", null=True, blank=True, max_length=255)  # Taxon
    item_description = models.CharField(null=True, blank=True, max_length=255)
    image = models.FileField(max_length=255, blank=True, upload_to="uploads/images/gdb", null=True)

    # Disposition fields
    loan_date = models.DateTimeField()
    loan_recipient = models.CharField(max_length=200)
    on_loan = models.BooleanField(default=False)  # Loan Status

    # Geospatial
    geom = models.GeometryField(srid=4326, blank=True, null=True)


    def __unicode__(self):
        """
        What is the best string representation for an occurrence instance?
        All collected items have catalogue numbers, but observations do not
        This method returns the catalog number if it exists, or a string with the id value
        if there is no catalog number.
        """
        return self.catalog_number


class Biology(Occurrence):
    # Taxonomy fields
    kingdom = models.CharField(null=True, blank=True, max_length=50)
    phylum = models.CharField(null=True, blank=True, max_length=50)
    tax_class = models.CharField("Class", null=True, blank=True, max_length=50)  # Class
    tax_order = models.CharField("Order", null=True, blank=True, max_length=50)  # Order
    family = models.CharField(null=True, blank=True, max_length=50)
    subfamily = models.CharField(null=True, blank=True, max_length=50)
    tribe = models.CharField(null=True, blank=True, max_length=50)
    genus = models.CharField(null=True, blank=True, max_length=50)
    specificepithet = models.CharField("Species Name", null=True, blank=True, max_length=50)  # Species
    infraspecificepithet = models.CharField(null=True, blank=True, max_length=50)
    infraspecificrank = models.CharField(null=True, blank=True, max_length=50)
    # Identification fields
    authoryearofscientificname = models.CharField(null=True, blank=True, max_length=50)
    nomenclaturalcode = models.CharField(null=True, blank=True, max_length=50)
    identificationqualifier = models.CharField(null=True, blank=True, max_length=50)
    identifiedby = models.CharField(null=True, blank=True, max_length=100)
    dateidentified = models.DateTimeField(null=True, blank=True)
    typestatus = models.CharField(null=True, blank=True, max_length=50)
    # Description fields
    sex = models.CharField(null=True, blank=True, max_length=50)
    lifestage = models.CharField(null=True, blank=True, max_length=50)
    preparations = models.CharField(null=True, blank=True, max_length=50)
    morphobanknum = models.IntegerField(null=True, blank=True)
    element = models.CharField(null=True, blank=True, max_length=50)
    side = models.CharField(null=True, blank=True, max_length=50)
    attributes = models.CharField(null=True, blank=True, max_length=50)
    notes = models.TextField(null=True, blank=True, max_length=64000)
    lower_tooth = models.CharField(null=True, blank=True, max_length=50)
    upper_tooth = models.CharField(null=True, blank=True, max_length=50)
    jaw = models.CharField(null=True, blank=True, max_length=50)
    mandible = models.CharField(null=True, blank=True, max_length=50)
    maxilla = models.CharField(null=True, blank=True, max_length=50)
    teeth = models.CharField(null=True, blank=True, max_length=50)
    cranial = models.CharField(null=True, blank=True, max_length=50)
    miscellaneous = models.CharField(null=True, blank=True, max_length=50)
    vertebral = models.CharField(null=True, blank=True, max_length=50)
    forelimb = models.CharField(null=True, blank=True, max_length=50)
    hindlimb = models.CharField(null=True, blank=True, max_length=50)
    NALMA = models.CharField(null=True, blank=True, max_length=50)
    sub_age = models.CharField(null=True, blank=True, max_length=50)


class Locality(models.Model):
    locality_number = models.IntegerField(primary_key=True)  # NOT NULL
    locality_field_number = models.CharField(null=True, blank=True, max_length=50)
    name = models.CharField(null=True, blank=True, max_length=50)  # Locality Name
    date_discovered = models.DateField(null=true, blank=True)
    formation = models.CharField(null=True, blank=True, max_length=50)  # Formation
    member = models.CharField(null=True, blank=True, max_length=50)
    NALMA = models.CharField(null=True, blank=True, max_length=50)
    survey = models.CharField(null=True, blank=True, max_length=50)
    quad_sheet = models.CharField(null=True, blank=True, max_length=50)
    verbatim_latitude = models.CharField(null=True, blank=True, max_length=50)  # Latitude
    verbatim_longitude = models.CharField(null=True, blank=True, max_length=50)  # Longitude
    verbatim_utm = models.CharField(null=True, blank=True, max_length=50)  # UTM
    verbatim_gps_coordinates = models.CharField(null=True, blank=True, max_length=50)  # GPS
    verbatim_elevation = models.IntegerField(null=True, blank=True)  # Elevation
    gps_date = models.DateField(null=True, blank=True, editable=True)
    resource_area = models.CharField(null=True, blank=True, max_length=50)
    notes = models.CharField(null=True, blank=True, max_length=50)
    cm_locality_number = models.IntegerField(null=True, blank=True)  # CM Loc #
    region = models.CharField(null=True, blank=True, max_length=50)
    blm_district = models.CharField(null=True, blank=True, max_length=50)
    county = models.CharField(null=True, blank=True, max_length=50)
    image = models.FileField(max_length=255, blank=True, upload_to="uploads/images/gdb", null=True)
    geom = models.GeometryField(srid=4326, blank=True, null=True)  # NOT NULL




