from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.files import File

from django.contrib.auth import login, authenticate, get_user
from django.contrib.auth.models import User

from DNAOrderApp.order.models import Document, Sample, Study, Display, Phenotype, SampleSubmission
from DNAOrderApp.order.models import UserProject, AffiliatedInstitute, PhenotypeType, DNAOrderAppUser

from DNAOrderApp.order.models import PhenotypeForm, SampleSubmissionForm, UserProjectForm, UserForm, UserProjectForm_FM
from DNAOrderApp.order.models import DNAOrderAppUserForm
from DNAOrderApp.order.forms import DocumentForm

from django.contrib import messages
from django.db import IntegrityError, DatabaseError
import base64
from django.template import Template, Context, RequestContext

import csv, string, re

formfile = ""

from django.contrib.auth.models import User


# new functions - after meeting

def delete_project(id):
    print "deleting a project"
    alert_msg = ""
    try:
        print "pkid ", id
        u = UserProject.objects.get(pk=id)
        u.delete()
        print "Check userproject table to see if it is deleted."

    except UserProject.DoesNotExist, e:
        alert_msg = '<div class="alert alert-error"><b>Uh Oh! </b>',e.message,"</div>"
    except AssertionError, e:
        alert_msg = '<div class="alert alert-error"><b>Uh Oh! </b>',e.message," </div>"
    except KeyError, e:
        alert_msg = '<div class="alert alert-error"><b>Uh Oh! </b>',e.message," </div>"

    userprojectlist_all = UserProject.objects.all().order_by('project_name')
    userprojectform = UserProjectForm() #unbound form, no associated data, empty form

    # it should return just the updated table
    fp = open('/Users/aw18/Project/ENV/DNAOrderApp/DNAOrderApp/order/templates/order/project-table.html')
    t = Template(fp.read())
    fp.close()
    c = Context({
            'userprojectform': userprojectform,
            'userprojectlist_all': userprojectlist_all,
            'alert_msg': alert_msg,
        })
    return HttpResponse(t.render(c))

def add_project(request):
    print "adding a project"
    alert_msg = ""
    print "tis is request.POST in add_project:", request.POST
    userprojectform = UserProjectForm(request.POST)
        
    if userprojectform.is_valid():
        userprojectform.save()
        print "Check userproject table to see if it has been saved properly."
        print "Successfully added a project"
        alert_msg = "<div class=\"alert alert-success\"><b>Good Job!</b> You have successfully added a project!</div>"

    else:
        alert_msg = '<div class="alert alert-error"><b>Uh Oh!</b> No project was added. Invalid Form. </div>'

    userprojectlist_all = UserProject.objects.all().order_by('project_name')
    userprojectform = UserProjectForm() #unbound form, no associated data, empty form

    # it should return just the updated table
    fp = open('/Users/aw18/Project/ENV/DNAOrderApp/DNAOrderApp/order/templates/order/project-table.html')
    t = Template(fp.read())
    fp.close()
    c = Context({
            'userprojectform': userprojectform,
            'userprojectlist_all': userprojectlist_all,
            'alert_msg': alert_msg,
        })

    return HttpResponse(t.render(c))

def handle_project(request, action=None, id=None):
    print "in handle_project"
    if action == "DELETE":
        if id != None:
            return delete_project(id)
    elif action == "ADD":
        return add_project(request)
    else:
        return HttpResponse("Everything failed! - handle project")


def delete_sample_submission(id):
    print "deleting a sample submission"
    alert_msg = ""
    try:
        print "pkid ", id
        s = SampleSubmission.objects.get(pk=id)
        s.delete()
        print "Check samplesubmission table to see if it is deleted."

    except SampleSubmission.DoesNotExist, e:
        alert_msg = '<div class="alert alert-error"><b>Uh Oh! </b>',e.message,"</div>"
    except AssertionError, e:
        alert_msg = '<div class="alert alert-error"><b>Uh Oh! </b>',e.message," </div>"
    except KeyError, e:
        alert_msg = '<div class="alert alert-error"><b>Uh Oh! </b>',e.message," </div>"

    samplesubmissionlist_all = SampleSubmission.objects.all().order_by('project_name')
    samplesubmissionform = SampleSubmissionForm() #unbound form, no associated data, empty form

    # it should return just the updated table
    fp = open('/Users/aw18/Project/ENV/DNAOrderApp/DNAOrderApp/order/templates/order/sample-submission-table.html')
    t = Template(fp.read())
    fp.close()
    c = Context({
            'samplesubmissionform': samplesubmissionform,
            'samplesubmissionlist_all': samplesubmissionlist_all,
            'alert_msg': alert_msg,
        })
    return HttpResponse(t.render(c))

def add_sample_submission(request):
    print "adding a sample submission"
    alert_msg = ""
    print "this is request.POST in ss", request.POST
    samplesubmissionform = SampleSubmissionForm(request.POST)

    if samplesubmissionform.is_valid():
        samplesubmissionform.save()
        alert_msg = "<div class=\"alert alert-success\"><b>Good Job!</b> You have successfully added a Sample Submission!</div>"
    else:
        alert_msg = '<div class="alert alert-error"><b>Uh Oh!</b> No Sample Submission was added. Invalid Form. </div>'

    samplesubmissionlist_all = SampleSubmission.objects.all().order_by('date_created')
    samplesubmissionform = SampleSubmissionForm() #unbound form, no associated data, empty form

    # it should return just the updated table
    fp = open('/Users/aw18/Project/ENV/DNAOrderApp/DNAOrderApp/order/templates/order/sample-submission-table.html')
    t = Template(fp.read())
    fp.close()
    c = Context({
            'samplesubmissionform': samplesubmissionform,
            'samplesubmissionlist_all':samplesubmissionlist_all,
            'alert_msg': alert_msg,
        })

    return HttpResponse(t.render(c))

def handle_sample_submission(request, action=None, id=None):
    print "in handle_sample_submission"
    if action == "DELETE":
        if id != None:
            return delete_sample_submission(id)
    elif action == "ADD":
        return add_sample_submission(request)
    else:
        return HttpResponse("Everything failed! - sample submission")



def delete_phenotype(id):
    print "deleting a phenotype"
    alert_msg = ""
    try:
        print "pkid ", id
        p = Phenotype.objects.get(pk=id)
        p.delete()
        print "Check phenotype table to see if it is deleted."

    except Phenotype.DoesNotExist, e:
        alert_msg = '<div class="alert alert-error"><b>Uh Oh! </b>',e.message,"</div>"
    except AssertionError, e:
        alert_msg = '<div class="alert alert-error"><b>Uh Oh! </b>',e.message," </div>"
    except KeyError, e:
        alert_msg = '<div class="alert alert-error"><b>Uh Oh! </b>',e.message," </div>"

    phenotypelist_all = Phenotype.objects.all().order_by('phenotype_name')
    print "phenotypelist_all",phenotypelist_all
    phenotypeform = PhenotypeForm() #unbound form, no associated data, empty form

    # it should return just the updated table
    fp = open('/Users/aw18/Project/ENV/DNAOrderApp/DNAOrderApp/order/templates/order/phenotype-table.html')
    t = Template(fp.read())
    fp.close()
    c = Context({
            'phenotypeform': phenotypeform,
            'phenotypelist_all':phenotypelist_all,
            'alert_msg': alert_msg,
        })
    return HttpResponse(t.render(c))

def add_phenotype(request):
    print "adding a phenotype"
    alert_msg = ""
    print "this is request.POST in phenotype", request.POST
    phenotypeform = PhenotypeForm(request.POST)

    if phenotypeform.is_valid():
        phenotypeform.save()
        alert_msg = "<div class=\"alert alert-success\"><b>Good Job!</b> You have successfully added a Phenotype!</div>"
    else:
        alert_msg = '<div class="alert alert-error"><b>Uh Oh!</b> No Phenotype was added. Invalid Form. </div>'

    phenotypelist_all = Phenotype.objects.all().order_by('phenotype_name')
    phenotypeform = PhenotypeForm() #unbound form, no associated data, empty form

    # it should return just the updated table
    fp = open('/Users/aw18/Project/ENV/DNAOrderApp/DNAOrderApp/order/templates/order/phenotype-table.html')
    t = Template(fp.read())
    fp.close()
    c = Context({
            'phenotypeform': phenotypeform,
            'phenotypelist_all':phenotypelist_all,
            'alert_msg': alert_msg,
        })

    return HttpResponse(t.render(c))

def handle_phenotype(request, action=None, id=None):
    print "in handle_phenotype"
    if action == "DELETE":
        print "deleting a phenotype"
        if id != None:
            return delete_phenotype(id)
    elif action == "ADD":
        return add_phenotype(request)
    else:
        return HttpResponse("Everything failed! - phenotype")


# USERS ARE INTERESTING AND HARD AND MIGHT NOT BE HIGH PRIORITY - DO THIS AFTER PHENOTYPES??????

def delete_user(id):
    print "deleting a user"
    alert_msg = ""
    try:
        print "pkid ", id
        u = User.objects.get(pk=id)
        u.delete()
        print "Check user table to see if it is deleted."

    except User.DoesNotExist, e:
        alert_msg = '<div class="alert alert-error"><b>Uh Oh! </b>',e.message,"</div>"
    except AssertionError, e:
        alert_msg = '<div class="alert alert-error"><b>Uh Oh! </b>',e.message," </div>"
    except KeyError, e:
        alert_msg = '<div class="alert alert-error"><b>Uh Oh! </b>',e.message," </div>"

    userlist_all = User.objects.all().order_by('project_name')
    userform = UserForm() #unbound form, no associated data, empty form

    # it should return just the updated table
    fp = open('/Users/aw18/Project/ENV/DNAOrderApp/DNAOrderApp/order/templates/order/user-table.html')
    t = Template(fp.read())
    fp.close()
    c = Context({
            'userform': userform,
            'userlist_all': userlist_all,
            'alert_msg': alert_msg,
        })
    return HttpResponse(t.render(c))

from django.contrib.auth.forms import UserCreationForm

def add_user(request):
    print "adding a user"
    alert_msg = ""
    print "this is request.POST in user", request.POST
    userform = UserForm(request.POST)
    userform2 = UserCreationForm(request.POST)

    if userform.is_valid():
        userform.save()
        alert_msg = "<div class=\"alert alert-success\"><b>Good Job!</b> You have successfully added a User!</div>"
    else:
        alert_msg = '<div class="alert alert-error"><b>Uh Oh!</b> No User was added. Invalid Form. </div>'


    if userform2.is_valid():
        userform2.save()
        alert_msg = "<div class=\"alert alert-success\"><b>Good Job!</b> You have successfully added a User!</div>"
    else:
        alert_msg = '<div class="alert alert-error"><b>Uh Oh!</b> No User was added. Invalid Form. </div>'

    userlist_all = User.objects.all().order_by('date_created')
    userform = UserForm() #unbound form, no associated data, empty form
    userform2 = UserCreationForm()

    # it should return just the updated table
    fp = open('/Users/aw18/Project/ENV/DNAOrderApp/DNAOrderApp/order/templates/order/user-table.html')
    t = Template(fp.read())
    fp.close()
    c = Context({
            'userform2': userform2,
            'userlist_all':userlist_all,
            'alert_msg': alert_msg,
        })

    return HttpResponse(t.render(c))

def handle_user(request, action=None, id=None):
    print "in handle_user"
    if action == "DELETE":
        if id != None:
            return delete_user(id)
    elif action == "ADD":
        return add_user(request)
    else:
        return HttpResponse("Everything failed! - user")


# RENDER THE ADMIN PAGE
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm, UserChangeForm, UserCreationForm, SetPasswordForm

def admin_page(request, table=None, pkid=None):
    print "in admin page 2"
    print "table: ", table
    print "pkid: ", pkid

    # CHECK IF USER HAS BEEN LOGGED IN
    if not request.user.is_authenticated():
        print request.user, "is not authenticated."
        return HttpResponseRedirect(reverse('failed_signin'))

    userprojectlist_all = UserProject.objects.all().order_by('project_name')
    userprojectform = UserProjectForm() #unbound form, no associated data, empty form

    samplesubmissionlist_all = SampleSubmission.objects.all().order_by('date_created')
    samplesubmissionform = SampleSubmissionForm() #unbound form, no associated data, empty form

    userlist_all = User.objects.all().order_by('username')
    userform = UserForm() #unbound form, no associated data, empty form

    dnaorderappuserform = DNAOrderAppUserForm()

    phenotypelist_all = Phenotype.objects.all().order_by('phenotype_name')
    phenotypeform = PhenotypeForm() #unbound form, no associated data, empty form

    #FOR DEMO PURPOSES, INITIALIZE WITH PHENOTYPE TYPE FILLED
    if not PhenotypeType.objects.all():
        p1 = PhenotypeType(phenotype_type="AffectionStatus")
        p2 = PhenotypeType(phenotype_type="Qualitative")
        p3 = PhenotypeType(phenotype_type="Quantitative")

        p1.save()
        p2.save()
        p3.save()


    ucf = UserCreationForm()

    return render(request, 'order/admin-page.html', {
            'userprojectform': userprojectform,
            'userprojectlist_all': userprojectlist_all,
            'samplesubmissionlist_all': samplesubmissionlist_all,
            'samplesubmissionform': samplesubmissionform,
            'userlist_all': userlist_all,
            'userform': userform,
            'phenotypeform': phenotypeform,
            'phenotypelist_all':phenotypelist_all,
            'dnaorderappuserform' : dnaorderappuserform,

            'ucf': ucf,
           
        })

# OLD STUFF


def project_list(request):
    print "inside project list"

    # CHECK IF USER HAS BEEN LOGGED IN
    if not request.user.is_authenticated():
        print request.user, "is not authenticated."
        return HttpResponseRedirect(reverse('failed_signin'))

    if request.method == 'DELETE':
        print "deleting a project"
        pkid = request.session[CONST_DELETE_PROJECT]
        print "pkid ", pkid
        u = UserProject.objects.get(pk=pkid)
        u.delete()
        print "Check userproject table to see if it is deleted."

    elif request.method == 'POST':
        userprojectform = UserProjectForm(request.POST)
        print "this is userprojectform", userprojectform

        if userprojectform.is_valid():
            userprojectform.save()
            print "Check userproject table to see if it has been saved properly."

            userprojectlist_all = UserProject.objects.all().order_by('project_name')

            #ASSUMING SOMEHOW I KNOW WHO I AM - faculty member
            # userprojectlist_user = UserProject.objects.filter(username_id=2)

            return userprojectform, userprojectlist_all

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
    # userprojectlist_user = UserProject.objects.filter(username_id=3)

    # userproject = UserProject()
    # print userproject
    return userprojectform, userprojectlist_all



# previous


def get_projectlist(user):
    return UserProject.objects.filter(username__username__exact=user)

# def get_phenolist_render_phenotable(request, ss):
#     print ss
#     print "inside get_phenolist"
#     phenotypelist_all = Phenotype.objects.filter(samplesubmission__sample_submission_name__exact=ss)
#     print "phenotypelist_all: ", phenotypelist_all

#     # it should return just the updated table
#     fp = open('/Users/aw18/Project/ENV/DNAOrderApp/DNAOrderApp/order/templates/order/phenotype-table.html')
#     t = Template(fp.read())
#     fp.close()
#     c = Context({
#             'phenotypelist_all':phenotypelist_all,
#         })

#     return HttpResponse(t.render(c))

# def get_top3phenolist(request, ss):
#     phenotypelist_all = Phenotype.objects.filter(samplesubmission__sample_submission_name__exact=ss)

#     fp = open('/Users/aw18/Project/ENV/DNAOrderApp/DNAOrderApp/order/templates/order/top3phenolist.html')
#     t = Template(fp.read())
#     fp.close()
#     c = Context({
#             'phenotypelist_all': phenotypelist_all,
#         })

#     return HttpResponse(t.render(c))

# def get_phenolist(request, proj_name):
#     ss_list = SampleSubmission.objects.filter(project_name__project_name__exact=proj_name)
    
#     ss_pheno_dict={}
#     for ss in ss_list:
#         ss_pheno_dict[ss] = ss.phenotype_list.all()

#     fp = open('/Users/aw18/Project/ENV/DNAOrderApp/DNAOrderApp/order/templates/order/top3phenolist.html')
#     t = Template(fp.read())
#     fp.close()
#     c = Context({
#             'ss_pheno_dict': ss_pheno_dict,
#         })
#     print ss_pheno_dict

#     return HttpResponse(t.render(c))

def get_phenolist_cp(proj_name):
    ss_list = SampleSubmission.objects.filter(project_name__project_name__exact=proj_name)
    
    ss_pheno_dict={}
    for ss in ss_list:
        ss_pheno_dict[ss] = ss.phenotype_list.all()

    print ss_pheno_dict
    return ss_pheno_dict


def add_phenotype_fmpage(request, id):
    print "adding a phenotype fmpage"
    print "id ", id
    alert_msg = ""
    print "this is request.POST in phenotype", request.POST
    phenotypeform = PhenotypeForm(request.POST)

    if phenotypeform.is_valid():
        print "in phenotypeform"
        p1 = phenotypeform.save()
        print "p1 is saved"
        ss = SampleSubmission.objects.get(pk=id)
        print "ss is called"
        ss.phenotype_list.add(p1)
        ss_name = ss.sample_submission_name

        print "check sample submission and phenotypes to see updates"

        alert_msg = "<div class=\"alert alert-success\"><b>Good Job!</b> You have successfully added a Phenotype!</div>"
    else:
        print "in else"
        alert_msg = '<div class="alert alert-error"><b>Uh Oh!</b> No Phenotype was added. Invalid Form. </div>'
        ss_name = ""

    phenotypelist_all = Phenotype.objects.filter(samplesubmission__pk__exact=id)
    # phenotypelist_all = Phenotype.objects.all().order_by('phenotype_name')
    phenotypeform = PhenotypeForm() #unbound form, no associated data, empty form

    # it should return just the updated table
    fp = open('/Users/aw18/Project/ENV/DNAOrderApp/DNAOrderApp/order/templates/order/phenotype-table-fmpage.html')
    t = Template(fp.read())
    fp.close()
    c = Context({
            'phenotypelist_all':phenotypelist_all,
            'alert_msg': alert_msg,
            'ssid' : id,
            'ss_name' : ss_name
        })

    return HttpResponse(t.render(c))

def render_phenoform(request, id=None):
    print "in render_phenoform with id, ", id
    phenotypeform = PhenotypeForm()

    return render_to_response('/Users/aw18/Project/ENV/DNAOrderApp/DNAOrderApp/order/templates/order/phenoform.html', { 'phenotypeform':phenotypeform, 'ssid':id} ,context_instance=RequestContext(request))

def handle_phenotype_fmpage(request, action=None, id=None):
    print "in handle_phenotype_fmpage"
    if action == "DELETE":
        print "deleting a phenotype"
        if id != None:
            return delete_phenotype(id)
    elif action == "ADD":
        return add_phenotype_fmpage(request, id)
    else:
        return HttpResponse("Everything failed! - phenotype")

def add_project_fmpage(request):
    print "adding a project - inside add project fmproject"
    alert_msg = ""
    print "tis is request.POST in add_project:", request.POST
    userprojectform = UserProjectForm(request.POST)

    if userprojectform.is_valid():
        userprojectform.save()
        print "this is request.user", request.user

        print "Check userproject table to see if it has been saved properly."
        print "Successfully added a project"
        alert_msg = "<div class=\"alert alert-success\"><b>Good Job!</b> You have successfully added a project!</div>"

    else:
        print "userproject not valid ", userprojectform, " ", userproject
        print e
        alert_msg = '<div class="alert alert-error"><b>Uh Oh!</b> No project was added. Invalid Form. </div>'


    # Make a dictionary with Project as key, and sample submission as value
    projectlist = get_projectlist(request.user)
    print "PROJECTLIST:", projectlist

    ss_pheno_dict = {}
    proj_ss_dict = {}
    for project in projectlist:
        print "project: ", project, " samplesubmission: ", SampleSubmission.objects.filter(project_name__project_name__exact=project)
        proj_ss_dict[project] = SampleSubmission.objects.filter(project_name__project_name__exact=project)
        print "proj_ss_dict: ", proj_ss_dict
        ss_pheno_dict.update(get_phenolist_cp(project))

    #Phenotype
    phenotypeform = PhenotypeForm() #unbound form, no associated data, empty form

    #Project
    userprojectform = UserProjectForm_FM(initial={'username': request.user, 'project_name': "HELLO!"}) #unbound form, no associated data, empty form

    # it should return just the updated table
    fp = open('/Users/aw18/Project/ENV/DNAOrderApp/DNAOrderApp/order/templates/order/project-table-fmpage.html')
    print "fp:" ,fp
    t1 = fp.read()
    print "template", t1
    try:
        t = Template(t1)
    except Exception as e:
        print e.message
    print "after Template"
    fp.close()
    c = Context({
            'username' : request.user,
            'myprojectlist' : projectlist,
            'proj_ss_dict' : proj_ss_dict,
            'phenotypeform' : phenotypeform,
            'ss_pheno_dict' : ss_pheno_dict,
            'userprojectform' : userprojectform,
            'alert_msg': alert_msg,
        })
    print HttpResponse(t.render(c))
    return HttpResponse(t.render(c))
        

def handle_project_fmpage(request, action=None, id=None):
    print "in handle_project_fmpage"
    if action == "DELETE":
        if id != None:
            pass
            # return delete_project(id)
    elif action == "ADD":
        print "adding a project"
        return add_project_fmpage(request)
    else:
        return HttpResponse("Everything failed! - handle project")

def fm_page(request):

    # CHECK IF USER HAS BEEN LOGGED IN
    if not request.user.is_authenticated():
        print request.user, "is not authenticated."
        return HttpResponseRedirect(reverse('failed_signin'))

    # Make a dictionary with Project as key, and sample submission as value
    projectlist = get_projectlist(request.user)
    print "PROJECTLIST:", projectlist

    ss_pheno_dict = {}
    proj_ss_dict = {}
    for project in projectlist:
        print "project: ", project, " samplesubmission: ", SampleSubmission.objects.filter(project_name__project_name__exact=project)
        proj_ss_dict[project] = SampleSubmission.objects.filter(project_name__project_name__exact=project)
        print "proj_ss_dict: ", proj_ss_dict
        ss_pheno_dict.update(get_phenolist_cp(project))

    #Phenotype
    phenotypeform = PhenotypeForm() #unbound form, no associated data, empty form

    #Project
    print "this is request.user", request.user
    userprojectform = UserProjectForm_FM(initial={'username': request.user}) #unbound form, no associated data, empty form

    #Sample Submission form
    samplesubmissionform = SampleSubmissionForm() #unbound form, no associated data, empty form

    #Contact list
    contact_list = DNAOrderAppUser.objects.all()

    #Affiliated Institute List
    affiliated_institute_list = AffiliatedInstitute.objects.all()
    print "this is affiliated_institute list", affiliated_institute_list


#---------------------------------------------------------------------------------------------
    # # What are my projects?
    # myprojectlist = get_projectlist(request.user)

    # for project in myprojectlist:
    #     print project

    # # What are the Sample Submissions for each of the projects?
    # ss_for_each_project_dict = {}
    # for project in myprojectlist:
    #     ss_for_each_project_dict[project] = []
    #     ss_for_each_project_dict[project].append(SampleSubmission.objects.filter(project_name__project_name__exact=project))
    #     print "ss_for_each_project: ",ss_for_each_project

    # # What are the Phenotypes associated with each Sample Submission
    # # Phenotype.objects.filter(samplesubmission__sample_submission_name__exact='HELLO')
#----------------------------------------------------------------------------------------------



    #     #Extract Username
    #     username = user.username
    #     print "username", username
    #     # User Project
    #     userproject = UserProject(pk=user.id)

    #     # Project Name
    #     projectname = userproject.project_name
    #     print "projectname", projectname
    #     #Created on
    #     datecreated = userproject.date_created

    #     #Last updated
    #     lastupdated = userproject.last_updated
    #     #Project status
    #     projectstatus = userproject.project_status
    #     # Last logged in
    #     last_logged_in = user.last_login
    #     # Date Joined
    #     date_joined = user.date_joined

    # #Associated Sample submissions
    # SampleSubmission.objects.filter()
    # #Associated Phenotype list to each of the sample submissions

    # #Who is this sample submission for?

    return render(request, 'order/fmprojectlist.html', {
        'username' : request.user,
        'myprojectlist' : projectlist,
        'proj_ss_dict' : proj_ss_dict,
        'phenotypeform' : phenotypeform,
        'ss_pheno_dict' : ss_pheno_dict,
        'userprojectform' : userprojectform,
        'samplesubmissionform' : samplesubmissionform,
        'contact_list' : contact_list,
        'affiliated_institute_list' : affiliated_institute_list
        })

def collab_page(request):

    # Who requested it
    # Requested Sample Submissions

    return render(request, 'order/collab-page.html', {
        })

def lab_tech_page(request):
    return render(request, 'order/lab-tech-page.html', {
        })


# OLD STUFF

# def project_list(request):
#     print "inside project list"

#     # CHECK IF USER HAS BEEN LOGGED IN
#     if not request.user.is_authenticated():
#         print request.user, "is not authenticated."
#         return HttpResponseRedirect(reverse('failed_signin'))

#     if request.method == 'DELETE':
#         print "deleting a project"
#         pkid = request.session[CONST_DELETE_PROJECT]
#         print "pkid ", pkid
#         u = UserProject.objects.get(pk=pkid)
#         u.delete()
#         print "Check userproject table to see if it is deleted."

#     elif request.method == 'POST':
#         userprojectform = UserProjectForm(request.POST)
#         print "this is userprojectform", userprojectform

#         if userprojectform.is_valid():
#             userprojectform.save()
#             print "Check userproject table to see if it has been saved properly."

#             userprojectlist_all = UserProject.objects.all().order_by('project_name')

#             #ASSUMING SOMEHOW I KNOW WHO I AM - faculty member
#             # userprojectlist_user = UserProject.objects.filter(username_id=2)

#             return userprojectform, userprojectlist_all

#     else:
#         # FIRST COMING TO THE PROJECT PAGE
#         # CREATE DUMMY USERS HERE
#         from django.contrib.auth.models import User
#         if User.objects.filter(username='facultymember').count() == 0:
#             user = User.objects.create_user(username='facultymember', email='facultymember@sanger.ac.uk', password='fmpassword')
#             user.save()

#         # DUMMY PROJECT STATUS
#         # from DNAOrderApp.order.models import ProjectStatus
#         # if ProjectStatus.objects.all().count() == 0:
#         #     project_status = ProjectStatus(project_status='In Progress')
#         #     project_status.save()
#         #     project_status = ProjectStatus(project_status = 'Complete')
#         #     project_status.save()

#     userprojectform = UserProjectForm() #unbound form, no associated data, empty form
#     userprojectlist_all = UserProject.objects.all().order_by('project_name')
#     print "projectlistall: ", userprojectlist_all

#     #ASSUMING SOMEHOW I KNOW WHO I AM 
#     # userprojectlist_user = UserProject.objects.filter(username_id=3)

#     # userproject = UserProject()
#     # print userproject
#     return userprojectform, userprojectlist_all


# Sample Submission Page
def sample_submission_list(request):
    print "in sample_submission_list"

    # CHECK IF USER HAS LOGGED IN
    if not request.user.is_authenticated():
        print request.user, "is not authenticated."
        return HttpResponseRedirect(reverse('failed_signin'))

    if request.method == 'DELETE':
        print "deleting a sample_submission"
        print request
        pkid = request.session[CONST_DELETE_SAMPLE_SUBMISSION]
        print "pkid ", pkid
        s = SampleSubmission.objects.get(pk=pkid)
        s.delete()
        print "Check samplesubmission table to see if it is deleted."


    elif request.method == 'POST':
        sform = SampleSubmissionForm(request.POST)
        print "this is sform", sform

        if sform.is_valid():
            sform.save()
            print "Check Sample Submission table to see if it's been saved"
            sform_project_name = sform.cleaned_data['project_name']

            # sample_submission_list_user = SampleSubmission.objects.filter(project_name=sform_project_name)
            sample_submission_list_all = SampleSubmission.objects.all().order_by('project_name')


            return sform, sample_submission_list_all
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

    sform = SampleSubmissionForm()
    print "this is sform", sform
    sample_submission_list_all = SampleSubmission.objects.all().order_by('project_name')
    print "this is sample_submission_list", sample_submission_list_all


    return sform, sample_submission_list_all


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

            sucess_alert = '<div class="alert alert-success"> You have successfully added a phenotype! </div>'

            return phenotypeForm, success_alert, phenotypelist

        # ERROR ALERT FOR INVALID BOUND FORM
        print "phenotypeForm is bound but invalid"
        phenotypelist = Phenotype.objects.all().order_by('phenotype_name')

        try_again_alert = '<div class="alert alert-block"> Oops! Try again - phenotype was not added. </div>'

        return phenotypeForm, try_again_alert, phenotypelist

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
    fill_in_alert = '<div class="alert alert-info"> Fill in the following form to add a phenotype. </div>'

    return phenotypeForm, fill_in_alert, phenotypelist

    def __unicode__(self):
        return self.sample_submission_name


def basic_http_auth_dnaorderappuser(f):
    def wrap(request, *args, **kwargs):
        if request.META.get('HTTP_AUTHORIZATION', False):
            authtype, auth = request.META['HTTP_AUTHORIZATION'].split(' ')
            auth = base64.b64decode(auth)
            username, password = auth.split(':')
            dnaorderappuser = authenticate(username=username, password=password)
            if dnaorderappuser is not None:
                print "dnaorderappuser.is_active", dnaorderappuser.is_active
                if dnaorderappuser.is_active:
                    #attaches the authenticated user to current session, saves userid in session.
                    login(request,dnaorderappuser)
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


# def basic_http_auth(f):
#     def wrap(request, *args, **kwargs):
#         if request.META.get('HTTP_AUTHORIZATION', False):
#             authtype, auth = request.META['HTTP_AUTHORIZATION'].split(' ')
#             auth = base64.b64decode(auth)
#             username, password = auth.split(':')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 print "user.is_active", user.is_active
#                 if user.is_active:
#                     #attaches the authenticated user to current session, saves userid in session.
#                     login(request,user)
#                     print "get_user:", get_user(request)
                    
#                     #Successful login
#                     return f(request, *args, **kwargs)
#                 else:
#                     #Return a 'disabled account' error message
#                     print "disabled account error message"

#             else:
#                 # Return an 'invalid login' error message
#                 print "User does not exist"
#                 r = HttpResponse("Auth Required", status = 401)
#                 r['WWW-Authenticate'] = 'Basic realm="bat"'
#                 return r
#         print "HTTP_AUTHORIZATION CANNOT BE FOUND IN request.META"
#         r = HttpResponse("Auth Required", status = 401)
#         r['WWW-Authenticate'] = 'Basic realm="bat"'
#         return r
        
#     return wrap

# @basic_http_auth
@basic_http_auth_dnaorderappuser
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