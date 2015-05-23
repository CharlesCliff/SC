#coding=utf-8
from django.shortcuts import render,render_to_response,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from models import Student,Teacher,Course,Sign,Answer,Group,stud_course_entry,MyUser,Test,Project,Project_Question
from models import Test_Answer,Student_Test_Answer,Groupinfo_Question,Groupinfo_Partner,Group_Outcome,Student_Test
from models import Group_Question_Outcome,Group_Student_Outcome
import json
from django.views.decorators.csrf import csrf_exempt
import simplejson
from django.contrib.auth.models import User,Group,Permission
from django.contrib.auth import authenticate,login as user_login,logout as user_logout
from django.contrib.contenttypes.models import ContentType
from django import template
from django.template import Template,Context
from django.template.loader import get_template
from django import forms
from django.core.urlresolvers import reverse
from django.core.files.base import ContentFile
from models import Student_Course_Rela
from models import *
from models import Project_Group
from models import ProjectQuestion,Student_TestQuestion_Answer,Student_Sign,Course_Sign
import datetime
@csrf_exempt
def student_register(request):
	if request.method == 'POST':
		username = request.POST.get('username','')
		password = request.POST.get('password','')
		realname = request.POST.get('realname','')
		print username,password,realname
		user = authenticate(username = username,password=password)
		if user is not None:
			return HttpResponse(json.dumps({'result':0,'message':'user already exists'}))
		else :
			if username and password and realname:
				print username,password,realname
				user = MyUser.objects.create_user(username = username,password=password,utype='student',first_name = realname,last_name=realname)
				user.is_active=True
				user.save
				userDict = [user.toDict()]
				return HttpResponse(json.dumps({'result':1,'message':'regster success','userList':userDict}))
	else :
		return HttpResponse(json.dumps({'result':false,'message':'wrong method'}))
####student login
@csrf_exempt
def student_login(request):
	if request.method=='POST':
		#先登出
		student_logout(request)
		username = request.POST.get('username','')
		password = request.POST.get('password','')
		print 'before authenticate',username,password
		user = authenticate(username=username,password=password)
		if user is not None :
			if user.is_active:
				user_login(request,user)
				userDict = [user.toDict()]
				return HttpResponse(json.dumps({'result':1,'message':'login success','userList':userDict}))
			else :
				return HttpResponse(json.dumps({'result':0,'message':'user not active'}))
		else :
			return HttpResponse(json.dumps({'result':0,'message':'user not exists or password is wrong'}))
	else :
		return HttpResponse(json.dumps({'result':false,'message':'wrong method'}))

@csrf_exempt
def student_logout(request):
	if request.method == 'POST':
		user = request.user
		user_logout(request)
		return HttpResponse(json.dumps({'result':True,'message':'logout successfully'}))
	else :
		return HttpResponse(json.dumps({'result':False,'message':'wrong method'})) 

@csrf_exempt
def student_changeRealName(request):
	if request.method == 'POST':
		user = request.user
		realname = request.POST.get('realname','')
		if user and realname:
			user.first_name = realname
			user.last_name = realname
			user.save
			return HttpResponse(json.dumps({'result':True,'message':'change realname successfully'}))
		else :
			return HttpResponse(json.dumps({'result':False,'message':' user not exists'})) 
	else :
		return HttpResponse(json.dumps({'result':False,'message':'wrong method'})) 


#get all course list
@csrf_exempt
def student_all_course(request):
	if request.method == 'POST':
#       print 'sessionid is : ',request.session._session_key
		clist =  Course.objects.all()
		cname = [c.name for c in clist]
#       for s in cname:
#           print s.encode('gb2312')
		response =  HttpResponse(json.dumps({'all_course_list':cname}))
		response.set_cookie('username','hello me')
		return response

#----------get student course-----------------------
@csrf_exempt
def student_my_course(request):
	if request.method == 'POST':
		user = request.user
				
		uid = user.id
			
		entry = stud_course_entry.objects.filter(student = uid)
		if len(entry):
			cids = [e.course for e in entry]
		#   for s in cids:
		#       print 'cid is: ',s
			cours = Course.objects.filter(id__in=cids)
			cname = [c.name for c in cours]
		#   for s in cname :
		#       print 'course: ',s
			return HttpResponse(json.dumps({'my_course_list':cname}))
		else :
			return HttpResponse(json.dumps({'my_course_list':[]}))

@csrf_exempt
def student_join_course(request):
	if request.method=='POST':
		cname = request.POST.get('coursename','')
		#print 'course name is : ' , cname
		cour = Course.objects.filter(name=cname)
		if len(cour)==1:
			cid = cour[0].id
		#   print 'cid is : ',cid
		user = request.user
		uid = user.id
		course = cour[0]
		sc = stud_course_entry.objects.filter(course = cid,student= uid)
		if len(sc):
			return HttpResponse(json.dumps({'result':0,'message':'already joined'}))
		else :
			entry = stud_course_entry(course=cid,student=uid)
			entry.save()
			course.number_student+=1
			course.save()
			return HttpResponse(json.dumps({'result':1,'message':'join course success'}))
	else :
		return HttpResponse('wrong method')


@csrf_exempt 
def student_course_test(request):
	if request.method=='POST':
		coursename = request.POST.get('coursename','')
		test = get_test(coursename)
		if test is  None:
			return HttpResponse('test is none')
		if len(test):
			tname = [(t.name,t.question_number) for t in test]
			#for t in tname:
			#   print "".join(t)
			return HttpResponse(json.dumps({'result':1,'message':'get test success','testlist':tname}))
		else:
			return HttpResponse(json.dumps({'result':0,'message':'test not exist'}))
	else:
		 return HttpResponse('wrong method')

@csrf_exempt
def student_course_project(request):
	if request.method == 'POST':
		cname = request.POST.get('coursename','')
		if cname :

			c = get_course_by_name(cname)
			if c:
				cid = c.id
				plist = get_project_by_course(cid)
				sce = stud_course_entry.objects.filter(course=c.id).order_by('student')
				sid = [t.student for t in sce]
				stdlist=MyUser.objects.filter(id__in=sid)
				studentlist = [t.username for t in stdlist]
				if plist:
					projectlist = [p.name for p in plist]
					return HttpResponse(json.dumps({'result':1,'message':'get project list success','projectlist':projectlist,'studentlist':studentlist}))
	return HttpResponse('error')


#--------get all the questions of the project by coursename and project name
@csrf_exempt
def student_project_question(request):
	if request.method == 'POST':
		cname = request.POST.get('coursename')
		pname = request.POST.get('projectname')
#       print 'cname: ',cname,' , ',pname
		if cname and pname :
			c = get_course_by_name(cname)
			if c:
#               print 'course is: ',c.id
				p = Project.objects.filter(name=pname,course=c.id)
				project = get_project_by_name(pname,c.id)
				if project:
#                   print 'project id is: ',project.id
				#if len(p):
				#   project = p[0]
					qlist = get_question_by_project(project.id)
					#qlist = Project_Question.objects.filter(pid=project.id)
					if len(qlist):
#                       print 'qlist is not none'
						pq = [[t.name,t.max_group,t.number_per_group] for t in qlist]
#                       print 'pq length: ',len(pq)
						return HttpResponse(json.dumps({'result':1,'message':'get project question success','questionlist':pq}))
	return HttpResponse('error')



@csrf_exempt
def student_test_answer(request):
	if request.method == 'POST':
		cname = request.POST.get('coursename','')
		tname = request.POST.get('testname','')
		user=request.user
#       print 'user is : ',user.id
		if cname and tname :
			course = get_course_by_name(cname)
			if course:
#               print 'course is: ',course.name
				test = get_test_by_name(tname,course.id)
				if test:
#                   print 'test is: ',test.id
					#check if the answer has been added
					ta = Student_Test_Answer.objects.filter(tid=test.id,sid=user.id)
					if len(ta):
						return HttpResponse(json.dumps({'result':1,'message':'answers has been added'}))
#                   print 'tid is:' ,test.id
					rightanswer = Test_Answer.objects.filter(tid=test.id).order_by('aid')
					if len(rightanswer)==0:
#                       print 'no right answer'
						return HttpResponse(json.dumps({'result':0,'message':'answers has been added'}))
					test_answer = [a.answer for a in rightanswer]
#                   print 'len of test_answer is: ',len(test_answer)
					i=0
					for i in range(0,len(test_answer)):
						outcome = 0
						key = "".join(["answer",str(i+1)])
#                       print 'key is: ',key
						aw = request.POST.get(key,'')
#                       print 'answeri is ',aw
						if aw==test_answer[i]:
							outcome = 1
#                       print 'userid is: ',user.id
						sid = user.id
						tid=test.id
						aid = i+1
						sta = Student_Test_Answer(tid = tid,sid=sid,aid=aid,answer=aw,outcome=outcome)
						sta.save()
					test.number_student+=1
					test.save()
					st = Student_Test(tid = test.id,sid = user.id,accuracy = 0)
					st.save()
					return HttpResponse(json.dumps({'result':1,'message':'save answer success'}))
				else:
					return HttpResponse(json.dumps({'result':0,'message':'test is none'}))
		else :
			return HttpResponse(json.dumps({'result':0,'message':'cname,tname, answer or user is none'}))
					
import chardet
@csrf_exempt 
def student_project_groupinfo(request):
	if request.method == 'POST':
		req = json.loads(request.body,encoding='utf8')
		cname = req['coursename']
		pname = req['projectname']
		memberlist = req['memberlist']
		questionlist = req['questionlist']
		if cname and pname and len(memberlist) and len(questionlist) :
			course = get_course_by_name(cname)
			if course:
				cid = course.id
				project = get_project_by_name(pname,cid)
				if project :
					pid = project.id
					sid = request.user.id
					tmp = Groupinfo_Question.objects.filter(pid=pid,sid=sid)
					if len(tmp):
						return HttpResponse(json.dumps({'result':0,'message':'groupinfo already exist'}))
					i = 0
					for i in range(len(questionlist)):
						question = get_question_by_name(questionlist[i],pid)
						gq = Groupinfo_Question(pid=pid,sid=sid,qid=question.id,qname=question.name,priority=i+1,priority_bak = i+1)
						gq.save()
						if i==0 :
							question.first_number+=1
						if i==1 :
							question.second_number+=1
						if i==2 :
							question.third_number+=1
						print ' i is: ',i
						question.save()
					i = 0
					for i in range(len(memberlist)):
						partner = MyUser.objects.get(username=memberlist[i])
						gpartner= Groupinfo_Partner(pid=pid,sid=sid,partner=partner.id)
						gpartner.save()
					project.number_student +=1
					project.save()
				#   if check_group_or_not(course,project.number_student):
				#       ranked_grouping(course,project)
					return HttpResponse(json.dumps({'result':1,'message':'add groupinfo success'}))
				return HttpResponse(json.dumps({'result':0,'message':'project not exist'}))
			return HttpResponse(json.dumps({'result':0,'message':'course not exist'}))
		return HttpResponse(json.dumps({'result':0,'message':'parameter are none'}))
	return HttpResponse(json.dumps({'result':0,'message':'request method is wrong'}))





##-------------new api for student----------##
@csrf_exempt
def get_student_course(request):
	# studentId = request.REQUEST.get('studentId','')
	# courseIdList = Student_Course_Rela.objects.filter(studentId = studentId)
	# courseList = Course.objects.filter(id__in=courseIdList)
	# if request.method == 'POST':
		courseList = Course.objects.all()
		courseListDict = [c.toDict() for c in courseList]
		return HttpResponse(json.dumps({'courseList':courseListDict,'result':True}))
@csrf_exempt
def get_test_by_course(request):
	# if request.method == 'POST':
		courseId = request.REQUEST.get('courseId','')
		testList = Test.objects.filter(course = courseId)
		testDictList = [t.toDict() for t in testList]
		return HttpResponse(json.dumps({'testList':testDictList,'result':True}))


@csrf_exempt
def get_project_by_course(request):
	courseId = request.REQUEST.get('courseId','')
	projectList = Project.objects.filter(course = courseId)
	pjson = [p.toJSON() for p in projectList]
	projectDictList =[j.toDict() for j in projectList] 
	return HttpResponse(json.dumps({'result':True,'projectList':projectDictList}))
@csrf_exempt
def get_test_question_by_testId(request):
	testId = request.REQUEST.get('testId','')
	testQuestionList = Test_Question.objects.filter(testId = testId)
	testQuestionDictList = [tq.toDict() for tq in testQuestionList]
	return HttpResponse(json.dumps({'testQuestionList':testQuestionDictList,'result':True}))


#----submit data part
@csrf_exempt
def submit_test_answer(request):
	if request.method == 'POST':
		print request.POST
		testId = request.POST.get('testId','')
		answers = request.POST.getlist('answers','')
		print testId, ':',answers
		if testId and answers :
			print type(answers)
			for a in answers:
				print a
		return HttpResponse(json.dumps({'result':True,'message':'save successfully'}))
def submit_test_answer_by_testQuestionId(request):
	if request.method == 'POST':
		print request.POST
		testId = request.POST.get('testId','')
		testQuestionId = request.POST.get('testQuestionId','')
		answer = request.POST.get('answer','')
		user = request.user
		if testId and testQuestionId and answer and user:
			sta = Student_TestQuestion_Answer(testId = testId,testQuestionId = testQuestionId,studentAnswer = answer,studentId = user.id,correct = 0)
			sta.save()
			return HttpResponse(json.dumps({'result':True,'message':'save successfully'}))
		else :
			return HttpResponse(json.dumps({'result':False,'message':'params wrong'}))
	else:
		return HttpResponse(json.dumps({'result':False,'message':'method wrong'}))		
@csrf_exempt
def add_project_group(request):
	if request.method == 'POST':
		print request.POST
		projectId = request.POST.get('projectId','')
		# leader = request.POST.get('leader','')
		memberList = request.POST.getlist('memberList[]')
		chosenQuestionId = request.POST.get('chosenQuestionId','')
		print projectId,': ',chosenQuestionId,': ',len(memberList)
		status = 0
		leader = '1100012936'
		user = request.user
		if projectId and memberList and chosenQuestionId and user:
			groupId = getGroupIdByProjectId(projectId)
			print 'groupID:',groupId
			leader = user.username
			for member in memberList :
				print 'member: ',member
				group = Project_Group(projectId = projectId, leader = leader , member = member, chosenQuestionId = chosenQuestionId,status = status,groupId = groupId)
				group.save()
			return HttpResponse(json.dumps({'result':1,'message':'creating group success'}))
		else :
			return HttpResponse(json.dumps({'result':0,'message':'params unclear while creating group'}))

@csrf_exempt
def get_group_create_by_self(request):
	user = request.user
	username = user.username
	if user and username :
		grouplist = Project_Group.objects.filter(leader = username).order_by('groupId')
		if grouplist :
			groupDict = [g.toDict() for g in grouplist]
			return HttpResponse(json.dumps({'result':1,'groupList':groupDict,'message':'get my group success'}))
		else :
			return HttpResponse(json.dumps({'result':0,'message':'no group create by myself get'}))
	else :
		return HttpResponse(json.dumps({'result':0,'message':'unrecognized user'}))
@csrf_exempt
def get_group_invited_me(request):
	user = request.user
	username = user.username
	if user and username :
		grouplist = Project_Group.objects.filter(member = username)
		if grouplist :
			groupDict = [g.toDict() for g in grouplist]
			return HttpResponse(json.dumps({'result':1,'groupList':groupDict,'message':'get my group success'}))
		else :
			return HttpResponse(json.dumps({'result':0,'message':'no group invited me'}))
	else :
		return HttpResponse(json.dumps({'result':0,'message':'unrecognized user'}))




def getGroupIdByProjectId(projectId):
	projectlist = Project_Group.objects.filter(projectId = projectId)
	if projectlist :
		gId = -1
		for p in projectlist :
			if p.groupId > gId :
				gId = p.groupId
			else :
				continue
		return gId
	else :
		return 1

@csrf_exempt
def getProjectQuestionByProjectId(request):
	if request.method == 'POST':
		projectId = request.POST.get('projectId','')
		print 'projectId : ',projectId
		if projectId :
	 		projectQuestionList = ProjectQuestion.objects.filter(projectId = projectId)
		 	if projectQuestionList:
		 		projectQuestionDict = [p.toDict() for p in projectQuestionList]
		 		return HttpResponse(json.dumps({'result':1,'projectQuestionList':projectQuestionDict,'message':'get project'}))
		 	else:
				return HttpResponse(json.dumps({'result':0,'message':'no projectQuestionList'}))
		else:
			return HttpResponse(json.dumps({'result':0,'message':'unrecognized projectId'}))

@csrf_exempt
def getAllStudentExceptMyself(request):
	if request.method == "POST":
		user = request.user
		username = user.username
		if user and username:
			userList = MyUser.objects.exclude(username = username).filter(utype = 'student')
			if userList:
				userDict = [user.toDict() for user in userList]
				return HttpResponse(json.dumps({'result':1,'userList':userDict}))
			else :
				return HttpResponse(json.dumps({'result':0,'message':'userlist empty'}))
		else :
			return HttpResponse(json.dumps({'result':0,'message':'user is null'}))

@csrf_exempt
def changePassword(request):
	if request.method == 'POST':
		password = request.POST.get('password','')
		username = request.POST.get('username','')
		user = request.user
		username = user.username

		if username and password:
			print username
			user.set_password(password)
			user.save()
			return HttpResponse(json.dumps({'result':True,'message':'password changed'}))
		else :
			return HttpResponse(json.dumps({'result':False,'message':'user not exists'}))
	else :
		return HttpResponse(json.dumps({'result':False,'message':'method wrong'}))

@csrf_exempt
def signInByDateAndId(request):
	if request.method == 'POST':
		user = request.user
		signId = request.POST.get('signId','')
		print signId,'....',user.id
		# userId = 2
		if signId and user:
			userId = user.id
			#check if has been existed
			print "before check "
			if checkIfExistedSignIn(signId,userId):
				return HttpResponse(json.dumps({'result':False,'message':'already signed In','code':1001}))
			print "after check"
			print "userid:",userId
			signtime = datetime.datetime.now
			stu_sign = Student_Sign(studentId = userId,signId=signId,signDate = signtime)
			print "before save"
			stu_sign.save()
			print "after save"
			return HttpResponse(json.dumps({'result':True,'message':'sign successfully'}))
		else:
			return HttpResponse(json.dumps({'result':False,'message':'user or signId nil','code':1002}))
	else:
		return HttpResponse(json.dumps({'result':False,'message':'method wrong','code':1010}))


def checkIfExistedSignIn(signId,studentId):
	slist = Student_Sign.objects.filter(studentId=studentId,signId=signId)
	if slist and len(slist)>0:
		return True
	else :
		return False


@csrf_exempt 
def getCourseSignId(request):
	if request.method == 'POST':
		courseId = request.POST.get('courseId','')
		return HttpResponse(json.dumps({'result':True,'signId':1,'message':'get sign id successfully'}))

@csrf_exempt
def getTeacherByCourse(request):
	if request.method == 'POST':
		user = request.user
		teacherId = request.POST.get('teacherId','')
		print teacherId
		if user and teacherId:
			teacher = MyUser.objects.get(id=teacherId)
			if teacher :
				teacherDict = [teacher.toDict()]
				return HttpResponse(json.dumps({'result':True,'userList':teacherDict,'message':'get teacher success'}))
			else :
				return HttpResponse(json.dumps({'result':False,'message':'teacher not found'}))
		else:
			return HttpResponse(json.dumps({'result':False,'message':'user or teacherId nil'}))
	else:
		return HttpResponse(json.dumps({'result':False,'message':'wrong method'}))
#------------------
#
from json import dumps, loads, JSONEncoder

from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils.functional import curry

class DjangoJSONEncoder(JSONEncoder):
	def default(self, obj):
		if isinstance(obj, QuerySet):
			# `default` must return a python serializable
			# structure, the easiest way is to load the JSON
			# string produced by `serialize` and return it
			return simplejson.loads(serialize('json', obj))
		return JSONEncoder.default(self,obj)

def toJSON(obj):
   if isinstance(obj, QuerySet):
	   return simplejson.dumps(obj, cls=DjangoJSONEncoder)
   if isinstance(obj, models.Model):
	   #do the same as above by making it a queryset first
	   set_obj = [obj]
	   set_str = simplejson.dumps(simplejson.loads(serialize('json', set_obj)))
	   #eliminate brackets in the beginning and the end 
	   str_obj = set_str[1:len(set_str)-2]
   return str_obj
