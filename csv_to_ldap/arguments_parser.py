import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="CSV to OpenLDAP")
    parser._action_groups.pop()
    optional = parser.add_argument_group('optional arguments')
    required = parser.add_argument_group('required arguments')
    optional.add_argument("-a", "--address",
                          help="OpenLDAP address, default is localhost",
                          default='localhost')
    required.add_argument("-u", "--user",
                          help="OpenLDAP user (dn)",
                          required=True)
    required.add_argument("-w", "--password",
                          help="OpenLDAP password",
                          required=True)
    required.add_argument("-s", "--smtp_host",
                          help="SMTP host, e.g 'smtp-mail.outlook.com'",
                          required=True)
    required.add_argument("-p", "--port",
                          help="SMTP port, e.g '587'",
                          required=True)
    required.add_argument("-e", "--email",
                          help="email sender, e.g 'test@hotmail.com'",
                          required=True)
    required.add_argument("-r", "--email_password",
                          help="email password",
                          required=True)
    optional.add_argument("-m", "--mysql_address",
                          help="MySQL address, default is localhost",
                          default='localhost')
    optional.add_argument("-n", "--mysql_user",
                          help="MySQL user, default is root",
                          default='root')
    required.add_argument("-o", "--mysql_password",
                          help="MySQL password",
                          required=True)
    required.add_argument("-f", "--file",
                          help="CSV file to parse",
                          required=True)
    return parser.parse_args()
