"""
用户表单文件

该文件定义了用户相关的表单，包括注册表单、登录表单、个人信息表单等。
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User


class UserRegisterForm(BaseUserCreationForm):
    """
    用户注册表单
    
    继承自Django的UserCreationForm，只包含用户名、密码和确认密码。
    """
    
    class Meta(BaseUserCreationForm.Meta):
        """
        表单元数据配置
        """
        # 直接引用User模型
        model = User
        fields = ('username',)
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': ' '
            }),
        }
        labels = {
            'username': '用户名',
        }
        help_texts = {
            'username': '用户名只能包含字母、数字和@/./+/-/_字符，长度4-20位',
        }
    
    def __init__(self, *args, **kwargs):
        """
        初始化表单
        
        为密码字段添加样式和占位符。
        """
        super().__init__(*args, **kwargs)
        
        # 为密码字段添加样式
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': ' '
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': ' '
        })
        
        # 更新标签
        self.fields['password1'].label = '密码'
        self.fields['password2'].label = '确认密码'
        
        # 添加密码帮助文本
        self.fields['password1'].help_text = '密码至少8位，建议包含字母和数字'
    
    def clean_username(self):
        """
        验证用户名
        
        验证用户名格式是否正确，以及是否已被注册。
        
        Returns:
            str: 清理后的用户名
            
        Raises:
            ValidationError: 用户名格式不正确或已被注册
        """
        username = self.cleaned_data.get('username')
        
        # 验证用户名长度
        if len(username) < 4:
            raise ValidationError('用户名长度不能少于4位')
        
        if len(username) > 20:
            raise ValidationError('用户名长度不能超过20位')
        
        # 验证用户名格式（只能包含字母、数字和@/./+/-/_字符）
        # Django的AbstractUser已经做了基本验证，这里可以添加额外的验证
        # 例如：不允许纯数字用户名
        if username.isdigit():
            raise ValidationError('用户名不能为纯数字')
        
        # 验证用户名是否已被注册
        if User.objects.filter(username=username).exists():
            raise ValidationError('该用户名已被注册')
        
        return username
    
    def clean_password1(self):
        """
        验证密码
        
        验证密码强度是否符合要求。
        
        Returns:
            str: 清理后的密码
            
        Raises:
            ValidationError: 密码强度不符合要求
        """
        password = self.cleaned_data.get('password1')
        
        # 验证密码长度
        if len(password) < 8:
            raise ValidationError('密码长度不能少于8位')
        
        # 验证密码是否包含字母
        if not any(c.isalpha() for c in password):
            raise ValidationError('密码必须包含至少一个字母')
        
        # 验证密码是否包含数字
        if not any(c.isdigit() for c in password):
            raise ValidationError('密码必须包含至少一个数字')
        
        return password


class UserLoginForm(AuthenticationForm):
    """
    用户登录表单
    
    继承自Django的AuthenticationForm，用于用户登录。
    """
    def __init__(self, *args, **kwargs):
        """
        初始化表单
        
        为用户名和密码字段添加样式。
        """
        super().__init__(*args, **kwargs)
        
        # 为用户名字段添加样式
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': ' '
        })
        self.fields['username'].label = '用户名'
        
        # 为密码字段添加样式
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': ' '
        })
        self.fields['password'].label = '密码'


class UserProfileForm(forms.ModelForm):
    """
    用户个人信息表单
    
    用于用户编辑个人信息，包括头像、生日、性别、个人简介等。
    """
    
    class Meta:
        """
        表单元数据配置
        """
        # 直接引用User模型
        model = User
        fields = ('avatar', 'birthday', 'gender', 'bio')
        widgets = {
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'birthday': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '请输入个人简介（最多500字）'
            }),
        }
        labels = {
            'avatar': '头像',
            'birthday': '生日',
            'gender': '性别',
            'bio': '个人简介',
        }
        help_texts = {
            'avatar': '请上传个人头像',
            'birthday': '请选择您的生日',
            'gender': '请选择您的性别',
            'bio': '请输入个人简介（最多500字）',
        }
