import sys
from arguments_parser import parse_args
from open_ldap import OpenLdap
from csv_parser import parse_csv, random_password
from smtp_mail import SmtpServer


def create_user(open_ldap, smtp, entries):
    """
    If the 'ldap_insert' returns True, then
    the email will be send with the account info.
    """
    try:
        if open_ldap.ldap_insert(entries):
            smtp.send_email(entries)
            return True
        else:
            return False
    except Exception as e:
        print('ERROR - ', e)
        return


def run(args):
    """
    Creates the OpenLDAP and SMTP
    objects and iterates over the .csv file.
    Calls the create_user function and check the
    result (if 'true' the count will be increased).
    Returns the total count of users created.
    """
    open_ldap = OpenLdap(args.user,
                         args.password,
                         args.address)
    smtp = SmtpServer(args.smtp_host,
                      args.port,
                      args.email,
                      args.email_password)
    entries = {}
    count = 0
    for row in parse_csv(args.file):
        try:
            entries['name'] = row['name']
            entries['lastname'] = row['lastname']
            entries['email'] = row['email']
        except KeyError as e:
            return "ERROR - Missing '{}' csv header".format(e)
        entries['password'] = random_password()
        if create_user(open_ldap, smtp, entries):
            count += 1
    return "INFO - Finished. Total of {} user(s) created".format(count)


def main():
    args = parse_args()
    print(run(args))
    return 0


if __name__ == "__main__":
    sys.exit(main())
