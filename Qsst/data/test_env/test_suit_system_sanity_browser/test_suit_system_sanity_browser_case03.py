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

class test_suit_system_sanity_browser_case03(TestCaseBase):
    '''

    @see: L{TestCaseBase <TestCaseBase>}
    '''
    '''
    "Procedure:
    Step1:Launch browser
    Step2:empty browser bookmark
    Step3:open baidu,save bookmark
    Step4:open sina,save bookmark
    Step5:via bookmark open website
    Verification: 
    ER1:via bookmark open website successfully
    
    '''
    
    def test_case_main(self, case_results):
        global case_flag , TAG,recoreName,p    
        case_flag = False
        recordName=''.join(__name__.split('_')[-2:])
        TAG = 'via bookmark visit website: Browser '
        log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR],  self.name +' : case Start')
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
        self.emptyBookmark()
        case_flag=self.saveBookmark()
        if search_text('has stopped',isScrollable=0):
            log_test_framework(self.name, "Popup has stopped")
            take_screenshot()
            click_textview_by_text('OK')
            case_flag=False
            
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
            entertext_edittext_by_id('url_bar','http://%s'%httpurl)
        elif search_view_by_id('url_bar'):
            click_textview_by_id('url_bar')
            sleep(3)
            send_key(KEY_DEL)
            entertext_edittext_by_id('url','http://%s'%httpurl)
        sleep(5)
        send_key(KEY_ENTER)
        sleep(3)
        if wait_for_fun(lambda:search_view_by_id(searchId),True, 60) or wait_for_fun(lambda:search_text(searchId,isScrollable=0),True,60):
            log_test_framework("system_sanity_browser_case4:", "OPen website pass")
            return True
        else:
            take_screenshot()
            return False
    
    #save bookmarks
    def saveBookmark(self):
        send_key(KEY_MENU)
        sleep(2)
        wait_for_fun(lambda:search_text('Bookmarks',isScrollable=0),True,5)
        click_textview_by_text('Bookmarks',isScrollable=0)
        sleep(2)
        if wait_for_fun(lambda:search_view_by_id('id/bookmark_empty_view'),True,3):
            log_test_framework(self.name, 'browser bookmark is null')
            send_key(KEY_BACK)
            sleep(1)
            self.openUrl('www.baidu.com', '百度一下')
            send_key(KEY_MENU)
            sleep(1)
            click_textview_by_id('id/button_two')
            sleep(2)
            self.openUrl('www.sina.com', '手机新浪')
            send_key(KEY_MENU)
            sleep(1)
            click_textview_by_id('id/button_two')
            sleep(2)
            send_key(KEY_MENU)
            sleep(2)
            if wait_for_fun(lambda:search_view_by_id('id/bookmark_empty_view'),True,3):
                case_flag=False
                log_test_framework(self.name, 'save bookmark fail')
                take_screenshot()
            else:
                click_textview_by_text('Bookmarks',isScrollable=0)
                sleep(2)
                click_textview_by_index(3)
                sleep(2)
                if wait_for_fun(lambda:search_text('手机新浪',isScrollable=0),True,120):                    
                    log_test_framework(self.name, 'via bookmark open website pass')
                    return True
        else:
            log_test_framework(self.name, 'clear all the bookmark fail')
            return False

    #empty all the bookmarks
    def emptyBookmark(self):
        send_key(KEY_MENU)
        sleep(2)
        wait_for_fun(lambda:search_text('Bookmarks',isScrollable=0),True,5)
        click_textview_by_text('Bookmarks',isScrollable=0)
        sleep(2)
        if not wait_for_fun(lambda:search_view_by_id('id/bookmark_empty_view'),True,3):
            while(True):
                if wait_for_fun(lambda:search_view_by_id('more'),True,3):
                    click_button_by_id('more')
                    sleep(2)
                    click_textview_by_text('Delete')
                    sleep(2)
                    if search_view_by_id('id/bookmark_empty_view'):
                        log_test_framework(self.name, 'clear all the bookmark success')
                        send_key(KEY_BACK)
                        sleep(2)
                        return True
            
        else:
            log_test_framework(self.name, 'current page is no bookmark')
            send_key(KEY_BACK)
            sleep(2)
            return True

            
        
        
                