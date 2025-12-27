from pyexpat.errors import messages
from urllib import request
from django.shortcuts import redirect, render
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password

from ISLtranslatorApp.models import ComplaintTable, FeedbackTable, LoginTable, UserTable

# Create your views here.

class LoginPage(View):
    def get(self, request):
        return render(request,'login1.html')
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        try:
            obj = LoginTable.objects.get(username=username, password = password)
            request.session['user_id'] = obj.id
            print('---------------->',obj)
            # Handle based on user type
            if obj.user_role == 'admin':
                return HttpResponse('''<script>alert("Welcome back");window.location='/AdminDash'</script>''')
            elif obj.user_role == 'user':
                return HttpResponse('''<script>alert("Welcome back");window.location='/userdash'</script>''')
            else:
                return HttpResponse('''<script>alert("User not found");window.location='/'</script>''')

        except LoginTable.DoesNotExist:
            # Handle case where login details do not exist
            return HttpResponse('''<script>alert("Invalid username or password");window.location='/'</script>''')
 
 # ////////////////////////// ADMIN ///////////////////////////////////////////////////////
 
        
class AddManageUser(View):
    def get(self, request):
        user=UserTable.objects.all()
        return render(request,'AddManageUser.html',{'users':user})
#Delete View
class deleteuser_delete(View):
    def get(self,request,id):
        delete=LoginTable.objects.get(id=id)
        delete.delete()
        return HttpResponse('''<script>alert("Successfully Updated");window.location='/AddManageUser'</script>''')
class ViewComplaint(View):
    def get(self, request):
        complaint=ComplaintTable.objects.all()
        return render(request,'ViewComplaint.html',{'complaints':complaint})
class SendReply(View):
    def post(self,request,id):
        obj=ComplaintTable.objects.get(id=id)
        obj.reply=request.POST['Reply']
        obj.save()
        return redirect('ViewComplaint')    
class ViewFeedback(View):
    def get(self, request):
        feedback=FeedbackTable.objects.all()
        return render(request,'ViewFeedback.html',{'feedbacks':feedback})      
class AdminDash(View):
    def get(self,request):
        return render(request,'AdminDash.html')     
    
    
    # ///////////////////////////////////// USER ////////////////////////////////////#
class reg(View):
    def get(self,request):
        return render(request,'user/reg.html') 
    def post(self,request):
        name = request.POST['name']
        email = request.POST['email']
        dob = request.POST['dob']
        gender = request.POST['gender']
        phone = request.POST['phone']
        password = request.POST['password']
        
        if LoginTable.objects.filter(username=name).exists():
            messages.error(request, "Username already exists")
            return HttpResponse('''<script>alert("Username alreday exists");window.location='/reg'</script>''')

        login_obj = LoginTable()
        login_obj.username=email
        login_obj.password=password
        login_obj.user_role="user"
        
        login_obj.save()
        
        user_obj = UserTable()
        user_obj.fullname = name
        user_obj.email = email
        user_obj.date_of_birth= dob
        user_obj.gender= gender
        user_obj.phone_no= phone  
        user_obj.LOGIN_ID=login_obj
        user_obj.save()
        return redirect('/')

        
    
class complaint(View):
    def get(self,request):
        return render(request,'user/complaint.html') 
    def post(self,request):
        obj=ComplaintTable()
        obj.complaint=request.POST['complaint']
        obj.USER_ID=UserTable.objects.get(LOGIN_ID__id=request.session['user_id'])
        obj.save()
        return redirect('userdash')
    
class feedback(View):
    def get(self,request):
        return render(request,'user/feedback.html') 
    def post(self,request):
        print('----------------->',request.session['user_id'] )
        obj=FeedbackTable()
        obj.feedback=request.POST['feedback']
        obj.USER_ID=UserTable.objects.get(LOGIN_ID__id=request.session['user_id'])
        obj.save()
        return redirect('userdash')
    
class viewcompuser(View):
    def get(self,request):
        complaint=ComplaintTable.objects.filter(USER_ID__LOGIN_ID_id=request.session['user_id'])
        
        return render(request,'user/viewcompuser.html',{'complaints':complaint})

from real_time_detection import detection
class detections(View):
    def get(self,request):
        detection()    
        return redirect('userdash')
 
from django.shortcuts import render
from django.http import StreamingHttpResponse
from camera import generate_frames

class isl_page(View):
    def get(self,request):
        return render(request, 'user/isl_live.html')

class video_feed(View):
    def get(self,request):
        return StreamingHttpResponse(
            generate_frames(),
            content_type='multipart/x-mixed-replace; boundary=frame'
        )
 
    
class userdash(View):
    def get(self,request):
        return render(request,'user/userdash.html')    

from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages

class change_password(View):
    def get(self, request):
        return render(request, 'user/changepassword.html')

    def post(self, request):
        login_id = request.session.get('user_id')

        login_obj = LoginTable.objects.get(id=login_id)

        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check current password
        if login_obj.password != current_password:
            messages.error(request, "Current password is incorrect")
            return redirect('change_password')

        # Check new password match
        if new_password != confirm_password:
            messages.error(request, "New passwords do not match")
            return redirect('change_password')

        # Update password
        login_obj.password = new_password
        login_obj.save()
        return HttpResponse('''<script>alert("Password changed successfully");window.location='/'</script>''')

import random
import string
from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


from django.core.mail import send_mail
from django.conf import settings

class forgot_password(View):
    def get(self, request):
        return render(request, 'user/forgotpassword.html')


    def post(self, request):
        email = request.POST.get("email")

        try:
            user = LoginTable.objects.get(username=email)

            password = user.password  # ❌ plain text only

            send_mail(
                subject="Your Password",
                message=f"Your password is: {password}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )

            return HttpResponse("Password sent to your email")

        except LoginTable.DoesNotExist:
            return render(request, 'user/forgotpassword.html', {
                'error': 'Email not registered'
            })


# class set_new_password(View):

#     def get(self, request):
#         return render(request, 'user/set_new_password.html')

#     def post(self, request):
#         email = request.session.get('reset_email')
#         print("EMAIL:", email)

#         if not email:
#             return redirect('forgot_password')

#         password = request.POST.get("password")
#         confirm = request.POST.get("confirm_password")

#         print(password, "************")
#         print(confirm, "????????????")

#         if password != confirm:
#             return render(request, 'user/set_new_password.html', {
#                 'error': 'Passwords do not match'
#             })

#         user = LoginTable.objects.get(username=email)
#         user.password = password
#         user.save()

#         del request.session['reset_email']

#         return HttpResponse('''<script>alert("Password changed successfully");window.location='/'</script>''')

import subprocess
from django.http import JsonResponse

from django.http import HttpResponseRedirect, JsonResponse
from django.views import View
import subprocess
import socket
import time

class StartSignAnimationView(View):
    def get(self, request):
        print("Starting sign animation frontend...")

        project_path = r"D:\ISLtranslator\ISLtranslator\sign_animation"
        frontend_url = "http://localhost:4200/"

        try:
            # Step 1: Check if frontend already running
            if self.is_port_in_use(4200):
                print("Frontend already running.")
                return HttpResponseRedirect(frontend_url)

            # Step 2: Start frontend in background
            subprocess.Popen(
                "npm start",
                cwd=project_path,
                shell=True
            )

            # Step 3: Wait for the server to come up (max 45 sec)
            print("Waiting for Angular server to start...")
            for i in range(45):
                if self.is_port_in_use(4200):
                    print("Angular server is up!")
                    return HttpResponseRedirect(frontend_url)
                time.sleep(1)

            # Step 4: Timeout
            print("Timeout: Angular did not start in time.")
            return JsonResponse({
                "status": "starting",
                "message": "Frontend is starting... Try refreshing after a few seconds."
            })

        except Exception as e:
            print("Error starting frontend:", e)
            return JsonResponse({"status": "error", "message": str(e)})

    @staticmethod
    def is_port_in_use(port):
        """Check if a given TCP port is in use (localhost)."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(("localhost", port)) == 0