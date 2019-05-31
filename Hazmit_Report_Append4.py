import json, os, uuid, collections, arcpy, shutil
# PyPDF2 is an open source module. This needs downloaded
from PyPDF2 import PdfFileMerger
# fpdf is an open source module. This needs downloaded
from fpdf import FPDF

#Section to create sitespecificList variable. 
class CustomPDF(FPDF):

    def header(self):
        # Set up a logo
        self.image(r'C:\Web_Print\YCPC Logo.jpg', 180, 18, 22)
        self.set_font('Helvetica', 'B', 18)

        self.ln(20)

        # Add an address
        self.cell(5)
        self.set_text_color(31, 73, 125)
        self.cell(20, 5, 'SITE-SPECIFIC HAZARD LIST FOR {}'.format(NameList), ln=1)
        self.set_line_width(1)
        self.set_draw_color(253, 185, 37)
        self.line(10, 40, 200, 40)

        # Line break
        self.ln(10)

    def footer(self):
        self.set_y(-10)

        self.set_font('Arial', 'I', 8)

        # Add a page number
        page = 'Page ' + str(self.page_no()) + '/{nb}'
        self.cell(0, 10, page, 0, 0, 'C')

def create_pdf(pdf_path):
    pdf = CustomPDF()
    # Create the special value {nb}
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Times', 'B', 15)
    line_no = 1
    for site in sitespecific:
        pdf.set_text_color(31, 73, 125)
        pdf.cell(10, 10, txt="{} - {}".format(line_no, site), ln=1)
        line_no += 1
    pdf.output(pdf_path)

arcpy.env.overwriteOutput = True

# Output to the scratch workspace
scratch = arcpy.env.scratchFolder
arcpy.AddMessage("  Scratch WS " + str(scratch))

#mxd = arcpy.mapping.MapDocument(arcpy.GetParameterAsText(0))
mxd = arcpy.mapping.MapDocument(r"C:\Web_Print\A4 Landscape2.mxd")

# Sets PIDN you want to use in the geoprocessing service
NameList = arcpy.GetParameterAsText(0)
#NameList = "36000KH0175B0"

# Output Variables
output_name = str(NameList) + '.pdf'
PDF_File = os.path.join(arcpy.env.scratchFolder + '\\' + output_name)
OutputFile = os.path.join(arcpy.env.scratchFolder + '\\' + "Appended_" + output_name)

# PDFS variables residing on the ArcGIS Server. Make sure folder is registered with ArcGIS Server Manager
flood_pdf = r"C:\Web_Print\Report\Flooding.pdf"
inundation_pdf = r"C:\Web_Print\Report\Dam Failure.pdf"
landslide_pdf = r"C:\Web_Print\Report\Landslide.pdf"
radon_pdf = r"C:\Web_Print\Report\Radon Exposure.pdf"
hazard_pdf = r"C:\Web_Print\Report\Environmental Hazards.pdf"
env_hazard = r"C:\Web_Print\Report\Environmental Hazards.pdf"
levee_pdf = r"C:\Web_Print\Report\Levee Failure.pdf"
sinkhole_pdf = r"C:\Web_Print\Report\Subsidence_Sinkhole.pdf"
nuclear_pdf = r"C:\Web_Print\Report\Nuclear Incidents.pdf"
earthquake_pdf = r"C:\Web_Print\Report\Earthquake.pdf"
drought_pdf = r"C:\Web_Print\Report\Drought.pdf"
wildfire_pdf = r"C:\Web_Print\Report\Wildfire.pdf"
urbanfire_pdf = r"C:\Web_Print\Report\UrbanFire_Explosion.pdf"
extreme_pdf = r"C:\Web_Print\Report\Extreme_Temperatures.pdf"
civildisturb_pdf = r"C:\Web_Print\Report\Civil Disturbance.pdf"
hailstorm_pdf = r"C:\Web_Print\Report\Hailstorm.pdf"
hurricane_pdf = r"C:\Web_Print\Report\Hurricane Tropical Storm Noreaster.pdf"
invasive_pdf = r"C:\Web_Print\Report\Invasive Species.pdf"
lightning_pdf = r"C:\Web_Print\Report\Lightning Strike.pdf"
massfood_pdf = r"C:\Web_Print\Report\Mass Food and Animal Contamination.pdf"
pandemic_pdf = r"C:\Web_Print\Report\Pandemic and Infectious Disease.pdf"
terrorism_pdf = r"C:\Web_Print\Report\Terrorism.pdf"
tornado_pdf = r"C:\Web_Print\Report\Tornado Windstorm.pdf"
winterstorm_pdf = r"C:\Web_Print\Report\Winter Storm.pdf"

sitespecificList = r"C:\Web_Print\Report\SiteSpecific_Hazards.pdf"
regionalList = r"C:\Web_Print\Report\Regional_Hazards.pdf"

# Lists used to append pdfs
pdfs = []
sitespecific = []

#Field Names associated with layer.name on line 121
fieldNames = ["PIDN",\
              "PROPADR",\
              "OWNER_FULL",\
              "LUC",\
              "FLOOD",\
              "INUNDATION",\
              "LANDSLIDE",\
              "RADON",\
              "ENIV_HAZARD",\
              "LEVEE",\
              "SINKHOLE",\
              "NUCLEAR",\
              "EARTHQUAKE",\
              "DROUGHT",\
              "WILDFIRE",\
              "URBANFIRE"]

#Lists thru Layers from mxd variable
for lyr in arcpy.mapping.ListLayers(mxd):
    if lyr.name == "Parcel Select":
        lyr.definitionQuery = "PIDN = '"+NameList+"'"
        with arcpy.da.SearchCursor(lyr, fieldNames) as cursor:
            for row in cursor:
                arcpy.AddMessage(u'{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}'.format(row[0], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15]))

                if row[4] != 'Not in any FEMA FLOOD ZONES':
                    FloodFile = os.path.join(arcpy.env.scratchFolder + '\\' + "Flood_" + output_name)
                    shutil.copy2(flood_pdf, FloodFile)
                    pdfs.append(FloodFile)
                    sitespecific.append("Flooding Information")

                if row[5] != 'Not in Inundation Area':
                    InundationFile = os.path.join(arcpy.env.scratchFolder + '\\' + "Inundation_" + output_name)
                    shutil.copy2(inundation_pdf, InundationFile)
                    pdfs.append(InundationFile)
                    sitespecific.append("Inundation Information")

                if row[6] != 'Not in Landslide Area':
                    LandslideFile = os.path.join(arcpy.env.scratchFolder + '\\' + "Landslide_" + output_name)
                    shutil.copy2(landslide_pdf, LandslideFile)
                    pdfs.append(LandslideFile)
                    sitespecific.append("Landslide Information")

                if row[7] != 'N/A':
                    RadonFile = os.path.join(arcpy.env.scratchFolder + '\\' + "Radon_" + output_name)
                    shutil.copy2(radon_pdf, RadonFile)
                    pdfs.append(RadonFile)
                    sitespecific.append("Radon Information")

                if row[8] != 'Not in Environmental Hazard Area':
                    HazardFile = os.path.join(arcpy.env.scratchFolder + '\\' + "Hazard_" + output_name)
                    shutil.copy2(hazard_pdf, HazardFile)
                    pdfs.append(HazardFile)
                    sitespecific.append("Environmental Hazard Information")

                if row[9] != 'Not in Levee Risk Area':
                    LeveeFile = os.path.join(arcpy.env.scratchFolder + '\\' + "Levee_" + output_name)
                    shutil.copy2(levee_pdf, LeveeFile)
                    pdfs.append(LeveeFile)
                    sitespecific.append("Levee Information")

                if row[10] != 'Not in Sinkhole Risk Area':
                    SinkholeFile = os.path.join(arcpy.env.scratchFolder + '\\' + "Sinkhole_" + output_name)
                    shutil.copy2(sinkhole_pdf, SinkholeFile)
                    pdfs.append(SinkholeFile)
                    sitespecific.append("Sinkhole Information")

                if row[11] != 'Not in a 10 Mile Radius':
                    NuclearFile = os.path.join(arcpy.env.scratchFolder + '\\' + "Nuclear_" + output_name)
                    shutil.copy2(nuclear_pdf, NuclearFile)
                    pdfs.append(NuclearFile)
                    sitespecific.append("Nuclear Information")

                if row[12] != 'N/A':
                    EarthquakeFile = os.path.join(arcpy.env.scratchFolder + '\\' + "Earthquake_" + output_name)
                    shutil.copy2(earthquake_pdf, EarthquakeFile)
                    pdfs.append(EarthquakeFile)
                    sitespecific.append("Earthquake Information")

                if row[13] != 'Not Water Challenged':
                    DroughtFile = os.path.join(arcpy.env.scratchFolder + '\\' + "Drought_" + output_name)
                    shutil.copy2(drought_pdf, DroughtFile)
                    pdfs.append(DroughtFile)
                    sitespecific.append("Drought Information")

                if row[14] != 'Not in Wildfire Zone':
                    WildfireFile = os.path.join(arcpy.env.scratchFolder + '\\' + "Wildfire_" + output_name)
                    shutil.copy2(wildfire_pdf, WildfireFile)
                    pdfs.append(WildfireFile)
                    sitespecific.append("Wildfire Information")

                if row[15] != 'Not in Urban Fire Zone':
                    UrbanfireFile = os.path.join(arcpy.env.scratchFolder + '\\' + "Urbanfire_" + output_name)
                    shutil.copy2(urbanfire_pdf, UrbanfireFile)
                    pdfs.append(UrbanfireFile)
                    sitespecific.append("Urban Fire Information")

del lyr

SiteSpecificFile = os.path.join(arcpy.env.scratchFolder + '\\' + "SiteSpecificList_" + output_name)
create_pdf(SiteSpecificFile)
pdfs.append(SiteSpecificFile)
pdfs.insert(0, pdfs.pop())

RegionalFile = os.path.join(arcpy.env.scratchFolder + '\\' + "RegionalList_" + output_name)
shutil.copy2(regionalList, RegionalFile)
pdfs.append(RegionalFile)

ExtremeFile = os.path.join(arcpy.env.scratchFolder + '\\' + "Extreme_" + output_name)
shutil.copy2(extreme_pdf, ExtremeFile)
pdfs.append(ExtremeFile)

CivilDisturbFile = os.path.join(arcpy.env.scratchFolder + '\\' + "CivilDisturb_" + output_name)
shutil.copy2(civildisturb_pdf, CivilDisturbFile)
pdfs.append(CivilDisturbFile)

HailstormFile = os.path.join(arcpy.env.scratchFolder + '\\' + "Hailstorm_" + output_name)
shutil.copy2(hailstorm_pdf, HailstormFile)
pdfs.append(HailstormFile)

HurricaneFile = os.path.join(arcpy.env.scratchFolder + '\\' + "Hurricane_" + output_name)
shutil.copy2(hurricane_pdf, HurricaneFile)
pdfs.append(HurricaneFile)

InvasiveFile = os.path.join(arcpy.env.scratchFolder + '\\' + "Extreme_" + output_name)
shutil.copy2(invasive_pdf, InvasiveFile)
pdfs.append(InvasiveFile)

LightningFile = os.path.join(arcpy.env.scratchFolder + '\\' + "Lightning_" + output_name)
shutil.copy2(lightning_pdf, LightningFile)
pdfs.append(LightningFile)

MassfoodFile = os.path.join(arcpy.env.scratchFolder + '\\' + "MassFood_" + output_name)
shutil.copy2(massfood_pdf, MassfoodFile)
pdfs.append(MassfoodFile)

PandemicFile = os.path.join(arcpy.env.scratchFolder + '\\' + "Pandemic_" + output_name)
shutil.copy2(pandemic_pdf, PandemicFile)
pdfs.append(PandemicFile)

TerrorismFile = os.path.join(arcpy.env.scratchFolder + '\\' + "Terrormism_" + output_name)
shutil.copy2(terrorism_pdf, TerrorismFile)
pdfs.append(TerrorismFile)

TornadoFile = os.path.join(arcpy.env.scratchFolder + '\\' + "Tornado_" + output_name)
shutil.copy2(tornado_pdf, TornadoFile)
pdfs.append(TornadoFile)

WinterstormFile = os.path.join(arcpy.env.scratchFolder + '\\' + "Winterstorm_" + output_name)
shutil.copy2(winterstorm_pdf, WinterstormFile)
pdfs.append(WinterstormFile)

#Section generates Data Driven Pages
mxd.dataDrivenPages.refresh()
ddp = mxd.dataDrivenPages
indexLayer = ddp.indexLayer
arcpy.SelectLayerByAttribute_management(indexLayer, "NEW_SELECTION", "PIDN = '"+NameList+"'")

for indexPage in ddp.selectedPages:
  ddp.currentPageID = indexPage
  ddp.exportToPDF(PDF_File, "CURRENT")

pdfs.append(PDF_File)

pdfs.insert(0, pdfs.pop())

#r_pdfs = list(reversed(pdfs))

arcpy.AddMessage(pdfs)

# Section to Append all the PDFS from pdfs list
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
    merger = PdfFileMerger()

    for pdf in pdfs:
        merger.append(pdf)

    merger.write(OutputFile)

del mxd

arcpy.SetParameterAsText(1, OutputFile)

arcpy.AddMessage("  Process Complete")
