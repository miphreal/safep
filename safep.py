#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Miphreal Adler'
__email__ = 'miphreal@gmail.com'
__version__ = '0.1'


'''
Designed to work with a passwords through cli.
'''


import cmd


class SafeStorage:
    def close(self):
        pass


class SafepCLI(cmd.Cmd):
    prompt = 'safep> '
    intro = 'safep %s'%__version__

    def do_exit(self, line):
        """
        Exit from safep.
        
        """
        return True

    def preloop(self):
        self.db = SafeStorage()

    def postloop(self):
        self.db.close()

    def do_ls(self, line):
        pass

    def do_mk(self, line):
        pass

    def do_rm(self, line):
        pass

    def do_ed(self, line):
        pass

    def do_chpass(self, line):
        pass



def parse_args():
    import optparse
    usage = '%prog [-f /path/to/pass] [-p password]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-f', '--file', default='~/.safep', dest='file',
                      help='path to passwords db [default: %default]')
    parser.add_option('-p', '--pass', dest='passwd', help='password for db')
    (options, args) = parser.parse_args()
    if not options.passwd:
        print 'password>',
        options.passwd = raw_input()
    return (options.file, options.passwd)


if __name__ == '__main__':

    print parse_args()
    SafepCLI().cmdloop()



