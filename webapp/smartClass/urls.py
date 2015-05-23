from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^test/$','smartClass.views.test'),
    #url(r'^testserver/','testserver.views.index'),
    url(r'^login/$','smartClass.views.login'),
    url(r'^register/$','smartClass.views.register'),
    url(r'^studentInfo','smartClass.views.studentInfo'),
    url(r'^teacher/$','smartClass.views.teacherIndex'),
    #url(r'^teacher/login/$','smartClass.views.teacher_login'),
    url(r'^teacher/register/$','smartClass.views.teacher_register'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATICFILES_DIRS}),
    url(r'^testform/$','smartClass.views.testform'),

)
urlpatterns += patterns('smartClass.teacherViews',
	url(r'^teacher/home/$','teacher_home',name='teacher_home'),
	url(r'^teacher/login/$','teacher_login',name='teacher_login'),
	url(r'^teacher/logout/$','teacher_logout',name='teacher_logout'),
	url(r'^teacher/register/','teacher_register',name='teacher_register'),
	url(r'^teacher/delete/course/$','delete_course',name='delete_course'),
	url(r'^teacher/course/project/end/$','course_end_group',name='course_end_group'),
	url(r'^teacher/course/project/begin/$','course_begin_group',name='course_begin_group'),
	url(r'^teacher/course/delete/test/$','delete_test',name='delete_test'),
	url(r'^teacher/course/delete/project/$','delete_project',name='delete_project'),
	url(r'^teacher/course/rollback/test/$','course_rollback_test',name='course_rollback_test'),
	url(r'^teacher/course/rollback/project/$','course_rollback_group',name='course_rollback_group'),
	url(r'^teacher/course/create/test/$','create_test',name='create_test'),
	url(r'^teacher/course/create/project/$','create_project',name='create_project'),	
	url(r'^teacher/create/course/$','create_course',name='create_course'),
	# url(r'^teacher/course/project/add/question/$','project_add_question',name='project_add_question'),
	url(r'^teacher/course/project/add/question/$','teacher_createProjectQuestion',name='project_add_question'),
	url(r'^teacher/course/project/(?P<project_name>\w+)/$','course_project',name='course_project'),
	url(r'^teacher/course/test/uploadfile/$','test_upload_file',name='test_upload_file'),
	url(r'^teacher/course/test/begin/$','course_begin_test',name='course_begin_test'),
	url(r'^teacher/course/test/end/$','course_end_test',name='course_end_test'),
	url(r'^teacher/course/test/add/answer/$','test_add_answer',name='test_add_answer'),
	url(r'^teacher/course/test/(?P<test_name>.+)/$','course_test',name='course_test'),
	url(r'^teacher/course/(?P<course_name>\w+)/$','teacher_course',name='teacher_course'),
	)

urlpatterns += patterns('smartClass.studentViews',
#	url(r'^teacher/logout/$','teacher_logout',name='teacher_logout'),
	url(r'^student/course/project/$','student_course_project'),
	url(r'^student/course/test/answer/$','student_test_answer'),
	url(r'^student/course/project/groupinfo/$','student_project_groupinfo'),
	url(r'^student/course/project/question/$','student_project_question'),

	url(r'^student/allcourse/$','student_all_course'),
	url(r'^student/mycourse/$','student_my_course'),
	url(r'^student/joincourse/$','student_join_course'),
	url(r'^student/course/test/$','student_course_test'),

)


#new api for app
urlpatterns += patterns('smartClass.studentViews',
	url(r'^student/get_project_by_course.json','get_project_by_course'),
	url(r'^student/get_test_by_course.json','get_test_by_course'),
	url(r'^student/get_test_question_by_testid.json','get_test_question_by_testId'),
	url(r'^student/submit_test_answers.done','submit_test_answer'),
	url(r'^student/get_course_by_studentid.json','get_student_course'),
	url(r'^student/register/$','student_register'),
	url(r'^student/login/$','student_login'),
	url(r'^student/login.done','student_login'),
	url(r'^student/register.done','student_register'),
	url(r'^student/get_group_created.json','get_group_create_by_self'),
	url(r'^student/get_group_invited_me.json','get_group_invited_me'),
	url(r'^student/get_project_question_by_projectId.json','getProjectQuestionByProjectId'),
	url(r'^student/get_all_student_except_myself.json','getAllStudentExceptMyself'),
	url(r'^student/add_project_group_by_projectId.done','add_project_group'),
	url(r'^student/submit_test_answer_by_testQuestionId.done','submit_test_answer_by_testQuestionId'),
	url(r'^student/changePassword.done','changePassword'),
	url(r'^student/logout.done','student_logout'),
	url(r'^student/changeRealName.done','student_changeRealName'),
	url(r'^student/signToServer.done','signInByDateAndId'),
	url(r'^student/getCourseTeacher.json','getTeacherByCourse'),
	url(r'^student/getCourseSignId.json','getCourseSignId')
	)

