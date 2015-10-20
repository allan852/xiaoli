#! -*- coding:utf-8 -*-

from flask.ext.wtf import Form
from wtforms import PasswordField, TextAreaField, HiddenField, StringField
from flask.ext.babel import lazy_gettext as _
from wtforms.validators import ValidationError, Email, Length, EqualTo, DataRequired

from xiaoli.models.account import Account
from xiaoli.models.session import db_session_cm


class LoginForm(Form):
    phone = StringField(_(u'手机号'),
                        validators=[DataRequired(message=_(u'手机号不能为空'))],
                        description=_(u'手机号'))
    password = PasswordField(_(u'密码'),
                             validators=[DataRequired(message=_(u'密码不能为空'))],
                             description=_(u'密码'))

    def validate_phone(form, field):
        with db_session_cm() as session:
            user = session.query(Account).filter(Account.cellphone == field.data.strip()).first()
            if not user or user.status == Account.STATUS_UNREGISTERED:
                raise ValidationError(_(u'手机号不存在'))

    def validate_password(form, field):
        with db_session_cm() as session:
            user = session.query(Account).filter(Account.cellphone == form.phone.data.strip()).first()
            if user:
                if not user.check_password(field.data.strip()):
                    raise ValidationError(_(u'密码不正确'))


class RegisterForm(Form):
    phone = StringField(_(u'手机号'),
                        validators=[DataRequired(message=_(u'手机号不能为空'))],
                        description=_(u'手机号'))
    password = PasswordField(_(u'密码'),
                             validators=[DataRequired(message=_(u'密码不能为空')),
                                         Length(min=6, max=30, message=_(u'密码最少6位， 最多30位'))],
                             description=_(u'密码'))

    password_check = PasswordField(_(u'密码确认'),
                                   validators=[DataRequired(message=_(u'确认密码不能为空')),
                                               EqualTo('password', message=_(u'密码不一致')),
                                               Length(min=6, max=30, message=_(u'密码最少6位， 最多30位'))],
                                   description=_(u'确认密码'))

    def validate_phone(form, field):
        with db_session_cm() as session:
            user = session.query(Account).filter(Account.cellphone == field.data.strip()).first()
            if user and user.status != Account.STATUS_UNREGISTERED:
                raise ValidationError(_(u'手机号已存在'))


class ForgotPasswordForm(Form):
    email = StringField(_(u'注册邮箱'),
                        validators=[DataRequired(message=_(u'邮箱不能为空')), Email(message=_(u'邮箱格式不正确'))],
                        description=_(u'注册邮箱'))

    def validate_email(form, field):
        user = Account.m.find({'email': field.data.strip()}).first()
        if not user:
            raise ValidationError(_(u'邮箱不存在'))


class ResetPasswordForm(Form):
    email = StringField(_(u'邮箱'), validators=[Email(message=_(u'邮箱格式不正确'))], description=_(u'邮箱'))

    id = HiddenField(_(u'ID'))
    key = HiddenField(_(u'KEY'))

    password = PasswordField(_(u'新密码'), description=_(u'新密码'))

    confirm_password = PasswordField(_(u'确认密码'), description=_(u'确认密码'))

    def validate_password(form, field):
        if field.data:
            length_validate = Length(min=6, max=30, message=_(u'密码最少6位， 最多30位'))
            length_validate(form, field)
        else:
            raise ValidationError(_(u'新密码不能为空'))

    def validate_confirm_password(form, field):
        if form.password.data and \
                not field.data:
            raise ValidationError(_(u'确认密码不能为空'))

        if form.password.data and field.data and \
                not field.data == form.password.data:
            raise ValidationError(_(u'两次密码不一致'))

