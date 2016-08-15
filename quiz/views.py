from django.shortcuts import render
from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json,requests
from models import UserDetails
from pprint import pprint
import sys
# Create your views here.
MY_ID=str(1179980365395638) 
class QuizView(generic.View):
    def get(self,request,*args,**kwargs):
        if self.request.GET['hub.verify_token']=='9990074416':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse("Error,Invalid Token")

    #override dispatch to handle post request without csrf        
    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args,**kwargs):
        return generic.View.dispatch(self,request,*args,**kwargs)

    def post(self,request,*arg,**kwargs):
        incoming_message=json.loads(self.request.body.decode('utf-8'))
        
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                if 'message' in message:

                    if message['sender']['id'] != MY_ID :
                        pprint (entry)
                        fbid=message['sender']['id']
                        if 'quick_reply' in message["message"]:
                            if message["message"]["text"]==message["message"]["quick_reply"]["payload"]:
                                post_message(fbid,'yeah !! its correct')
                            else:
                                post_message(fbid,"incorrect answer !! correct answer is " + message["message"]["quick_reply"]["payload"])
                        else:
                            
                                #post_message(message['sender']['id'],message['message']['text'])
                                send_quick_reply(message['sender']['id'])
                if 'quick_reply' in message:
                    print ("message sent is -- ", )
                    pprint ( message)
            
        return HttpResponse()

def post_message(fbid,recieved_msg):
    post_url='https://graph.facebook.com/v2.6/me/messages?access_token=EAAPssNxnMjABAOVVxXjgWdPPGGopWHf5k6DynsJGsAuONwAJqZBnRtNlOWTZApiGpAtaNaqqNXgjaG2kkY9MJ9gbefbo8FPAoXwwdJfdCQXM0blTNzW7L1sUGfYxHGAhKiZAmXXYaYLyWf8fch5XNrJRBWYpDyXd1Tdn8qWWgZDZD' 
    response_msg=json.dumps({"recipient":{"id":fbid},"message":{"text":recieved_msg}})
    pprint (response_msg)
    status=requests.post(post_url,headers={'Content-Type':'application/json'},data=response_msg)
    #pprint(status.json())
    print (fbid)
    print (get_user_details(fbid) )

def get_user_details(fbid):
    try:
        
        if not UserDetails.objects.filter(fb_id=fbid).exists():
            post_url="https://graph.facebook.com/v2.7/{0}".format(fbid)
            params={'fields':'first_name,last_name', 'access_token':'EAAPssNxnMjABAOVVxXjgWdPPGGopWHf5k6DynsJGsAuONwAJqZBnRtNlOWTZApiGpAtaNaqqNXgjaG2kkY9MJ9gbefbo8FPAoXwwdJfdCQXM0blTNzW7L1sUGfYxHGAhKiZAmXXYaYLyWf8fch5XNrJRBWYpDyXd1Tdn8qWWgZDZD'}
            user_details=requests.get(post_url,params).json()
            user_details['fb_id']=fbid
            user,already=UserDetails.objects.get_or_create(user_details)
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
        post_url='https://graph.facebook.com/v2.6/me/messages?access_token=EAAPssNxnMjABAOVVxXjgWdPPGGopWHf5k6DynsJGsAuONwAJqZBnRtNlOWTZApiGpAtaNaqqNXgjaG2kkY9MJ9gbefbo8FPAoXwwdJfdCQXM0blTNzW7L1sUGfYxHGAhKiZAmXXYaYLyWf8fch5XNrJRBWYpDyXd1Tdn8qWWgZDZD'
        data=json.dumps({"recipient":{"id":fbid}, "message": create_question("who is president of india",['rahul','obama','modi','pranab'],'pranab') })
        pprint (data)
        status=requests.post(post_url,headers={'Content-Type':'application/json'},data=data).json()
        print (status)
    except:
        print ("Error Occured ",sys.exc_info()  )

def create_question(title,options,answer):
    message={}
    message['text']=title
    quickreplies=[]
    for option in options:
        reply={}
        reply['content_type']='text'
        reply['title']=option
        reply['payload']=answer
        quickreplies.append(reply)
    message['quick_replies']=quickreplies
    return message
    


