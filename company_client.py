from db import client, models
import validators

def input_aborted():
    print("input aborted")
    quit()

'''
Get company name
'''
while True:
    name = input("Enter company name: ")
    name = str(name).strip()
    if name == 'q':
        input_aborted()
    elif len(name) > 1:
        break
    else:
        print("Invalid input – at least one character is needed. Enter q to abort.")

'''
Get company URL
'''
while True:
    url = input("Enter company URL: ")
    url = str(url).strip()
    if url == 'q':
        input_aborted()
    elif validators.url(url):
        break
    else:
        print("Enter a valid URL or enter q to abort.")

'''
Get company job tool
'''
while True:
    jobtool = input("Enter company Jobtool: ")
    jobtool = str(jobtool).strip().capitalize()
    if jobtool == 'Q':
        input_aborted()
    else:
        try:
            jobtool = models.JobTool(jobtool)
            break
        except ValueError:
            print("Enter a valid jobtool or enter q to abort.")

client.add_company(link=url, name=name, jobtool=jobtool)