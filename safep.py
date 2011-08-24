#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Miphreal Adler'
__email__ = 'miphreal@gmail.com'
__version__ = '0.1'


'''
Designed to work with a passwords through cli.
'''


import cmd



class SafepCLI(cmd.Cmd):
    prompt = 'safep> '
    intro = 'safep %s'%__version__

    def do_exit(self, line):
        """
        Exit from safep.
        
        """
        return True

    def preloop(self):
        # TODO. open passwords db
        pass

    def postloop(self):
        # TODO. close passwords db
        pass

    def do_ls(self, line):
        pass

    def do_mk(self, line):
        pass

    def do_rm(self, line):
        pass

    def do_chpass(self, line):
        pass



if __name__ == '__main__':
    import optparse

    parser = optparse.OptionParser()
    parser.add_option('-f', '--file',
                      default='~/.safep',
                      dest='file',
                      help='path to passwords db [default: %default]')
    parser.add_option('-p', '--pass',
                      dest='pass',
                      help='password for db')
    parser.parse_args()

    SafepCMD().cmdloop()



