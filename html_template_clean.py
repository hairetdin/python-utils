# -*- coding: utf-8 -*-
import os, sys
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')

def tempate_clean_files(current_dir):
    required_files = []
    links = []
    # exclude .php files
    #links = [ f for f in os.listdir(os.getcwd()) if not f.endswith(".php") ]
    for root, subdirs, files in os.walk(current_dir):
        for filename in files:
            if filename.endswith(".html"):
                #print('root - ',root)
                #print('subdirs - ', subdirs)
                html_file_name = os.path.join(root, filename)
                links.append(html_file_name)

                html_file = open(html_file_name,'r')
                html_doc = html_file.read()

                soup = BeautifulSoup(html_doc, 'html.parser')

                #css
                required_css_files = [link.get('href') for link in soup.find_all('link')]
                links.extend(required_css_files)
                #image append
                required_logo_files = [link.get('data-dark-logo') for link in soup.find_all('a')]
                links.extend(required_logo_files)
                #image
                required_img_files = [link.get('src') for link in soup.find_all('img')]
                links.extend(required_img_files)
                #href links
                required_link_files = [link.get('href') for link in soup.find_all('a')]
                links.extend(required_link_files)
                #js
                required_js_files = [link.get('src') for link in soup.find_all('script')]
                links.extend(required_js_files)

    # create full path for links and copy to required_files list
    for index, f in enumerate(links):
        #print(current_dir)
        #print(f)
        if f is None:
            pass
        elif (f[:7] == 'http://'):
            pass
        elif (f[:1] == '#'):
            pass
        elif (f[:1] == '/'):
            required_files.append(f)
        else:
            fname = os.path.join(current_dir, f)
            if os.path.isfile(fname):
                required_files.append(fname)

    return required_files

def remove_files(dest_dir, required_files_list):
    #remove all except required_files_list
    for root, subdirs, files in os.walk(dest_dir):
        for filename in files:
            file_name = os.path.join(root, filename)
            if 'fonts' in os.path.split(root):
                pass
            else:
                if not file_name in required_files_list:
                    os.remove(file_name)


if __name__ == "__main__":
    clean_dir = sys.argv[1]
    current_dir = os.getcwd()
    src = os.path.join(current_dir, clean_dir)
    dest_dir = os.path.join(current_dir, clean_dir+'_clean-template')
    os.system("cp -rf '{}' '{}'".format(src, dest_dir))

    required_files_list = tempate_clean_files(dest_dir)
    remove_files(dest_dir, required_files_list)
    print('The cleaned template created in dir: {}'.format(dest_dir))
