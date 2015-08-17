from django.contrib.auth.models import User
from userroles.models import set_user_role
from userroles import roles

# Read in some file with usersnames, emails, etc.
username = "tmp"
email = "vsochat@stanford.edu"
password = "tmppassword"
user = User.objects.create_user(username, email, password)

# At this point, user is a User object that has already been saved
# to the database. You can continue to change its attributes
# if you want to change other fields.

# Now set user role
set_user_role(user, roles.question_editor) # roles.question_editor
                                           # roles.assessment_editor
                                           # roles.behavior_editor

