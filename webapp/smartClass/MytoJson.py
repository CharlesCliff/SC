from django.utils import simplejson
from django.db import models
from django.core.serializers import serialize,deserialize
from django.db.models.query import QuerySet

class MyEncoder(simplejson.JSONEncoder):
     """ 继承自simplejson的编码基类，用于处理复杂类型的编码
     """
     def default(self,obj):
             if isinstance(obj,QuerySet):
                 """ Queryset实例
                 直接使用Django内置的序列化工具进行序列化
                 但是如果直接返回serialize('json',obj)
                 则在simplejson序列化时会被从当成字符串处理
                 则会多出前后的双引号
                 因此这里先获得序列化后的对象
                 然后再用simplejson反序列化一次
                 得到一个标准的字典（dict）对象
                 """
                 return simplejson.loads(serialize('json',obj))
             if isinstance(obj,models.Model):
                 """
                 如果传入的是单个对象，区别于QuerySet的就是
                 Django不支持序列化单个对象
                 因此，首先用单个对象来构造一个只有一个对象的数组
                 这是就可以看做是QuerySet对象
                 然后此时再用Django来进行序列化
                 就如同处理QuerySet一样
                 但是由于序列化QuerySet会被'[]'所包围
                 因此使用string[1:-1]来去除
                 由于序列化QuerySet而带入的'[]'
                 """
                 return simplejson.loads(serialize('json',[obj])[1:-1])
             if hasattr(obj, 'isoformat'):
                 #处理日期类型
                 return obj.isoformat()
             return simplejson.JSONEncoder.default(self,obj)

def jsonBack(json):
     """    进行Json字符串的反序列化
         一般来说，从网络得回的POST（或者GET）
         参数中所包含json数据
         例如，用POST传过来的参数中有一个key value键值对为
         request.POST['update']
         = "[{pk:1,name:'changename'},{pk:2,name:'changename2'}]"
         要将这个value进行反序列化
         则可以使用Django内置的序列化与反序列化
         但是问题在于
         传回的有可能是代表单个对象的json字符串
         如：
         request.POST['update'] = "{pk:1,name:'changename'}"
         这是，由于Django无法处理单个对象
         因此要做适当的处理
         将其模拟成一个数组，也就是用'[]'进行包围
         再进行反序列化
     """
     if json[0] == '[':
         return deserialize('json',json)
     else:
         return deserialize('json','[' + json +']')

def getJson(**args):
     """    使用MyEncoder这个自定义的规则类来序列化对象
     """
     result = dict(args)
     return simplejson.dumps(result,cls=MyEncoder)

class Project(models.Model):
    pid = models.IntegerField(default=0)#未使用的id
    name = models.CharField(max_length=30)#项目名
    course = models.IntegerField()#所在课程id
    group_number = models.IntegerField(default=0)#所分组数
    is_grouped = models.BooleanField(default=False)#是否分组 0 未分组 1已分组
    status = models.IntegerField(default=-1)#状态 0未添加题目 1未开始分组 2分组已开始 3分组借宿
    files = models.FileField(upload_to='static/files/project')#项目上传文件
    file_url = models.CharField(max_length=30)#文件url
    number_student = models.IntegerField(default=0)#已提交组队信息的学生名单
    btime = models.DateTimeField(default=datetime.datetime.now)
    etime = models.DateTimeField(default=datetime.datetime.now)
    ctime = models.DateTimeField(default=datetime.datetime.now)
    mtime = models.DateTimeField(default=datetime.datetime.now)
    def __unicode__(self):
       return self.name
    # def toJson(self):
    #     import json
    #     return json.dumps(dict([(attr,getattr(self,attr)) for attr in [f.name for f in self._meta.fields]]))
    def  toDict(self):
        return dict([(attr,getattr(self,attr)) for attr in [f.name for f in self._meta.fields]])
    def toJSON(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)
    
        d = {}
        for field in self._meta.fields:
            attr = field.name
            if isinstance(getattr(self, attr),datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr),datetime.date):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            elif isinstance(getattr(self,attr),FieldFile):
                d[attr] = None
                print 'here at files\n'
                continue
            else:
                d[attr] = getattr(self, attr)

        import json
        return json.dumps(d)

    def printself(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)
        d = {}
        for attr in fields:
            if isinstance(getattr(self,attr),FieldFile):
                print 'here at files\n'
            print attr,',---,',getattr(self,attr),' ,',type(getattr(self,attr))
