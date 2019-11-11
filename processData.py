import json 
import os
import pandas as pd

pathFolder = './output/Risk_Management'
# print(os.listdir(pathFolder))
# exit()
# datasets = []
c = 0
categories =["Keywords\n","Author Information\n","Funding\n","Publisher\n","Categories / Classification\n"]

def getTitle(lines):
    return lines[0]

def getBy(lines):
    return lines[1][3:]



# def getResea

keyword = ["Published","Author Keywords","Document Type","KeyWords Plus","Reprint Address","Addresses","E-mail Addresses","Research Areas","Web of Science Categories"]

dataset = []

for i in os.listdir(pathFolder):
    # c += 1
    pathFile = pathFolder + '/' + i
    with open(pathFile) as f:
        lines = f.readlines()
        kw = []
        data = {
            "Title":"",
            "By":"",
            "View ResearcherID and ORCID":"",
            "Abstract":"",
            "Published":"",
            "Author Keywords":"",
            "Document Type":"",
            "KeyWords Plus" : "",
            "Reprint Address" : "",
            "Addresses":"",
            "E-mail Addresses":"",
            "Funding Agency Grant Number":"",
            "Publisher":"",
            "Research Areas":"",
            "Web of Science Categories":""
        }
        for line in lines:
           p = line.find(":")
           if p != -1:
               kw.append(line[:p])
           else:
               kw.append(line)
        # print(len(kw))
        # print(i)
        data["Title"] = lines[0]
        data["By"] = lines[1][3:]
        if lines[2] != "View ResearcherID and ORCID\n":
            data["View ResearcherID and ORCID"] = lines[2]
        else:
            data["View ResearcherID and ORCID"] = lines[3]

        data["Publisher"] = lines[len(lines)-5]
        try:
            if "Funding Agency Grant Number\n" in lines:
                funding_id = lines.index("Funding Agency Grant Number\n")
                view_funding_id = lines.index("Publisher\n")
                data["Funding Agency Grant Number"] = lines[funding_id:view_funding_id]
        except:
            print("View funding text: %s", i)

        try:
            if "Abstract\n" in lines:
                abstract_id = lines.index("Abstract\n")
                keyword_id = lines.index("Keywords\n")
                data["Abstract"] = lines[abstract_id+1]
        except:
            print("Keywords %s ",i)
            # print(i,publisher_id)
            # if publisher_id > 0:
                # print(i,publisher_id)
                # data["Publisher"] = lines[publisher_id+1]

        for cate in keyword:
            if cate in kw:
                p = kw.index(cate)
                data[cate] = lines[p][lines[p].find(":")+1:]

        dataset.append(data)
                # print(cate,kw.index(cate))
            # if cate not in lines:
                # c += 1
                # print(i,cate)
                # break

df = pd.DataFrame(dataset)
df.to_csv("data.csv",index=False)

print("total doc: %d " % c)