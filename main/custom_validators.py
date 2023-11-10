from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class PasswordCombinationValidator:
    def validate(self,password,user=None):
        if password.isupper() == True:
            raise ValidationError(_("password dont have lowercase letters"),
                                  code="no lowercase",
                                  )
        if password.islower() == True:
            raise ValidationError(_("passworr dont have uppercase letters"),
                                  code="no uppercase",
                                  )
        if password.isdigit() == True:
            raise ValidationError(_("password has no letter"),
                                  code="no letter",
                                  )
        if password.isalpha() ==True:
            raise ValidationError(_("password should not be letter alone"),
                                  code="no numbers",
                                  )
    def get_help_text(self):
        return _("the password should be a combination of uppercase,lowercase,number and special symbols")
