import os
import pymysql #to use mysql 
pymysql.version_info = (1, 3, 13, "final", 0)
pymysql.install_as_MySQLdb()
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cm6)q4k#-=q^ll8#au0tuam9m)mq4ofku1r0+yx4$gtiv1+l4_' #여기는 잘라줘

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True #개발과정에서 에러 체크하기 위한 용도로 켜둠. 실제 서비스 단계에서는 false로 변경됨. 

ALLOWED_HOSTS = ['ec2-13-125-100-8.ap-northeast-2.compute.amazonaws.com','13.125.100.8'] #현재 ec2 퍼블릭 dns랑 ip주소를 포함시켜서 이 주소로 접속 할 수 있게함. 주소는 가리거나 대체해도 될듯.



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'tt_apis', #api app

    'rest_framework', #django_rest_framework
    'corsheaders', #cors 설정 허용을 위함
    'allauth',
    'allauth.account',
    # 'allauth.account.context_processors',
    # ' allauth.socialaccount.context_processors.socialaccount',
    'rest_auth.registration',
    'django.contrib.sites',
]

SITE_ID = 1
# AUTH_USER_MODEL = 'tt_apis.User'
# REST_USE_JWT = True
# ACCOUNT_EMAIL_REQUIRED = False
# ACCOUNT_USERNAME_REQUIRED = False
# ACCOUNT_EMAIL_VERIFICATION = None
# ACCOUNT_LOGOUT_ON_GET = True

MIDDLEWARE = [ #기본설정
    'corsheaders.middleware.CorsMiddleware',    
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    #'django.middleware.csrf.CsrfViewMiddleware', #api test단계에서 csrf exception을 무시하고 테스트 하기 위해 꺼둔 옵션

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'api.urls' #url routing에 대한 정보를 포함하고 있는 파일

TEMPLATES = [ #기본설정
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "allauth.account.context_processors.account",
                "allauth.socialaccount.context_processors.socialaccount",
            ],
        },
    },
]

WSGI_APPLICATION = 'api.wsgi.application' #wsgi 설정파일


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = { #DB정보 설정해줌. PW는 가려주세요
     'default': {
        'ENGINE': 'django.db.backends.mysql', #mysql 사용


        'NAME': 'ttobak', # DB명

        'USER': 'root', # 데이터베이스 계정
        'PASSWORD': 'soma2020', # 계정 비밀번호
        'HOST': 'ttobak.cbbaovh5sf1x.ap-northeast-2.rds.amazonaws.com', # 데이테베이스 주소(IP)
        'PORT': '3306', # 데이터베이스 포트(보통은 3306)
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO'", #에러 방지하기 위해 옵션 추가해줌
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [ #기본 설정
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ko-kr' #기본 언어 셋


TIME_ZONE = 'Asia/Seoul' #타임존 설정

USE_I18N = True #기본 설정

USE_L10N = True #기본설정

USE_TZ = True #기본 설정

REST_FRAMEWORK = { #허용된 상태만 restframework에 접근할 수 있도록 설정해줌.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',

    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ],
}



# CORS_ORIGIN_WHITELIST = ( #실제 api를 호출하게 될 주소를 포함시켜서 cors설정을 허용해줌.
#     'http://localhost:3000',
#     'http://127.0.0.1:3000',
#     'http://ec2-13.125.100.8.ap-northeast-2.compute.amazonaws.com:3000',
#     'http://ec2-13.125.100.8.ap-northeast-2.compute.amazonaws.com', 
# )
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True #개발 단계에서 테스트를 보다 편하게 하기 위해 모든 접근에 대해서 허용해둠. 곧 닫을 예정.

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/' #static 파일 경로
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/' #media 파일 경로
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

