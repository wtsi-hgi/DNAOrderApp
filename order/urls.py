from django.conf.urls import patterns, url

from order import views

urlpatterns = patterns('',

    # Testing pages
    url(r'^test$', views.test, name='base_test'),
    # Login / Sign Up Page
    url(r'^$', views.login_signup_page, name='login_signup_page'),

# User Profile Page
    url(r'^user_profile$', views.user_profile, name='user_profile_page'),

# User Home Page, with the list of outgoing and incoming projects
    url(r'^user_home$', views.user_home, name='user_home'),

# POP-UP: Phenotype Selection Page
    url(r'^pheno_select$', views.pheno_select, name='pheno_select'),

# POP-UP: Choose the method that the wells will be filled: Manual or Robot?

# POP-UP ROBOT: Please Upload Mapping files
    # Will require an uploader and a parser, SHOWS UPLOADED FORMAT

# POP-UP UPLOADED FORMAT: Shows a table of the csv, vcf file.

# POP-UP MANUAL: Choose a Style you would like to work in, may CUSTOMIZE ORDER

# POP-UP CUSTOMIZE ORDER: A picture of the 96 wells and lets user specify order

# WELL-FILLING FORM
    url(r'^well_filling_form$', views.well_filling_form, name='well_filling_form')
)

"""
  url(r'^$', views.index, name='index'),
        url(r'^faculty_member$', views.faculty_member_page, name='faculty_member'),
        url(r'^upload_empty_manifest$', views.upload_empty_manifest, name='upload_empty_manifest'),
        url(r'^collaborator$', views.collaborator_page, name='collaborator'),
        url(r'^upload_result_page$', views.upload_result_page, name='upload_result_page'),
        url(r'^plate_fill_type$', views.plate_fill_type, name='plate_fill_type'),
        url(r'^plate_fill_order$', views.plate_fill_order, name='plate_fill_order'),
        url(r'^customized_plate_fill_order$', views.customized_plate_fill_order, name='customized_plate_fill_order'),
        url(r'^fill_wells$', views.fill_wells, name='fill_wells'),
        url(r'^time$', views.current_datetime, name='time')
"""
