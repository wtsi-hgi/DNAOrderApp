DNAOrderApp
===========

A web application that aims to improve the interface for ordering DNA sequences from our collaborators. The current system generates an excel sheet (manifest) that is sent to our collaborators to be filled out as they fill the plates up with samples of the requested DNA sequences. The order that the DNA sequences are listed on the excel sheet is not very accommodating to the lab technician's workflow -  we're hoping that the GUI that we provide could make it easier to fill out the order form and reduce the error rate of mislabelling the wells. 

Installation
============
For Mac OSX, first install macports, then:
```bash
# Install prerequisites using macports
port install py27-virtualenv py27-mysql py27-django
# Configure a python virtualenv 
virtualenv-2.7 ~/python-virtualenv
# Clone git repository into virtualenv directory and install settings template
(cd ~/python-virtualenv &&  git clone https://github.com/wtsi-hgi/DNAOrderApp.git && cp DNAOrderApp/DNAOrderApp/settings.py.tmpl DNAOrderApp/DNAOrderApp/settings.py)
# Edit settings (DNAOrderApp/DNAOrderApp/settings.py) as needed
# Run server
VIRTUAL_ENV=$(echo ~/python-virtualenv) python ~/python-virtualenv/DNAOrderApp/manage.py runserver
```

Forked
=======
https://github.com/jschr/bootstrap-modal <br>
https://github.com/sigurdga/django-jquery-file-upload <br>
https://github.com/doph/minimal-django-file-upload-example <br>
https://github.com/python-excel/xlrd <br>


License
=======
See LICENSE


