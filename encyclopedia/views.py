from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
from markdown2 import Markdown
from random import choice,randint
#----------------------------------------------------------
class NewEntry(forms.Form):
    title,content=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control rounded-0","id":"exampleFormControlTextarea2","placeholder":"Enter your Page Title.","style":"height: 40px; width: 30%"})),forms.CharField(widget=forms.Textarea(attrs={"class":"form-control rounded-0","id":"exampleFormControlTextarea1","placeholder":"Write your page contents.","style":"height: 500px; width: 90%;"}))
class Search(forms.Form):
	search=forms.CharField(widget=forms.TextInput(attrs={"class":"search","placeholder":"Search Encyclopedia","style":"width:100%; height:30px;positition:absolute;border:2px solid black;border-radius:10px;outline:none;padding:2px;"}))
def index(request):
	if request.method=="POST":
		form=Search(request.POST)
		if form.is_valid():
			query_ele=form.cleaned_data["search"]
			result=[]
			foundstatus=False
			list_entries=util.list_entries()
			if len(query_ele)>2:
				l=0
				u=len(list_entries)-1
				while l<=u:
					mid=(l+u)//2
					if list_entries[mid]>query_ele:

						u=mid-1
					elif list_entries[mid]<query_ele:
						l=mid+1
					else:
						l=u+1
						foundstatus=True 
						return HttpResponseRedirect(reverse('display_cont',args=(list_entries[mid],)))
			if not foundstatus:	
				if len(query_ele)==2:
					result=[i for i in list_entries if (query_ele==i[:2].title() or query_ele==i[:2].lower() or query_ele==i[:2].upper())]
					foundstatus=True
					return render(request,'encyclopedia/index.html',{"entries":result,"message":"Suggested results found!!","search":Search()})	
			if not foundstatus:

				return render(request,'encyclopedia/index.html',{"entries":result,"message":"Search result not found!!","search":Search()})	
		else:
			return render(request,'encyclopedia/index.html',{"entries":util.list_entries(),"search":Search()})
	else:
		return render(request,'encyclopedia/index.html',{"entries":util.list_entries(),"search":Search()})
		
def display_cont(request,title):
	md=Markdown()
	all_entries=util.list_entries()
	if title.title() in all_entries  or title.upper() in all_entries:
		content=util.get_entry(title)
		html=md.convert(content)
		content={"content":html,"search":Search(),"title":title}
		return render(request,"encyclopedia/display_content.html",content)
	else:
		return render(request,"encyclopedia/display_content.html",{"message":"Entry Not Found!!","search":Search()})
def add(request):
	if request.method=="POST":
		form=NewEntry(request.POST)
		if form.is_valid():
			title=form.cleaned_data["title"]
			content=form.cleaned_data["content"]
			if title.title() not in util.list_entries():
				util.save_entry(title.title(),content)
				return HttpResponseRedirect(reverse("index"))
			else:
				return render(request,"encyclopedia/create.html",{"message":"Page title already exists.Please change your page title and add again!!","form":form,"search":Search()})
		else:
			return render(request,"encyclopedia/create.html",{"error":"Invalid! Try Again","form":form})
	else:
		return render(request,"encyclopedia/create.html",{"form":NewEntry(),"search":Search()})

def random(request):
	if request.method=='GET':
		entry=choice(util.list_entries())
		md=Markdown()	
		content=util.get_entry(entry)
		html=md.convert(content)
		return HttpResponseRedirect(reverse("display_cont",args=(entry,)))
#------------------------------------------------------------------------
def edit(request,page_title):
	if request.method=="GET":
		page=util.get_entry(page_title)
		return render(request,"encyclopedia/edit.html",{"search":Search(),"edit":NewEntry(initial={'content':page,'title':page_title})})
	else:
		return HttpResponseRedirect(reverse("display_cont"))
#----------------------------------------------------------------		
def update(request):
	if request.method=='POST':	     
		form=NewEntry(request.POST)
		if form.is_valid():
			title=form.cleaned_data['title']
			content=form.cleaned_data['content']
			util.save_entry(title,content)
			return HttpResponseRedirect(reverse("display_cont",args=(title,)))
		else:
			return render(request,"encyclopedia/edit.html",{"search":Search(),"form":NewEntry(initial={'content':page,'title':title})})