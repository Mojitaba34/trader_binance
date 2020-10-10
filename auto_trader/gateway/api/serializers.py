from rest_framework import serializers

from gateway.models import User

"""
The serializer for make Input data Readable and Always satays in this shape! For User Registertion And Also saves The user on DataBase
"""

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['username', 'fullname', 'email' , 'password', 'password2']


    def save(self):
        user = User(
            username= self.validated_data['username'],
            fullname= self.validated_data['fullname'],
            email= self.validated_data['email'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'Password':'Password must match. Check the password Again'})
        user.set_password(password)
        user.save()
        return user





    
    



