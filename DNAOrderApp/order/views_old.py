from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.files import File

from django.contrib.auth import login, authenticate, get_user

from DNAOrderApp.order.models import Document, Sample, Study, Display, Phenotype, SampleSubmission
from DNAOrderApp.order.models import UserProject, Source

from DNAOrderApp.order.models import PhenotypeForm, SampleSubmissionForm, UserProjectForm
#from DNAOrderApp.order.models import SampleForm, StudyForm
from DNAOrderApp.order.forms import DocumentForm

from django.contrib import messages
from django.db import IntegrityError, DatabaseError
import base64



import csv, string, re

formfile = ""


"""tutorial"""

def clear_form_file(request):
    global formfile 
    formfile = ""

    if not formfile:  #formfile is empty
        return True
    else:
        return False

# Binding a File to the Form
def bind_file_to_form(request):

    if request.method == 'POST':
        print "INSIDE BIND_FILE_TO_FORM, POST"
        form = DocumentForm(request.POST, request.FILES)
    else:
        print "IN THE ELSE, BIND_FILE_TO_FORM, POST"
        form = DocumentForm()

    return form

# preview page
# Display top and bottom 5 rows 
def preview(request):
    print "INSIDE PROJECT_LIST"
    global formfile
    print "this is formfile: ", formfile

    # Requires rendering of the top and bottom 5 of the rows from excel
    study_name = ""
    supplier_name = ""
    num_of_plates = 0
    headings = [" Sanger Plate ID ", " Sanger Sample ID "]
    rows = []

    if not formfile: # if form is an empty string
        formfile = bind_file_to_form(request)
        form = bind_file_to_form(request)
        print "INSIDE PROJECT LIST, SETTING FORMFILE AND FORM TO A FILE"
    else:
        form = formfile
        print "INSIDE PROJECT LIST, FORMFILE BEEN SET ALREADY, SETTING FORM TO BE FORMFILE"

    # if request.method == 'POST':
    #     form = DocumentForm(request.POST, request.FILES)

    if form.is_valid():

        # Helper function to show the extracted data to user
        results = handle_upload_file(request.FILES['docfile'])

        study_name = results[0]
        supplier_name = results[1]
        num_of_plates = results[2]

        sanger_plate_id = 0
        ind = -1
        for j in range(0,len(results[4])):

            if j%96 == 0:
                ind += 1
                sanger_plate_id = list(results[3])[ind]  

            print j, results[1], sanger_plate_id, results[4][j]

                
            row = [sanger_plate_id, results[4][j]]
            rows.append(row)

            # Redirect to the document list after POST
            # return HttpResponseRedirect(reverse('project-list'))
    # else:
    #     print "IN THE ELSE"
    #     form = DocumentForm() #A empty, unbound form 

    # Top 5
    top5 = rows[0:5]
    print "top 5: ", top5

    # Bottom 5
    bottom5 = rows[-5:]
    print "bottom 5: ", bottom5

    # Render list page with the documents and the form
    return render_to_response(
        'order/preview.html',
        {'form': form,
        'study_name': study_name,
        'supplier_name': supplier_name,
        'num_of_plates': num_of_plates,
        'headings': headings,
        'top5': top5,
        'bottom5': bottom5
         },
        context_instance=RequestContext(request)
    )

# Save and upload the manifest file into database
def save_files(request):
    # helper function to extract the info from excel
    print "INSIDE SAVE_FILE!"
    global formfile
    display_dict = {}
    newdoc_flag = False
    recent_document = []

    if not formfile: # if form is an empty string
        formfile = bind_file_to_form(request)
        form = bind_file_to_form(request)
        print "INSIDE SAVE_FILE, SETTING FORMFILE AND FORM TO BE THE RECENT_DOC"
    else:
        form = formfile
        print "INSIDE SAVE_FILE, FORMFILE BEEN SET ALREADY, SETTING FORM TO BE FORMFILE"

    form = bind_file_to_form(request)

    # if request.method == 'POST':
    #     print "SAVE_FILE INSIDE POST"
    #     form = DocumentForm(request.POST, request.FILES)
    #     return "form.is_valid():", form.is_valid()

    if form.is_valid():
        print "INSIDE IS VALID"
        # Will show the uploaded document
        newdoc = Document(docfile = request.FILES['docfile'])
        newdoc.save()
        newdoc_flag = True

            # Helper function to show the extracted data to user
        results = handle_upload_file(request.FILES['docfile'])

        print "BEFORE STUDY"
        print type(results[0])
        print results[0]
        #Store the study name
        try: 
            study = Study(study_name=results[0])
            study.save()
            print "AFTER STUDY: study saved"
        except IntegrityError:
            print "Study already exists"
            messages.info(request, u"Study already exists")

            sanger_plate_id = 0
            ind = -1
            for j in range(0,len(results[4])):

                if j%96 == 0:
                    ind += 1
                    sanger_plate_id = list(results[3])[ind]  

                print j, results[1], sanger_plate_id, results[4][j]
                print "type: " , j, type(results[1]), type(sanger_plate_id), type(results[4][j])

                # Store the sample data extracted from the excel form into the database
                sample = Sample(supplier_name=results[1], sanger_plate_id=sanger_plate_id, sanger_sample_id=results[4][j])
                print "after sample's been made"
                try:
                    sample.save()
                    print "sample save"
                except IntegrityError:
                    print "Integrity Error"

                
            # Redirect to the document list after POST
            # return HttpResponseRedirect(reverse('project-list'))
    # else:
    #     print "IN THE ELSE"
    #     form = DocumentForm() #A empty, unbound form 

    # recent document uploaded
    if Document.objects.all().exists() and newdoc_flag:
        recent_document = Document.objects.order_by('-id')[0]
        print "INSIDE DOCUMENT.OBJECTS.ALL().EXISTS AND NEWDOC_FLAG"
        print "newdoc_flag is: ", newdoc_flag
    else:
        recent_document = []

    print "save-file: ", recent_document, form
    # Render list page with the documents and the form
    return render_to_response(
        'order/sample-submission.html',
        {'recent_document': recent_document,
        'form': form,
         },
        context_instance=RequestContext(request)
    )

# # Simply putting the manifest into the proper directory
# def manifest_upload(request):
#     print "INSIDE MANIFEST_UPLOAD"
#     # helper function to extract the info from excel
#     display_dict = {}
#     newdoc_flag = False
#     recent_document = []
#     if request.method == 'POST':
#         print "IN THE POST"
#         form = DocumentForm(request.POST, request.FILES)

#         if form.is_valid():
#             print "INSIDE IS_VALID"
#             # Will show the uploaded document
#             newdoc = Document(docfile = request.FILES['docfile'])
#             newdoc.save()
#             newdoc_flag = True

#             print "BEFORE HANDLE UPLOAD FILE"
#             # Helper function to show the extracted data to user
#             results = handle_upload_file(request.FILES['docfile'])
#             print "AFTER HANDLE_UPLOAD_FILE INSIDE MANIFEST_UPLOAD"

#             sanger_plate_id = 0
#             ind = -1
#             for j in range(0,len(results[5])):

#                 if j%96 == 0:
#                     ind += 1
#                     sanger_plate_id = list(results[4])[ind]  

#                 print j, results[1], sanger_plate_id, results[5][j]

#                 # Store the data extracted from the excel form into the database
#                 #study = Study(study_name=results[0])
#                 #sample = Sample(supplier_name=results[1], sanger_plate_id=sanger_plate_id, sanger_sample_id=results[5][j])

#                 #Display Top 5 and Bottom 5 rows to user to show what's been extracted to the user.
#                 display_dict = {'study_name': results[0],
#                             'supplier_name': results[1],
#                             'sanger_plate_id': sanger_plate_id,
#                             'sanger_sample_id': results[5][j]}

#             # Redirect to the document list after POST
#             # return HttpResponseRedirect(reverse('project-list'))
#     else:
#         print "IN THE ELSE"
#         form = DocumentForm() #A empty, unbound form 

#     # recent document uploaded
#     if Document.objects.all().exists() and newdoc_flag:
#         recent_document = Document.objects.order_by('-id')[0]
#         print "INSIDE DOCUMENT.OBJECTS.ALL().EXISTS AND NEWDOC_FLAG"
#         print "newdoc_flag is: ", newdoc_flag
#     else:
#         recent_document = []

#     print "RECENT DOCUMENT : ", recent_document
#     return recent_document, form, display_dict


 



# Extracting out needed info from manifest
def handle_upload_file(f):
    print "INSIDE HANDLE UPLOAD FILE"
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
    headercount = 0 #did not return this, no use outside


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

    return study_name, supplier_name, num_plates, sanger_plate_id, sanger_sample_id





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

def basic_http_auth(f):
    def wrap(request, *args, **kwargs):
        if request.META.get('HTTP_AUTHORIZATION', False):
            authtype, auth = request.META['HTTP_AUTHORIZATION'].split(' ')
            auth = base64.b64decode(auth)
            username, password = auth.split(':')
            user = authenticate(username=username, password=password)
            if user is not None:
                print "user.is_active", user.is_active
                if user.is_active:
                    #attaches the authenticated user to current session, saves userid in session.
                    login(request,user)
                    print "get_user:", get_user(request)
                    
                    #Successful login
                    return f(request, *args, **kwargs)
                else:
                    #Return a 'disabled account' error message
                    print "disabled account error message"

            else:
                # Return an 'invalid login' error message
                print "User does not exist"
                r = HttpResponse("Auth Required", status = 401)
                r['WWW-Authenticate'] = 'Basic realm="bat"'
                return r
        print "HTTP_AUTHORIZATION CANNOT BE FOUND IN request.META"
        r = HttpResponse("Auth Required", status = 401)
        r['WWW-Authenticate'] = 'Basic realm="bat"'
        return r
        
    return wrap

@basic_http_auth
def signin(request):
    title = 'Sign In'
    print "inside login page"
    for key, value in request.session.items():
        print "request.session: ", key, value

    print "request.user.is_authenticated():", request.user.is_authenticated()
    print "request.user, ", request.user

    if not request.user.is_authenticated():
        print request.user, "is not authenticated."
        return HttpResponseRedirect(reverse('failed_signin'))

    # SUCCESSFULLY AUTHENTICATED USER
    return render(request, 'order/signin.html', {
        'title' : title,
        'realuser' : request.user
        })

def failed_signin(request):
    return render(request, 'order/failed_signin.html', {})

# ENTRY PAGE TO DIRECT USERS TO LOGIN
def index(request):
    title = 'Home'
    for key, value in request.session.items():
        print key, "corresponds to", value
    return render(request, 'order/index.html', {
        'title' : title,
        })

def project_list(request):
    print "inside project list"

    # CHECK IF USER HAS BEEN LOGGED IN
    if not request.user.is_authenticated():
        print request.user, "is not authenticated."
        return HttpResponseRedirect(reverse('failed_signin'))

    if request.method == 'DELETE':
        print "deleting a project"

    elif request.method == 'POST':
        userprojectform = UserProjectForm(request.POST)
        print "this is userprojectform", userprojectform

        if userprojectform.is_valid():
            userprojectform.save()
            print "Check userproject table to see if it has been saved properly."

            userprojectlist_all = UserProject.objects.all().order_by('project_name')

            #ASSUMING SOMEHOW I KNOW WHO I AM - faculty member
            userprojectlist_user = UserProject.objects.filter(username_id=2)


            return render(request, 'order/project-list.html', {
                'userprojectform': userprojectform,
                'userprojectlist_all': userprojectlist_all,
                'userprojectlist_user' : userprojectlist_user
            })

    else:
        # FIRST COMING TO THE PROJECT PAGE
        # CREATE DUMMY USERS HERE
        from django.contrib.auth.models import User
        if User.objects.filter(username='facultymember').count() == 0:
            user = User.objects.create_user(username='facultymember', email='facultymember@sanger.ac.uk', password='fmpassword')
            user.save()

        # DUMMY PROJECT STATUS
        # from DNAOrderApp.order.models import ProjectStatus
        # if ProjectStatus.objects.all().count() == 0:
        #     project_status = ProjectStatus(project_status='In Progress')
        #     project_status.save()
        #     project_status = ProjectStatus(project_status = 'Complete')
        #     project_status.save()

    userprojectform = UserProjectForm() #unbound form, no associated data, empty form
    userprojectlist_all = UserProject.objects.all().order_by('project_name')
    print "projectlistall: ", userprojectlist_all

    #ASSUMING SOMEHOW I KNOW WHO I AM 
    userprojectlist_user = UserProject.objects.filter(username_id=3)

    userproject = UserProject()
    print userproject
    return render(request, 'order/project-list.html', {
            'userprojectform' : userprojectform,
            'userprojectlist_all' : userprojectlist_all,
            'userprojectlist_user' : userprojectlist_user,
            'username' : request.user,
        })


# Phenotype Selection Page
def pheno_select(request, id=-1):
    print "in pheno_select"

    # CHECK IF USER HAS LOGGED IN
    if not request.user.is_authenticated():
        print request.user, "is not authenticated."
        return HttpResponseRedirect(reverse('failed_signin'))

    # RETURNING TO THE PAGE AFTER SUBMIT HAS BEEN PRESSED
    if request.method == 'DELETE' and id != -1:

        print "deleting a phenotype"
        del_pheno = Phenotype.objects.get(pk=id)
        print "del_pheno: ", del_pheno
        del_pheno.delete()
        phenotypelist = Phenotype.objects.all().order_by('phenotype_name')
        print "phenotypelist: ", phenotypelist
        phenotypeForm = PhenotypeForm() #unbound form, no associated data, empty form
        print "phenotypeForm: ", phenotypeForm


    elif request.method == 'POST':

        phenotypeForm = PhenotypeForm(request.POST) # bound form has submitted data; an invalid bound form
                                                    # is rendered, it can include inline error messages telling
                                                    # telling the user what data to correct. !!!

        print "this is phenotypeForm ", phenotypeForm

        if phenotypeForm.is_valid():
            phenotype_name = phenotypeForm.cleaned_data['phenotype_name']
            phenotype_type = phenotypeForm.cleaned_data['phenotype_type']
            phenotype_description = phenotypeForm.cleaned_data['phenotype_description']
            phenotype_definition = phenotypeForm.cleaned_data['phenotype_definition']

            print phenotype_name, phenotype_type, phenotype_description, phenotype_definition

            phenotypeForm.save()
            print "Check phenotype table to see if it has been saved properly."

            phenotypelist = Phenotype.objects.all().order_by('phenotype_name')

            return render(request, 'order/pheno-select.html', {
                'phenotypeForm': phenotypeForm,
                'success_alert' : '<div class="alert alert-success"> You have successfully added a phenotype! </div>',
                'phenotypelist' : phenotypelist,
            })

        # ERROR ALERT FOR INVALID BOUND FORM
        print "phenotypeForm is bound but invalid"
        phenotypelist = Phenotype.objects.all().order_by('phenotype_name')
        return render(request, 'order/pheno-select.html', {
                'phenotypeForm': phenotypeForm,
                'try_again_alert' : '<div class="alert alert-block"> Oops! Try again - phenotype was not added. </div>',
                'phenotypelist' : phenotypelist,
            })
    else:
        # FIRST COMING TO THE PHENO_SELECT PAGE
        phenotypeForm = PhenotypeForm() #unbound form, no associated data, empty form
        print "exiting", phenotypeForm
        print "phenotypelist ", Phenotype.objects.all()
        phenotypelist = Phenotype.objects.all().order_by('phenotype_name')


        # INITIALIZING ADDING PHENOTYPE TYPE IN THERE FIRST TIME AROUND
        from DNAOrderApp.order.models import PhenotypeType
        if PhenotypeType.objects.all().count() == 0:
            pt1 = PhenotypeType(phenotype_type="Affection Status")
            pt2 = PhenotypeType(phenotype_type="Qualitative")
            pt3 = PhenotypeType(phenotype_type="Quantitative")
            pt1.save()
            pt2.save()
            pt3.save()


    print "RENDERING OUTSIDE"
    return render(request, 'order/pheno-select.html', {
            'phenotypeForm': phenotypeForm,
            'fill_in_alert': '<div class="alert alert-info"> Fill in the following form to add a phenotype. </div>',
            'phenotypelist' : phenotypelist,

        })

    def __unicode__(self):
        return self.sample_submission_name

# Sample Submission Page
def sample_submission_list(request):
    print "in sample_submission_list"

    # CHECK IF USER HAS LOGGED IN
    if not request.user.is_authenticated():
        print request.user, "is not authenticated."
        return HttpResponseRedirect(reverse('failed_signin'))

    if request.method == 'DELETE':
        print "deleting a sample_submission"

    elif request.method == 'POST':
        sform = SampleSubmissionForm(request.POST)
        print "this is sform", sform

        if sform.is_valid():
            sform.save()
            print "Check Sample Submission table to see if it's been saved"
            sform_project_name = sform.cleaned_data['project_name']

            sample_submission_list_user = SampleSubmission.objects.filter(project_name=sform_project_name)
            sample_submission_list = SampleSubmission.objects.all().order_by('project_name')

            return render(request, 'order/sample-submission.html', {
                'sform': sform,
                'sample_submission_list' : sample_submission_list,
                'sample_submission_list_user' : sample_submission_list_user,
            })

    else:
        # DUMMY SOURCE
        from DNAOrderApp.order.models import Source
        if Source.objects.all().count() == 0:
            source = Source(source_name="Sanger Center", contact_name="Dr.Who", 
                source_description="Office located somewhere in the land far far away")
            source.save()
            source = Source(source_name="Addenbrookes Hospital", contact_name="Dr.How", 
                source_description="Office located somewhere in the land very closeby")
            source.save()

        # INITIALIZING ADDING PHENOTYPE TYPE IN THERE FIRST TIME AROUND
        from DNAOrderApp.order.models import PhenotypeType
        if PhenotypeType.objects.all().count() == 0:
            pt1 = PhenotypeType(phenotype_type="Affection Status")
            pt2 = PhenotypeType(phenotype_type="Qualitative")
            pt3 = PhenotypeType(phenotype_type="Quantitative")
            pt1.save()
            pt2.save()
            pt3.save()

        # DUMMY PHENOTYPES
        from DNAOrderApp.order.models import Phenotype, PhenotypeType
        if Phenotype.objects.all().count() == 0:
            pt1=PhenotypeType.objects.get(pk=1)
            p1 = Phenotype(phenotype_name="Sex", phenotype_type=pt1, phenotype_description="Sex", phenotype_definition="M/F")
            p1.save()

            pt2 = PhenotypeType.objects.get(pk=1)
            p2 = Phenotype(phenotype_name="Year of birth", phenotype_type=pt2, phenotype_description="Year of birth", phenotype_definition="YYYY")
            p2.save()

            pt3 = PhenotypeType.objects.get(pk=3)
            p3 = Phenotype(phenotype_name="Smoking status", phenotype_type=pt3, phenotype_description="Smoking status", phenotype_definition="Smoker/Non-smoker")
            p3.save()

        sample_submission_list = SampleSubmission.objects.all().order_by('project_name')
        sform = SampleSubmissionForm()
        print "this is sform", sform


    return render(request, 'order/sample-submission.html', {
            'sform' : sform,
            'sample_submission_list' : sample_submission_list
        })

# TRYING OUT BOOTSTRAP TUTORIAL
def base(request):
    return render(request, 'order/base.html', {})

# About Page
def about(request):
    return render(request, 'order/about.html', {})


# Contact Page
def contact(request):
        return render(request, 'order/contact.html', {})

# Login / Sign Up Page
def signup(request):
    # Check to see if you already exist in the database
    print "INSIDE SIGNUP!"
    return render(request, 'order/sign-up.html', {})

# User Profile Page
def user_profile(request):
    return render(request, 'order/profile.html', {})

# User Home Page, with the list of outgoing and incoming projects
def user_home(request):
    pass

# Index legend
def index_legend(request):
    return render(request, 'order/index_legend.html', {})

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
