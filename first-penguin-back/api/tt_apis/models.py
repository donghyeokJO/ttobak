from django.db import models

class FocScript(models.Model):
    fs_id = models.AutoField(primary_key=True)
    conv_id = models.IntegerField()
    script = models.CharField(max_length = 1000)

    class Meta:
        db_table = 'foc_script'

class Icon(models.Model):
    ic_id = models.AutoField(primary_key=True)
    ic_path = models.CharField(max_length=255)

    class Meta:
        db_table = 'icon'

class StuFocArr(models.Model):
    sfarr_id = models.AutoField(primary_key=True)
    stu = models.ForeignKey('Student',on_delete = models.PROTECT,null=True,db_column = 'stu_id')
    o0 = models.IntegerField()
    o1 = models.IntegerField()
    o2 = models.IntegerField()
    o3 = models.IntegerField()
    stucnt = models.IntegerField(default = 0)

    class Meta:
        db_table = 'stu_foc_arr'

class StuIc(models.Model):
    stu = models.ForeignKey('Student', on_delete=models.PROTECT,null=True,db_column = 'stu_id')
    ic = models.ForeignKey('Icon', on_delete=models.PROTECT,null=True,db_column = 'ic_id')
    class Meta:
        db_table = 'stu_ic'

class Student(models.Model):
    stu_id = models.AutoField(primary_key=True)
    stu_name = models.CharField(max_length=255)
    stu_birth = models.IntegerField(null=True)
    stu_gender = models.CharField(max_length=5)
    regi_date = models.DateField(auto_now_add = True)
    modi_date = models.DateField(auto_now = True)
    ic = models.ForeignKey('Icon',on_delete=models.PROTECT,null=True,db_column = 'ic_id')
    activated = models.CharField(max_length=1,null=True)
    
    class Meta:
        db_table = 'student'

class User(models.Model):
    usr_id = models.AutoField(primary_key=True)
    usr_name = models.CharField(max_length=255)
    usr_email = models.CharField(max_length=255,unique=True)
    usr_pw = models.CharField(max_length=255)
    regi_date = models.DateField(auto_now_add=True)
    modi_date = models.DateField(auto_now=True)
    activated = models.CharField(max_length=1,null=True)

    class Meta:
        db_table = 'user'

class UsrStu(models.Model):

    usr = models.ForeignKey('User', on_delete=models.PROTECT,null=True,db_column = 'usr_id')
    stu = models.ForeignKey('Student', on_delete=models.PROTECT,null=True,db_column = 'stu_id')

    class Meta:
        db_table = 'usr_stu'

class TestIdx(models.Model):
    idx_id = models.AutoField(primary_key = True)
    idx_txt = models.CharField(max_length = 10)

    class Meta:
        db_table = "test_idx"

class TestMaster(models.Model):
    ques_id = models.AutoField(primary_key = True)
    test_idx = models.ForeignKey('TestIdx',on_delete=models.PROTECT,null=True,db_column = 'idx_id')
    ques_level = models.IntegerField() #question level
    ques_path1 = models.CharField(max_length=255) #voice path1
    ques_path2 = models.CharField(max_length=255,null=True) #voice path2(swp_only)
    ques_int = models.IntegerField(null=True) #frequency for swp
    ques_char = models.CharField(max_length = 10,null=True) #character for ph

    class Meta:
        db_table = "test_master"

class StuTest(models.Model):
    stu = models.ForeignKey('Student',on_delete = models.PROTECT,null=True,db_column='stu_id')
    ques = models.ForeignKey('TestMaster',on_delete=models.PROTECT,null=True,related_name='ques_normal')
    ques2 = models.ForeignKey('TestMaster',on_delete = models.PROTECT,null=True,related_name = 'ques_ph')
    T_OR_F = (
        ('Y',"yes"),
        ('N',"no"),
    )
    test_txt = models.CharField(max_length=10,null=True)
    is_correct = models.CharField(max_length=1,choices = T_OR_F)
    date = models.DateField(auto_now_add=True)
    full_score = models.IntegerField(null=True)
    phone_score = models.IntegerField(null=True)
    speed_score = models.IntegerField(null=True)
    rhythm_score = models.IntegerField(null=True)
    is_review = models.CharField(max_length=1,choices=T_OR_F,null=True)
    class Meta:
        db_table = "stu_test"

class ComCure(models.Model):
    com_id = models.AutoField(primary_key=True)
    com_level = models.IntegerField()
    com_w1 = models.CharField(max_length=10)
    com_w2 = models.CharField(max_length=10)
    com_w3 = models.CharField(max_length=10)
    com_e1 = models.CharField(max_length=10)
    com_e2 = models.CharField(max_length=10)
    com_e3 = models.CharField(max_length=10)
    com_e4 = models.CharField(max_length=10)
    com_ans = models.CharField(max_length=10)
    com_w1path = models.CharField(max_length=255)
    com_w2path = models.CharField(max_length=255)
    com_w3path = models.CharField(max_length=255)
    com_e1path = models.CharField(max_length=255)
    com_e2path = models.CharField(max_length=255)
    com_e3path = models.CharField(max_length=255)
    com_e4path = models.CharField(max_length=255)

    class Meta:
        db_table = "com_cure"

class CureIdx(models.Model):
    idx_id = models.AutoField(primary_key = True)
    idx_txt = models.CharField(max_length = 20)
    read_order = models.IntegerField(null=True)
    curr_order = models.IntegerField(null=True)
    class Meta:
        db_table = "cure_idx"
    
class CureMaster(models.Model):
    cure_id = models.AutoField(primary_key=True)
    cure_level = models.IntegerField(null=True)
    cure_idx = models.ForeignKey('CureIdx',on_delete=models.PROTECT,null=True,db_column = 'idx_id')
    cure_path = models.CharField(max_length=255)
    cure_path2 = models.CharField(max_length=255)
    cure_tid = models.IntegerField(null=True) #text identifier for poemtext and selfcure
    cure_word = models.CharField(max_length =10)
    cure_word2 = models.CharField(max_length = 10) #for vowelsound and consosound
    cure_text = models.CharField(max_length = 255) #for longer words like poem

    class Meta:
        db_table = "cure_master"


class StuCure(models.Model):
    stu = models.ForeignKey('Student',on_delete = models.PROTECT,null=True,db_column='stu_id')
    cure = models.ForeignKey('CureMaster',on_delete=models.PROTECT,null=True,related_name='q1')
    cure_2 = models.ForeignKey('CureMaster',on_delete=models.PROTECT,null=True,related_name='q2') 
    cure_3 = models.ForeignKey('CureMaster',on_delete=models.PROTECT,null=True,related_name='q3') ## 2 and 3 for consomatch
    com_cure = models.ForeignKey('ComCure',on_delete = models.PROTECT,null=True,db_column = 'com_id') ##for com_cure record
    T_OR_F = (
        ('Y',"yes"),
        ('N',"no"),
    )
    cure_txt = models.CharField(max_length=50,null=True)
    is_correct = models.CharField(max_length=1,choices = T_OR_F,null=True)
    date = models.DateField(auto_now_add=True)
    full_score = models.IntegerField(null=True)
    phone_score = models.IntegerField(null=True)
    speed_score = models.IntegerField(null=True)
    rhythm_score = models.IntegerField(null=True)
    is_review = models.CharField(max_length=1,choices=T_OR_F,null=True)
    is_daily = models.CharField(max_length=1,choices = T_OR_F,null=True)
    is_first = models.CharField(max_length = 1, choices = T_OR_F,null=True)
    stu_answer = models.CharField(max_length = 255,null=True)
    ori_answer = models.CharField(max_length = 255,null=True)
    class Meta:
        db_table = "stu_cure"

class StuCurrent(models.Model):
    stu = models.ForeignKey('Student',on_delete=models.PROTECT,null=True,db_column='stu_id')
    cur_read = models.CharField(max_length=50)
    cur_curr = models.CharField(max_length=50)
    cur_read_id = models.IntegerField(null=True)
    read_level = models.IntegerField(null=True)
    curr_level = models.IntegerField(null=True)
    cur_curr_last1 = models.IntegerField(null=True)
    cur_curr_last2 = models.IntegerField(null=True)
    cur_curr_last3 = models.IntegerField(null=True)

    class Meta:
        db_table = "stu_current"

class TestCurrent(models.Model):
    stu = models.ForeignKey('Student',on_delete = models.PROTECT,null=True,db_column ='stu_id')
    swp_freq = models.IntegerField(null=True)
    swp_lev = models.IntegerField(null=True)
    swp_passed = models.IntegerField(null=True)
    swp_did = models.IntegerField(null=True)
    # ph_count = models.IntegerField(null=True)
    focus_lev = models.IntegerField(null = True)
    focus_passed = models.IntegerField(null=True)
    focus_did = models.IntegerField(null = True)

    class Meta:
        db_table = 'test_current'

class MainImg(models.Model):
    img_id = models.AutoField(primary_key=True)
    img_path = models.CharField(max_length = 255)
    img_desc = models.CharField(max_length = 255)

    class Meta:
        db_table = "main_img"

class WordImg(models.Model):
    img_id = models.AutoField(primary_key=True)
    img_path = models.CharField(max_length=255)
    img_desc = models.CharField(max_length=255)

    class Meta:
        db_table = "word_img"

class Voice(models.Model):
    voc_id = models.AutoField(primary_key = True)
    voc_path = models.CharField(max_length = 255)
    voc_desc = models.CharField(max_length = 255)
    voc_script = models.CharField(max_length = 255)

    class Meta:
        db_table = "voice"

class StuStatus(models.Model):
    stu = models.ForeignKey('Student',on_delete = models.PROTECT,null=True,db_column ='stu_id')
    status = models.CharField(max_length = 10)
    date = models.DateField(auto_now = True)

    class Meta:
        db_table = 'stu_status'
