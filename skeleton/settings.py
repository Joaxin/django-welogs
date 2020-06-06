"""
Django settings for QU project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xc3=e7kw8lr+pbjo+3g_x++hs4n3rij2=$s=ygu$+$9fp!@^t2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    # Third-party admin
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    # 'django.contrib.postgres',
    

    # Third-party
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'taggit',
    'imagekit',
    'crispy_forms',
    'debug_toolbar',
    'markdownx',
    'rosetta',
    # 'rest_framework',
    'rest_framework',
    # Local
    'users.apps.UsersConfig',
    'op',
    'aphor',
]

# django.contrib.sites
SITE_ID = 1


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # debug
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'skeleton.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'skeleton.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'


LANGUAGES = (
    ('en-us', ('English')),
    ('cn', ('Chinese')),
)

TIME_ZONE = 'Asia/Shanghai'
# TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Email

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = 'smtp.163.com'
EMAIL_HOST_USER = 'llsites@163.com'
EMAIL_HOST_PASSWORD = 'llsite142857s'
EMAIL_PORT = 465  # SMTP服务端口，默认是25
# EMAIL_USE_TLS = True
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = '注册确认 <llsites@163.com>'

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT =  os.path.join(BASE_DIR, 'media').replace('\\', '/') 
# 定义主机IP
HOST = "http://localhost:8000/"
# 定义图片暂存目录和模型图片目录
TEMP_IMAGE_SUB_DIR = "/tempimg/"
# 图片暂存目录
TEMP_IMAGE_DIR = MEDIA_ROOT + TEMP_IMAGE_SUB_DIR
# 模型图片目录
MODEL_IMAGE_SUB_DIR = "/model_images/"
MODEL_IMAGE_DIR = MEDIA_ROOT + MODEL_IMAGE_SUB_DIR
# 定义缩略图URL:http://127.0.0.1:8000/mdedia/tempimg/
WEB_HOST_MEDIA_URL = HOST+ MEDIA_URL[1:]+ TEMP_IMAGE_SUB_DIR
# 定义模型中保存的图片URL:http://127.0.0.1:8000/mdedia/model_images/
MODEL_MEDIA_URL = HOST + MEDIA_URL[1:] + MODEL_IMAGE_SUB_DIR


# Auth 
AUTH_USER_MODEL = 'users.CustomUser'

# CRISPY FORMS
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Django-debug-toolbar to work
INTERNAL_IPS = ['127.0.0.1']

# Django-Allauth Config
LOGIN_REDIRECT_URL = '/accounts/profile/'
ACCOUNT_LOGOUT_REDIRECT_URL = 'home'

AUTHENTICATION_BACKENDS = (
     # django admin所使用的用户登录与django-allauth无关 
    "django.contrib.auth.backends.ModelBackend",
      # allauth 身份验证
    "allauth.account.auth_backends.AuthenticationBackend",
)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASS': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_USERNAME_REQUIRED = False
# 指定要使用的登录方法(用户名、电子邮件地址两者之一)
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
# 要求用户注册时必须填写email
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
# 注册中邮件验证方法: "强制(mandatory)"、 "可选(optional)" 或 "否(none)" 之一
# 注册成功后，会发送一封验证邮件，用户必须验证邮箱后，才能登陆
ACCOUNT_EMAIL_VERIFICATION ="optional"

# 作用于第三方账号的注册
SOCIALACCOUNT_EMAIL_VERIFICATION = 'optional'
# 邮件发送后的冷却时间(以秒为单位)
ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN =180
# 邮箱确认邮件的截止日期(天数)
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1


# 登录尝试失败的次数
ACCOUNT_LOGIN_ATTEMPTS_LIMIT =5
# 从上次失败的登录尝试，用户被禁止尝试登录的持续时间
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT =300
# 更改为True，用户一旦确认他们的电子邮件地址，就会自动登录
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False

# 更改或设置密码后是否自动退出
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE =False
# 更改为True，用户将在重置密码后自动登录
ACCOUNT_LOGIN_ON_PASSWORD_RESET =False
# 控制会话的生命周期，可选项还有: "False" 和 "True"
ACCOUNT_SESSION_REMEMBER =None

# 用户注册时是否需要输入邮箱两遍
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE =False
# 用户注册时是否需要用户输入两遍密码
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE =True
# 用户不能使用的用户名列表
ACCOUNT_USERNAME_BLACKLIST =[]
# 加强电子邮件地址的唯一性
ACCOUNT_UNIQUE_EMAIL =True 
# 用户名允许的最小长度的整数
ACCOUNT_USERNAME_MIN_LENGTH =1
# 使用从社交账号提供者检索的字段(如用户名、邮件)来绕过注册表单
SOCIALACCOUNT_AUTO_SIGNUP =True 

# 用户登出是否需要确认确认(True表示直接退出，不用确认；False表示需要确认)
ACCOUNT_LOGOUT_ON_GET = False


# markdownx options
MARKDOWNX_EDITOR_RESIZABLE = False
MARKDOWNX_MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra',
    'markdown.extensions.nl2br',
    'markdown.extensions.codehilite',
    'fenced_code', 'codehilite'
]
MARKDOWNX_MEDIA_PATH = datetime.datetime.now().strftime('markdown/upload/%Y/%m/%d')
MARKDOWNX_UPLOAD_MAX_SIZE = 4 * 1024 * 1024
MARKDOWNX_UPLOAD_CONTENT_TYPES = ['image/jpeg', 'image/png', 'image/svg+xml']
MARKDOWNX_IMAGE_MAX_SIZE = {
    'size': (800, 500),
    'quality': 90
}
