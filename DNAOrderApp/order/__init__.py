#To create baseline data

#Create Groups
# from django.contrib.auth.models import User, Group
# #Get or Create the Group
# fmgroup, created = Group.objects.get_or_create(name="Faculty Member")
# cgroup, created = Group.objects.get_or_create(name="Collaborator")
# labgroup, created = Group.objects.get_or_create(name="Lab Technician")
# admin, created = Group.objects.get_or_create(name="Admin")


# #Setting Permissions to the Group
# from django.contrib.auth.models import Permission
# Permission.objects.get(name='can add unit')
# mygroup.permissions.add(Permission.objects.get(name='can add unit'))


# #Create Users
# from django.contrib.auth.models import User
# from DNAOrderApp.order.models import DNAOrderAppUser

# fm_user = DNAOrderAppUser(username='fm-member@email.com', 'fm-member@email.com', 'fm-member-password')
# fm_user.is_staff = True
# fm_user.is_superuser = True
# fm_user.save()

# collab_user = DNAOrderAppUser(username='collab-member@email.com', 'collab-member@email.com', 'collab-member-password')
# collab_user.is_staff = True
# collab_user.is_superuser = True
# collab_user.save()

# lab_tech_user = DNAOrderAppUser(username='lab-tech-member@email.com', 'lab-tech-member@email.com', 'lab-tech-password')
# lab_tech_user.is_staff = True
# lab_tech_user.is_superuser = True
# lab_tech_user.save()

# #Add fakeusers to group
# fm_user.groups.add(fmgroup)
# collab_user.groups.add(cgroup)
# lab_tech_user.groups.add(labgroup)
