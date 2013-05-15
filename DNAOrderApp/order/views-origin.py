from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.files import File

from DNAOrderApp.order.models import Document, Sample, Study, Display
#from DNAOrderApp.order.models import SampleForm, StudyForm
from DNAOrderApp.order.forms import DocumentForm


import csv, string, re


"""tutorial"""
# Simply putting the manifest into the proper directory
def manifest_upload(request):
    # helper function to extract the info from excel
    display_dict = {}
    newdoc_flag = False
    recent_document = []
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            # Will show the uploaded document
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            newdoc_flag = True

            # Helper function to show the extracted data to user
            results = handle_upload_file(request.FILES['docfile'])

            sanger_plate_id = 0
            ind = -1
            for j in range(0,len(results[5])):

                if j%96 == 0:
                    ind += 1
                    sanger_plate_id = list(results[4])[ind]  

                print j, results[1], sanger_plate_id, results[5][j]

                #Display what's been taken from the manifest to user
                display_dict = {'study_name': results[0],
                            'supplier_name': results[1],
                            'sanger_plate_id': sanger_plate_id,
                            'sanger_sample_id': results[5][j]}

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('project-list'))
    else:
        form = DocumentForm() #A empty, unbound form 

    # recent document uploaded
    if Document.objects.all().exists() and newdoc_flag:
        recent_document = Document.objects.order_by('-id')[0]
    else:
        recent_document = []

    print "recent_document: ", recent_document
    # Render list page with the documents and the form
    return render_to_response(
        'order/project-list.html',
        {'recent_document': recent_document,
        'form': form,
        'display_dict': display_dict, 
         },
        context_instance=RequestContext(request)
    )

# This is to commit all the fields into the database to create a project
def save(request):
    pass

def manifest_upload_1(request):
    #Handle file upload
    print "bye"
    display_dict = {}
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            print "yay"
            # Will show the uploaded document
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            results = handle_upload_file(request.FILES['docfile'])
            study = Study(study_name=results[0])

            sanger_plate_id = 0
            ind = -1
            for j in range(0,len(results[5])):

                if j%96 == 0:
                    ind += 1
                    sanger_plate_id = list(results[4])[ind]  

                print j, results[1], sanger_plate_id, results[5][j]

                sample = Sample(supplier_name=results[1], sanger_plate_id=sanger_plate_id, sanger_sample_id=results[5][j])
                sanger_sample_id

                #Display what's been taken from the manifest to user
                display_dict = {'study_name': results[0],
                            'supplier_name': results[1],
                            'sanger_plate_id': sanger_plate_id,
                            'sanger_sample_id': results[5][j]}

            
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('project-list'))
    else:
        form = DocumentForm() #A empty, unbound form

    print "hello"
    # Load documents for the list page
    documents = Document.objects.all()
    recent_document = Document.objects.order_by('-id')[0]

    # Render list page with the documents and the form
    return render_to_response(
        'order/project-list.html',
        {'documents': documents, 
        'recent_document': recent_document,
        'form': form, 
        'display_dict': display_dict, 
         },
        context_instance=RequestContext(request)
    )

# Extracting out needed info from manifest
def handle_upload_file(f):
    print "handle upload file"
    #open the file
    data = csv.reader(f)
    #print f.name
    ext_list = f.name.split('.') #GET FILE TYPE

    list = data.next()
    print list

    study_name = 0
    supplier_name = 0
    num_plates = 0
    sanger_plate_id = set()
    spid_size = 0
    sanger_sample_id = []
    headercount = 0


    while (list):
        

        if ( ext_list[-1] == 'xls' or ext_list[-1] == 'xlsx'):
            print "THIS IS AN EXCEL FILE"

        elif ( ext_list[-1] == 'csv'):

            if headercount >= 6 and list[spid]:    #SANGER PLATE ID, SANGER SAMPLE ID
                
                sanger_plate_id.add(list[spid])

                #if (len(sanger_plate_id) != spid_size):
                #    for sample in sanger_sample_id:
                #        Sample(supplier_name=supplier_name, sanger_sample_id=sample, sanger_plate_id=list(sanger_plate_id)[spid_size-2])
                #        Sample.save()

                sanger_sample_id.append(list[ssid])
                

            else: #HEADER
                if any(x == ' Study:' for x in list ):
                    print "Study: ", list[list.index(' Study:') + 1]
                    study_name = list[list.index(' Study:') + 1]
                    headercount += 1

                elif any( x == ' Supplier:' for x in list):
                    print "Supplier: ", list[list.index(' Supplier:') + 1]
                    supplier_name = list[list.index(' Supplier:') + 1]
                    headercount += 1

                elif any( x == ' No. Plates Sent:' for x in list ):
                    print "No. Plates Sent: ", list[list.index(' No. Plates Sent:') + 1]
                    num_plates = list[list.index(' No. Plates Sent:') + 1]
                    headercount += 1
                
                elif any( x == 'SANGER PLATE ID' for x in list ):
                    print "SANGER PLATE ID index: ", list.index('SANGER PLATE ID')
                    spid = list.index('SANGER PLATE ID')
                    headercount += 1

                    print "WELL # index: ", list.index('WELL')
                    wellid = list.index('WELL')
                    headercount += 1

                    print "SANGER SAMPLE ID index: ", list.index('SANGER SAMPLE ID')
                    ssid = list.index('SANGER SAMPLE ID')
                    headercount += 1

        else:
            print "UNKNOWN FILE TYPE"

        try: 
            list = data.next()
        except StopIteration:
            break

    return study_name, supplier_name, num_plates, headercount, sanger_plate_id, sanger_sample_id


# CONSIDERING TRANSLATING AN EXISTING STUDY MODEL INTO A FORM TO FILL IN BY THE USER....
# IF I THINK OF ERADICATING MANIFEST UPLOAD

def pheno_list(request):
    return render(request, 'order/pheno-list.html', {})

def welcome_collab(request):
    return render(request, 'order/welcome-collaborator.html', {})

#TUTORIAL
def contact(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = ContactForm() # An unbound form

    return render(request, 'contact.html', {
        'form': form,
    })

def _96plate(request):
    return render(request, 'order/96plate.html', {})

""" ACTUAL DNA ORDER APP """ 
# Test
def test(request):
    return render(request, 'order/base_template.html', {})

def index(request):
    title = 'Home'
    return render(request, 'order/index.html', {'title' : title})

# TRYING OUT BOOTSTRAP TUTORIAL
def base(request):
    return render(request, 'order/base.html', {})

# About Page
def about(request):
    return render(request, 'order/about.html', {})

# Project List Page
def project_list(request):
    # helper function to extract the info from excel
    display_dict = {}
    newdoc_flag = False

    manifest_upload(request)

    if request.method == 'POST':
        print "inside project_list POST"
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            # Will show the uploaded document
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            newdoc_flag = True
            print "project_list: saved the document"

            # Helper function to show the extracted data to user
            results = handle_upload_file(request.FILES['docfile'])
            print "showing results"

            sanger_plate_id = 0
            ind = -1
            for j in range(0,len(results[5])):

                if j%96 == 0:
                    ind += 1
                    sanger_plate_id = list(results[4])[ind]  

                print j, results[1], sanger_plate_id, results[5][j]

                #Display what's been taken from the manifest to user
                display_dict = {'study_name': results[0],
                            'supplier_name': results[1],
                            'sanger_plate_id': sanger_plate_id,
                            'sanger_sample_id': results[5][j]}

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('project-list'))
    else:
        form = DocumentForm() #A empty, unbound form 

    # recent document uploaded
    if Document.objects.all().exists() and newdoc_flag:
        recent_document = Document.objects.order_by('-id')[0]
    else:
        recent_document = []

    print "recent_document: ", recent_document, form, display_dict
    # Render list page with the documents and the form
    return render_to_response(
        'order/project-list.html',
        {'recent_document': recent_document,
        'form': form,
        'display_dict': display_dict, 
         },
        context_instance=RequestContext(request)
    )

# Contact Page
def contact(request):
        return render(request, 'order/contact.html', {})

# Login / Sign Up Page
def signup(request):
    return render(request, 'order/sign-up.html', {})

# User Profile Page
def user_profile(request):
    pass
    # return render(request, 'order/user_profile.html', {})

# User Home Page, with the list of outgoing and incoming projects
def user_home(request):
    pass

# POP-UP: Phenotype Selection Page
def pheno_select(request):
    return render(request, 'order/pheno-select.html', {})

# POP-UP: Choose the method that the wells will be filled: Manual or Robot?

# POP-UP ROBOT: Please Upload Mapping files
    # Will require an uploader and a parser, SHOWS UPLOADED FORMAT

# POP-UP UPLOADED FORMAT: Shows a table of the csv, vcf file.

# POP-UP MANUAL: Choose a Style you would like to work in, may CUSTOMIZE ORDER

# POP-UP CUSTOMIZE ORDER: A picture of the 96 wells and lets user specify order

# WELL-FILLING FORM
def well_filling_form(request):
    pass

def test_template(request):
    return render(request, 'order/test_template.html', {})

"""

def index(request):
    return render(request, 'order/index.html', {})
    
def faculty_member_page(request):
    return render(request, 'order/faculty_member.html', {})
    # return HttpResponse("Welcome Faculty Member. Here's your Project List")

def upload_empty_manifest(request):
    return HttpResponse("Please download the manifest from the Sequencescape and upload the \
        excel sheet here.")

def collaborator_page(request):
    return render(request, 'order/collaborator.html', {})

def plate_fill_type(request):
    return render(request, 'order/plate_fill_type.html', {})

def plate_fill_order(request):
    return render(request, 'order/plate_fill_order.html', {})

def customized_plate_fill_order(request):
    return HttpResponse("Please specify the order the wells are being filled")

def upload_result_page(request):
    return HttpResponse("You have successfully uploaded the manifest/ Manifest failed to upload")

def fill_wells(request):
    return render(request, 'order/fill_wells.html', {})

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
    
"""
