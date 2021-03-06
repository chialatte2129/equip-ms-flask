from flask_admin.form.upload import ImageUploadField
from flask_admin.form import thumbgen_filename
from flask_admin.form.fields import Select2Field
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import url_for
from main.models import User
from uuid import uuid4
from jinja2 import Markup
import os.path as op

File_path = op.join (op.dirname(__file__),'static')

class UserView(ModelView):
    # Disable model creation
    can_create = True
    column_display_pk = True
    form_display_pk = True
    column_list = ('ACCOUNT','NAME', 'POSITION', 'AUTH', 'PICTURE')
    form_columns = ( 'NAME','ACCOUNT', 'PASSWORD', 'POSITION', 'AUTH', 'PICTURE')
    column_labels = dict(ACCOUNT="帳號",NAME="姓名",AUTH='權限',PICTURE='大頭照',PASSWORD="密碼",POSITION="職稱")
    
    form_overrides = dict(
        AUTH=Select2Field
    )
    form_args = dict(
        AUTH=dict(
            choices=[
                ('system', '管理員'),
                ('user', '使用者')
            ]
        )
    )

    def is_accessible(self):#登錄了才能顯示，沒有登錄就不顯示
        user_object = User.query.get(current_user.get_id())
        return user_object.AUTH=="system"
    
    def is_visible(self):
        user_object = User.query.get(current_user.get_id())
        return user_object.AUTH=="system"

    def getinfo(self):
        return "this is another model"

    def __init__(self, session, **kwargs):
        super(UserView, self).__init__(User, session, **kwargs)

class UserAdmin(UserView):
    def _list_thumbnail(view, context, model, name):
        if not model.PICTURE:
            return ''
        return Markup('<img src="%s">' % url_for('static',filename=thumbgen_filename(model.PICTURE)))

    column_formatters = {
        'PICTURE': _list_thumbnail
    }

    temp_uuid = str(uuid4())
    form_extra_fields = {
        'PICTURE': ImageUploadField('大頭照',
            base_path=File_path,
            relative_path=f'uploadFile/{temp_uuid}/',
            thumbnail_size=(60, 60, True)
        )
    }