#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Miphreal Adler'
__email__ = 'miphreal@gmail.com'
__version__ = '0.1'


'''
Designed to work with a passwords through cli.
'''


import cmd
import getpass

from storage import SafeStorage





class SafepCLI(cmd.Cmd):
    prompt = '\nsafep> '
    intro = 'safep {}\n{} <{}>'.format(__version__, __author__, __email__)

    def __init__(self, db, passwd):
        cmd.Cmd.__init__(self)
        self.db = SafeStorage(db, passwd)
        self.user = getpass.getuser()

    def do_exit(self, line):
        """
        Exit from safep.
        """
        self.db.close()
        return True

    def _print_record(self, i, r):
        print '{:>4} {:<15}{:<15}{:<15}{}'.format(i, *r)

    def do_ls(self, word, with_passwords=False):
        """
        Print records without passwords (******)
        > ls word_for_search
        """
        indxs = self.db.search(word)
        records = self.db.get_records(indxs, with_passwords)
        print '  id {:<15}{:<15}{:<15}{}'.format('name','user','password','key words')
        for i,r in zip(indxs, records):
            self._print_record(i, r)

    def do_lsp(self, word):
        """
        Print records with passwords.
        """
        self.do_ls(word, with_passwords=True)

    def do_mk(self, line):
        """
        Create record.
        """
        name = raw_input('name: ')
        user = raw_input('user [%s]: '%self.user) or self.user
        password = getpass.getpass('password:')
        kw = raw_input('key words: ')

        self._print_record('*',(name,user,'******',kw))
        choice = raw_input('Create this record? [y]/n: ') or 'y'
        if choice in ('y','Y'):
            self.db.add(name,user,password,kw)


    def do_rm(self, indx):
        """
        Delete record.
        > rm id
        """
        indx = int(indx)
        self._print_record(indx, self.db.get_record(indx))
        inp = raw_input('Delete this record? [y]/n: ') or 'y'
        if inp in ('y','Y'):
            self.db.delete(indx)

    def do_ed(self, indx):
        """
        Edit record.
        > ed id
        """
        indx = int(indx)
        (name, user, passwd, kw) = self.db.get_record(indx, True)

        name = raw_input('name [%s]: '%name) or name
        user = raw_input('user [%s]: '%user) or user
        password = getpass.getpass('password[***]:') or passwd
        kw = raw_input('key words [%s]: '%kw) or kw

        self.db.edit(indx, (name,user,passwd,kw))
        

    def do_chpass(self, line):
        """
        Replace password for db.
        > chpass new_password
        """
        password = getpass.getpass('password: ')
        self.db.change_password(password)



def parse_args():
    import optparse

    usage = '%prog [-f /path/to/pass] [-p password]'
    parser = optparse.OptionParser(usage=usage, version='safep %s'%__version__)
    parser.add_option('-f', '--file', default='~/.safep', dest='file',
                      help='path to passwords db [default: %default]')
    parser.add_option('-p', '--pass', dest='passwd', help='password for db')

    (options, args) = parser.parse_args()

    if not options.passwd:
        import getpass
        #print 'password>',
        #options.passwd = raw_input()
        options.passwd = getpass.getpass('password> ')
        
    return options.file, options.passwd


if __name__ == '__main__':
    SafepCLI(*parse_args()).cmdloop()



