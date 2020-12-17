## 또박이 API 정의 문서

API Document for **또박이** 
All of the APIs include responses automatically created by server. i.e) 404 not found / 500 Internal Server Error / etc..

** All the urls should be concatenated with "https://ttobakaudio.s3-ap-northeast-2.amazonaws.com"

**is_review parameter includes information whether the student solves the problem for a daily study or for a review session.

**idx_txt parameter for treatment uses the same indicator for each study in gitlab. For diagnose, 'swp' for sweep test, 'ph' for recognition, 'foc' for attention

**parameters for pronunciation use exactly same parameters of audio server.

## Part 1 -  USER

**register**
----
* **URL**
	/user/register

* **Method:**
	  `POST`
*  **URL Params**
   **Required:**
   **Optional:**

* **Data Params**
	  `email=[alphanumeric]` |  `pw = [alphanumeric]` | `name = [alphanumeric]`
* **Response:**

	* **Code:** 200 <br />
     **Content:** `{ "message" : '성공적으로 회원가입 되었습니다.',"u_id":integer,"code": 1 }`

OR

  * **Code:** 200<br />
    **Content:** `{ "message" : "이미 존재하는 이메일입니다.","code":2 }`

* **Sample Call:**
  ```javascript
    $.ajax({
      url: "link/to/api/users/register",
      dataType: "json",
      type : "POST",
      data : { 
	    "email" : sample@sample.comm
		  "pw" : password,
		  "name" : name
		},success : function(r) {
        console.log(r);
      }
    });
    ```

 
 **signin**
----
* **URL**
	/user/signin

* **Method:**
	  `POST`
*  **URL Params**
   **Required:**
   **Optional:**

* **Data Params**
	  `email=[alphanumeric]` |  `pw = [alphanumeric]` 
* **Success Response:**  
   
   * **Code:** 200 <br />
    **Content:** `{ "u_id" : [integer],"code" : 1  }`
 
OR

  * **Code:** 200 <br />
    **Content:** `{ "message": "비밀번호가 일치하지 않습니다.", "code":2 }`

  OR
  
  * **Code:** 200 <br  />
  **Content:**  `{"message": "가입된 메일 주소가 존재하지 않습니다. " , "code" : 3}`


* **Sample Call:**
  ```javascript
    $.ajax({
      url: "link/to/api/users/signin",
      dataType: "json",
      type : "POST",
      data : { 
	     "email" : sample@sample.comm
		   "pw" : password,
		},success : function(r) {
         console.log(r)
      }
    });

 **modify**
----
* **URL**
	/user/modify

* **Method:**
	  `POST`
*  **URL Params**
   **Required:**
   **Optional:**

* **Data Params**
	  `email=[alphanumeric]` |  `pw = [alphanumeric]`  | `name =[alphanumeric]` | `u_id = [integer]`
* **Success Response:**  
  
  * **Code:** 200 <br />
    **Content:** `{ "message" : "변경사항이 저장되었습니다.","code" : 1 }`
 
OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "이미 존재하는 이메일입니다.","code":2 }`

  OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "존재하지 않는 회원입니다.","code":3 }`

* **Sample Call:**
  ```javascript
    $.ajax({
      url: "link/to/api/users/modify",
      dataType: "json",
      type : "POST",
      data : { 
	     "email" : sample@sample.comm
		   "pw" : password,
		   "name" : name
		},success : function(r) {
	         console.log(r)
      }
    });

 **delete**
----
* **URL**
	/user/delete

* **Method:**
	  `POST`
*  **URL Params**
   **Required:**
   **Optional:**

* **Data Params**
	  `u_id=[integer]`
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ "message" : "성공적으로 삭제 되었습니다.","code":1}`
 
OR 

  * **Code:** 200 <br />
    **Content:** `{ "message" : "존재하지 않는 회원입니다." , "code": 2 }`

* **Sample Call:**
  ```javascript
    $.ajax({
      url: "link/to/api/users/delete",
      dataType: "json",
      type : "POST",
      data : { 
	     "id" : 0
		},success : function(r) {
         alert(r['message'])
      }
    });

 **get**
----
* **URL**
	/user/get

* **Method:**
	  `POST`
*  **URL Params**
   **Required:**
   **Optional:**

* **Data Params**
	  `u_id = [integer]`
	  
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ "u_id":[integer],"name" : [alphanumeric], "email" : [alphanumeric], "students": [list of students],"code" : 1 }`
 
OR 

  * **Code:** 200 <br />
    **Content:** `{ "message" : "존재하지 않는 회원입니다.","code" :2 }`

 
* **Sample Call:**
  ```javascript
    $.ajax({
      url: "link/to/api/user/get",
      dataType: "json",
      type : "POST",
      data : { 
	     "u_id" : 0,
		},success : function(r) {
	         console.log(r)
      }
    });

## Part2 - Student

 **add**
----
* **URL**
	/student/add

* **Method:**
	  `POST`
*  **URL Params**
   **Required:**
   **Optional:**

* **Data Params**
	  `name=[alphanumeric]` | `birth=[date]` | `gender=[alphanumeric]` | `u_id = [integer]`
	  
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ "message" : "성공적으로 추가 되었습니다.","s_id":[integer],"code" : 1 }`
 
OR 

  * **Code:** 200 <br />
    **Content:** `{ "message" : "존재하지 않는 회원입니다.", "code" :2 }`

OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "학습자는 3명까지만 추가할 수 있습니다.", "code" :3 }`
    
* **Sample Call:**
  ```javascript
    $.ajax({
      url: "link/to/api/student/add",
      dataType: "json",
      type : "POST",
      data : { 
	     "u_id" : 0,
	     "name" : "홍길동",
	     "birth" : "1998-08-11",
	     "gender" : "female",
		},success : function(r) {
	         console.log(r)
      }
    });
    
 **modify**
----
* **URL**
	/student/modify

* **Method:**
	  `POST`
*  **URL Params**
   **Required:**
   **Optional:**

* **Data Params**
	  `name=[alphanumeric]` | `birth=[date]` | `gender=[alphanumeric]` | `s_id = [integer]` | `u_id = [integer]`
	  
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ "message" : "성공적으로 수정 되었습니다." "code" : 1 }`
 
OR 

  * **Code:** 200 <br />
    **Content:** `{ "message" : "존재하지 않는 학습자 입니다.","code" : 2 }`

  OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "존재하지 않는 회원입니다.", "code":3 }`

* **Sample Call:**
  ```javascript
    $.ajax({
      url: "link/to/api/student/modify",
      dataType: "json",
      type : "POST",
      data : { 
	     "s_id" : 1,
	     "u_id" : 0,
	     "name" : "홍길동",
	     "birth" : "1998-08-11",
	     "gender" : "female",
		},success : function(r) {
	         console.log(r)
      }
    });

 **delete**
----
* **URL**
	/student/delete

* **Method:**
	  `POST`
*  **URL Params**
   **Required:**
   **Optional:**

* **Data Params**
	 `s_id = [integer]` | `u_id = [integer]`
	  
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ "message" : "성공적으로 삭제 되었습니다.","code" :1  }`

OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "존재하지 않는 학습자입니다. ", "code" : 2 }`

  OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "존재하지 않는 회원입니다." ,"code" : 3 }`

* **Sample Call:**
  ```javascript
    $.ajax({
      url: "link/to/api/student/delete",
      dataType: "json",
      type : "POST",
      data : { 
	     "s_id" : 1,
	     "u_id" : 0,
		},success : function(r) {
	         console.log(r)
      }
    });
    
 **get**
----
* **URL**
	/student/get

* **Method:**
	  `POST`
*  **URL Params**
   **Required:**
   **Optional:**

* **Data Params**
	   `s_id = [integer]` | `u_id = [integer]`
	  
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ "s_id":[integer],"name": [string], "birth" : [date] , "gender" : ['male' or 'female'],"ic_id" : [integer],"code":1 }`
 
OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "존재하지 않는 학습자 입니다.", "code" : 2  }`

  OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "존재하지 않는 회원입니다.","code" : 3 }`

* **Sample Call:**
  ```javascript
    $.ajax({
      url: "link/to/api/student/get",
      dataType: "json",
      type : "POST",
      data : { 
	     "s_id" : 1,
	     "u_id" : 0,
		},success : function(r) {
	         console.log(r)
      }
    });    
   

## Part3 - Swp

 **ask**
----
* **URL**
	/diagnose/ask

* **Method:**
	  `POST`
*  **URL Params**
   **Required:**
   **Optional:**

* **Data Params**
	   `s_id = [integer] | idx_txt = "swp"` 
	  
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ "swp" : { "ques_id" : [integer], "ques_path1" : [path_to_down_path] , "ques_path2" : [path_to_up_path] } , "answers" : { set_of_five answer_set } , "code":1}`
 
OR

  * **Code:** 200 <br />
    **Content:** `{ "message"  : "해당 학습이 존재하지 않습니다.","code": 2 }`

  OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "해당 학습자가 존재하지 않습니다.","code": 3 }`
 
  OR

  * **Code:** 200 <br />
    **Content:** `{ "voice" : [list of sample voice]("voc_path" : path, "voc_script" : script "voc_desc" : description for voice),"sample_ques" : ["ques_id": 71,"ques_path1":"/diagnose/01_sweeps/d_500_80.mp3","ques_path2":"/diagnose/01_sweeps/u_500_80.mp3"],"code": "tutorial" }`



  
  

* **Sample Call:**
  ```javascript
    $.ajax({
      url: "link/to/api/cure/ask",
      dataType: "json",
      type : "POST",
      data : { 
	     "s_id" : 1,
	     "idx_txt" : "swp"
		},success : function(r) {
	         console.log(r)
      }
    });   

 **answer**
----
* **URL**
	/diagnose/answer

* **Method:**
	  `POST`
*  **URL Params**
   **Required:**
   **Optional:**

* **Data Params**
	   `s_id = [integer]` | `ques_id = [integer] | ori_answer1 = [up/down] | ori_answer2 = [up/down] | stu_answer1 =[up/down] | stu_answer = [up/down] , is_review = [True/False], idx_txt = "swp"` 
	  
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ "is_correct" : ["T" or "F"], "to_next" : [True/False], "to_next_freq" : [True/False] }`
    
 *stop when to_next == "모든 문제를 풀었습니다"*
 
OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "해당하는 검사가 존재하지 않습니다.","code" : 2 }`

  OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "해당 학습자가 존재하지 않습니다." ,"code" : 3 }`

* **Sample Call:**
  ```javascript
    $.ajax({
      url: "link/to/api/diagnose/answer",
      dataType: "json",
      type : "POST",
      data : { 
	     "s_id" : 1,
	     "ques_id" : 1,
	     "ori_answer1" : "up",
	     "ori_answer2" : "up",
	     "stu_answer1" : "up",
	     "stu_answer2" : "down",
	     "is_review" : "T",
	     "idx_txt" : "swp"
		},success : function(r) {
	         console.log(r)
      }
    });   


## Part4 - Recognition
 **ask**
----
* **URL**
	/diagnose/ask

* **Method:**
	  `POST`
*  **URL Params**
   **Required:**
   **Optional:**

* **Data Params**
	   `s_id = [integer] | idx_txt = "ph"` 
	  
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ "phs" : {set of 50 character("ques_id" : [integer], "ques_path1" : [path], "ques_char" : [character]) },"answers" : {set of 25 answer set(integers mean the ques_id1, ques_id2, ques_id of answer) }"code":1}`
 
OR 

  * **Code:** 200 <br />
    **Content:** `{ "message" : "해당 레벨의 문제가 존재하지 않습니다.","code":2 }`

  OR

  * **Code:** 200<br />
    **Content:** `{ "message" : "해당 학습자가 존재하지 않습니다.","code":3 }`

OR

  * **Code:** 200 <br />
    **Content:** `{ "voice" : [list of sample voice]("voc_path" : path, "voc_script" : script "voc_desc" : description for voice),"sample_ques" : [sample question] {"ques_id": 84,"ques_path1": "/diagnose/02_recognition/text_01_0001_0001.mp3","ques_char": "귀"},{"ques_id": 85,"ques_path1": "/diagnose/02_recognition/text_01_0002_0001.mp3",
"ques_char": "남"},"code": "tutorial" }`



* **Sample Call:**
  ```javascript
    $.ajax({
      url: "link/to/diagnose/ask",
      dataType: "json",
      type : "POST",
      data : { 
	     "idx_txt" : "ph",
	     "s_id" : 1
		},success : function(r) {
	         console.log(r)
      }
    });   

 **answer**
----
* **URL**
	/diagnose/answer

* **Method:**
	  `POST`
*  **URL Params**
   **Required:**
   **Optional:**

* **Data Params**
	   `s_id = [integer]` | `ques_id1 = [integer] | ques_id2 = [integer] | stu_answer = [character] | ori_answer = [character] | is_review = ["T" or "F"] | idx_txt = "ph" ` 
	  
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ "is_correct" : ["T" or "F"],"code":1 }`
 
OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "해당하는 검사가 존재하지 않습니다.","code" : 2 }`

  OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "해당 학습자가 존재하지 않습니다.","code":3 }`

* **Sample Call:**
  ```javascript
    $.ajax({
      url: "link/to/api/diagnose/answer",
      dataType: "json",
      type : "POST",
      data : { 
	     "s_id" : 1,
	     "ques_id1" : 2,
	     "ques_id2" : 3
	     "ori_answer" : "귀",
	     "stu_answer" : "남",
	     "is_review" : "F",
	     "idx_txt" : "ph"
		},success : function(r) {
	         console.log(r)
      }
    });   
*call for every 25 questions*

## Part5 - Attention

 **ask**
----
* **URL**
	/diagnose/ask

* **Method:**
	  `POST`
*  **URL Params**
   **Required:**
   **Optional:**

* **Data Params**
	   `idx_txt = "foc" | s_id = [integer] `
		  
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"focus" : {set of 5 question("ques_id" : [integer],"ques_path1": path, "ques_int" : [integer], "ques_char" : [character], "ques_level : [integer])},"code" : 1}`

 *Use the five questions in numerical order of ques_level. Do not mind ques_int*
 
OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "해당하는 문제가 존재하지 않습니다.","code":2 }`

  OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "해당하는 학습자가 존재하지 않습니다.","code": 3 }`

OR

  * **Code:** 200 <br />
    **Content:** `{ "voice" : [list of sample voice]("voc_path" : path, "voc_script" : script "voc_desc" : description for voice),"sample_ques" : [sample question]{"ques_id": 534,"ques_path1": "/diagnose/03_attention/atten_01_01_0001.mp3","ques_char": "엄마랑 동물원에 갔습니다"},"code": "tutorial" }`


* **Sample Call:**
  ```javascript
    $.ajax({
      url: "link/to/api/diagnose/ask",
      dataType: "json",
      type : "POST",
      data : { 
	     "idx_txt" : "foc",
	     "s_id" : 1
		},success : function(r) {
	         console.log(r)
      }
    });   


 **answer**
----
* **URL**
	/diagnose/answer

* **Method:**
	  `POST`
*  **URL Params**
   **Required:**
   **Optional:**

* **Data Params**
	   `s_id = [integer]` | `ques_id = [integer] | full_score = [integer] | phone_score = [integer] | speed_score = [integer] | rhythm_score = [integer] | is_review = ["T" or "F"] | idx_txt = "foc"`
		  
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ "is_pass": [True/False], "to_next_level" : [True],"is_stop" : [True/False], "code":1}`
    
 *diagnose finishes when is_stop == True OR to_next_level =="모든 문제를 학습했습니다" *

OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "해당하는 검사가 존재하지 않습니다.","code":2 }`

  OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "해당하는 학습자가 존재하지 않습니다.","code": 3 }`

* **Sample Call:**
  ```javascript
    $.ajax({
      url: "link/to/api/diagnose/answer",
      dataType: "json",
      type : "POST",
      data : { 
	     "full_score" : 90,
	     "phone_score" : 80,
	     "speed_score" : 5,
	     "rhythm_score" : 5,
	     "idx_txt" : "foc",
	     "ques_id" : 1,
	     "s_id" : 1,
	     "is_review" : "F"
		},success : function(r) {
	         console.log(r)
      }
    });

 **result**
----
* **URL**
	/diagnose/result

* **Method:**
	  `POST`
*  **URL Params**
   **Required:**
   **Optional:**

* **Data Params**
	   `s_id = [integer]` 
		  
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ "result":{"총 문제 개수":[integer],"총 맞은 개수":[integer],"청각처리속도" : {"총 문제 개수" : [integer],"맞은 개수": [integer]},"음운청취력": {"총 문제 개수": [integer],"맞은 개수":[integer]},"선택적 집중력" :{"총 문제 개수":[integer],"맞은 개수":[integer]}} "code":1}`
    
  OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "해당하는 학습자가 존재하지 않습니다.","code": 2 }`

* **Sample Call:**
  ```javascript
    $.ajax({
      url: "link/to/api/diagnose/result",
      dataType: "json",
      type : "POST",
      data : { 
	     "s_id" : 1
		},success : function(r) {
	         console.log(r)
      }
    });   
  
  
 **tutorial answer**
----
* **URL**
	/diagnose/answer

* **Method:**
	  `POST`
*  **URL Params**
   **Required:**
   **Optional:**

* **Data Params**
	   `s_id = [integer] | idx_txt = [character] | tutorial = "true"` 
		  
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ "is_okay" : True/False} "code":1}`
    
  OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "해당하는 검사가 존재하지 않습니다.","code": 2 }`
      
   OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "해당하는 학습자가 존재하지 않습니다.","code": 3 }`


* **Sample Call:**
  ```javascript
    $.ajax({
      url: "link/to/api/diagnose/answer",
      dataType: "json",
      type : "POST",
      data : { 
	     "s_id" : 1,
	     "idx_txt" : "swp",
	     "tutorial" : "true"
		},success : function(r) {
	         console.log(r)
      }
    });   
  
 **okay**
----
*return if student can conduct another  test or not*
* **URL**
	/diagnose/okay

* **Method:**
	  `POST`
*  **URL Params**
   **Required:**
   **Optional:**

* **Data Params**
	   `s_id = [integer]` 
		  
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ "is_okay" : True/False} "code":1}`
    
   OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "해당하는 학습자가 존재하지 않습니다.","code": 2 }`


* **Sample Call:**
  ```javascript
    $.ajax({
      url: "link/to/api/diagnose/okay",
      dataType: "json",
      type : "POST",
      data : { 
	     "s_id" : 1,
	     "idx_txt" : "swp",
	     "tutorial" : "true"
		},success : function(r) {
	         console.log(r)
      }
    });   
  
   **tutorial answer**
----
* **URL**
	/diagnose/answer

* **Method:**
	  `POST`
*  **URL Params**
   **Required:**
   **Optional:**

* **Data Params**
	   `s_id = [integer] | idx_txt = [character] | tutorial = "true"` 
		  
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ "is_okay" : True/False} "code":1}`
    
  OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "해당하는 검사가 존재하지 않습니다.","code": 2 }`
      
   OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "해당하는 학습자가 존재하지 않습니다.","code": 3 }`


* **Sample Call:**
  ```javascript
    $.ajax({
      url: "link/to/api/diagnose/answer",
      dataType: "json",
      type : "POST",
      data : { 
	     "s_id" : 1
		},success : function(r) {
	         console.log(r)
      }
    });   

 **did**
----
*tells if the this diagnose is the students' first or not*
* **URL**
	/diagnose/did

* **Method:**
	  `POST`
*  **URL Params**
   **Required:**
   **Optional:**

* **Data Params**
	   `s_id = [integer]` 
		  
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ "is_first" : True/False} "code":1}`
    

   OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "해당 학습자가 존재하지 않습니다.","code": 2 }`


* **Sample Call:**
  ```javascript
    $.ajax({
      url: "link/to/api/diagnose/did",
      dataType: "json",
      type : "POST",
      data : { 
	     "s_id" : 1
		},success : function(r) {
	         console.log(r)
      }
    });    
    
## Part6 - Treatment

 **ask**
----
* **URL**
	/cure/ask

* **Method:**
	  `POST`
*  **URL Params**
   **Required:**
   **Optional:**

* **Data Params**
	   `s_id = [integer] `

*include idx_txt = [idx_txt] incase of student choose what to study. ex) idx_txt = "poem", s_id = [integer]*

*in case of review, please set the idx_txt = 'review'. But the review function is still in progress, and will be updated soon.*
		  
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ "read": {set of 10 daily read contents("cure_id" : [integer], "cure_level" : level, "cure_path" : path, "cure_tid" : [integer], "cure_text": corresponding text)}, "cure" : {set of questions. normally 10, but please check the ask_form.txt}, "answers" : {set of answers. only in case of consomatch. Plase check ask_form.txt},"read_voice" : [instruction voices]{"voc_path": path, "voc_script" :script, "voc_desc" : description },"daily_cure" : [idx_txt],"daily_read" : [idx_txt], "tut_voice" : [list of sample voice],"sample_ques" : [sample question], "code":[1(normal case)/"review"(review case)/"specified"(arbitrary case)] / "tutorial"(for 1st time of each cure)}`

*in case of code == review or specified, daily_cure will be omitted*
 
OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "존재하지 않는 학습자입니다.","code": 2 }`

*Please do not send back the answer for tutorial question.*
*check out tut_ques.txt for tutorial question / tutorial voice form*

* **Sample Call:**
  ```javascript
    $.ajax({
      url: "link/to/api/cure/ask",
      dataType: "json",
      type : "POST",
      data : { 
	     "s_id" : 1
		},success : function(r) {
	         console.log(r)
      }
    });   

answer(1) - read(poem,text,selfpoem,selftext) 
----
* **URL**
	/cure/answer

* **Method:**
	  `POST`
*  **URL Params**
   **Required:**
   **Optional:**

* **Data Params**
	   `s_id = [integer]` | `cure_id = [integer] | full_score = [integer] | phone_score = [integer] | rhythm_score = [integer] | speed_score = [integer] | is_review = ["T" or "F"] | is_daily = ["T" or "F"] |  idx_txt = [idx_txt]`
		  
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ is_okay=[True/False],class=['A' ~ 'D'],"class_voice": path, "code":1 }`
 
  OR
  
  * **Code:** 200 <br />
    **Content:** `{ is_okay = [True/False],class = ['A' ~'D'], "class_voice": path, "message" : "더 이상 학습할 문제가 없습니다.","code": 2 }`

*class voice can be null*

  OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "해당 학습자가 존재하지 않습니다.","code": 3 }`

  OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "해당 학습이 존재하지 않습니다.","code": 4 }`
   

*Please do not send back the answer for tutorial question.*
    
* **Sample Call:**
  ```javascript
    $.ajax({
      url: "link/to/api/cure/answer",
      dataType: "json",
      type : "POST",
      data : { 
	     "full_score" : 80,
	     "phone_score" : 70,
	     "speed_score" : 5,
	     "rhythm_score " : 5,
	     "is_review" : "F",
	     "idx_txt" : "poem"
	     "cure_id" : 1
	     "s_id" : 1
		},success : function(r) {
	         console.log(r)
      }
    });   

 **answer(2) - count, vowelsound, consocommon, consosound , common**
----
* **URL**
	/cure/answer

* **Method:**
	  `POST`
*  **URL Params**
   **Required:**
   **Optional:**

* **Data Params**
	   `s_id = [integer]` | `cure_id = [integer] | ori_answer = [character] | stu_answer = [character] | is_review = ["T" or "F"] | is_daily = ["T" or "F"] | idx_txt = [idx_txt]`

*in case of count, stu_answer & ori_answer can be integer*
*for the others, they should be character/word*
		  
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ "is_correct";[True/False],"correct_voice" : path, "code":1 }`
 
  OR
  
  * **Code:** 200 <br />
    **Content:** `{ "is_correct" :[True/False],"correct_voice" : path, "message" : "모든 문제를 학습하였습니다.","code": 2 }`

*correct voice can be null*

  OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "해당 학습자가 존재하지 않습니다.","code": 3 }`

  OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "해당 학습이 존재하지 않습니다.","code": 4 }`
    
* **Sample Call:**
  ```javascript
    $.ajax({
      url: "link/to/api/cure/answer",
      dataType: "json",
      type : "POST",
      data : { 
	     "ori_answer" : 5,
	     "stu_answer" : 3,
	     "is_review" : "F",
	     "idx_txt" : "count"
	     "cure_id" : 1
	     "s_id" : 1
		},success : function(r) {
	         console.log(r)
      }
    });   

 answer(3) - vowelword, consoword 
----
* **URL**
	/cure/answer

* **Method:**
	  `POST`
*  **URL Params**
   **Required:**
   **Optional:**

* **Data Params**
	   `s_id = [integer]` | `cure_id = [integer] | full_score = [integer] | phone_score = [integer] | rhythm_score = [integer] | speed_score = [integer] | is_review = ["T" or "F"] | is_daily = ["T" or "F"] | idx_txt = [idx_txt]`
		  
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ is_okay=[True/False],class=['A' ~ 'D'],"class_voice" : path,"code":1 }`
 
 *class voice can be null*
 
  OR
  
  * **Code:** 200 <br />
    **Content:** `{ is_okay = [True/False],class = ['A' ~'D'],"class_voice" : path, "message" : "모든 문제를 학습하였습니다.","code": 2 }`

  OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "해당 학습자가 존재하지 않습니다.","code": 3 }`

  OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "해당 학습이 존재하지 않습니다.","code": 4 }`
    
* **Sample Call:**
  ```javascript
    $.ajax({
      url: "link/to/api/cure/answer",
      dataType: "json",
      type : "POST",
      data : { 
	     "full_score" : 80,
	     "phone_score" : 70,
	     "speed_score" : 5,
	     "rhythm_score " : 5,
	     "is_review" : "F",
	     "idx_txt" : "poem"
	     "cure_id" : 1
	     "s_id" : 1
		},success : function(r) {
	         console.log(r)
      }
    });   

 answer(4) - consomatch 
----
* **URL**
	/cure/answer

* **Method:**
	  `POST`
*  **URL Params**
   **Required:**
   **Optional:**

* **Data Params**
	   `s_id = [integer]` | `cure_id = [integer] | cure_id2 = [integer] | cure_id3 = [integer] | ori_answer = [character] | stu_answer = [character] | is_review = ["T" or "F"] | is_daily = ["T" or "F"] | idx_txt = [idx_txt]`

*ori_answer & stu_answer should be the word*

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ is_correct=[True/False],correct_voice= path,"code":1 }`
 
  OR
  
  * **Code:** 200 <br />
    **Content:** `{ is_correct = [True/False],correct_voice= path, "message" : "모든 문제를 학습하였습니다.","code": 2 }`

  OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "해당 학습자가 존재하지 않습니다.","code": 3 }`

  OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "해당 학습이 존재하지 않습니다.","code": 4 }`
    
* **Sample Call:**
  ```javascript
    $.ajax({
      url: "link/to/api/cure/answer",
      dataType: "json",
      type : "POST",
      data : { 
	     "cure_id" : 2,
	     "cure_id2" : 3,
	     "cure_id3" : 4,
	     "stu_answer " : "가방",
	     "ori_answer" : "오리",
	     "idx_txt" : "consomatch",
	     "is_review" : "F"
	     "s_id" : 1
		},success : function(r) {
	         console.log(r)
      }
    });   
    
save
----
* **URL**
	/cure/save

* **Method:**
	  `POST`
*  **URL Params**
   **Required:**
   **Optional:**

* **Data Params**
	   `s_id = [integer]` 
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ current: {[read],[treatment]} ,"code":1 }`
 
  OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "해당 학습자가 존재하지 않습니다.","code": 2 }`
  
* **Sample Call:**
  ```javascript
    $.ajax({
      url: "link/to/api/cure/save",
      dataType: "json",
      type : "POST",
      data : { 
	     "s_id" : 1
		},success : function(r) {
	         console.log(r)
      }
    });   
    
**tutorial answer**
----
* **URL**
	/cure/answer

* **Method:**
	  `POST`
*  **URL Params**
   **Required:**
   **Optional:**

* **Data Params**
	   `s_id = [integer] | idx_txt = [character] | tutorial = "true" | ques_id = [integer]` 
		  
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ "is_okay" : True/False} "code":1}`
    
  OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "해당하는 학습이 존재하지 않습니다.","code": "err" }`
      
   OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "해당하는 학습자가 존재하지 않습니다.","code": 3 }`


* **Sample Call:**
  ```javascript
    $.ajax({
      url: "link/to/api/cure/answer",
      dataType: "json",
      type : "POST",
      data : { 
	     "s_id" : 1,
	     "idx_txt" : "count",
	     "tutorial" : "true",
	     "ques_id" : 77
		},success : function(r) {
	         console.log(r)
      }
    });   
    
## Part6 - Statistics

 **ask**
----
* **URL**
	/statistic/ask

* **Method:**
	  `POST`
*  **URL Params**
   **Required:**
   **Optional:**

* **Data Params**
	   `s_id = [integer] | cure_or_test = [cure/test],  period = [day/week/month]`  
	  
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ "amount" : set of integer{학습량} , "score" : set of integer{성취도} , "voice_score" : set of integer(발음 정확도), "class" : 3 of[high/mid/low],"code":"cure"}`

*will be sorted by period
for cure statistics*
 
  OR
  
  * **Code:** 200 <br />
    **Content:** `{ "score_swp" : set of integer{점수} , "score_ph" : set of integer{점수} , "score_foc" : set of integer(점수),"class" : 3 of [high/mid/low],"result" : status[고위험험/저위험/경미/정상],"code":"diagnose"}`
 
  OR

  * **Code:** 200 <br />
    **Content:** `{ "message" : "해당 학습자가 존재하지 않습니다.","code": 2 }`
 


* **Sample Call:**
  ```javascript
    $.ajax({
      url: "link/to/api/statistics/ask",
      dataType: "json",
      type : "POST",
      data : { 
	     "s_id" : 1,
	     "cure_or_test" : "cure",
	     "period" : "day"
		},success : function(r) {
	         console.log(r)
      }
    });   

