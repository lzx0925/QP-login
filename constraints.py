def password_check(password):
    if len(password)<8 or type(password) != str:    # return false if password length less than 8 or not string
        return False
    for c in password:                              # return false if password contains non-numeric/non-alpha char
        if not c.isalnum():                         # can only contain 0-9, A-Z, a-z
            return False
    return True


def email_check(email):
    if len(email) > 50 or '@' not in email:         # return false if email length exceed 50 or no @ symbol
        return False
    l = email.split('@')                            # e.g. recipient_name @ domain_name . top_level_domain
    if len(l) > 2 or l[1] == '':                    # return false if more than 1 @ or no domain name
        return False
    recipient = l[0]
    domain = l[1].split('.')                        # e.g. domain_name.top_level_domain
    if len(domain) < 2 or '' in domain:             # return false if missing top level domain or domain name
        return False
    return True
