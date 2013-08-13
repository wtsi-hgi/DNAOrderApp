from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.files import File

from django.contrib.auth import login, authenticate, get_user
from django.contrib.auth.models import User

from DNAOrderApp.order.models import Document, Sample, Study, Display, Phenotype, SampleSubmission, TempSSAffiliatedInstituteForm
from DNAOrderApp.order.models import UserProject, AffiliatedInstitute, PhenotypeType, DNAOrderAppUser, TempSSAffiliatedInstitute
from DNAOrderApp.order.models import TempSSDNAOrderAppUser, TempSSDNAOrderAppUserForm

from DNAOrderApp.order.models import PhenotypeForm, SampleSubmissionForm, UserProjectForm, UserForm, UserProjectForm_FM, TempSSPhenotype
from DNAOrderApp.order.models import DNAOrderAppUserForm, AffiliatedInstituteForm, TempSampleSubmissionForm, TempSampleSubmission, TempSSPhenotypeForm
from DNAOrderApp.order.forms import DocumentForm

from django.contrib import messages
from django.db import IntegrityError, DatabaseError, transaction
from django.core.exceptions import ObjectDoesNotExist
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


def add_dnaorderappuser(request):
    print "adding dnaorderappuser"
    alert_msg = ""
    dnaorderappuserform = DNAOrderAppUserForm(request.POST)

    if dnaorderappuserform.is_valid():
        print "is valid"
        dnaorderappuserform.save()
        alert_msg = "<div class=\"alert alert-success\"><b>Good Job!</b> You have successfully added a DNA Order App User!</div>"
    else:
        print "is not valid"
        alert_msg = '<div class="alert alert-error"><b>Uh Oh!</b> No DNA Order App User was added. Invalid Form. </div>'

    dnaorderappuserlist_all = DNAOrderAppUser.objects.all().order_by('date_joined')
    dnaorderappuserform = DNAOrderAppUserForm()

    # it should return just the updated table
    fp = open('/Users/aw18/Project/ENV/DNAOrderApp/DNAOrderApp/order/templates/order/dnaorderappuser-table.html')
    t = Template(fp.read())
    fp.close()
    c = Context({
            'dnaorderappuserform': dnaorderappuserform,
            'dnaorderappuserlist_all': dnaorderappuserlist_all,
            'alert_msg': alert_msg,
        })

    return HttpResponse(t.render(c))


def handle_dnaorderappuser(request, action=None, id=None):
    print "in handle dnaorderappuser"
    if action == "DELETE":
        print "in delete dnaorderappuser"
    elif action == "ADD":
        return add_dnaorderappuser(request)
    else:
        return HttpResponse("Everything failed! - dnaorderappuser")


def add_affiliated_institute(request):
    print "add affiliated institute"
    aif = AffiliatedInstituteForm(request.POST)

    if aif.is_valid():
        aif.save()
        alert_msg = "<div class=\"alert alert-success\"><b>Good Job!</b> You have successfully added an Affiliated Institute!</div>"
    else:
        alert_msg = '<div class="alert alert-error"><b>Uh Oh!</b> No Affiliated Institute was added. Invalid Form. </div>'

    ailist_all = AffiliatedInstitute.objects.all().order_by('ai_name')
    aif = AffiliatedInstituteForm()

    # it should return just the updated table
    fp = open('/Users/aw18/Project/ENV/DNAOrderApp/DNAOrderApp/order/templates/order/ai-table.html')
    t = Template(fp.read())
    fp.close()
    c = Context({
            'aif': aif,
            'ailist_all': ailist_all,
            'alert_msg': alert_msg,
        })

    return HttpResponse(t.render(c))


def handle_affiliated_institute(request, action=None):
    print "affiliated institute"
    if action == "ADD":
        return add_affiliated_institute(request)
    else:
        return HttpResponse("Everything failed! - affiliated institute")

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
    aif = AffiliatedInstituteForm()

    ailist_all = AffiliatedInstitute.objects.all().order_by('ai_name')

    # EXPERIMENTING FORMSETS 
    # from django.forms.formsets import formset_factory
    # PhenotypeFormSet = formset_factory(PhenotypeForm, extra=2)
    # formset = PhenotypeFormSet(initial=[
    #     {'phenotype_name': 'Monkeys',
    #     'phenotype_description': 'hello world',
    #     }
    # ])

    # print "this is formset", formset

    # EXPERIMENTING MODEL FORMSETS
    # from django.forms.models import modelformset_factory
    # PhenotypeFormSet = modelformset_factory(Phenotype, can_delete=True)

    # formset = PhenotypeFormSet(queryset=Phenotype.objects.none())
    # print "this is phenotypeformset ", formset


    # EXPERIMENTING WITH INLINE FORMSETS
   

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
            'aif' : aif,
            'ailist_all' : ailist_all,
            # 'PhenotypeFormSet' : formset,

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

def handle_ai_fmpage(request, action=None, id=None):
    print "in handle_ai_fmpage"
    if action == "DELETE":
        print "deleting an AI"
        if id != None:
            return delete_ai_fmpage(id)
    elif action == "ADD":
        return add_ai_fmpage(request)
    else:
        return HttpResponse("Everything failed! - phenotype")


def add_ai_fmpage(request):
    '''
    When you see the AI displayed on the label, this hasn't been associated with 
    the sample submission yet. To be associated you need to create the entire 
    sample submission first. Clicking the save button will only save the existence
    of this affiliated institute.
    '''
    print "inside add_ai_fmpage"
    alert_msg = ""
    print "this is request.POST in ai", request.POST
    aiform = AffiliatedInstituteForm(request.POST)

    if aiform.is_valid():
        print "in if"
        ai = aiform.save()
        print 'this is ai', ai.ai_name, ai.ai_description
        alert_msg = "<div class=\"alert alert-success\"><b>Good Job!</b> You have successfully added an Affiliated Institute!</div>"
        ai_name = ai.ai_name
        ai_description = ai.ai_description

        fp = open('/Users/aw18/Project/ENV/DNAOrderApp/DNAOrderApp/order/templates/order/ai-label-fmpage.html')
        t = Template(fp.read())
        fp.close()
        c = Context({
            'alert_msg': alert_msg,
            'ai_name' : ai_name,
            'ai_description': ai_description
        })

    else:
        print "in else"
        alert_msg = '<div class="alert alert-error"><b>Uh Oh!</b> No Affiliated Institute was added. Invalid Form. </div>'
        aiform = AffiliatedInstituteForm()

        fp = open('/Users/aw18/Project/ENV/DNAOrderApp/DNAOrderApp/order/templates/order/ai-label-fmpage.html')
        t = Template(fp.read())
        fp.close()
        c = Context({
            'alert_msg': alert_msg,
            'aiform' : aiform
        })

    return HttpResponse(t.render(c))


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


def edit_tss_page_5(request, action=None, tssid=None, ssid=None):
    print "in edit tss page 5"
    if action == 'FINAL_SUBMIT':
        print "in final submit"
    else:
        print "in the else - edit tss page 5"
        # First time webpage is called using GET
        try:
            tss = TempSampleSubmission.objects.get(pk=tssid)
            tssphenolist_all = TempSSPhenotype.objects.filter(tmp_ss=tss)
            tssai = TempSSAffiliatedInstitute.objects.get(tmp_ss=tss)
            tssdnaorderappuserlist_all = DNAOrderAppUser.objects.filter(tempssdnaorderappuser__tmp_ss__id=tssid)
        except ObjectDoesNotExist:
            # If some forms are incomplete
            print "Incomplete forms ", ex.message
            alert_msg = "<div class=\"alert alert-error\"><b>Incomplete Forms!</b> Please go back and complete them.</div>"
            fp = open('/Users/aw18/Project/ENV/DNAOrderApp/DNAOrderApp/order/templates/order/edit-tmp-sample-submission-4.html')
            t = Template(fp.read())
            fp.close()
            tempuserlist_all = DNAOrderAppUser.objects.filter(tempssdnaorderappuser__tmp_ss__id=tssid)
            tssuserform = TempSSDNAOrderAppUserForm()
            c = Context({
                            'alert_msg': alert_msg,
                            'tssid' : tssid,
                            'tempuserlist_all': tempuserlist_all,
                            'tssuserform': tssuserform
            })
            return HttpResponse(t.render(c))


    return render(request, 'order/edit-tmp-sample-submission-5.html', {
        'tss' : tss,
        'tssphenolist_all' : tssphenolist_all,
        'tssai' : tssai,
        'tssdnaorderappuserlist_all' : tssdnaorderappuserlist_all,
        'tssid' : tssid,
        'ssid' : ssid
        })


def tss_page_5(request, action=None, tssid=None):
    print "in tss page 5"
    print "tssid", tssid
    if action == 'FINAL_SUBMIT':
        # Submit everything from temporary database to actual database
        # Display the new row in the main page with the information
        print "in post - tss page 5"
        ss = SampleSubmission()

        # Setting up all the objects needed
        tss = TempSampleSubmission.objects.get(pk=tssid)
        tssphenolist_all = TempSSPhenotype.objects.filter(tmp_ss=tss)
        tssai = TempSSAffiliatedInstitute.objects.get(tmp_ss=tss)
        tssdnaorderappuserlist_all = DNAOrderAppUser.objects.filter(tempssdnaorderappuser__tmp_ss__id=tssid)

        print "TYPE TSSAI TMP AI NAME", "ai_name = '" + tssai.tmp_ai_name +"'"
        try:
            ai = AffiliatedInstitute.objects.get(ai_name=tssai.tmp_ai_name)
            print ai 
        except ObjectDoesNotExist:
            # Creating the associated affiliated institute object (foreign key)
            #if affiliated institute does not exist in the database
            print "in not ai - tss page 5"
            ai = AffiliatedInstitute()
            ai.ai_name = tssai.tmp_ai_name 
            ai.ai_description = tssai.tmp_ai_description
            ai.save()

        ss.affiliated_institute = ai

        try:
            up = UserProject.objects.get(project_name=tss.tmp_project_name)
        except ObjectDoesNotExist:
            # Foreign key project_name
            up = UserProject()
            up.username = DNAOrderAppUser.objects.get(username=request.user)
            up.project_name = tss.tmp_project_name
            up.save()

        ss.project_name = up

        try:
            ss.sample_submission_name = tss.tmp_sample_submission_name
            ss.sample_num = tss.tmp_sample_num
        except IntegrityError as e:
            print "Integrity Error :", e

        # Need to save before adding to many to many relationships
        ss.save()

        # Many to Many relationship
        for tsspheno in tssphenolist_all:

            try: 
                pheno = Phenotype.objects.get(phenotype_name=tsspheno.tmp_phenotype_name, phenotype_type=tsspheno.tmp_phenotype_type)
            except ObjectDoesNotExist:
                pheno = Phenotype()
                pheno.phenotype_name = tsspheno.tmp_phenotype_name 
                pheno.phenotype_type = tsspheno.tmp_phenotype_type
                pheno.phenotype_description = tsspheno.tmp_phenotype_description
                pheno.phenotype_definition = tsspheno.tmp_phenotype_definition
                pheno.save()
            
            ss.phenotype_list.add(pheno)
            del pheno

        for tssuser in tssdnaorderappuserlist_all:
            ss.contact_list.add(tssuser)

        
        ss.save()
        print "Check Sample Submission to see if it is saved - tss page 5"
        print "Deleting the temporary rows"

        # Deleting all the associated temporary rows
        tss.delete() 
        tssphenolist_all.delete()
        tssai.delete()
        tssdnaorderappuserlist_all.delete()

        return HttpResponseRedirect(reverse("fmprojectlist"))


    else:
        print "in the else - tss page 5"
        # first time web page is being called or being called by GET method
        try:
            tss = TempSampleSubmission.objects.get(pk=tssid)
            tssphenolist_all = TempSSPhenotype.objects.filter(tmp_ss=tss)
            tssai = TempSSAffiliatedInstitute.objects.get(tmp_ss=tss)
            tssdnaorderappuserlist_all = DNAOrderAppUser.objects.filter(tempssdnaorderappuser__tmp_ss__id=tssid)
        except ObjectDoesNotExist, ex:
            # If some forms are incomplete
            print "Incomplete forms ", ex.message
            alert_msg = "<div class=\"alert alert-error\"><b>Incomplete Forms!</b> Please go back and complete them.</div>"
            fp = open('/Users/aw18/Project/ENV/DNAOrderApp/DNAOrderApp/order/templates/order/tmp-sample-submission-4.html')
            t = Template(fp.read())
            fp.close()
            tempuserlist_all = DNAOrderAppUser.objects.filter(tempssdnaorderappuser__tmp_ss__id=tssid)
            tssuserform = TempSSDNAOrderAppUserForm()
            c = Context({
                            'alert_msg': alert_msg,
                            'tssid' : tssid,
                            'tempuserlist_all': tempuserlist_all,
                            'tssuserform': tssuserform
            })
            return HttpResponse(t.render(c))
            


    return render(request, 'order/tmp-sample-submission-5.html', {
        'tss' : tss,
        'tssphenolist_all' : tssphenolist_all,
        'tssai' : tssai,
        'tssdnaorderappuserlist_all' : tssdnaorderappuserlist_all,
        'tssid' : tssid
        })

def tss_page_4(request, tssid=None):
    print "in tss page 4"
    # At present we don't know what the external collaborator's authentication system 
    # is going to be like. So we're ignoring the cases where we need to create the collab's user account.
    # Only caring about user that exists in the system already.

    if request.method == "POST":
        print "in post - tss page 4"
        tssuserform = TempSSDNAOrderAppUserForm(request.POST)

        if tssuserform.is_valid():
            try:
                tssuser = tssuserform.save(commit=False)
                tssuser.tmp_ss = TempSampleSubmission.objects.get(pk=tssid)
                tssuser.save()
                print "saved tssuser"
            except ObjectDoesNotExist:
                print "TempSampleSubmission does not exist"
            except Exception as e:
                print "General exception being thrown: ", e
        else:
            print "invalid form"
    else:
        #first time webpage is being called or from a GET method
        print "not in post - tss page 4"

    # tempuserlist_all = DNAOrderAppUser.objects.filter(tempssdnaorderappuser__tmp_ss__exact=tssid)
    # tempuserlist_all = DNAOrderAppUser.objects.filter(tempssdnaorderappuser__tmp_ss__tmp_project_name=tssid)
    tempuserlist_all = DNAOrderAppUser.objects.filter(tempssdnaorderappuser__tmp_ss__id=tssid)
    tssuserform = TempSSDNAOrderAppUserForm()

    return render(request, 'order/tmp-sample-submission-4.html', {
        'tssuserform' : tssuserform,
        'tempuserlist_all' : tempuserlist_all,
        'tssid' : tssid
        })


def tss_page_2(request, tssid=None):
    print "in tss page 2"
    if request.method == "POST":
        print "in post"
        tssphenoform = TempSSPhenotypeForm(request.POST)

        if tssphenoform.is_valid():
            try:
                tsspheno = tssphenoform.save(commit=False)
                tsspheno.tmp_ss = TempSampleSubmission.objects.get(pk=tssid)
                tsspheno.save()
                print "saved tsspheno"

            except ObjectDoesNotExist:
                print "TempSampleSubmission does not exist"
            except Exception as e:
                print "General exception being thrown: ", e
        else:
            print "invalid form"
    else:
        #first time webpage is being called or from a GET method
        print "not in post - tss page 2"
        print "tssid", tssid
        try:
            #if a tsspheno exist
            tsspheno_old = TempSSPhenotype.objects.get(pk=tssid)
            
            data = {    
                        'tmp_ss' : tsspheno_old.tmp_ss.id,
                        'tmp_phenotype_name': tsspheno_old.tmp_phenotype_name,
                        'tmp_phenotype_type': tsspheno_old.tmp_phenotype_type.id,
                        'tmp_phenotype_description': tsspheno_old.tmp_phenotype_description,
                        'tmp_phenotype_definition': tsspheno_old.tmp_phenotype_definition
                    }
            tssphenoform = TempSSPhenotypeForm(data)
            print "check if tssform is bound:", tssphenoform.is_bound
            print "check if tssform is valid: ", tssphenoform.is_valid()
            print tssphenoform.errors
        except ObjectDoesNotExist:
            if not tssid:
                print "FAIL - MEANING TEMP SAMPLE SUBMISSION DID NOT SAVE. impossible."
            #if tsspheno does not exist
            tssphenoform = TempSSPhenotypeForm()


    tempphenotypelist_all = TempSSPhenotype.objects.filter(tmp_ss__pk__exact=tssid)

    return render(request, 'order/tmp-sample-submission-2.html', {
        'tssphenoform': tssphenoform,
        'tssid' : tssid,
        'tempphenotypelist_all' : tempphenotypelist_all
        })

def tss_page_3(request, tssid=None):
    print "in tss page 3"

    if request.method == "POST":
        print "in post - tss page 3"
        
        #if tssai exists already and just want to update
        tss = TempSampleSubmission.objects.get(pk=tssid)
        print 'request.post', request.POST, ' ', request.POST['tmp_ai_name']
        print "hi",TempSSAffiliatedInstitute.objects.filter(tmp_ss=tss)
        print "hello",TempSSAffiliatedInstitute.objects.filter(tmp_ai_name=request.POST['tmp_ai_name'])
        instance = TempSSAffiliatedInstitute.objects.filter(tmp_ss=tss) or TempSSAffiliatedInstitute.objects.filter(tmp_ai_name=request.POST['tmp_ai_name'])
        if not instance:
            print "hello"
            tssaiform = TempSSAffiliatedInstituteForm(request.POST)
        else:
            print "in else"
            tssaiform = TempSSAffiliatedInstituteForm(data=request.POST, instance=instance[0])
        print "tssaiform? "
        
        if tssaiform.is_valid():
            try:
                tssai = tssaiform.save(commit=False)
                tss = TempSampleSubmission.objects.get(pk=tssid)
                tssai.tmp_ss = tss 
                tssai.save()
                print "in valid - tss page 3", tssai.id
                return HttpResponseRedirect(reverse('tss-page-4', args=[tssid]))
            except ObjectDoesNotExist:
                print "TempSampleSubmission does not exist"
            except Exception as e:
                print "General exception being thrown - tss page 3:", e
        else:
            print "invalid form", tssaiform.errors
            return HttpResponseRedirect(reverse('tss-page-4', args=[tssid]))
        
    else:
        #first time webpage is being called, using GET
        print "not in post - tss page 3"
        try:
            #if a tssai exist for tss
            tss = TempSampleSubmission.objects.get(pk=tssid)
            tssai_old = TempSSAffiliatedInstitute.objects.get(tmp_ss=tss)
            data = {    'tmp_ss': tssai_old.tmp_ss,
                        'tmp_ai_name': tssai_old.tmp_ai_name,
                        'tmp_ai_description': tssai_old.tmp_ai_description 
                    }
            tssaiform = TempSSAffiliatedInstituteForm(data) #instantiate it with a form, allows user to update
            print "check if tssaiform is bound:", tssaiform.is_bound
            print "check if tssaiform is valid: ", tssaiform.is_valid()
            print tssaiform.errors
        except ObjectDoesNotExist:
            tssaiform = TempSSAffiliatedInstituteForm() #unbound form, no associated data, empty form

    return render(request, 'order/tmp-sample-submission-3.html', {
        'tssid' : tssid,
        'tssaiform' : tssaiform
        })

def edit_tss_page_3(request, ssid=None, tssid=None):
    print "in edit tss page 3"

    if request.method == "POST":
        print "in the post - edit tss page 3"
        try:
            #if tssai exists already and just want to update
            tss = TempSampleSubmission.objects.get(pk=tssid)
            instance = TempSSAffiliatedInstitute.objects.get(tmp_ss=tss)
            tssaiform = TempSSAffiliatedInstituteForm(data=request.POST, instance=instance)
        except ObjectDoesNotExist:
            tssaiform = TempSSAffiliatedInstituteForm(request.POST)

        if tssaiform.is_valid():
            try:
                tssai = tssaiform.save(commit=False)
                tss = TempSampleSubmission.objects.get(pk=tssid)
                tssai.tmp_ss = tss
                tssai.save()
                return HttpResponseRedirect(reverse('edit-ss-fmpage', kwargs={'ssid':ssid, 'tssid':tss.id}))
                # return HttpResponseRedirect(reverse('edit-tss-page-4', kwargs={'ssid':ssid, 'tssid': tss.id}))
            except ObjectDoesNotExist:
                print "TempSampleSubmission does not exist"
            except Exception as e:
                print "General exception being thrown - edit tss page 3: ", e
        else:
            # If the form is invalid ie. missing fields, invalid inputs - should generate an alert message 
            # and stay on the form
            print "invalid form", tssaiform.errors
    else:
        #first time webpage is being called, using GET
        print "not in post - edit tss page 3"
        tss = TempSampleSubmission.objects.get(pk=tssid)
        tssai = TempSSAffiliatedInstitute.objects.get(tmp_ss=tss)
        tssaiform = TempSSAffiliatedInstituteForm(instance=tssai)

        # DEPRECATED!!!
        # ss = SampleSubmission.objects.get(pk=ssid)
        # tss = TempSampleSubmission.objects.get(pk=tssid)
        # data = {   
        #             'tmp_ss' : tss,
        #             'tmp_ai_name' : ss.affiliated_institute.ai_name, 
        #             'tmp_ai_description' : ss.affiliated_institute.ai_description
        # }
        # tssaiform = TempSSAffiliatedInstituteForm(data)
    return render(request, 'order/edit-tmp-sample-submission-3.html', {
        'tssid' : tssid,
        'ssid' : ssid,
        'tssaiform' : tssaiform
        })

def edit_tss_page_4(request, ssid=None, tssid=None):
    print "in edit tss page 4"

    if request.method == "POST":
        print "in post - edit tss page 4"
        tssuserform = TempSSDNAOrderAppUserForm(request.POST)

        if tssuserform.is_valid():
            try:
                tssuser = tssuserform.save(commit=False)
                tssuser.tmp_ss = TempSampleSubmission.objects.get(pk=tssid)
                tssuser.save()
                print "saved tssuser"
            except ObjectDoesNotExist:
                print "TempSampleSubmission does not exist"
            except Exception as e:
                print "General exception being thrown: ", e
        else:
            print "invalid form"
    else:
        # first time webpage is being called or from a GET method
        print "in the else - edit tss page 4"
        pass
        
    tss = TempSampleSubmission.objects.get(pk=tssid)
    tssuserlist = DNAOrderAppUser.objects.filter(tempssdnaorderappuser__tmp_ss__exact=tss)
    tssuserform = TempSSDNAOrderAppUserForm()

        # Taking the contact list from existing sample submission and created tempssdnaorderappuser
    #     ss = SampleSubmission.objects.get(pk=ssid)
    #     for user in ss.contact_list.all():
    #         tssuser = TempSSDNAOrderAppUser()
    #         tssuser.tmp_ss = tss
    #         tssuser.tmp_dnaorderappuser = user

    # ss = SampleSubmission.objects.get(pk=ssid)
    # tempuserlist_all = ss.contact_list.all()

    # tssuserform = TempSSDNAOrderAppUserForm()

    return render(request, 'order/edit-tmp-sample-submission-4.html', {
        'tssuserform' : tssuserform,
        'tssuserlist' : tssuserlist,
        'tssid' : tssid,
        'ssid' : ssid
        })

def edit_tss_page_2(request, ssid=None, tssid=None):
    print "in edit tss page 2"
    if request.method == "POST":
        print "in the post - edit tss page 2"
        tssphenoform = TempSSPhenotypeForm(request.POST)

        if tssphenoform.is_valid():
            try:
                print "in try"
                tsspheno = tssphenoform.save(commit=False)
                tsspheno.tmp_ss = TempSampleSubmission.objects.get(pk=tssid)
                tsspheno.save()
            except ObjectDoesNotExist:
                print "TempSampleSubmission does not exist"
            except Exception as e:
                print "General exception being thrown: ", e
        else:
            print "invalid form"
    else:
        #first time webpage is being called or from a GET method
        # Creating temp phenotypes from existing sample submission's phenotype list
        print "not in post - edit tss page 2"
        pass

    try:
        tss = TempSampleSubmission.objects.get(pk=tssid)
        tssphenotypelist_all = TempSSPhenotype.objects.filter(tmp_ss=tss)
    except ObjectDoesNotExist:
        print "TempSampleSubmission does not exist!"
    
    tssphenoform = TempSSPhenotypeForm()

    # DEPRECATED!!!!!
    #     ss = SampleSubmission.objects.get(pk=ssid)
    #     tss = TempSampleSubmission.objects.get(pk=tssid)
        
    #     if not TempSSPhenotype.objects.filter(tmp_ss__pk__exact=tssid):
    #         for pheno in ss.phenotype_list.all():
    #             tsspheno = TempSSPhenotype()
    #             tsspheno.tmp_ss = tss 
    #             tsspheno.tmp_phenotype_name = pheno.phenotype_name
    #             tsspheno.tmp_phenotype_type = pheno.phenotype_type
    #             tsspheno.tmp_phenotype_description = pheno.phenotype_description
    #             tsspheno.tmp_phenotype_definition = pheno.phenotype_definition
    #             tsspheno.save()
    #             del tsspheno

    # tssphenoform = TempSSPhenotypeForm()
    # tempphenotypelist_all = TempSSPhenotype.objects.filter(tmp_ss__pk__exact=tssid)

    return render(request, 'order/edit-tmp-sample-submission-2.html', {
        'tssphenoform': tssphenoform,
        'tssid' : tssid,
        'ssid' : ssid,
        'tssphenotypelist_all' : tssphenotypelist_all
        })


def edit_tss_page_1(request, projid=None, ssid=None, tssid=None):
    # The idea is, using the sample temp format to change the existing sample submission.
    # I only need projid, not for samplesubmission but because TempSampleSubmissionForm needs it. 
    # After this point, I don't need it anymore. I only need ssid and tssid
    print "in edit tss page 1"
    print "ssid", ssid

    if request.method == "POST":
        print "in post - edit tss page 1"
        print 'tssid ', tssid
        print 'ssid ', ssid
        print 'projid ', projid
        # this creates a new TempSampleSubmission and allows user to modify the TempSampleSubmission
        try:
            print "in try - edit tss page 1"
            # proj = UserProject.objects.get(pk=projid)
            # instance = TempSampleSubmission.objects.get(tmp_project_name=proj)
            instance = TempSampleSubmission.objects.get(pk=tssid)
            print 'instance', instance
            tssform = TempSampleSubmissionForm(data=request.POST, instance=instance)
            print "after tssform request instance - edit tss page 1"
        except ObjectDoesNotExist:
            print "object does not exist - edit tss page 1"
            #if TempSampleSubmission does not exist...or project does not exist
            # using try-except statements as an 'if else' format is not the best practice, will change if time permits.
            tssform = TempSampleSubmissionForm(request.POST)

        if tssform.is_valid():
            try:
                print "in is valid"
                tss = tssform.save(commit=False)
                proj = UserProject.objects.get(pk=projid)
                tss.tmp_project_name = proj 
                tss.save()
                print "it's saved! ", tss
                print "ssid", ssid, "tssid ", tss.id
                return HttpResponseRedirect(reverse('edit-ss-fmpage', kwargs={'ssid':ssid, 'tssid':tss.id}))
            except ObjectDoesNotExist:
                print "User Project does not exist"
            except ValueError:
                print "Invalid tss form"
            except Exception as e:
                print "General exception being thrown: ", e
        else:
            print "invalid form", tssform.errors 
    else:
        print "in the else edit tss page 1"
        # Using try-except as an 'if-else' format. It's not best practice, will change if time permits.
        try:
            print "in the else - try"
            tss = TempSampleSubmission.objects.get(pk=tssid)
            print tss
            data = {    'tmp_project_name' : tss.tmp_project_name,
                        'tmp_sample_submission_name' : tss.tmp_sample_submission_name,
                        'tmp_sample_num' : tss.tmp_sample_num
            }
        except ObjectDoesNotExist:
            print "object does not exist"
            ss = SampleSubmission.objects.get(pk=ssid)
            data = {    'tmp_project_name' : ss.project_name,
                        'tmp_sample_submission_name' : ss.sample_submission_name,
                        'tmp_sample_num' : ss.sample_num
            }
        tssform = TempSampleSubmissionForm(data)
        print 'tssid ', tssid
        print 'ssid ', ssid
        print 'projid ', projid
        print 'tssform ', tssform

    return render(request, 'order/edit-tmp-sample-submission-1.html', {
        'tssform' : tssform,
        'projid' : projid,
        'ssid' : ssid,
        'tssid' : tssid
    })

def tss_page_1(request, projid=None):
    print "in tss page 1"
    print "this projid ", projid

    if request.method == "POST":
        print "in post?" #Allows user to modify 
        try:
            proj = UserProject.objects.get(pk=projid)
            instance = TempSampleSubmission.objects.get(tmp_project_name=proj)
            tssform = TempSampleSubmissionForm(data=request.POST, instance=instance)
            print "tss form?"
        except ObjectDoesNotExist:
            #If TempSampleSubmission does not exist
            print "tss did not exist yet, creating one"
            tssform = TempSampleSubmissionForm(request.POST)

        if tssform.is_valid():
            try:
                tss = tssform.save(commit=False)
                proj = UserProject.objects.get(pk=projid)
                tss.tmp_project_name = proj
                tss.tmp_add_flag = True
                tss.save()
                print "in valid", tss.id
                return HttpResponseRedirect(reverse('tss-page-2', args=[tss.id]))
            except ObjectDoesNotExist:
                print "User Project does not exist"
            except ValueError:
                print "Invalid tss form"
            except Exception as e:
                print "General exception being thrown: ", e
        else:
            print "invalid form", tssform.errors
            alert_msg = "<div class=\"alert alert-error\"><b>Please complete the form.</b></div>"
            return render(request, 'order/tmp-sample-submission-1.html', {
                            'tssform' : tssform,
                            'projid' : projid,
                            'alert_msg' : alert_msg
                    })
    else:
        print "not in post"

        try:
            # if Temporary sample submission already exists already
            proj = UserProject.objects.get(pk=projid)
            tss = TempSampleSubmission.objects.get(tmp_project_name=proj, tmp_add_flag=True)
            tssid = tss.id
            tssform = TempSampleSubmissionForm(instance=tss)
        except ObjectDoesNotExist:
            # else create a temporary sample submission, with the known project
            # first time webpage is being called, using GET
            tssform = TempSampleSubmissionForm()

        # if TempSampleSubmission.objects.filter(pk=tssid).count() == 0:
        #     # if no temporary sample submission exists, create one.
        # else:
        #     try:
        #         #if a tss exist for projid = (user, project), UserProject
        #         proj = UserProject.objects.get(pk=projid)
        #         tss_old = TempSampleSubmission.objects.get(tmp_project_name=proj) #if tss exists
        #         data = {    'tmp_project_name' : tss_old.tmp_project_name,
        #                     'tmp_sample_submission_name' : tss_old.tmp_sample_submission_name, 
        #                     'tmp_sample_num' : tss_old.tmp_sample_num }

        #         tssform = TempSampleSubmissionForm(data) #instantiate it with a form, allows user to update
        #         print "check if tssform is bound:", tssform.is_bound
        #         print "check if tssform is valid: ", tssform.is_valid()
        #         print tssform.errors
        #     except ObjectDoesNotExist:
        #         tssform = TempSampleSubmissionForm() #unbound form, no associated data, empty form
    return render(request, 'order/tmp-sample-submission-1.html', {
        'tssform' : tssform,
        'projid' : projid,
        'tssid' : tssid
        })


@transaction.commit_on_success
def edit_ss_fmpage(request, ssid=None, tssid=None):
    print 'in edit ss fmpage'
    print 'ssid', ssid, 'tssid', tssid

    if request.method == "POST":
        print "in the post - edit_ss_fmpage"

        # Idea is check if there's any changes, if there is, then update Sample Submission
        tss = TempSampleSubmission.objects.get(pk=tssid)
        print 'tss',tss
        tssai = TempSSAffiliatedInstitute.objects.get(tmp_ss=tss)
        print 'tssai', tssai
        tssuserlist = DNAOrderAppUser.objects.filter(tempssdnaorderappuser__tmp_ss__exact=tss)
        print 'tssuserlist', tssuserlist
        tssphenolist = TempSSPhenotype.objects.filter(tmp_ss=tss)
        print 'tssphenolist', tssphenolist

        ss = SampleSubmission.objects.get(pk=ssid)
        print 'ss', ss
        print 'ss project name before', ss.project_name
        ss.project_name = tss.tmp_project_name
        print 'ss project name after', ss.project_name
        print 'ss sample submission name before', ss.sample_submission_name
        ss.sample_submission_name = tss.tmp_sample_submission_name
        print 'ss sample submission name after', ss.sample_submission_name
        print 'ss sample num before', ss.sample_num
        ss.sample_num = tss.tmp_sample_num
        print 'ss sample num after', ss.sample_num
        print 'ss ai before', ss.affiliated_institute

        try:
            ai = AffiliatedInstitute.objects.get(ai_name=tssai.tmp_ai_name)
        except ObjectDoesNotExist:
            ai = AffiliatedInstitute()
            ai.ai_name = tssai.tmp_ai_name
            ai.ai_description = tssai.tmp_ai_description
            ai.save()

        ss.affiliated_institute = ai
        del ai
        print 'ss ai after', ss.affiliated_institute

        print 'ss contact list before', ss.contact_list
        # compare contact list
        newuser_list = list(set(tssuserlist) - set(ss.contact_list.all()))

        for nw in newuser_list:
            # User exists, because there's no way to create new users at the moment
            ss.contact_list.add(nw)
        print 'ss contact list after', ss.contact_list

        # You have the phenotype list from the sample submission
        # you have the tss list from tsspheno
        # Need to associate sample submission to the new phenotype from tsspheno
        # somehow make tss comparable to phenotypes, so then to create the new phenotypes and associate it to the present ss.
        # phenotype is unique by name and type
        # tempssphenotype is unique by name, ss, type
        # so compare name and type only
        psslist = ss.phenotype_list.all().values_list('phenotype_name', 'phenotype_type_id')
        print "after psslist"
        tptsslist = TempSSPhenotype.objects.filter(tmp_ss=tss).values_list('tmp_phenotype_name','tmp_phenotype_type')
        print "after tptsslist"
        newphenotype_list = list(set(tptsslist)-set(psslist))
        print "made a remaining list ", newphenotype_list

        for np in newphenotype_list:
            try:
                print "before temppsspheno"
                tempsspheno = TempSSPhenotype.objects.get(tmp_phenotype_name=np[0],tmp_phenotype_type=np[1])
                print "After tempsspheno"

                # Check if these phenotypes exist first, it just might not be associated with the present sample submission
                pheno = Phenotype.objects.get(phenotype_name=np[0],phenotype_type=np[1])
                print "after pheno is made"
                ss.phenotype_list.add(pheno)
                print "add to ss phenotype list"
            except TempSSPhenotype.DoesNotExist:
                print "TempSSPhenotype does not exist!"
            except Phenotype.DoesNotExist:
                print "in phenotype does not exist"
                pheno = Phenotype()
                pheno.phenotype_name = tempsspheno.tmp_phenotype_name
                pheno.phenotype_type = tempsspheno.tmp_phenotype_type
                pheno.phenotype_description = tempsspheno.tmp_phenotype_description
                pheno.phenotype_definition = tempsspheno.tmp_phenotype_definition
                pheno.save()
                ss.phenotype_list.add(pheno)
                print "add ss.phenotypelist"
                del pheno 
        
        print "before saving ss"
        ss.save()

        print "tssai before"
        tssai.delete()
        print "tssai after"
        print "tss phenolist before"
        tssphenolist.delete()
        print "tss phenolist after"
        print "tssdnaorderappuser before"
        TempSSDNAOrderAppUser.objects.filter(tmp_ss=tss).delete()
        print "tssdnaorderappuser after"
        print "tss before"
        tss.delete()
        print "tss after"
        
        return HttpResponseRedirect(reverse('fmprojectlist'))
    else:
        print "in the else - edit_ss_fmpage"
        # first time being called, GET
        ss = SampleSubmission.objects.get(pk=ssid)
        print "ss", ss

        # I'm using filter and count here because I didn't want to use get, which causes an ObjectDoesNotExist
        if TempSampleSubmission.objects.filter(pk=tssid).count() == 0:
            # No Temp Sample Submission made for this sample submission yet. So create all the 
            # associated temporary tables for it.
            print "tempss when 0"
            with transaction.commit_on_success():
                try:
                    # Some reason fmpage refreshes and 'Edit' is clicked, no tssid is provided in that scenario
                    # But its temporary sample submission has already been created.
                    tss = TempSampleSubmission.objects.get(tmp_sample_submission_name=ss.sample_submission_name)
                    tssid = tss.id
                except ObjectDoesNotExist:
                    print "before tss"
                    tss = TempSampleSubmission()
                    print "after tss"
                    tss.tmp_project_name = ss.project_name
                    print "after project name", ss.project_name, " and ", tss.tmp_project_name
                    tss.tmp_sample_submission_name = ss.sample_submission_name
                    print "after tssname"
                    tss.tmp_sample_num = ss.sample_num
                    print "after tss num"
                    print tss
                    tss.save()
                    print "saving !!!! "
                    tssid = tss.id
                    print "tssid", tssid

                # instantiate tsspheno
                tssphenolist = []
                for pheno in ss.phenotype_list.all():
                    try:
                        print "in try tsspheno"
                        tsspheno = TempSSPhenotype.objects.get(tmp_ss=tss, tmp_phenotype_name=pheno.phenotype_name, tmp_phenotype_type=pheno.phenotype_type)
                    except ObjectDoesNotExist:
                        print "in tsspheno doesnotexist"
                        tsspheno = TempSSPhenotype()
                        tsspheno.tmp_ss = tss 
                        tsspheno.tmp_phenotype_name = pheno.phenotype_name
                        tsspheno.tmp_phenotype_type = pheno.phenotype_type
                        tsspheno.tmp_phenotype_description = pheno.phenotype_description
                        tsspheno.tmp_phenotype_definition = pheno.phenotype_definition
                        tsspheno.save()
                    tssphenolist.append(tsspheno)
                    del tsspheno
                print "tsspheno after"

                # instantiate tempssaffiliatedinstitute 
                try:
                    print "in try tssai"
                    tssai = TempSSAffiliatedInstitute.objects.get(tmp_ss=tss)
                except ObjectDoesNotExist:
                    print "in tssai does not exist"
                    tssai = TempSSAffiliatedInstitute()
                    tssai.tmp_ss = tss 
                    tssai.tmp_ai_name = ss.affiliated_institute.ai_name
                    tssai.tmp_ai_description = ss.affiliated_institute.ai_description
                    tssai.save()
                print "after tssai"

                # instantitate tempssdnaorderappuser so to create a filled form
                tssuserlist = []
                for user in ss.contact_list.all():
                    try:
                        print "in tssdoauser in try"
                        tssdoauser = TempSSDNAOrderAppUser.objects.get(tmp_ss=tss, tmp_dnaorderappuser=user)
                    except ObjectDoesNotExist:
                        print "in tssodauser does not exist"
                        tssdoauser = TempSSDNAOrderAppUser()
                        tssdoauser.tmp_ss = tss 
                        tssdoauser.tmp_dnaorderappuser = user
                        tssdoauser.save()
                    tssuserlist.append(tssdoauser.tmp_dnaorderappuser)
                    del tssdoauser
                print "after tssusrlist"
        else:
            print "not 0"
            tss = TempSampleSubmission.objects.get(pk=tssid)
            tssid = tss.id
            tssphenolist = TempSSPhenotype.objects.filter(tmp_ss=tss)
            tssai = TempSSAffiliatedInstitute.objects.get(tmp_ss=tss)
            tssuserlist = DNAOrderAppUser.objects.filter(tempssdnaorderappuser__tmp_ss__exact=tss)

    return render(request, 'order/edit-ss-fmpage.html', {
        'tss' : tss,
        'tssai' : tssai,
        'tssphenolist' : tssphenolist,
        'tssuserlist' : tssuserlist,
        'ssid' : ssid,
        'tssid' : tssid
        })


def handle_tss_pages(request, action=None, projid=None, tssid=None):
    print "in handle_tss_pages"
    if action == "TSS1":
        print "TSS1 - sample submission name and desc"
        return tss_page_1(request, projid)
    elif action == "TSS2":
        print "TSS2 - phenotypes"
        return tss_page_2(request, tssid)
    elif action == "TSS3":
        print "TSS3 - affiliated institute"
        return tss_page_3(request, tssid)
    elif action == "TSS4":
        print "TSS4 - personnels"
        return tss_page_4(request)
    else:
        return HttpResponse("Everything failed! - phenotype")


def add_project_fmpage(request):
    print "adding a project - fmproject"

    if request.method == "POST":
        print "in post - fmproject"
        userprojectform = UserProjectForm(request.POST)
        if userprojectform.is_valid():
            userprojectform.save()
        else:
            print "invalid form - adding a project, errors :", userprojectform.errors
    else:
        print "not in post - adding a project - fmproject"

    # Make a dictionary with Project as key, and sample submission as value
    projectlist = get_projectlist(request.user)

    proj_ss_dict = {}
    ss_pheno_dict = {}
    for project in projectlist:
        proj_ss_dict[project] = SampleSubmission.objects.filter(project_name__project_name__exact=project)
        ss_pheno_dict.update(get_phenolist_cp(project))

    #Phenotype
    # phenotypeform = PhenotypeForm() #unbound form, no associated data, empty form

    #Project
    # userprojectform = UserProjectForm_FM(initial={'username': request.user, 'project_name': "HELLO!"}) #unbound form, no associated data, empty form

    # it should return just the updated table
    fp = open('/Users/aw18/Project/ENV/DNAOrderApp/DNAOrderApp/order/templates/order/project-table-fmpage.html')
    t1 = fp.read()
    try:
        t = Template(t1)
        fp.close()
    except Exception as e:
        print e.message
    c = Context({
            'username' : request.user,
            'proj_ss_dict' : proj_ss_dict,
            # 'phenotypeform' : phenotypeform,
            'ss_pheno_dict' : ss_pheno_dict,
            # 'userprojectform' : userprojectform,
        })
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


def add_contact_fmpage(request):
    print "in add_contact_fmpage"
    alert_msg = ""

    d = DNAOrderAppUser.objects.create_user(username="johnlennon",)




def handle_contact_fmpage(request, action=None, id=None):
    print "in handle_contact_fmpage"
    if action == "DELETE":
        if id != None:
            pass
    elif action == "ADD":
        print "adding a contact"
        return add_contact_fmpage(request)
    else:
        return HttpResponse("Everything failed - handle contact fmpage")


def get_contactlist_cp(proj_name):
    print "in get_contactlist_cp"
    ss_list = SampleSubmission.objects.filter(project_name__project_name__exact=proj_name)
    print "ss_list", ss_list

    ss_contacts_dict={}
    for ss in ss_list:
        username = [doauser.encode("utf8") for doauser in DNAOrderAppUser.objects.filter(samplesubmission__pk__exact=ss.id).values_list('username', flat=True)]
        print "username", username
        ss_contacts_dict[ss] = username

    return ss_contacts_dict

def fm_page(request):

    # CHECK IF USER HAS BEEN LOGGED IN
    if not request.user.is_authenticated():
        print request.user, "is not authenticated."
        return HttpResponseRedirect(reverse('failed_signin'))

    # Make a dictionary with Project as key, and sample submission as value
    projectlist = get_projectlist(request.user)
    print "PROJECTLIST:", projectlist

    ss_pheno_dict = {}
    ss_contacts_dict = {}
    proj_ss_dict = {}
    for project in projectlist:
        print "project: ", project, " samplesubmission: ", SampleSubmission.objects.filter(project_name__project_name__exact=project)
        proj_ss_dict[project] = SampleSubmission.objects.filter(project_name__project_name__exact=project)
        print "proj_ss_dict: ", proj_ss_dict
        ss_pheno_dict.update(get_phenolist_cp(project))
        ss_contacts_dict.update(get_contactlist_cp(project))
        print "ss_contacts_dict ", ss_contacts_dict

    #Phenotype
    phenotypeform = PhenotypeForm() #unbound form, no associated data, empty form

    #Project
    print "this is request.user", request.user
    userprojectform = UserProjectForm_FM(initial={'username': request.user}) #unbound form, no associated data, empty form

    #Contact list
    contact_list = DNAOrderAppUser.objects.all()

    #Sample Submission form
    samplesubmissionform = SampleSubmissionForm() #unbound form, no associated data, empty form



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
        'ss_contacts_dict' : ss_contacts_dict,
        'phenotypeform' : phenotypeform,
        'ss_pheno_dict' : ss_pheno_dict,
        'userprojectform' : userprojectform,
        'samplesubmissionform' : samplesubmissionform,
        'contact_list' : contact_list,
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