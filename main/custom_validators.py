from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class PasswordCombinationValidator:
    def validate(self,password,user=None):
        special_char = "@#$_&-+()/?!;:"
        status = ""

        if password.isupper() == True:
            raise ValidationError(_("Password don't have lowercase letters"),
                                  code="no lowercase",
                                  )
        if password.islower() == True:
            raise ValidationError(_("Password don't have uppercase letters"),
                                  code="no uppercase",
                                  )
        if password.isalpha() ==True:
            raise ValidationError(_("Password should not be letters alone"),
                                  code="no numbers",
                                  )
        for i in special_char:
            if password.find(i) != -1:
                status += "1"

        if status == "":
            raise ValidationError(_("Password do not contain special characters"),
                                  code="no special characters",
                                  )


    def get_help_text(self):
        return _("the password should be a combination of uppercase,lowercase,number and special symbols")
