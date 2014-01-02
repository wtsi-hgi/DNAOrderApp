# Copyright (c) 2013 Genome Research Ltd.
# 
# Author: Albertina Wong <aw18@sanger.ac.uk>
# 
# This file is part of DNAOrderApp.
# 
# DNAOrderApp is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation; either version 3 of the License, or (at your option) any
# later version.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls import patterns, url
from DNAOrderApp.order import views

urlpatterns = patterns('',

    # NEW REVAMPED SITE, ONE WEBPAGE PER USER

    # Faculty member page
    url(r'^fm-page$', views.fm_page, name='fmprojectlist'),

    # Admin page
    url(r'^admin-page/((?P<table>[^/]*)/(?P<pkid>\d*))?/?$', views.admin_page, name='admin-page'),
    url(r'^api/handle_project/(?P<action>\w+)/?(?P<id>\d+)?/?', views.handle_project, name='handle_project'),
    url(r'^api/handle_project_fmpage/(?P<action>\w+)/?(?P<id>\d+)?/?', views.handle_project_fmpage, name='handle_project_fmpage'),
    url(r'^api/handle_sample_submission/(?P<action>\w+)/?(?P<id>\d+)?/?', views.handle_sample_submission, name='handle_sample_submission'),
    url(r'^api/handle_user/(?P<action>\w+)/?(?P<id>\d+)?/?', views.handle_user, name='handle_user'),
    url(r'^api/handle_dnaorderappuser/(?P<action>\w+)/?(?P<id>\d+)?/?', views.handle_dnaorderappuser, name='handle_dnaorderappuser'),
    url(r'^api/handle_phenotype/(?P<action>\w+)/?(?P<id>\d+)?/?', views.handle_phenotype, name='handle_phenotype'),
    url(r'^api/handle_phenotype_fmpage/(?P<action>\w+)/?(?P<id>\d+)?/?', views.handle_phenotype_fmpage, name='handle_phenotype_fmpage'),
    url(r'^render_phenoform/?(?P<id>\d+)?/?$', views.render_phenoform, name='render_phenoform'),
    url(r'^api/handle_contact_fmpage/(?P<action>\w+)/?(?P<id>\d+)?/?', views.handle_contact_fmpage, name='handle_contact_fmpage'),
    url(r'^api/handle_ai_fmpage/(?P<action>\w+)/?(?P<id>\d+)?/?', views.handle_ai_fmpage, name='handle_ai_fmpage'),

    url(r'^api/handle_affiliated_institute/(?P<action>\w+)/?', views.handle_affiliated_institute, name='handle_affiliated_institute'),
    # url(r'^get_top3phenolist/(?P<ss>[\w ]+)/?$', views.get_top3phenolist, name='get_top3phenolist'),
    # url(r'^admin-page$', views.admin_page, name='admin-page'),
    # url(r'^admin-page/(?P<table>[^/]+)/(?P<pkid>\d+)/$', views.admin_page, name='admin-page-table-pkid'),

    # Temp SS page
    url(r'^handle_tss_pages/(?P<action>\w+)/?(?P<projid>\d+)?/?(?P<tssid>\d+)?/?$', views.handle_tss_pages, name="handle_tss_pages"), #next button
    url(r'^tss-page-1/(?P<projid>\d+)?/?$', views.tss_page_1, name='tss-page-1'), #sample name and sample num
    url(r'^tss-page-2/(?P<tssid>\d+)?/?$', views.tss_page_2, name='tss-page-2'), #phenotype list
    url(r'^tss-page-3/?(?P<tssid>\d+)?/?$', views.tss_page_3, name='tss-page-3'), #affiliated institute 
    url(r'^tss-page-4/(?P<tssid>\d+)?/?$', views.tss_page_4, name='tss-page-4'), #personnels
    url(r'^tss-page-5/(?P<tssid>\d+)?/?(?P<action>\w+)?/?$', views.tss_page_5, name='tss-page-5'), #summary

    url(r'^edit-tss-page-1/(?P<ssid>\d+)/(?P<projid>\w+)/?(?P<tssid>\d+)?$', views.edit_tss_page_1, name='edit-tss-page-1'), #edit sample name and sample num
    url(r'^edit-tss-page-2/(?P<ssid>\d+)/(?P<tssid>\d+)/?$', views.edit_tss_page_2, name='edit-tss-page-2'), # edit phenotype list
    url(r'^edit-tss-page-3/(?P<ssid>\d+)/(?P<tssid>\d+)/?$', views.edit_tss_page_3, name='edit-tss-page-3'), # edit affiliated institute 
    url(r'^edit-tss-page-4/(?P<ssid>\d+)/(?P<tssid>\d+)/?$', views.edit_tss_page_4, name='edit-tss-page-4'), # edit personnels
    url(r'^edit-tss-page-5/(?P<ssid>\d+)/(?P<tssid>\d+)/?(?P<action>\w+)?/?$', views.edit_tss_page_5, name='edit-tss-page-5'), # edit summary

    # Edit SS page
    url(r'^edit-ss-fmpage/(?P<ssid>\d+)/(?P<tssid>\d+)?$', views.edit_ss_fmpage, name='edit-ss-fmpage'), #edit sample name and sample num

    # Collaborator PI page
    url(r'^collab-page$', views.collab_page, name='collab-page'),
    url(r'^collab-page/set-request-sent/(?P<ssid>\d+)/?$', views.set_request_sent_ss, name="set-request-sent"),

    # Well-filling pages
    url(r'^well-filling-1$', views.well_filling_1, name='well-filling-1'), # choose way of well filling
    url(r'^well-filling-2$', views.well_filling_2, name='well-filling-2'), # choose order of well filling
    url(r'^well-filling-2-customize$', views.well_filling_2_customize, name='well-filling-2-customize'), # customize order of well filling
    url(r'^well-filling-3-manual$', views.well_filling_3_manual, name='well-filling-3-manual'), # well filling procedure - manual
    url(r'^well-filling-3-robot$', views.well_filling_3_robot, name='well-filling-3-robot'), # well filling procedure - robot

    # Lab Technician page
    url(r'^lab-tech-page$', views.lab_tech_page, name='lab-tech-page'),

    # Index page
    url(r'^index$', views.index, name='index'),
    url(r'^failed_signin$', views.failed_signin, name='failed_signin'),
    url(r'^signin$', views.signin, name='signin')

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

"""
# Testing pages
url(r'^index-legend$', views.index_legend, name='index-legend'),
url(r'^preview$', views.preview, name='preview'),
url(r'^test$', views.test, name='base_template'),
url(r'^pheno-list$', views.pheno_list, name='pheno-list' ),
url(r'^welcome-collaborator$', views.welcome_collab, name='welcome-collab'),
url(r'^96plate.html$', views._96plate, name='96plate'), #GONE


# BOOTSTRAP TUTORIAL
url(r'^base$', views.base, name='base'),

# About Page
url(r'^about$', views.about, name='about'),

# Project List Page
url(r'^project-list$', views.project_list, name='project-list'),
url(r'^save-file$', views.save_files, name='save-file'),
url(r'^sample-submission$', views.sample_submission_list, name='sample-submission'),

# Manifest Upload Page
#url(r'^manifest-upload$', views.manifest_upload, name='manifest-upload'),

# Pheno Select Page
url(r'^pheno-select$', views.pheno_select, name='pheno-select'),
url(r'^pheno-select/(?P<id>\d+)/$', views.pheno_select, name='pheno-select-id'),

# Contact Page
url(r'^contact$', views.contact, name='contact'),

# Login / Sign Up Page
url(r'^sign-up$', views.signup, name='sign-up'),

# User Profile Page
    url(r'^user_profile$', views.user_profile, name='user_profile'),


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
    """
