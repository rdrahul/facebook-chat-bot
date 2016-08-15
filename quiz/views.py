from django.shortcuts import render
from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json,requests,random
import util
from models import UserDetails
from pprint import pprint
from models import Questions
import sys

# Create your views here.
MY_ID='1179980365395638'
ACCESS_TOKEN='EAAPssNxnMjABAOVVxXjgWdPPGGopWHf5k6DynsJGsAuONwAJqZBnRtNlOWTZApiGpAtaNaqqNXgjaG2kkY9MJ9gbefbo8FPAoXwwdJfdCQXM0blTNzW7L1sUGfYxHGAhKiZAmXXYaYLyWf8fch5XNrJRBWYpDyXd1Tdn8qWWgZDZD'
MESSAGE_POST_URL='https://graph.facebook.com/v2.6/me/messages?access_token={0}'.format(ACCESS_TOKEN)

class QuizView(generic.View):
    ''' The generic view for the quiz app'''

    def get(self,request,*args,**kwargs):
        'Get request handler - Required to verify the webhook'

        if self.request.GET['hub.verify_token']=='9990074416':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse("Error,Invalid Token")


    #override dispatch to handle post request without csrf        
    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args,**kwargs):
        return generic.View.dispatch(self,request,*args,**kwargs)



    def post(self,request,*arg,**kwargs):
        ''' Handling post requests '''
        incoming_message=json.loads(self.request.body.decode('utf-8'))        
        try:
            #refer to facebook api to know what's going on
            for entry in incoming_message['entry']:
                for message in entry['messaging']:
                    if 'message' in message:
                        if message['sender']['id'] != MY_ID :               # sometimes facebook echos back sent messages,to avoid that
                            pprint (entry)
                            fbid=message['sender']['id']
                            if 'quick_reply' in message["message"]:
                                got_answer=message["message"]["text"].lower()
                                correct_answer=message["message"]["quick_reply"]["payload"].lower()
                                if got_answer==correct_answer:
                                    post_message(fbid,"correct !! nice  work {0}  !!".format(get_user_details(fbid)))
                                else:
                                    post_message(fbid,"incorrect... sorry correct answer was {0} ".format(correct_answer))
                            else:
                                route(fbid,message['message']['text'])
                                    #post_message(message['sender']['id'],message['message']['text'])
                                    #send_quick_reply(message['sender']['id'])
        except :
            print ("Error Occured ",sys.exc_info() )
            return HttpResponse(status=500)
        finally:
            return HttpResponse(status=200)

def post_message(fbid,recieved_msg):
    post_url=MESSAGE_POST_URL
    response_msg=json.dumps({"recipient":{"id":fbid},"message":{"text":recieved_msg}})
    pprint (response_msg)
    status=requests.post(post_url,headers={'Content-Type':'application/json'},data=response_msg)
    #pprint(status.json())
    print (fbid)
    print (get_user_details(fbid) )

def get_user_details(fbid):
    ''' the current user details '''
    try:
        if not UserDetails.objects.filter(fb_id=fbid).exists():
            post_url="https://graph.facebook.com/v2.7/{0}".format(fbid)
            params={'fields':'first_name,last_name', 'access_token':ACCESS_TOKEN}
            user_details=requests.get(post_url,params).json()
            user_details['fb_id']=fbid
            user=UserDetails()
            user.fb_id=fbid
            user.first_name=user_details['first_name']
            user.last_name=user_details['last_name']
            user.save()
            return user_details['first_name']
        else:
            user=UserDetails.objects.get(fb_id=fbid)
            return user.first_name

    except:
        print ("Error Occured ",sys.exc_info()  )
        return




def send_quick_reply(fbid):
    try:
        print (fbid)
        post_url=MESSAGE_POST_URL
        question=get_random_question(fbid)
        data=json.dumps({"recipient":{"id":fbid}, "message": create_question(fbid,question) })
        #pprint (data)
        status=requests.post(post_url,headers={'Content-Type':'application/json'},data=data).json()
        #print (status)
    except:
        print ("Error Occured ",sys.exc_info()  )



def create_question(fbid,question):
    ''' Creates a question and returns dictionary in required format'''
    title=question.question
    options=[question.option1,question.option2,question.option3,question.option4]
    answer=question.answer
    post_message(fbid,title)                        # Ask the question first
    message={}
    message['text']="Select an option"              #then give the options
    quickreplies=[]
    for option in options:
        reply={}
        reply['content_type']='text'
        reply['title']=option[:20]
        reply['payload']=answer.lower()
        quickreplies.append(reply)
    message['quick_replies']=quickreplies
    return message
    
def get_random_question(fbid):
    all_questions=Questions.objects.all()
    return random.choice(all_questions)


def route(fbid,message):
    '''response to user messages'''
    if 'quiz' in message.lower():
        send_quick_reply(fbid)
    else:
        post_message(fbid," Why don't you try typing 'Quiz' ")