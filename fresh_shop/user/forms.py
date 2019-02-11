from django import forms

from user.models import User, UserAddress


class UserRegisterForm(forms.Form):

    username = forms.CharField(max_length=20, min_length=5, required=True, error_messages={
        'required':'用户名不能为空',
        'max_length':'用户名不能超过20位字符',
        'min_length':'用户名不能少于5字符',
    })
    pwd = forms.CharField(max_length=20, min_length=8, required=True, error_messages={
        'required': '密码不能为空',
        'max_length': '密码不能超过20位字符',
        'min_length': '密码不能少于8字符',
    })
    cpwd = forms.CharField(max_length=20, min_length=8, required=True, error_messages={
        'required': '密码不能为空',
        'max_length': '密码不能超过20位字符',
        'min_length': '密码不能少于8字符',
    })
    email = forms.CharField(required=True, error_messages={
        'required': '密码不能为空',
    })
    #验证自动调用
    def clean(self):
        user = User.objects.filter(username=self.cleaned_data.get('username'))

        if user:
            raise forms.ValidationError({'username':'该用户已存在请去登录'})

        pwd = self.cleaned_data.get('pwd')
        cpwd = self.cleaned_data.get('cpwd')
        if pwd != cpwd:
            raise forms.ValidationError({'pwd':'确认密码和密码不一致'})
        return self.cleaned_data

class UserLoginForm(forms.Form):

    username = forms.CharField(max_length=20, min_length=5, required=True, error_messages={
        'required':'用户名不能为空',
        'max_length':'用户名不能超过20位字符',
        'min_length':'用户名不能少于5字符',
    })
    pwd = forms.CharField(max_length=20, min_length=8, required=True, error_messages={
        'required': '密码不能为空',
        'max_length': '密码不能超过20位字符',
        'min_length': '密码不能少于8字符',
    })

    def clean(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError({'username':'用户不存在请去注册'})

        return self.cleaned_data


class UserSiteForm(forms.Form):
    signer_name = forms.CharField(max_length=20, min_length=2, required=True, error_messages={
        'required':'收件人名字不能为空',
        'max_length':'收件人名字不能超过20位字符',
        'min_length':'收件人名字不能少于2字符',
    })
    site = forms.CharField(max_length=666, min_length=6, required=True, error_messages={
        'required': '地址不能为空',
        'max_length': '地址不能超过666位字符',
        'min_length': '地址不能少于6字符',
    })
    postcode = forms.CharField(max_length=12, min_length=5, required=True,
                                error_messages = {
                                    'required': '邮编不能为空',
                                    'max_length': '邮编不能超过12位字符',
                                    'min_length': '邮编不能少于5字符',
                                })
    phone = forms.CharField(max_length=12, min_length=11, required=True,
                                error_messages = {
                                    'required': '手机号码不能为空',
                                    'max_length': '手机号码不能超过12位字符',
                                    'min_length': '手机号码不能少于11字符',
                                })
    # def clean(self):
    #     signer_name = self.cleaned_data.get('signer_name')
    #     user = UserAddress.objects.filter(username=signer_name).first()
    #     if not user:
    #         raise forms.ValidationError({'username':'用户不存在请去注册'})
    #
    #     return self.cleaned_data