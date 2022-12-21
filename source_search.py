import requests
import urllib3
import re
from colorama import Fore
import sys

def font_style(title,items,chois):

    show_title = '\r\n' + Fore.RED + title + Fore.RESET + '\r\n' + Fore.YELLOW + '-' * 20 + Fore.RESET + '\r\n'
    print(show_title)

    if chois == 1:
        start = Fore.GREEN + "<!-- "
        end =  " -->" + Fore.RESET
    elif chois == 2:
        start = Fore.BLUE + "[ "
        end =  " ]" + Fore.RESET
    elif chois == 3:
        start = Fore.CYAN + "[ "
        end =  " ]" + Fore.RESET
    elif chois == 4:
        start = Fore.MAGENTA + "<meta "
        end =  " >" + Fore.RESET

    for item in items:

        show_item = start + item + end
        print(show_item)

    ending = '\r\n' + "*" * 40
    print(ending)

def extract_commands(data):

    commands = re.findall(r'<!--(.*?)-->',data)
    commands_count = len(commands)

    title = f"Found {commands_count} command"
    
    font_style(title,commands,1)
    

def extract_js_files(data):

    scripts = re.findall(r'<script(.*?)</script>',data)
    scripts_count = len(scripts)
    
    title = f"Found {scripts_count} script"
    
    items = []

    for script in scripts:
        if len(script) >= 0:
            
            js_files1 = re.findall(r'src="(.*?)"',script)
            js_files2 = re.findall(r"src='(.*?)'",script)


            if len(js_files1) > 0:
                
                items += js_files1

            elif len(js_files2) > 0:
                
                items += js_files2

    font_style(title,items,2)



def extract_links(data):

    links = re.findall(r'src="(.*?)"',data)
    links += re.findall(r"src='(.*?)'",data)
    links += re.findall(r'href="(.*?)"',data)
    links += re.findall(r"href='(.*?)'",data)

    for link in links:
        dom = link.find(".whitneyfarms.com")
        print(type(link))
        
        if dom == -1:
          links.remove(link) 
    
    count_links = len(links)
    title = f"Found {count_links} Link"
    
    font_style(title,links,3)
    print(len(links))

def extract_meta(data):

    data = re.findall(r"<meta(.*?)>",data)
    meta_count = len(data)
    title = f"Found {meta_count} Meta Tag Data"
    font_style(title,data,4)


def make_requests(target):

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # proxy = {'http':'http://127.0.0.1:8080','https':'https://127.0.0.1:8080'}

    r = requests.get(target,verify=False)
    if r.status_code == 200:
        extract_commands(r.text)
        extract_js_files(r.text)
        #extract_links(r.text)
        answer = input("Do You Want To Get The Meta Tags Content [y/n] ? ")
        print(answer)
        if answer.lower() == "y":
            extract_meta(r.text)
        else:
            print("You Select No")
        
    else:
        print(f"Error : Status Code {r.status_code}")


if len(sys.argv) > 1:
    make_requests(sys.argv[1])
else:
    print(f"Usage: {sys.argv[0]} https://www.domain.com/")
