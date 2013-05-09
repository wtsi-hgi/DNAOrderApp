from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.files import File

from DNAOrderApp.order.models import Document
from DNAOrderApp.order.forms import DocumentForm

import csv, string, re

"""tutorial"""
def manifest_upload(request):
    #Handle file upload
    print "bye"
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            #newdoc = Document(docfile = request.FILES['docfile'])
            #newdoc.save()
            handle_upload_file(request.FILES['docfile'])
            
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('project-list'))
    else:
        form = DocumentForm() #A empty, unbound form

    print "hello"
    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'order/project-list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )

def handle_upload_file(f):
    print "handle upload file"
    #open the file
    data = csv.reader(f)
    #print f.name
    ext_list = f.name.split('.') #GET FILE TYPE
    list = data.next()
    print list

    while (list):
        

        if ( ext_list[-1] == 'xls' or ext_list[-1] == 'xlsx'):
            print "THIS IS AN EXCEL FILE"


        elif ( ext_list[-1] == 'csv'):
            #print "THIS IS A CSV FILE"
            if (data.line_num < 10):
                print list

            if any(x == ' Study:' for x in list ):
                print "Study: ", list[list.index(' Study:')]
                
                
            elif any( x == ' Supplier:' for x in list):
                print "Supplier: ", list[list.index(' Supplier:')]
            elif any( x == ' No. Plates Sent:' for x in list ):
                print "No. Plates Sent: ", list[list.index(' No. Plates Sent:')]
            elif any( x == 'SANGER PLATE ID' for x in list ):
                print "HEADERS!!!"
                print "SANGER PLATE ID: ", list[list.index('SANGER PLATE ID')]
                print "SANGER SAMPLE ID: ", list[list.index('SANGER SAMPLE ID')]

                # Collect the indices for SANGER PLATE ID,
                # SANGER SAMPLE ID, SUPPLIER SAMPLE NAME


        else:
            print "UNKNOWN FILE TYPE"

        try: 
            list = data.next()
        except StopIteration:
            break

    return 

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
    form = DocumentForm() #A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()
    return render(request, 'order/project-list.html', 
        {'documents': documents, 'form': form})

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