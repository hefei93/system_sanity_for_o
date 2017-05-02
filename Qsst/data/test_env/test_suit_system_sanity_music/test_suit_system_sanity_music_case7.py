'''
@author: hu_ch
'''

import fs_wrapper
import settings.common as SC
from case_utility import *
from logging_wrapper import log_test_case, save_fail_log, print_report_line
from test_case_base import TestCaseBase
from qrd_shared.case import *
from qrd_shared.mms.Mms import *



class test_suit_system_sanity_music_case7(TestCaseBase):
    '''

    @see: L{TestCaseBase <TestCaseBase>}
    '''
    '''
    precodition:recording a file
    "Procedure:
    Step1:Launch music
    Step2:search recording file
    Verification: 
    ER1:can search recording file
    
    '''
    
    
    def test_case_main(self, case_results):
        global case_flag , TAG    ,recoreName,p 
        recordName=''.join(__name__.split('_')[-2:])    
        case_flag = False
        TAG = "check music tab: Music "
        log_test_framework(TAG, self.name+" -Start")
        
        """
        
        cases contents you need to add
        
        
        """

        
        
        p=subprocess.Popen('adb shell screenrecord /sdcard/%s.mp4'%recordName,shell=True)
        start_activity('com.android.music','com.android.music.MusicBrowserActivity')
#         if wait_for_fun(lambda:search_view_by_id('permission_allow_button'), True, 5):
#             phone.permission_allow()             
        if wait_for_fun(lambda:search_view_by_id('search'), True, 5):
            log_test_framework("system_sanity_music_case7:", "Launch music pass")                                         
        elif search_text('has stopped'):
            log_test_framework("system_sanity_music_case7:", "Popup has stopped")
            take_screenshot()
            case_flag=False
            click_textview_by_text('OK')
            sleep(2)         
        else:
            log_test_framework("system_sanity_music_case7:", "launch music fail")
            take_screenshot()
            case_flag=False
        case_flag=self.click_songtab('Artists') 
        case_flag=self.click_songtab('Albums')
        case_flag=self.click_songtab('Songs')
        case_flag=self.click_songtab('Playlists')
        for i in range(4):
            send_key(KEY_BACK)
            sleep(1)
        send_key(KEY_HOME)
        if case_flag:
            qsst_log_case_status(STATUS_SUCCESS, "" , SEVERITY_HIGH)
        else:
            qsst_log_case_status(STATUS_FAILED, "", SEVERITY_HIGH)
        
        case_results.append((self.case_config_map[fs_wrapper.CASE_NAME_ATTR], case_flag))        
        
    def test_case_end(self):
        '''
        record the case result

        '''
        log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], TAG + ' : end')
        if can_continue() and case_flag == True:
            # shutdown()
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], TAG + ': case pass')
            print_report_line(self.case_config_map[fs_wrapper.CASE_NAME_ATTR] + TAG + ' : \tpass')
        else:
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], TAG + ' : case fail')
            print_report_line(self.case_config_map[fs_wrapper.CASE_NAME_ATTR] + TAG + ' : \tfail')
            save_fail_log()
        p.terminate() 
            
    def click_songtab(self,tabname=''):
        #click point to open drawer
        click(90,150)
        sleep(2)
        click_textview_by_text(tabname)
        sleep(3)
        if wait_for_fun(lambda:search_view_by_id('search'),True,5):
            case_flag=True
        if search_text("has stopped|Unfortunately|isn't responding", searchFlag=TEXT_MATCHES_REGEX,isScrollable=0):
            take_screenshot()
            click_textview_by_text('OK|Close', searchFlag=TEXT_MATCHES_REGEX)
            case_flag=False
        else:
            case_flag=True
        return case_flag
  
