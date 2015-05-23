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
from django.contrib.auth.decorators import *
from django.views.decorators import *
from models import *
#表单
#test


#
#the following part is for the teacher to
# login,createClass and checkInfo
#
#
def teacherRegister_view(request):
    return render_to_response('register.html',{'title':'SmartClass Teacher'})



#---------------group algorith part-----------------------
import random
def check_group_or_not(course,pnumber):
	if isinstance(course,Course) and pnumber:
		if course.number_student == pnumber:
			return True
		return False
	return False

def random_group(slist,question,pid):
	max_group = question.max_group
	group_size = question.number_per_group
	qid = question.id
	qname = question.name
	gout = Group_Outcome.objects.filter(pid=pid).order_by('gid')
	gid = -1
	if len(gout):
		for g in gout:
			if g.gid > gid:
				gid = g.gid

	if slist and max_group and group_size:
		i = 0
		totalstudent = len(slist)
		snumber = totalstudent
		kick_list = []
		while snumber > 0 and max_group>0:
			i+=1
			gid =gid+ 1
			#snumber = len(slist)
			j = group_size
			Group_Question_Outcome(gid = gid,pid = pid,qid = qid,qname = qname).save()
			while j  > 0 and snumber>0:
				rand = random.randint(0,totalstudent-1)
				if rand in kick_list :
					continue
				student = slist[rand]
				gout = Group_Outcome(gid = gid,sid = student.id,pid = pid,qid = qid,qname = qname)
				gout.save()
				Group_Student_Outcome(gid=gid,sid = student.id,pid = qid,sname=student.username).save()
				j -=1
				snumber-=1
				#slist.remove(rand)	
				kick_list.append(rand)
				print 'kick number is :' ,rand
			print 'gid is ',gid
			max_group-=1
		print 'befor chage information,,',len(slist)
		if len(slist):
			for s in slist:
				print 'for student sid is : ',s.id
				q = Groupinfo_Question.objects.filter(sid=s.id,pid=pid)
				if len(q) :
					print len(q), ' is the length of q'
					for t in q :
						t.priority = -1
						print 'information change '
						t.save()

		return True	
	return False

#------random kick out---------------------------------
def random_chose(studentlist,kick_number,pid):
	if studentlsit and kick_number :
		number = len(studentlist)
		kick_list=[]
		while kick_number>0:
			kick = random.randint(0,number-1)
			if kick in kick_list:
				continue
			if change_student_status(studentlist[kick],pid):
				#studentlist.remove(kick)
				kick_list.append(kick)
				#number-=1
				kick_number -=1
			#else:	
				#return False
		#return studentlist
		return True
	return False

def change_student_status(student,pid):
	if isinstance(student,MyUser) and student.utype=='student':
		sid = student.id
		sq0 = Groupinfo_Question.objects.filter(sid= sid,pid=pid,priority=0)
		sq1 = Groupinfo_Question.objects.filter(sid= sid,pid=pid,priority=1)
		sq2 = Groupinfo_Question.objects.filter(sid= sid,pid=pid,priority=2)
		sq3 = Groupinfo_Question.objects.filter(sid= sid,pid=pid,priority=3)
		if sq0:
			return False
		elif sq2 is None and sq3 is None:
			sq0 = Groupinfo_Question(pid = pid,sid = sid,priority=0)
			sq0.save()
			#sq1.delete()
			sq1.priority=-1
			sq1.save()
			return True
		elif sq1 and sq2 :
			sq2.priority = 1
			qid = sq2.qid
			q = Project_Question.objects.get(id = qid)
			q.first_number+=1
			q.save()
			#sq1.delete()
			sq1.priority = -1
			sq1.save()
			return True
		elif sq1 and sq3:
			sq3.priority = 1
			qid = sq3.qid
			q = Project_Question.objects.get(id=qid)
			q.first_number+=1
			q.save()
			#sq1.delete()
			sq1.priority = -1
			sq1.save()
			return True
		return False
	return False

def ranked_grouping(course,project):
	if isinstance(course,Course) and isinstance(project,Project):
		number_student = project.number_student
		qlist = get_question_by_project(project.id)
		#---get every question's first_choice student list---
		while number_student>0:
			project_statistic(project,course)
			top_question = get_top_question(qlist)
			if top_question is None:
				break
			student_list = get_student_list_by_question(top_question.id)
			#begin of top_question group
			if top_question and number_student and student_list:
				max_number = top_question.max_group*top_question.number_per_group
				join_number = top_question.first_number
				if len(student_list) == top_question.first_number:
					join_number = top_question.first_number
				else :
					join_number = len(student_list)
				if join_number <= max_number :
					random_group(student_list,top_question,project.id)
					number_student -= join_number
				else :
					kick_number = join_number - max_number
					slist = None
					if  random_chose(student_list,kick_number,project.id):
						slist = get_student_list_by_question(top_question.id)
					if slist is not None:
						random_group(slist,top_question,project.id)
						number_student-=max_number
					else :
						return None
				#clear_question(top_question,project.id)
				#qlist.remove(top_question)
				top_question.first_number = -1
				top_question.save()
			else:
				return None	
		return None
	return None

def get_student_list_by_question(qid):
	if qid:
		slist = Groupinfo_Question.objects.filter(qid=qid,priority__in=[0,1])
		idlist = [t.sid for t in slist]
		if len(slist):
			ulist = MyUser.objects.filter(id__in=idlist)
			return ulist
		return None
	return None

def get_top_question(qlist):
	if len(qlist):
		max_tmp = -1
		tmp = None
		for q in qlist:
			if isinstance(q,Project_Question):
				if q.first_number > max_tmp:
					max_tmp = q.first_number
					tmp = q
		return tmp
	return None

#def random_group_method(project,course):
	


class question_():
	pid= None
	qid = None
	first_number = None
	second_number = None
	third_number = None
	status = None
class groupinfo():
	sid = None
	pid = None
	qid = None
	priority = None
	status = None
class student():
	sid = None
	status = None
list_question_ = []
list_groupinfo = []

def get_statistics(project,course):
	if project and course :
		pid = project.id
		quest = get_question_by_project(pid)
		
		for q in quest:
			tmp = question_(pid=q.pid,qid=q.id,first_number=q.first_number,second_number=q.second_number,third_number=q.third_number)
			list_question_.append(tmp)
		gi = Groupinfo_Question.objects.filter(pid=pid)
		for t in gi:
			tmp = groupinfo(sid=t.sid,pid=t.pid,qid=t.qid,priority=t.priority)
			list_groupinfo.append(tmp) 
		return True
	return False

def rank_group(project,course):
	if isinstance(project,Project) and isinstance(course,Course) and project and course :
		get_statistics(project,course)
		begin_random_gouping(project,course)
#-------end of grouping algorith-----------------------------
#-------------------------------------------Test statistics-------------
# statistic of test
#
#----------------------------------		
def test_statistic(course,test):
	if isinstance(course,Course) and isinstance(test,Test) and course and test:
		print 'begin statistic '
		tid = test.id
		testanswer = Test_Answer.objects.filter(tid__exact=tid)
		if len(testanswer):
			for t in testanswer:
				aid = t.aid
				sta = Student_Test_Answer.objects.filter(aid=aid ,tid=tid)
				accuracy = 0
				if len(sta):
					for st in sta :
						accuracy+=st.outcome
				studnumber = test.number_student
				outcome = (float(accuracy)/float(studnumber))*100
				t.accuracy = outcome
				t.save()
			print 'end statistic'
			return True
		return False

def student_test_statistic(course,test,user):
	if isinstance(course,Course) and isinstance(test,Test)and isinstance(user,MyUser)  and course and test and user:
		print 'begin student statistic'
		tid = test.id
		st = Student_Test.objects.filter(tid=tid)
		print 'len of st: ',len(st)
		for s in st:
			
			sta = Student_Test_Answer.objects.filter(sid = s.sid ,tid=tid)
			accuracy = 0
			if len(sta):
				for t in sta :
					accuracy +=t.outcome
				qnumber = test.question_number
				outcome = (float(accuracy)/float(qnumber))*100
				s.accuracy = outcome
				s.save()
				print 'end student statistic'
		return False
	return False
#--------------------------------------------------------------------------------------------------------------------------------------
#
#teacher api part
#
#--------------------------------------------------------------------------------------------------------------------------------------
@csrf_exempt
def teacher_register(request):
    username=None
    password=None
    password2=None
    errors=[]
    flag = False
    if request.method == 'GET':
	return render_to_response('register.html',RequestContext(request,{'title':'TeacherRegister'}))	
    elif request.method == 'POST' :
        username = request.POST.get('username','')
        password =request.POST.get('password','')
        password2 = request.POST.get('password2','')
        #user = MyUser.objects.filter(username = username)
        user = authenticate(username=username,password=password)
        if  user:
            errors.append("User Already exists.")
            c = RequestContext(request,{'title':'UserExists','errors':errors})
            return render_to_response('register.html',c)
        else :
            if not username:
                errors.append("Please Enter username.")
            if not password :
                errors.append('Please enter password.')
            if not password2 :
                errors.append('Please re-enter password.')
            if password is not None and password2 is not None:
                if password!=password2:
                    errors.append('password did not the same')
                else : 
                    flag=True
            if username and password and password2 and flag :
                user = MyUser.objects.create_user(username=username,password=password,utype='teacher')
                user.is_active=True
                user.save
                nuser = authenticate(username=username,password=password)
                user_login(request,nuser)
                request.session['user']=user.id
                request.session['type'] = 'teacher'
                return render_to_response('home.html',RequestContext(request,{'title':'TeacherHome'}))
            return render_to_response('register.html',{'title':'RegisterError','errors':errors})

            
        #check if the user already existed
        
@csrf_exempt
def teacher_login1(request):
    errors=[]
    if request.method=='POST':
	username = request.POST['username']
	password = request.POST['password']
        ##debug
#	print "username is :",username," password is : ",password
        user = MyUser.objects.get(username=username)
 #       print "user.password is : ",user.password.encode('utf8')
        if user is not None:
            if user.is_active:
                if user.password==password:
                    reqeust.session['user']=user.id
	            return HttpResponseRedirect('../home')
		else :
		    errors.append('password is wrong')
	    else :
		errors.append('user is not active')
	else :
	    errors.append('username does not exist')
	return render_to_response('login.html',RequestContext(request,{'title':'LoginError','errors':errors}))
    else:
	 return HttpResponse('method wrong')
     
    ##check if the user exists
    user = Teacher.objects.filter(teach_id__exact = username, password = password)
    return HttpResponseRedirect('/teacherIndex/')

@csrf_exempt
def teacher_login(request):
    errors=[]
    if request.method=='POST':
	username = request.POST['username']
	password = request.POST['password']
        ##debug
	#print "username is :",username," password is : ",password
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                    user_login(request,user)
	#	    print "user logined: ",request.user.username.encode('gb2312')," type is : ",request.user.utype.encode('gb2312')
                    request.session['user']=user.id
	            return HttpResponseRedirect('../home')
	    else :
		errors.append('user is not active')
	else :
	    errors.append('username or password is wrong')
	return render_to_response('login.html',RequestContext(request,{'title':'LoginError','errors':errors}))
    elif request.method=='GET':
	return render_to_response('login.html',RequestContext(request,{'title':'TeacherLogin'}))
	 #return HttpResponse('method wrong')
     
#-----------teacher logout
@csrf_exempt
def teacher_logout(request):
	user = request.user
	#print 'user is : ',user.username
	user_logout(request)
	return HttpResponseRedirect(reverse('teacher_login'))

#------------------------
def myauthenticate(username,password):
    user = MyUser.objects.get(username=username,password=password)
    return user
def mylogin(request,user):
    request.session['user']=user.id
    return

@csrf_exempt
def teacherIndex(request):
    ##get the username for the session
    return HttpResponse('<h>Hello Teacher</h>')           

@csrf_exempt
@login_required
def teacher_home(request):
    #get the courses the teacher teaches
    user=request.user
    #print "at home user is :",user.username
    course=Course.objects.filter(teacher=user.id)
  #  for c in course :
   #     print "course Name: ",c.name.encode('gb2312')
    return render_to_response('home.html',RequestContext(request,{'title':'TeacherHome','courses':course}))

@csrf_exempt
@login_required
def create_course(request):
    if  request.method == 'POST':
        name=request.POST.get('course-name','')
     #   print "course is : ", name
	number = request.POST.get('max-number','')
        try:
            c = Course.objects.get(name__exact=name)
            if c:
	        message="Class Already Exist!"
	        return render_to_response('home.html',RequestContext(request,{'title':'TeacherHome','message':message}))

        except:
           print "course does not exists"
        user = request.user
        
	cou = Course(name=name,teacher=user.id)#,max_number=number)
        cou.save()
        #yield render_to_response('home.html',RequestContext(request,{'title':'TeacherHome','message':'Create Success!'}))
        return HttpResponseRedirect(reverse('teacher_home'))

@csrf_exempt
@login_required
def teacher_course(request,course_name):
	cname = course_name
        #cname = request.GET.get('course','')
    #try:
        c = Course.objects.get(name=cname)
	cid = c.id
	#get the test of this course
	tests = Test.objects.filter(course = cid)
	#get the bighomework of the course
	project = Project.objects.filter(course= cid)
	request.session['course']=cname
	request.session['courseid']=cid
      #  print "the get corse is :",c.name.encode('gb2312')
        return render_to_response('course.html',RequestContext(request,{'title':'CourseHome','course':c,'tests':tests,'projects':project}))
    #except :
     #   return HttpResponse('course not exists')    
@csrf_exempt
@login_required
def teacher_course_by_id(request,courseId):
	course = Course.objects.get(id=courseId)
	tests = Test.objects.filter(course = course.id)
	projects = Project.objects.filter(course=course.id)
	request.session['courseObject'] = course
	request.session['course'] = course.name
	request.session['courseid'] = course.id
	return render_to_response('course.html',RequestContext(request,{'title':course.name,'course':c,'tests':tests,'projects':projects}))


#-----------course/project
class goutcomeform():
	def __init__(self,gid,qname,studentlist):
		self.gid = gid+1
		self.qname = qname
		self.studentlist = studentlist	
@csrf_exempt
@login_required
def course_project(request,project_name):
	pname = project_name
	p = Project.objects.get(name=pname)
	request.session['project']=p.id
	request.session['project_name']=p.name
	questions = Project_Question.objects.filter(pid=p.id)
	studentlist=[]
	gout = Group_Outcome.objects.filter(pid=p.id).order_by('gid')
	gqout = Group_Question_Outcome.objects.filter(pid = p.id).order_by('gid')
	goutcomelist = []
	for t in gqout:
		gstudentlist = Group_Student_Outcome.objects.filter(gid=t.gid,pid=t.qid)
		gsname = [gs.sname for gs in gstudentlist]
		print 'gsname list : ',gsname
	#	gstr = ''
	#	for sn in gsname:
	#		tmp = " ".join(sn)
	#		gstr=gstr.join(tmp)
	#	print gstr
		goutcome1 = goutcomeform(t.gid,t.qname,gsname)
		goutcomelist.append(goutcome1)
		#studentlist.append(gstr)
	beginstatus=None
	endstatus=None
	rollbackstatus=0
	if p.status==1:
		beginstatus=1
	elif p.status==2:
		endstatus=1
	elif p.status==3:
		rollbackstatus=1
	print 'group outcome len : ',len(goutcomelist)
	c = RequestContext(request,
		{'title':'Project',
		 'project':p,
		 'questions':questions,
		 'beginstatus':beginstatus,
		 'endstatus':endstatus,
		 'rollbackstatus':rollbackstatus,
		 'group_outcome':goutcomelist
		})
	return render_to_response('project.html',c)


def project_student_groupinfo(request):
	if request.method == 'POST':
		return HttpResponse('return ')
	return HttpResponse('method wrong')

def get_student_groupinfo_by_project(project,sid):
	if project and isinstance(project,Project) and sid :
		gq  = Groupinfo_Question.objects.filter(pid = project.id,sid = sid)
		return None
	return None		
#--------------------add question----
@csrf_exempt
@login_required
def project_add_question(request):
	if request.method=='POST':
		qid = request.POST.get('question_id','')
		pid = request.session['project']
		qname = request.POST.get('question_name','')
		number_per_group = request.POST.get('per_number','')
		max_group = request.POST.get('max_group','')
		pad = Project_Question.objects.filter(name=qname)
		pname = request.session['project_name']
		if len(pad):
			return HttpResponse('question already exist')
		else :
			q = Project_Question(name=qname,qid=qid,pid=pid,number_per_group=number_per_group,max_group=max_group)
			q.save()
			project = get_project_by_id(pid)
			project.status = 1
			project.save()
			return HttpResponseRedirect(reverse('course_project',args=(pname,)))
			
@csrf_exempt
@login_required
def course_begin_group(request):
	if request.method == 'POST':
		pid = request.session['project']
		project = get_project_by_id(pid)
		pname= request.session['project_name']
		if project:
			project.status = 2
			project.save()
			return HttpResponseRedirect(reverse('course_project',args=(pname,)))
		return HttpResponse('project none')
	return HttpResponse('method is wrong')

@csrf_exempt
@login_required
def course_end_group(request):
	if request.method == 'POST':
		pid = request.session['project']
		cname=request.session['course']
		pname= request.session['project_name']
		course = get_course_by_name(cname)
		project = get_project_by_id(pid)
		if project:
			course = get_course_by_id(project.course)
			print 'status change: ',project.status
			project.status = 3
			project.save()
			#---统计组队信息
			project_statistic(project,course)
			#----进行分组----
			print 'before group'
			ranked_grouping(course,project)

			print 'end group'
			return HttpResponseRedirect(reverse('course_project',args=(pname,)))
		return HttpResponse('project none')
	return HttpResponse('method is wrong')

#####----------------------------#########
###统计已提交的组队信息
###---------------------------------

def project_statistic(project,course):
	if isinstance(project,Project) and isinstance(course,Course):
		question = Project_Question.objects.filter(pid=project.id)
		for q in question:
			qid = q.id
			firstnumber = 0
			secondnumber=0
			thirdnumber = 0
			sq1 = Groupinfo_Question.objects.filter(qid = qid ,priority = 1)
			sq2 = Groupinfo_Question.objects.filter(qid = qid ,priority = 2)
			sq3 = Groupinfo_Question.objects.filter(qid = qid ,priority = 3)
			firstnumber = len(sq1)
			secondnumber = len(sq2)
			thirdnumber = len(sq3)
			if firstnumber == q.first_number:
				print 'first number is equal'
			else :
				print 'first not equal'
				q.first_number = firstnumber
			if secondnumber == q.second_number:
				print 'second number is equal'
			else:
				print 'second not equal'
				q.second_number = secondnumber
			if thirdnumber == q.third_number:
				print 'third number is equal'
			else:
				print 'third number is not equal'
				q.third_number = thirdnumber
			q.save()
		return True
	return False



@csrf_exempt
@login_required
def course_rollback_group(request):
	if request.method == 'POST':
		pid = request.session['project']
		project = get_project_by_id(pid)
		pname= request.session['project_name']
		if project:
			project.status = 1
			project.save()
			return HttpResponseRedirect(reverse('course_project',args=(pname,)))
		return HttpResponse('project none')
	return HttpResponse('method is wrong')
		
		
#--------course/test---------------------------
@csrf_exempt
@login_required
def course_test(request,test_name):
	tname = test_name
	#print 'testname is : ',tname.encode('gb2312')
	cid = request.session['courseid']
	t = Test.objects.get(name=tname,course=cid)
	answer_range=range(1,t.question_number+1)
	test_answer = Test_Answer.objects.filter(tid=t.id).order_by('aid')
	#print 'testanswer is: ',len(test_answer)
	beginstatus =None
	endstatus = None
	rollbackstatus = 0
	if t.status==2:
		beginstatus = 1
	elif t.status==3:
		endstatus = 1
	elif t.status == 4 :
		rollbackstatus = 1 
	c = RequestContext(request,{'title':'Test','test':t,'answer_range':answer_range,'test_answer':test_answer,'beginstatus':beginstatus,'endstatus':endstatus,'rollbackstatus':rollbackstatus})
	request.session['test']=t.id
	request.session['testname']=tname
	return render_to_response('testing.html',c)

@csrf_exempt
@login_required
def course_test_by_id(request,testId):
	test = Test.objects.get(id=testId)
	#courseId = request.session['courseid']
	answer_range = range(1,t.question_number+1)
	test_answer = Test_Answer.objects.filter(tid = test.id).order_by('aid')
	test_question = Test_Question.objects.filter(testId = test.id).order_by('questionId')
	beginstatus =None
	endstatus = None
	rollbackstatus = 0
	if t.status==2:
		beginstatus = 1
	elif t.status==3:
		endstatus = 1
	elif t.status == 4 :
		rollbackstatus = 1 
	context = RequestContext(request,{'title':'Test',
		'test':t,'answer_range':answer_range,'test_answer':test_answer,
		'beginstatus':beginstatus,'endstatus':endstatus,
		'rollbackstatus':rollbackstatus,'test_question':test_question})
	request.session['testObject'] = test
	request.session['testId'] = test.id
	request.session['testname'] = test.name
	return render_to_response('testing.html',context)


@csrf_exempt
def course_rollback_test(request):
	if request.method == 'POST':
		tname = request.session['testname']
		cid = request.session['courseid']
		test = get_test_by_name(tname,cid)
		if test:
			test.status = 2
			test.save()
			return HttpResponseRedirect(reverse('course_test',args=(tname,)))
		return HttpResponse('test is none')
	return HttpResponse('method is wrong')

@csrf_exempt
@login_required
def create_test(request):
	c=None
	if request.method=='POST':
		testname = request.POST.get('testname','')
		number = request.POST.get('q_number','')
		if 'course' in request.session:
			c = Course.objects.get(name=request.session['course'])
		if c :
			t = Test(name=testname,course = c.id ,question_number=number)
			t.save()
			c.number_test+=1
			c.save()
			return HttpResponseRedirect(reverse('teacher_course',args=(c.name,)))
	else :
		return HttpResponse('wrong method')

@csrf_exempt
@login_required
def test_add_question(request):
	testId = request.testId
	content = request.content
	questionId = request.questionId
	answer = request.answer
	if testId and questionId and content and answer:
		tq = Test_Question(testId=testId,questionId = questionId,content = content, answer = answer)
		tq.save()
		return HttpResponseRedirect(reverse('teacher_course_by_id',args=(request.session['courseObject'].id,)))
		return HttpResponseRedirect(reverse('course_test',args=(tname,)))



@csrf_exempt
@login_required
def course_begin_test(request):
	if request.method == 'POST':
		testname = request.session['testname']
		tid = request.session['test']
		test = get_test_by_id(tid)
		if test:
			test.status=3
			test.save()
			return HttpResponseRedirect(reverse('course_test',args=(testname,)))
		return HttpResponse('test is none')
	return HttpResponse('method is wrong')

@csrf_exempt
@login_required
def course_end_test(request):
	if request.method == 'POST':
		testname = request.session['testname']
		tid = request.session['test']
		test = get_test_by_id(tid)
		course = get_course_by_id(request.session['courseid'])
		if test:
			test.status=4
			test.save()
			test_statistic(course,test)
			student_test_statistic(course,test,request.user)
			return HttpResponseRedirect(reverse('course_test',args=(testname,)))
		return HttpResponse('test is none')
	return HttpResponse('method is wrong')


#----------add answers-----
@csrf_exempt
@login_required
def test_add_answer(request):
	if request.method=='POST':
		cid = request.session['course']
		tid = request.session['test']
		test = Test.objects.get(id=tid)
		tname = request.session['testname']
	#	print 'testname is: ',tname
		qnumber = test.question_number
		for i in range(1,qnumber+1):
			key = "".join(["answer_",str(i)])
			qkey = "".join(["question_",str(i)])
			ckey = "".join(["choice_",str(i)])
	#		print 'key is: ',key
			aid = i
			answer = request.POST.get(key,'')
			question = request.POST.get(qkey,'')
			choice = request.POST.get(ckey,'')
			ta = Test_Answer.objects.filter(tid=tid,aid=aid)
			tq = Test_Question.objects.filter(testId = tid,questionId = i)
			if len(ta) or len(tq):
				continue
				#return HttpResponse('answer %d already exists' % i)
			else :
				temp = Test_Answer(tid = tid,aid=aid,answer=answer)
				temp.save()
				tmp = Test_Question(testId = tid,questionId = i ,answer = answer,content = question,choice = choice)
				tmp.save()
		test.status = 1
		return HttpResponseRedirect(reverse('course_test',args=(tname,)))


#-------------create_project
@csrf_exempt
@login_required
def create_project(request):
	c=None
	if request.method =='POST':
		name = request.POST.get('projectname','')
	#	print 'course name is : ',request.session['course']
		if 'course' in request.session:
			c = Course.objects.get(name=request.session['course'])
		if c :
			w = Project.objects.filter(course = c.id ,name = name )
			if len(w):
				return HttpResponse('project already exists')
			else:
				w = Project(name=name,course=c.id,pid=10,status = 0)
				w.save()
				c.number_project +=1
				c.save()
				return HttpResponseRedirect(reverse('teacher_course',args=(c.name,)))
		else :
			return HttpResponse('course not exist')
						 


#####------delete api part-----------

#------delete course
@csrf_exempt
def delete_course(request):
	if request.method=='POST':
		cid = request.POST.get('course','')
#		print 'delete cid is: ',cid
		remove_course_by_id(cid)
		return HttpResponseRedirect(reverse('teacher_home'))
@csrf_exempt
def delete_test(request):
	if request.method == 'POST':
		tid = request.POST.get('test','')
		test = get_test_by_id(int(tid))
		cname = request.session['course']
		remove_test_by_id(tid)
		course = get_course_by_name(cname)
		if course:
			course.number_test -=1
			course.save()
		return HttpResponseRedirect(reverse('teacher_course',args=(cname,)))

@csrf_exempt
def delete_project(request):
	if request.method == 'POST':
		pid = request.POST.get('project','')
		remove_project_by_id(pid)
		cname = request.session['course']
		course = get_course_by_id(request.session['courseid'])
		if course:
			course.number_project -=1
			course.save()
		return HttpResponseRedirect(reverse('teacher_course',args=(cname,)))

####------------------remove api ---------------
##
##
##
#####-----------------------------------------

def remove_course_by_id(cid):
	if cid:
		course = Course.objects.filter(id=cid)
		for c in course:
			remove_test_by_course(c.id)
			remove_project_by_course(c.id)
			c.delete()
def remove_test_by_course(cid):
	if cid:
		test = Test.objects.filter(course=cid)
		if len(test):
			for t in test:
				remove_answer_by_test(t.id)
				t.delete()
			return True
	return
def remove_test_by_id(tid):
	if tid:
		test = Test.objects.get(id=tid)
		if test:
			remove_answer_by_test(test.id)
			test.delete()
			return True

def remove_project_by_id(pid):
	if pid:
		project = Project.objects.get(id=pid)
		if project:
			remove_question_by_project(project.id)
			project.delete()
			return True

def remove_project_by_course(cid):
	if cid:
		project = Project.objects.filter(course = cid)
		if project:
			for p in project:
				remove_question_by_project(p.id)
				p.delete()
			return True
				
def remove_question_by_project(pid):
	if pid:
		pq = Project_Question.objects.filter(pid = pid)
		for p in pq :
			pq.delete()
		return True
def remove_answer_by_test(tid):
	if tid:
		ta = Test_Answer.objects.filter(tid=tid)
		if len(ta):
			for t in ta:
				t.delete()
			return True
@csrf_exempt
def login_view(request):
   #logout(request)
   errors=[]
   errors.append("login out")
   return render_to_response('login.html',RequestContext(request,{'titel':'TeacherLogin','errors':errors}))


#####--------general api -----------

#----get course test --------
def get_test(coursename):
	course = Course.objects.filter(name=coursename)
	if len(course)==0:
		return None 
	elif len(course)==1:
		test = Test.objects.filter(course__exact=course[0].id)
		return test
	return None
#------get course project----
def get_project(coursename):
	course = Course.objects.filter(name=coursename)
	if len(course)==1:
		project = Project.objects.filter(course=course[0].id)
		return project
	return None
####--------upload test files-------
@csrf_exempt
def test_upload_file(request):
	if request.method=='POST':
		uf = UpForm(request.POST,request.FILES)
		if uf.is_valid():
			testfile = uf.cleaned_data['testfile']
			test = get_test_by_name(request.session['testname'],request.session['courseid'])
			if test:
				test.files = testfile
				tid = test.id
				test._meta.get_field('files').upload_to='static/files/test/'+str(tid)+'/'
				test.files.name =str(tid)+'_'+ test.files.name
#				print 'url is: ',test.files.url,' ',test.files.name,' ',test.files.path,' ',test.files
				test.file_url='files/test/'+str(tid)+'/'+test.files.name
				test.status = 2
				test.save()
				return HttpResponseRedirect(reverse('course_test',args=(test.name,)))
			else:
				return HttpResponse('test is None')
		else :
			return HttpResponse('form is not valid')
	else:
		return HttpResponse('method is wrong')

class UpForm(forms.Form):
	testfile = forms.FileField()
#-----------------access database api ---
#
##
#
#
#---------------------------------------------
def get_test_by_name(testname,cid):
	if testname and cid:
		
		test = Test.objects.filter(name=testname,course=cid)
		if len(test):
			return test[0]
	return None

def get_test_by_id(tid):
	if tid:
#		print 'tid is : ',tid
		test = Test.objects.filter(id=tid)
		if len(test):
			return test[0]
	return None

def get_project_by_id(pid):
	if pid:
		p = Project.objects.filter(id=pid)
		if len(p):
			return p[0]
	return None
def get_project_by_name(pname,cid):
	if pname and cid:
		project = Project.objects.filter(name=pname,course=cid)
		if len(project):
			return project[0]
	return None
	

def get_course_by_id(cid):
	if cid:
		course = Course.objects.get(id=cid)
		if course:
			return course
		else:
			return None

def get_course_by_name(cname):
	if cname:
		c = Course.objects.filter(name = cname)
		if len(c):
			return c[0]
		return None
	return None

def get_project_by_course(cid):
	if cid:
		c = Course.objects.filter(id = cid)
		if len(c):
			plist = Project.objects.filter(course = cid)
			if len(plist):
				return plist
			return None
		return None
	return None

def get_question_by_project(pid):
	if pid:
		pq = Project_Question.objects.filter(pid = pid)
		if len(pq):
			return pq
		return None
	return None
def get_question_by_name(qname,pid):
	if qname and pid:
		question = Project_Question.objects.filter(name=qname,pid=pid)
		if len(question):
			return question[0]
		return None
	return None
#----------------------EOF
#
#
#
@csrf_exempt
def teacher_createProjectQuestion(request):
	if request.method=='POST':
		qid = request.POST.get('question_id','')
		pid = request.session['project']
		qname = request.POST.get('question_name','')
		number_per_group = request.POST.get('per_number','')
		max_group = request.POST.get('max_group','')
		# pad = Project_Question.objects.filter(name=qname)
		pad = ProjectQuestion.objects.filter(name = qname )
		pname = request.session['project_name']
		describe = request.POST.get('describe','')
		if len(pad):
			return HttpResponse('question already exist')
		else :
			# q = Project_Question(name=qname,qid=qid,pid=pid,number_per_group=number_per_group,max_group=max_group)
			q = ProjectQuestion(name = qname,questionId = qid,projectId = pid,numberPerGroup = number_per_group,maxGroup = max_group,describe = describe)
			q.save()
			qp = Project_Question(name=qname,qid=qid,pid=pid,number_per_group=number_per_group,max_group=max_group)
			qp.save()
			
			project = get_project_by_id(pid)
			project.status = 1
			project.save()
			return HttpResponseRedirect(reverse('course_project',args=(pname,)))
