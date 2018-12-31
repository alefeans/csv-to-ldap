import sys
from arguments_parser import parse_args
from open_ldap import OpenLdap
from csv_parser import parse_csv, random_password
from smtp_mail import SmtpServer
from my_sql import MySQLConnector


def create_user(open_ldap, smtp, mysql, entries):
    """
    If the 'ldap_insert' returns True, then 
    the data will be inserted in MySQL and the
    email will be send with the account info.
    Else, returns 'None'.
    """
    try:
        if open_ldap.ldap_insert(entries):
            mysql.insert_items(entries)
            smtp.send_email(entries)
            return True
        else:
            return
    except Exception as e:
        print('ERROR - ', e)
        return


def run(args):
    """
    Creates the OpenLDAP, MySQL and SMTP
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
    mysql = MySQLConnector(args.mysql_user,
                           args.mysql_password,
                           args.mysql_address)
    entries = {}
    count = 0
    for row in parse_csv(args.file):
        entries['name'] = row['name']
        entries['lastname'] = row['lastname']
        entries['email'] = row['email']
        entries['password'] = random_password()
        if create_user(open_ldap, smtp, mysql, entries):
            count += 1
    return "INFO - Finished. Total of {} user(s) created".format(count)


def main():
    args = parse_args()
    print(run(args))
    return 0


if __name__ == "__main__":
    sys.exit(main())
