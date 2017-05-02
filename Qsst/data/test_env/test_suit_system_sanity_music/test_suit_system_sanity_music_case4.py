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



class test_suit_system_sanity_music_case4(TestCaseBase):
    '''

    @see: L{TestCaseBase <TestCaseBase>}
    '''
    '''
    "Procedure:
    Step1:Launch music
    Step2:Play a music file
    step3:Delete music
    Verification: 
    ER1:music can be deleted
    
    '''
    
    
    def test_case_main(self, case_results):
        global case_flag , TAG     ,recoreName,p 
        recordName=''.join(__name__.split('_')[-2:])   
        case_flag = False
        TAG = "delete music: Music "
        log_test_framework(TAG, self.name+" -Start")
        
        """
        
        cases contents you need to add
        
        
        """


        p=subprocess.Popen('adb shell screenrecord /sdcard/%s.mp4'%recordName,shell=True)
        start_activity('com.android.music','com.android.music.MusicBrowserActivity')
#         if wait_for_fun(lambda:search_view_by_id('permission_allow_button'), True, 5):
#             phone.permission_allow() 
        self.click_songtab('Artists')
        self.click_songtab('Songs')        
        if wait_for_fun(lambda:search_view_by_id('search'), True, 5):
            song1=self.getSongName()
            log_test_framework(self.name, 'the first song is:'+song1)
            log_test_framework("gp_sanity_music_case4:", "Launch music pass")  
            log_test_framework(self.name,'exist play indicator')          
            click_button_by_id('play_indicator')
            sleep(4)
            click_textview_by_text('Play')
            sleep(5)
            click_button_by_id('play_indicator')
            sleep(2)
            click_textview_by_text('Delete')
            sleep(2)
            click_textview_by_text('OK')
            sleep(5)
            song2=self.getSongName()
            log_test_framework(self.name,'after delete song is'+song2)
            if not song1==song2:
                log_test_framework(self.name, 'Delete playing music pass')
                case_flag=True  
            elif search_text('has stopped'):
                  log_test_framework("gp_sanity_music_case4:", "Popup has stopped") 
                  take_screenshot()             
        elif search_text('has stopped'):
            log_test_framework("gp_sanity_music_case4:", "Popup has stopped")
            take_screenshot()
            click_textview_by_text('OK')
            sleep(2)
        else:
            log_test_framework("maybe not in music screen:", "Delete music fail")
            take_screenshot()
        send_key(KEY_BACK)
        sleep(1)
        send_key(KEY_BACK)
        sleep(1)
        send_key(KEY_HOME)
        sleep(1)        
       

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
            
    def getSongName(self):
        songName=get_view_text_by_id(VIEW_TEXT_VIEW,'com.android.music:id/line1')
        return songName
  
