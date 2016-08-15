''' UTILITY FILE TO HELP IN POPULATING THE DATABASE'''

from models import Questions
import json
import os ,random
import requests
from pprint import pprint 
from random import randrange
BASE_DIR=os.path.dirname(__file__)
DRY_RUN=False
WIKI='https://en.wikipedia.org/w/api.php?action=opensearch&limit=1&namespace=0&search=jeff%20bezos'
def extract_info():
    file=open(BASE_DIR+'/ceo.json','r')
    jsonfile=json.load(file)
    
    executives=[]
    companies=[]

    for i in range(50):
        executives.append( jsonfile['ceo'][str(i+1)] )
        companies.append(jsonfile['company'][str(i+1)])

    companies=map(lambda x : "Who is Executive of " + x + "?",companies)

    list_q_and_a=zip(companies,executives)

    for q,a in list_q_and_a:
        update_database(q,a,executives)

def update_database(question  , answer,options):
    count =0
    option=[]
    counter=3
    while counter > 0:
        rand_choice=random.choice(options)
        if not rand_choice is answer:
            option.append(rand_choice)
            counter-=1

    rand_index=randrange(0,4)
    option.insert(rand_index,answer)
    print (option)

    link=get_wiki_link(answer)
    
    

    if DRY_RUN:
        count +=1
    else:
        try:
            new_ques=Questions()
            new_ques.question=question
            new_ques.answer=answer
            new_ques.option1=option[0]
            new_ques.option2=option[1]
            new_ques.option3=option[2]
            new_ques.option4=option[3]
            if not link is None:
                new_ques.links=link
            new_ques.save()
            print (new_ques)
        
        except:
            print ("Some Error Occured")


def get_wiki_link(search):
    try:
        params={'action':'opensearch','limit':'1','namespace':'0','search':search}
        status=requests.get(WIKI,params=params).json()
        pprint (status)
        return (status[-1][0])
    except:
        return None