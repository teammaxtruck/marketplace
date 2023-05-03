from rest_framework import serializers
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from usersapp.models import User,Country,State,City,Language,Keylang
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from usersapp.utils import Util

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class CountryStateCitySerializer(serializers.ModelSerializer):
   # country=
    class Meta:
        model = City
        fields = '__all__'

#-----------------------------
class UserRegistrationSerializer(serializers.ModelSerializer):
  # We are writing this becoz we need confirm password field in our Registratin Request
  password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  class Meta:
    model = User
    fields=['email', 'fullname','phone','code','country','state','city','type_user','profile_image','bg_image', 'password', 'password2']
    extra_kwargs={
      'password':{'write_only':True}
    }

  # Validating Password and Confirm Password while Registration
  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    return attrs

  def create(self, validate_data):
    return User.objects.create_user(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password']

class UserChangePasswordSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    uid = self.context.get('uid')
    user = self.context.get('user')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    user.set_password(password)
    user.save()
    return attrs

class UserPutProfileSerializer(serializers.ModelSerializer):

  class Meta:
    model = User
    # fields = "__all__"
    fields = ['id', 'type_user','email','code','phone', 'fullname','profile_image','bg_image','country','state','city']

class UserwebProfileSerializer(serializers.ModelSerializer):
 
  class Meta:
    model = User
    # fields = "__all__"
    fields = ['id', 'type_user','email','code','phone', 'fullname','profile_image','bg_image','country','state','city']
class UserProfileSerializer(serializers.ModelSerializer):
  country=serializers.SlugRelatedField(many=False, slug_field="country",queryset=Country.objects.all())
  state=serializers.SlugRelatedField(many=False, slug_field="state",queryset=State.objects.all())
  city=serializers.SlugRelatedField(many=False, slug_field="city",queryset=City.objects.all())
  class Meta:
    model = User
    # fields = "__all__"
    fields = ['id', 'type_user','email','code','phone', 'fullname','profile_image','bg_image','country','state','city']
class UserActiveSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'      
class SendPasswordResetEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    fields = ['email']

  def validate(self, attrs):
    email = attrs.get('email')
    if User.objects.filter(email=email).exists():
      user = User.objects.get(email = email)
      uid = urlsafe_base64_encode(force_bytes(user.id))
      #print('Encoded UID', uid)
      token = PasswordResetTokenGenerator().make_token(user)
      #print('Password Reset Token', token)
      link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
      #print('Password Reset Link', link)
      # Send EMail
      body = 'Click Following Link to Reset Your Password '+link
      data = {
        'subject':'Reset Your Password',
        'body':body,
        'to_email':user.email
      }
    #ayman do that#  Util.send_email(data)
      return attrs
    else:
      raise serializers.ValidationError('You are not a Registered User')

class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      password2 = attrs.get('password2')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != password2:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      id = smart_str(urlsafe_base64_decode(uid))
      user = User.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name', 'code']
class KeylangSerializer(serializers.ModelSerializer):
   # lang=serializers.SlugRelatedField(many=False, slug_field="name",queryset=Language.objects.all())
    class Meta:
        model = Keylang
        fields = '__all__'
