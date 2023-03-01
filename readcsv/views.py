from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings

# Create your views here.

# View to read and parse csv into unique email addresses and domains with count
def readcsv(request):

    csvPath = r"{}/emails.csv".format(settings.STATICFILES_DIRS[0])

    uniqueEmailsList = []
    domainDict = {}
    domainsString = ""

    with open(csvPath, 'r') as csvFile:
        
        lines = csvFile.readlines()
        
        ##print("There are {} emails in the file.".format(len(lines)))
        
        for email in lines:
            
            #email = email.strip()
            
            if email not in uniqueEmailsList:
                
                uniqueEmailsList.append(email)
                
            domain = email.split('@')[1]
            
            if domain not in domainDict.keys():
                
                domainDict[domain] = 1
            else:
                domainDict[domain] += 1

    uniqueEmailsList.sort()

    emailsString = ''.join(uniqueEmailsList)

    # Build domain string from dict for nice displaying
    keys = list(domainDict.keys())
    keys.sort()

    sortedDomains = {key: domainDict[key] for key in keys}

    #for key in domainDict.keys():
    for key in sortedDomains.keys():

        domainsString += "{}: {}\n".format(key.strip(), domainDict[key])

    # Send data as json response 
    data = {
        "uniqueEmails": emailsString,
        "domains": domainsString
    }

    return JsonResponse(data)

# View just to display the html
def displayHTML(request):

    return render(request, 'readcsv/readcsv_process.html')
