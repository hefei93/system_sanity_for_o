# coding=utf-8
'''
   provide some interface of filemanager application.

   This class will provide operations api of filemanager application.

   1.Developer can directly call those api to perform some operation.

   2.Developer can add some new api.


   @author: U{chenhu<C_huch@qti.qualcmm.com>}
   @version: version 1.0.0
   @requires: python 2.7+
   @license:

   @see: L{Base <Base>}
   @note:
   @attention:
   @bug:
   @warning:



'''
from case_utility import *
from qrd_shared.Base import Base
from logging_wrapper import log_test_framework
import time



class Filemanager(Base):
    '''
    Filemanager is a class for operating file manager application.

    @see: L{Base <Base>}
    '''
    global TAG , count 
    '''@var count: count login,init value is 0
       @var TAG: "tag of Settings"
       @attention: modify by min.sheng,change TAG to global
    '''
    count = 0
    TAG = "Filemanager"
   
    
    def __init__(self):
        '''
        init method.
        '''
        self.mode_name = "filemanager"
        Base.__init__(self, self.mode_name)
        self.debug_print('Filemanager init:%f' % (time.time()))
        

    def intoInternal(self):
        '''
        into file manager internal storage
        '''
        if wait_for_fun(lambda:search_view_by_desc('Open navigation drawer'), True, 5):
            click_textview_by_desc('Open navigation drawer')
            if wait_for_fun(lambda:search_text('Internal shared storage'), True, 5):
                click_textview_by_text('Internal shared storage',searchFlag=TEXT_MATCHES)
                sleep(3)
            else:
                log_test_framework("file manager has no internal option", self.name + " ERROR")
        else:
            log_test_framework("file manager has no more option", self.name + " ERROR")
                
        
        
        










    
    

    

            

            

        
    
                         
                
  

                        

    
 


                        
 
    
                                                                                                                                                                                                                                        