# coding=utf-8
'''
@author: hu_ch
for android N
'''

import fs_wrapper
import settings.common as SC
from case_utility import *
from logging_wrapper import log_test_case, save_fail_log, print_report_line
from test_case_base import TestCaseBase
from qrd_shared.case import *
from test_suit_system_sanity_browser import *
from urlparse import clear_cache

class test_suit_system_sanity_browser_case04(TestCaseBase):
    '''

    @see: L{TestCaseBase <TestCaseBase>}
    '''
    '''
    "Procedure:
    Step1:Launch browser
    Step2:open website one by one
    Verification: 
    ER1:can open website successfuly
    
    '''
    
    def test_case_main(self, case_results):
        global case_flag , TAG, recoreName,p    
        case_flag = False
        recordName=''.join(__name__.split('_')[-2:]) 
        result=[]
        TAG = 'visit 10 websites'
        log_test_framework(TAG, self.name + " -Start")



        start_activity("com.android.browser", "org.chromium.chrome.browser.ChromeTabbedActivity")
        p=subprocess.Popen('adb shell screenrecord /sdcard/%s.mp4'%recordName,shell=True)
        if wait_for_fun(lambda:search_view_by_id('permission_allow_button'), True, 15):
            phone.permission_allow()
        if wait_for_fun(lambda:search_view_by_id('terms_accept'), True, 15):            
            click_button_by_id('terms_accept')
            if wait_for_fun(lambda:search_view_by_id('next_button'), True, 5):
                click_button_by_id('next_button')
                if wait_for_fun(lambda:search_view_by_id('next_button'), True, 5):
                    click_button_by_id('next_button')
                    if wait_for_fun(lambda:search_view_by_id('next_button'), True, 5):
                        click_button_by_id('next_button') 
        # self.openUrl('youtube.com ')
        #case_flag1=self.openUrl('tw.yahoo.com','id/swe_favicon_badge')  
        #result.append(case_flag1)
        #self.openUrl('facebook.com', searchId)
        #self.openUrl('twitter.com', searchId)
        #self.openUrl('udn.com/NEWS/mainpage.shtml', searchId)
        case_flag2=self.openUrl('www.msn.com', 'sb_form_go')
        result.append(case_flag2)
        case_flag3=self.openUrl('wikipedia.com', 'Wikipedia')
        result.append(case_flag3)
        case_flag4=self.openUrl('www.sina.com','手机新浪')
        result.append(case_flag4)
        case_flag5=self.openUrl('www.youku.com', 'mheader_channel_handle')
        result.append(case_flag5)
        case_flag6=self.openUrl('wap.qq.com', 'info.3g') 
        result.append(case_flag6)
        case_flag=not False in result
         
        if search_text('has stopped',isScrollable=0,searchFlag=TEXT_CONTAINS):
            log_test_framework("system_sanity_browser_case4:", "Popup has stopped")
            take_screenshot()
            click_textview_by_text('OK')
            sleep(2)      
            case_flag=False 
        
        for temp in range(4):
            send_key(KEY_BACK)
            if search_text('QUIT',searchFlag=TEXT_MATCHES,isScrollable=0):
                click_textview_by_text('QUIT')
                sleep(2)
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
        '''
        @attention: modify by min.sheng
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
     #open url :http://www.pengfu.com
    def openUrl(self,httpurl='www.baidu.com',searchId='id/toolbar_shadow'):
        if search_view_by_id('url'):
            click_textview_by_id('url')
            sleep(3)
            send_key(KEY_DEL)
            entertext_edittext_by_id('url','http://%s'%httpurl)
        elif search_view_by_id('url_bar'):
            click_textview_by_id('url_bar')
            sleep(3)
            send_key(KEY_DEL)
            entertext_edittext_by_id('url_bar','http://%s'%httpurl)
        sleep(5)
        send_key(KEY_ENTER)
        sleep(3)
        if wait_for_fun(lambda:search_view_by_id(searchId),True, 60) or wait_for_fun(lambda:search_text(searchId,isScrollable=0),True,60):
            log_test_framework("system_sanity_browser_case4:", "OPen website pass")
            return True
        else:
            take_screenshot()
            return False

    