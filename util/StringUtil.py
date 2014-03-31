'''
Created on Oct 9, 2012

@author: brian
'''

class StringUtil(object):

    @staticmethod
    def cstrip (string):
        return string.strip(' \t\n\r')    