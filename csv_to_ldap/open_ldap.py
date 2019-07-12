import sys
import ldap3
from ldap3 import Server, Connection


class OpenLdap:

    def __init__(self, user, password, address):
        self.user = user
        self.password = password
        self.address = address
        self.server = Server(self.address)

    def _ldap_connector(self):
        try:
            conn = Connection(self.server, self.user, self.password, auto_bind=True)
            return conn
        except ldap3.core.exceptions.LDAPSocketOpenError as e:
            print('ERROR - LDAP - Bind Failed: ', e)
            sys.exit()

    def ldap_insert(self, entries):
        objectClass = [
            'top',
            'person',
            'organizationalPerson',
            'inetOrgPerson',
        ]
        try:
            item = {
                'uid': entries['name'],
                'cn': entries['name'] + ' ' + entries['lastname'],
                'givenname': entries['name'],
                'sn': entries['lastname'],
                'mail': entries['email'],
                'userPassword': entries['password'],
            }
        except KeyError:
            print('ERROR - Wrong entries in OpenLDAP items')
            return False
        conn = self._ldap_connector()
        try:
            user = self.user.split(',')
            user[0] = 'cn=' + entries['name']
            dn = ','.join(user)
            if conn.add(dn, objectClass, item):
                print("INFO - LDAP - Creating user '{}' on OpenLDAP".format(entries['name']))
                return True
            else:
                print('WARN - LDAP - ', conn.result['description'])
                return False
        except Exception as e:
            print('ERROR - LDAP - ', e)
            sys.exit()
        finally:
            conn.unbind()
