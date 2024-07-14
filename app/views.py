from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import user_passes_test,login_required
from app.forms import UserForm
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Idea,Idea_viewed,Token,UserProfile,Idea_bought,deal_status,bugs_and_messages,Extra_token_request,Agent_call_request,User
from django.http import JsonResponse,HttpResponse
from django.core.mail import send_mail
import json
import razorpay
from django.shortcuts import redirect

# Create your views here.

# def custom_login_required(redirect_to='/'):
#     def decorator(view_func):
#         @wraps(view_func)
#         def _wrapped_view(request, *args, **kwargs):
#             if request.user.is_authenticated:
#                 return view_func(request, *args, **kwargs)
#             else:
#                 return redirect(redirect_to)
#         return _wrapped_view
#     return decorator

@csrf_exempt
def home(request):
    if request.user.is_anonymous == False:
      try:
        token = Token.objects.get(user=request.user)
        return render(request, 'home.html',{'token':token})
      except Exception as e:
        token = Token(user = request.user)
        token.save()
        profiles = UserProfile(user=request.user)
        profiles.save()
        return render(request, 'home.html',{'token':token})
    else:
        return render(request, 'home.html')


@login_required(login_url='Userlogin')
def Userlogout(request):
    logout(request)
    return redirect('home')

def allusers(request):
    user = request.user
    if user.is_staff:
       allusers= User.objects.order_by('-date_joined')
       allusers_count = User.objects.count()
       return render(request, 'allusers.html', {'allusers': allusers,'allusers_count': allusers_count})
    else:
        return redirect(home)

# @login_required(login_url='Userlogin')
def contact(request):
    user = request.user
    if request.user.is_anonymous == False:
      token = Token.objects.get(user=request.user)
      if request.method == 'POST':
        name = request.POST.get('name')
        mail = request.POST.get('email')
        message = request.POST.get('message')
        bugsandmessages = bugs_and_messages(mail = mail, message = message,name = name)
        bugsandmessages.save()
        messages.success(request,'Message sent successfully.')
        return render(request, 'contact.html',{'token':token,'user':user})
      return render(request, 'contact.html',{'token':token,'user':user})
    else:
        if request.method == 'POST':
            name = request.POST.get('name')
            mail = request.POST.get('email')
            message = request.POST.get('message')
            bugsandmessages = bugs_and_messages(mail = mail, message = message,name = name)
            bugsandmessages.save()
            messages.success(request,'Message sent successfully.')
            return render(request, 'contact.html',{'user':user})
        return render(request, 'contact.html',{'user':user})
    
@login_required(login_url='Userlogin')
def invest(request):
    if request.method =='POST':
        token = Token.objects.get(user=request.user)
        industry = request.POST.get('industry')
        if industry == 'All':
            Ideas = Idea.objects.filter(idea_approved = 'Yes')
            return render(request,'invest.html',{'Ideas': Ideas,'token':token})
        else:
            Ideas = Idea.objects.filter(idea_approved = 'Yes',idea_industry= industry)
            return render(request,'invest.html',{'Ideas': Ideas,'industry' : industry ,'token':token})
    
    token = Token.objects.get(user=request.user)
    Ideas = Idea.objects.filter(idea_approved = 'Yes',)
    return render(request,'invest.html',{'Ideas': Ideas,'token':token})
    
def example_idea(request):
    return render(request,'example_idea.html')

@csrf_exempt
def billing(request , Idea_id):
    Ideas = Idea.objects.get(id= Idea_id)
    client = razorpay.Client(auth=('rzp_test_ClH6E4FgEWpPoz','UbdU2Jdi241y6fNAZKA7Bi1Q'))
    amount = Ideas.idea_instant_investment
    amount2 = Ideas.idea_total_investment
    service_fee = amount2*0.02
    total= service_fee+amount
    total_rzp = total*100
    if request.method=='POST':
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        print(razorpay_payment_id)
        payment = client.payment.fetch(razorpay_payment_id)
        payment_amount = int(payment['amount'])
        print(payment_amount)
        order = client.order.create({'amount': payment_amount, 'currency':'INR', 'payment_capture': '1'})
        razorpay_order_id = request.POST.get('razorpay_order_id')
        print(razorpay_order_id)
        if payment_amount == total_rzp:
            return redirect('idea_provider',Idea_id=Idea_id)
        else:
            return HttpResponse('Error Occurred, Please contact us and report your problem.')
    return render(request,'billing.html',{'Ideas':Ideas,'service_fee':service_fee,'total':total,'total_rzp':total_rzp,'Idea_id':Idea_id})

def idea_provider(request , Idea_id):
    referrer = request.META.get('HTTP_REFERER', '')
    print(referrer)
    if "/billing" in referrer :
        Ideas = Idea.objects.get(id= Idea_id)
        Ideabought=Idea_bought(user=request.user,Idea = Ideas)
        Ideabought.save()
    # subject = 'Regarding your startup Idea posted on NIKI & TONY'
    # message = 'Hey '+Ideas.idea_posted_by_name+', Your Idea that you posted on NIKI & TONY has been bought by an Investor named '+request.user.first_name+' '+request.user.last_name+'. Your quoted instant investment for your idea has been paid by the investor to the company. Once you login to your account and update the status of your deal in your profile after discussing with your investor, then the instant investment money will be transferred to your account.'
    # from_email = 'bvsnikhilesh21@gmail.com'  # Replace with your email
    # recipient_list = [Ideas.idea_posted_by_mail]
    # send_mail(subject, message, from_email, recipient_list)
        return render(request,'idea_provider.html',{'Ideas':Ideas})
    else:
        return redirect(invest)
def details_edit(request):
    user = request.user  # Fetch the logged-in user details
    user_profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        address = request.POST.get('address')
        profession = request.POST.get('profession')
        mobile = request.POST.get('mobile')
        gender = request.POST.get('gender')
        user_profile.address = address
        user_profile.profession = profession
        user_profile.mobile = mobile
        user_profile.gender = gender
        user_profile.save()
        return redirect(profile)
    return render(request, 'details_edit.html', {'user': user,'user_profile': user_profile})


def profile(request): 
   try :
    user = request.user
    Ideas = Idea.objects.filter(uploaded_by=user).order_by('-posted_datetime') 
    Ideaviewed =Idea_viewed.objects.filter(user=user).order_by('-viewed_at')
    Ideabought=Idea_bought.objects.filter(user=user).order_by('-bought_at')
    profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        idea_id = int(request.POST.get('idea_id'))
        role = request.POST.get('role')
        print(role)
        # try :
        deal_Status = deal_status.objects.filter(idea_id = idea_id)
        if not deal_Status.exists():
          if role == 'investor':
            investor_username = request.POST.get('investor_username')
            investor_deal_status = request.POST.get('investor_deal_status')
            dealStatus= deal_status(idea_id=idea_id,investor_username=investor_username,investor_deal_status=investor_deal_status)
            dealStatus.save()
            return render(request, 'profile.html', {'user': user, 'Ideas': Ideas,'Ideaviewed':Ideaviewed,'profile':profile,'Idea_bought':Ideabought})
          elif role == 'idea_provider':
            idea_provider_username = request.POST.get('idea_provider_username')
            idea_provider_deal_status = request.POST.get('idea_provider_deal_status')
            dealStatus= deal_status(idea_id=idea_id,idea_provider_username=idea_provider_username,idea_provider_deal_status=idea_provider_deal_status)
            dealStatus.save()
            return render(request, 'profile.html', {'user': user, 'Ideas': Ideas,'Ideaviewed':Ideaviewed,'profile':profile,'Idea_bought':Ideabought})
        else:  
         if role == 'investor':
            investor_username = request.POST.get('investor_username')
            investor_deal_status = request.POST.get('investor_deal_status')
            dealstatus = list(deal_Status)
            for obj in dealstatus:
                obj.idea_id = idea_id
                obj.investor_username = investor_username
                obj.investor_deal_status = investor_deal_status
                obj.save()
            # dealStatus= dealstatus(investor_username=investor_username,investor_deal_status=investor_deal_status)
            # dealstatus.save()
            return render(request, 'profile.html', {'user': user, 'Ideas': Ideas,'Ideaviewed':Ideaviewed,'profile':profile,'Idea_bought':Ideabought})
         elif role == 'idea_provider':
            idea_provider_username = request.POST.get('idea_provider_username')
            idea_provider_deal_status = request.POST.get('idea_provider_deal_status')
            dealstatus = list(deal_Status)
            for obj in dealstatus:
                obj.idea_id = idea_id
                obj.idea_provider_username = idea_provider_username
                obj.idea_provider_deal_status = idea_provider_deal_status
                obj.save()
            # dealStatus= dealstatus(idea_provider_username=idea_provider_username,idea_provider_deal_status=idea_provider_deal_status)
            # dealStatus.save()
            return render(request, 'profile.html', {'user': user, 'Ideas': Ideas,'Ideaviewed':Ideaviewed,'profile':profile,'Idea_bought':Ideabought})
        # except deal_status.DoesNotExist:
        #   dealstatus = deal_status.objects.create({'idea_id' : idea_id})
        if role == 'investor':
            investor_username = request.POST.get('investor_username')
            investor_deal_status = request.POST.get('investor_deal_status')
            dealStatus= dealstatus(investor_username=investor_username,investor_deal_status=investor_deal_status)
            dealStatus.save()
            return render(request, 'profile.html', {'user': user, 'Ideas': Ideas,'Ideaviewed':Ideaviewed,'profile':profile,'Idea_bought':Ideabought})
        elif role == 'idea_provider':
            idea_provider_username = request.POST.get('idea_provider_username')
            idea_provider_deal_status = request.POST.get('idea_provider_deal_status')
            dealStatus= dealstatus(idea_provider_username=idea_provider_username,idea_provider_deal_status=idea_provider_deal_status)
            dealStatus.save()
            return render(request, 'profile.html', {'user': user, 'Ideas': Ideas,'Ideaviewed':Ideaviewed,'profile':profile,'Idea_bought':Ideabought})

        # else:
        #     return HttpResponse('Sorry')
        # else:
        #   if role == 'investor':
        #     investor_username = request.POST.get('investor_username')
        #     investor_deal_status = request.POST.get('investor_deal_status')
        #     dealstatus= deal_status(idea_id=idea_id,investor_username=investor_username,investor_deal_status=investor_deal_status)
        #     dealstatus.save()
        #     return render(request, 'profile.html', {'user': user, 'Ideas': Ideas,'Ideaviewed':Ideaviewed,'profile':profile,'Idea_bought':Ideabought})
        #   elif role == 'idea_provider':
        #     idea_provider_username = request.POST.get('idea_provider_username')
        #     idea_provider_deal_status = request.POST.get('idea_provider_deal_status')
        #     dealstatus= deal_status(idea_id=idea_id,idea_provider_username=idea_provider_username,idea_provider_deal_status=idea_provider_deal_status)
        #     dealstatus.save()
        #     return render(request, 'profile.html', {'user': user, 'Ideas': Ideas,'Ideaviewed':Ideaviewed,'profile':profile,'Idea_bought':Ideabought})     

    return render(request, 'profile.html', {'user': user, 'Ideas': Ideas,'Ideaviewed':Ideaviewed,'profile':profile,'Idea_bought':Ideabought})
   except Exception as e:
        user = request.user
        profiles = UserProfile(user=request.user)
        profiles.save()
        return redirect('profile')
        # Ideas = Idea.objects.filter(uploaded_by=user).order_by('-posted_datetime') 
        # Ideaviewed =Idea_viewed.objects.filter(user=user).order_by('-viewed_at')
        # Ideabought=Idea_bought.objects.filter(user=user).order_by('-bought_at')
        # if request.method == 'POST':
        #    idea_id = int(request.POST.get('idea_id'))
        #    role = request.POST.get('role')
        #    print(role)
        # # try :
        #    deal_Status = deal_status.objects.filter(idea_id = idea_id)
        #    if not deal_Status.exists():
        #         if role == 'investor':
        #             investor_username = request.POST.get('investor_username')
        #             investor_deal_status = request.POST.get('investor_deal_status')
        #             dealStatus= deal_status(idea_id=idea_id,investor_username=investor_username,investor_deal_status=investor_deal_status)
        #             dealStatus.save()
        #             return render(request, 'profile.html', {'user': user, 'Ideas': Ideas,'Ideaviewed':Ideaviewed,'profile':profile,'Idea_bought':Ideabought})
        #         elif role == 'idea_provider':
        #             idea_provider_username = request.POST.get('idea_provider_username')
        #             idea_provider_deal_status = request.POST.get('idea_provider_deal_status')
        #             dealStatus= deal_status(idea_id=idea_id,idea_provider_username=idea_provider_username,idea_provider_deal_status=idea_provider_deal_status)
        #             dealStatus.save()
        #             return render(request, 'profile.html', {'user': user, 'Ideas': Ideas,'Ideaviewed':Ideaviewed,'profile':profile,'Idea_bought':Ideabought})
        #    else:  
        #         if role == 'investor':
        #             investor_username = request.POST.get('investor_username')
        #             investor_deal_status = request.POST.get('investor_deal_status')
        #             dealstatus = list(deal_Status)
        #             for obj in dealstatus:
        #                 obj.idea_id = idea_id
        #                 obj.investor_username = investor_username
        #                 obj.investor_deal_status = investor_deal_status
        #                 obj.save()
        #             # dealStatus= dealstatus(investor_username=investor_username,investor_deal_status=investor_deal_status)
        #             # dealstatus.save()
        #             return render(request, 'profile.html', {'user': user, 'Ideas': Ideas,'Ideaviewed':Ideaviewed,'profile':profile,'Idea_bought':Ideabought})
        #         elif role == 'idea_provider':
        #             idea_provider_username = request.POST.get('idea_provider_username')
        #             idea_provider_deal_status = request.POST.get('idea_provider_deal_status')
        #             dealstatus = list(deal_Status)
        #             for obj in dealstatus:
        #                 obj.idea_id = idea_id
        #                 obj.idea_provider_username = idea_provider_username
        #                 obj.idea_provider_deal_status = idea_provider_deal_status
        #                 obj.save()
        #             # dealStatus= dealstatus(idea_provider_username=idea_provider_username,idea_provider_deal_status=idea_provider_deal_status)
        #             # dealStatus.save()
        #             return render(request, 'profile.html', {'user': user, 'Ideas': Ideas,'Ideaviewed':Ideaviewed,'profile':profile,'Idea_bought':Ideabought})
        # # except deal_status.DoesNotExist:
        # #   dealstatus = deal_status.objects.create({'idea_id' : idea_id})
        #    if role == 'investor':
        #         investor_username = request.POST.get('investor_username')
        #         investor_deal_status = request.POST.get('investor_deal_status')
        #         dealStatus= dealstatus(investor_username=investor_username,investor_deal_status=investor_deal_status)
        #         dealStatus.save()
        #         return render(request, 'profile.html', {'user': user, 'Ideas': Ideas,'Ideaviewed':Ideaviewed,'profile':profile,'Idea_bought':Ideabought})
        #    elif role == 'idea_provider':
        #         idea_provider_username = request.POST.get('idea_provider_username')
        #         idea_provider_deal_status = request.POST.get('idea_provider_deal_status')
        #         dealStatus= dealstatus(idea_provider_username=idea_provider_username,idea_provider_deal_status=idea_provider_deal_status)
        #         dealStatus.save()
        #         return render(request, 'profile.html', {'user': user, 'Ideas': Ideas,'Ideaviewed':Ideaviewed,'profile':profile,'Idea_bought':Ideabought})

        # return render(request, 'profile.html', {'user': user, 'Ideas': Ideas,'Ideaviewed':Ideaviewed,'Idea_bought':Ideabought})

# @login_required(login_url='Userlogin')
# def invest_idea(request , Idea_id):
#     referrer = request.META.get('HTTP_REFERER', '')
#     token = Token.objects.get(user=request.user)
#     # client = razorpay.Client(auth=('rzp_test_ClH6E4FgEWpPoz','UbdU2Jdi241y6fNAZKA7Bi1Q'))
#     if "/invest" in referrer:
#         if token.balance >= 50:
#             token.balance-=50
#             token.save()
#             Ideas = Idea.objects.get(id= Idea_id)
#             Ideaviewed = Idea_viewed(user=request.user, Idea=Ideas)
#             Ideaviewed.save()
#             # amount = Ideas.idea_instant_investment
#             # if request.method == 'POST':   
#             #     razorpay_payment_id = request.POST.get('razorpay_payment_id')
#             #     print(razorpay_payment_id)
#             #     payment = client.payment.fetch(razorpay_payment_id)
#             #     payment_amount = int(payment['amount'])
#             #     print(payment_amount)
#             #     order = client.order.create({'amount': payment_amount, 'currency':'INR', 'payment_capture': '1'})
#             #     razorpay_order_id = request.POST.get('razorpay_order_id')
#             #     print(razorpay_order_id)
#             #     if payment_amount == amount:
#             # else:
#             return render(request, 'invest_idea.html', {'Ideas':Ideas,'Idea_id':Idea_id})
#         else:
#             messages.success(request,'Insufficient Tokens')
#             return redirect(deposit)
    
#     else:
#         return redirect(invest)

@login_required(login_url='Userlogin')
def invest_idea(request , Idea_id):
    referrer = request.META.get('HTTP_REFERER')
    token = Token.objects.get(user=request.user)
    Ideas = Idea.objects.get(id= Idea_id)
    ideaViewed = Idea_viewed.objects.filter(user = request.user, Idea = Ideas)

    if not ideaViewed.exists():
        if token.balance >= 50:
            token.balance-=50
            token.save()
            # Ideas = Idea.objects.get(id= Idea_id)
            Ideaviewed = Idea_viewed(user=request.user, Idea=Ideas)
            Ideaviewed.save()
            # if request.method == 'POST':
            #     Agent_call_requests = Agent_call_request(user = request.user, Idea = Ideas )
            #     Agent_call_requests.save()
            #     messages.success(request,'Your request has been reached to our team. We will cotact you shortly.')
            #     return redirect(home)
            return render(request, 'invest_idea.html', {'Ideas':Ideas,'Idea_id':Idea_id})
        else:
            messages.success(request,'Insufficient Tokens')
            return redirect(deposit)
    elif  ideaViewed.exists() :
         return render(request, 'invest_idea.html', {'Ideas':Ideas,'Idea_id':Idea_id})
        
    
def agent_call_request(request, Idea_id):
    Ideas = Idea.objects.get(id= Idea_id)
    try:
        Agent_call_requests = Agent_call_request(user = request.user, Idea = Ideas )
        Agent_call_requests.save()
        messages.success(request,'Your request has reached us. Our team will contact you shortly. Please continue your journey with us.')
        return redirect(home)
    except Exception as e :
        messages.success(request,'You have already booked a call. Our team will reach you soon.')
        return redirect(home)
    
@login_required(login_url='Userlogin')
def ideas(request):
    token = Token.objects.get(user=request.user)
    user = request.user
    profile=UserProfile.objects.get(user=user)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        industry = request.POST.get('industry')
        instant_investment = request.POST.get('instant investment')
        total_investment = request.POST.get('total investment')
        name = user.first_name +' '+ user.last_name
        mail = request.user.email
        mobile = profile.mobile
        address = profile.address
        Ideas = Idea(idea_title= title, idea_description=description, idea_industry= industry, idea_instant_investment= instant_investment, idea_total_investment= total_investment,idea_posted_by_name=name,idea_posted_by_mail=mail,uploaded_by=request.user,idea_posted_by_mobile=mobile,idea_posted_by_address=address)
        Ideas.save()
        messages.success(request,'Your Idea is now in the database and awaiting approval of the host before it is open to investors.')
        return redirect(home)
    return render(request,'ideas.html',{'token':token})

def Userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:  
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'Incorrect Username or Password')
            return render(request, 'login.html')
    return render(request, 'login.html')


    
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        profession = request.POST.get('profession')
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            user_1 = User.objects.get(username = username)
            try:
                user = authenticate(request, username=username, password=password)
                login(request, user)
                token = Token(user = request.user)
                token.save()
                profile = UserProfile(user=request.user,mobile=mobile,profession=profession,address=address)
                profile.save()
                return redirect('home')
            except Exception as e:
                login(request,user_1)
                token = Token(user = user_1)
                token.save()
                profile = UserProfile(user=user_1,mobile=mobile,profession=profession,address=address)
                profile.save()
                return redirect('home')
        elif not form.is_valid():
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}')                
    else:
        form = UserForm()

    return render(request, 'register.html', {'form': form}) 


# @login_required(login_url='Userlogin')
# def deposit(request):
#     token = Token.objects.get(user = request.user)
#     print('1')
#     client = razorpay.Client(auth=('rzp_test_ClH6E4FgEWpPoz','UbdU2Jdi241y6fNAZKA7Bi1Q'))  
#     print('2')
#     if request.method == 'POST':
#         razorpay_payment_id = request.POST.get('razorpay_payment_id')
#         print(razorpay_payment_id)
#         payment = client.payment.fetch(razorpay_payment_id)
#         payment_amount = int(payment['amount'])
#         print(payment_amount)
#         order = client.order.create({'amount': payment_amount, 'currency':'INR', 'payment_capture': '1'})
#         razorpay_order_id = request.POST.get('razorpay_order_id')
#         print(razorpay_order_id)
#         if payment_amount== 10000:
#              token.balance += 120
#              token.save()
#              messages.success(request,'Your wallet has been credited with 120 tokens successfully.') 
#              return redirect(home)
#         elif payment_amount== 20000:
#             token.balance += 250
#             token.save()
#             messages.success(request,'Your wallet has been credited with 250 tokens successfully.')
#             return redirect(home)
#         elif payment_amount== 30000:
#             token.balance += 380
#             token.save()
#             messages.success(request,'Your wallet has been credited with 380 tokens successfully.')
#             return redirect(home)
#     return render(request,'deposit.html',{'token':token})

@login_required(login_url='Userlogin')
def deposit(request):
    token = Token.objects.get(user = request.user)
    if request.method == 'POST':
        Extra_token_requests = Extra_token_request(user = request.user)
        Extra_token_requests.save()
        messages.success(request,'Your request has been reached to our team. We will cotact you shortly.')
        return render(request,'deposit.html',{'token':token})
    return render(request,'deposit.html',{'token':token})