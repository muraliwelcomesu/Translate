import os
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import subprocess

class srt_Rec():
    def __init__(self):
        self.LineNo = ''
        self.Duration = ''
        self.Eng1 = ''
        self.Eng2 = ''
        self.Trn1 = ''
        self.Trn2 = ''
        
class Translate():
    
    def __init__(self,FileName,FromLang,ToLang):
        self.FileName = FileName
        self.FromLang = FromLang
        self.ToLang = ToLang
        
    
    def isDuration(self,line):
        reg_dur = re.compile(r'\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d')
        if  reg_dur.search(line) is not None:
            return True
        else:
            return False
            
    def isLine(self,line):
        try:
            line_no = int(line)
            return True
        except:
            return False
        
    def is_Eng(self,line):
        if  re.search('[a-zA-Z]', line) is not None:
            return True
        else:
            return False  
    
    def file_to_ListRec(self):
        print('starting file_to_ListRec')
        file_in  = open(self.FileName,encoding="utf-8",mode = 'r')
        l_all_lines = []
        rec_line = srt_Rec()
        for lines in file_in:
            if self.isLine(lines):
                if rec_line.LineNo is not None:
                    l_all_lines.append(rec_line)
                    del rec_line
                rec_line = srt_Rec()
                rec_line.LineNo = lines
            if self.isDuration(lines):
                rec_line.Duration = lines
            if self.is_Eng(lines):
                if rec_line.Eng1 != '':
                    rec_line.Eng2 = lines
                else:
                    rec_line.Eng1 = lines
        
        if rec_line.LineNo != '':
            l_all_lines.append(rec_line)
            del rec_line
    
        file_in.close()
        print('Completed file_to_ListRec')
        return l_all_lines
     
    def ListRec_to_File(self,list_rec):
        print('starting ListRec_to_File')
        filename1, file_extension1 = os.path.splitext(self.FileName)
        file2 = filename1 + '_1' + file_extension1
        file_out = open(file2,encoding="utf-8",mode = 'w')
        if int(len(list_rec)) > 0:
            for line in list_rec:
                if line.LineNo != '':
                    file_out.write(line.LineNo)
                if line.Duration != '':
                    file_out.write(line.Duration)
                if line.Eng1 != '':
                    file_out.write(line.Eng1)
                if line.Eng2 != '':
                    file_out.write(line.Eng2)
                if line.Trn1 != '':
                    file_out.write(line.Trn1)
                if line.Trn2 != '':
                    file_out.write(line.Trn2)
                file_out.write('\n')
        file_out.close()
        print('Completed ListRec_to_File')

    def format_list(self,p_list):
        l_space = '%20'
        l_newline = '%0A'
        l_str = ''
        l_str_original = ''
        for line in p_list:
            l_str_original = l_str_original + line + '\n'
            l_str = l_str + line.replace(' ',l_space) + l_newline
        return l_str,l_str_original
    
    def google_Translate(self,p_list):
        print('inside translate function')
        l_format_input = self.format_list(p_list)
        url = 'https://translate.google.com/#{}/{}/{}'.format(self.FromLang,self.ToLang,l_format_input)
        print(url)
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(firefox_options=options)
        driver.set_page_load_timeout(30)
        driver.get(url)
        time.sleep(2)
        l_trans_text = driver.find_element_by_xpath('/html/body/div[3]/div[2]/form/div[2]/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div/span[2]').text
        list_1 = l_trans_text.split('\n')
        print('output printing...')
        print(list_1)
        driver.quit()
        return list_1
    
    def process_file(self):
        print('Start of process_file')
        l_lines = self.file_to_ListRec()
        l_count = 0
        l_output = ''
        for line in l_lines:
            l_tmp_list = []
            if line.Eng1 != '':
                l_tmp_list.append(line.Eng1)
            if line.Eng2 != '':
                l_tmp_list.append(line.Eng2)
            l_tmp_cnt = 0
            while int(l_tmp_cnt) < 1:
                print('inside loop calling translate')
                l_count = l_count + 1
                try:
                    l_output = self.google_Translate(self.FromLang,self.ToLang,l_tmp_list)
                except:
                    print('Some Exception in translating')

                if l_output is not None:
                    l_tmp_cnt = 2;
                if l_count > 5:
                    print('retry again-'+str(l_count))
                    time.sleep(1)
                    l_count = 0
                    break
            print(l_output)
            line.Trn1 = l_output
            time.sleep(1)
        self.ListRec_to_File(l_lines)
        print('Return from  of process_file')
            

if __name__ == "__main__":
    print('Starting')
    os.chdir('D:\\work_dir\\Test')
    obj_translate = Translate('test1.srt','en','ta')
    obj_translate.process_file()
    print('Completed')
    

