from django.contrib import admin

from .models import Account

""" 定義したモデルをimportしてきて、モデルをadminページ(管理画面)上でみえるように
    するため  admin.site.register(Post)　でモデルを登録。
"""

admin.site.register(Account)
