import pymysql

conn = pymysql.connect(host='ttobak.cbbaovh5sf1x.ap-northeast-2.rds.amazonaws.com',user='root',password='soma2020',db='ttobak',charset='utf8')

curs = conn.cursor()

sql = """insert into voice(voc_path,voc_desc,voc_script) values (%s,%s,%s)"""

voices = [
'올라가는 소리와 내려가는 소리를 지금부터 놓아 볼거에요.',
'이 소리는 올라가는 소리예요. 올라가는 소리 버튼을 눌러 볼까요?',
'이 소리는 내려가는 소리예요. 내려가는 소리 버튼을 눌러 볼까요?',
'이제 스스로 해 볼까요?',
'잘 듣고 들려준 소리와 똑같은 소리를 찾아 볼까요?',
'지금부터 들려주는 목소리를 듣고 그대로 따라해 볼까요?',
'앞으로 이 목소리에만 귀를 기울여 주세요. 다른 목소리가 나올 수 있는데 무시하면 돼요.',
'정말 수고 많았어요.',
'들려주는 동시를 듣고 그대로 따라해 볼까요?',
'지금부터 들려주는 소리를 잘 들어보세요.',
'이 소리는 쇠, 구, 슬 3개의 소리로 되어 있죠? 들려준 소리의 숫자만큼 사과를 옮겨 보세요.',
'잘 했어요! 이제부터 스스로 해 볼까요?',
'지금부터 같은 소리를 찾아볼 거에요. 첫 소리에 집중해서 들어보세요.',
'고기, 고모, 고향 모두 고 가 앞에 들어가죠? 고를 찾아 눌러볼까요?',
'잘 했어요! 지금부터 첫 소리를 찾아볼까요?',
'지금부터 같은 소리를 찾아볼 거에요. 마지막 소리에 집중해서 들어보세요.',
'기러기, 드라이기, 냉난방기 모두 기 가 뒤에 들어가죠? 기를 찾아 눌러볼까요?',
'잘 했어요! 지금부터 마지막 소리를 찾아볼까요?',
'지금부터 같은 소리를 찾아볼 거에요. 들려주는 소리에 집중해 보세요.',
'불개미, 소개팅, 무지개 모두 개 가 들어가죠? 개를 찾아 눌러볼까요?',
'잘 했어요! 지금부터 같은 소리를 찾아볼까요?',
'들은 그대로 따라해 볼까요?',
'잘 했어요! 지금부터 다른 소리들도 듣고 따라해 볼까요?',
'아 소리를 들려줬어요. 아래에서 아 소리를 찾아볼까요?',
'잘 했어요! 지금부터 다른 소리들도 듣고 찾아 볼까요?',
'가방 을 들려줬지요? 그림 카드에서 가방을 찾아 볼까요?',
'이 그림은 가방이지요? 가방의 첫 소리를 아래에서 찾아볼까요?',
'잘 했어요! 지금부터 다른 그림들도 보고 첫 소리를 찾아 볼까요?',
'아래 써 있는 강산을 발음해 볼까요?',
'잘 했어요! 지금부터 다른 단어들도 읽어 볼까요?',
'뭐 소리를 들려주었죠? 아래에서 뭐 소리를 찾아 볼까요?',
'잘 했어요! 지금부터 다른 소리들도 듣고 찾아볼까요?',
'잘 했어요!',
'최고예요!',
'다시 한 번 해볼까요?',
'조금 아쉬워요. 힘 내서 다시 해봐요',
'귀 소리를 들려줬어요. 아래에서 귀 소리를 찾아 볼까요?',
'속도를 더 빠르게 읽어 볼까요?',
'속도를 더 천천히 읽어 볼까요?',
'박자에 맞게 읽어 볼까요?',
'잘 했어요! 지금부터 소리를 듣고 소리와 같은 그림을 찾아 볼까요?']

desc = [
    'swp_intro', #1
    'swp_up',#2
    'swp_down',#3
    'swp_end',#4
    'ph_intro',#5
    'foc_intro',#6
    'foc_good',#7
    'diag_end', #8
    'poem_intro', #9
    'listen_carefully', #10
    'count_expln',#11
    'count_good',#12
    'common_lev1_intro', #13
    'common_lev1_expln',#14
    'common_lev1_good',#15
    'common_lev2_intro',#16
    'common_lev2_expln',#17
    'common_lev2_good',#18
    'common_lev3_intro',#19
    'common_lev3_expln',#20
    'common_lev3_good',#21
    'repeat',#22
    'vowelword_good', #23
    'vowelsound_expln', #24
    'vowelsound_good', #25
    'consomatch_expln', #26
    'consocommon_expln', #27
    'consocommon_good', #28
    'consoword_expln', #29
    'consoword_good', #30
    'consosound_expln', #31
    'consosound_good', #32
    'good',#33
    'good',#34
    'retry',#35
    'retry',#36
    'ph_expln',#37
    'speed_up',#38
    'speed_down',#39
    'rhythm',#40
    'pic_match'#41
]

num = len(voices)
for n in range(num):
    path = '/extra/extra_00'
    if n+1 < 10:
        path += '0' + str(n+1) + '.mp3'
    else:
        path += str(n+1) + '.mp3'
    curs.execute(sql,(path,desc[n],voices[n]))
    
conn.commit()

conn.close()
