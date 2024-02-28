from collections import ChainMap
from fileinput import FileInput
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.template import loader
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required 
import datetime
import uuid, re 
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str 
from django.conf import settings 
from PharmaPill import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User 

from AuthenticApp.models import db_Profile
from StorePharma.models import db_Medicine, medicine_Image, med_Cart_list, about_Pharma
from StorePharma.models import med_Order, OptionList, Pharma_TimeTable, Blogs_Pharma, med_OrderMedicine

# -------------------------------------- ----------------------- home ---------------------- //
 
def home(request):  
    template = loader.get_template('home.html')  
    user_email = request.user.email
    medicine_show = db_Medicine.objects.all()
    image_med = medicine_Image.objects.all()    
    obj_Profile =  db_Profile.objects.filter(char_email = user_email)
    obj_Option = OptionList.objects.filter().all()
    timeSet = Pharma_TimeTable.objects.all()
    obj_about = about_Pharma.objects.all() 
    obj_blog = Blogs_Pharma.objects.all()
    obj_OrderMedicine = med_OrderMedicine.objects.all()

    context = {
        'timeSet': timeSet,
        'obj_Profile': obj_Profile,
        'show_medicine' : medicine_show,
        'med_image' : image_med,
        'obj_Option': obj_Option,
        'obj_about': obj_about,
        'obj_blog': obj_blog, 
        'obj_OrderMedicine': obj_OrderMedicine
    }
    return HttpResponse(template.render(context, request))

# ***********************************   *Medicine*   ***************************************************
def medicine(request):  
    template = loader.get_template('User/Medicine.html')  
    medicine_show = db_Medicine.objects.all()
    image_med = medicine_Image.objects.all()
    obj_Option = OptionList.objects.filter().all()
    obj_about = about_Pharma.objects.all() 
    timeSet = Pharma_TimeTable.objects.all()
    obj_OrderMedicine = med_OrderMedicine.objects.all()

    context = {
        'show_medicine' : medicine_show,
        'med_image' : image_med,
        'obj_Option': obj_Option,
        'obj_about': obj_about,
        'timeSet': timeSet,
        'obj_OrderMedicine': obj_OrderMedicine,
    }
    return HttpResponse(template.render(context, request))

# ***********************************   *Profile*   ***************************************************
def profile(request):  
    template = loader.get_template('Profile.html') 
    user_email = request.user.email 
    user_obj = User.objects.filter(email = user_email).first() 
    Profile_view = db_Profile.objects.filter(char_email = user_email).first()  
    order_Med = med_Order.objects.filter(order_email = user_email) 
    obj_Medicine = db_Medicine.objects.all()
    obj_cart = med_Cart_list.objects.filter(cart_email = user_email) 
    obj_Option = OptionList.objects.filter().all()
    timeSet = Pharma_TimeTable.objects.all()
    obj_about = about_Pharma.objects.all()
    obj_OrderMedicine = med_OrderMedicine.objects.all()

    context = {
        'timeSet': timeSet,
        'Profile_view' : Profile_view,
        'user_obj' : user_obj,
        'order_Med': order_Med, 
        'obj_Medicine': obj_Medicine,
        'obj_cart': obj_cart,
        'obj_Option': obj_Option,
        'obj_about': obj_about,
        'obj_OrderMedicine': obj_OrderMedicine,

    }
    return HttpResponse(template.render(context, request))

# ***********************************   *Update Profile*   ***************************************************
def update_Profile(request):  
    template = loader.get_template('Profile.html') 
    user_email = request.user.email 
    user_obj = User.objects.filter(email = user_email).first() 
    Profile_view = db_Profile.objects.filter(char_email = user_email).first()  
    if request.method == "POST":
        # var_email = request.POST.get('input_email')
        var_fname = request.POST.get('input_fname')
        var_lname = request.POST.get('input_lname')
        var_gender = request.POST.get('input_gender')
        var_address = request.POST.get('input_address')
        var_address_Country = request.POST.get('input_address_Country')
        var_DoB = request.POST.get('input_DoB')
        var_phoneNumber = request.POST.get('input_PhNumber')

        if var_fname == "":
            var_fname = user_obj.first_name
        if var_lname == "":
            var_lname = user_obj.last_name
        if var_gender is None:
            var_gender = Profile_view.db_gender
        if var_address == "":
            var_address = Profile_view.db_address
        if var_address_Country == "":
            var_address_Country = Profile_view.db_address_Country
        if var_phoneNumber == "":
            var_phoneNumber = Profile_view.db_phoneNumber
        if var_DoB == "2024-01-01":
            var_DoB = Profile_view.db_date_DoB

        if len(request.FILES) != 0:
            var_photo = request.FILES['input_image']
        else:
            var_photo = Profile_view.db_photo
    try:
        Profile_view.db_phoneNumber = var_phoneNumber
        Profile_view.db_address = var_address
        Profile_view.db_address_Country = var_address_Country
        Profile_view.db_date_DoB = var_DoB
        Profile_view.db_gender = var_gender
        Profile_view.db_photo = var_photo
        Profile_view.save()

        user_obj.first_name = var_fname
        user_obj.last_name = var_lname 
        user_obj.save()
        messages.success(request, 'Your Profile are Successfully Added!')
        return redirect('profile')
    except Exception as e:
        print(e)
    context = {
        'Profile_view' : Profile_view,
        'user_obj' : user_obj,

    }
    return HttpResponse(template.render(context, request))


# ***********************************   *Admin Control*   ***************************************************
def admin_control(request):  
    template = loader.get_template('Admin/admin_Control.html')   
    medicine_show = db_Medicine.objects.all()
    image_med = medicine_Image.objects.all()
    order_Med = med_Order.objects.filter() 
    obj_Medicine = db_Medicine.objects.all()
    obj_cart = med_Cart_list.objects.filter()
    obj_Option = OptionList.objects.filter().all()
    obj_Order = med_Order.objects.filter().all()
    obj_profile = db_Profile.objects.filter().all()
    obj_User = User.objects.all() 
    timeSet = Pharma_TimeTable.objects.all() 
    obj_about = about_Pharma.objects.all()
    obj_OrderMedicine = med_OrderMedicine.objects.all()

    context = {
        'timeSet': timeSet,
        'show_medicine' : medicine_show,
        'med_image' : image_med,
        'obj_Option': obj_Option,
        'obj_Order': obj_Order,
        'obj_profile': obj_profile,
        'obj_User': obj_User,
        'order_Med': order_Med,
        'obj_Medicine': obj_Medicine,
        'obj_cart': obj_cart,
        'obj_about': obj_about,
        'obj_OrderMedicine': obj_OrderMedicine,
    }
    return HttpResponse(template.render(context, request))


# ***********************************   *Medicine Order*   ***************************************************
def medicine_order(request):  
    template = loader.get_template('Admin/medicine_order.html')   
    medicine_show = db_Medicine.objects.all()
    image_med = medicine_Image.objects.all() 
    order_Med = med_Order.objects.filter() 
    obj_Medicine = db_Medicine.objects.all()
    obj_cart = med_Cart_list.objects.filter()
    obj_Option = OptionList.objects.filter().all()
    obj_Order = med_Order.objects.filter().all()
    obj_profile = db_Profile.objects.filter().all()
    obj_User = User.objects.all() 
    timeSet = Pharma_TimeTable.objects.all()
    obj_about = about_Pharma.objects.all()
    obj_OrderMedicine = med_OrderMedicine.objects.all()
    context = {
        'timeSet': timeSet,
        'show_medicine' : medicine_show,
        'med_image' : image_med,
        'obj_Option': obj_Option,
        'obj_Order': obj_Order,
        'obj_profile': obj_profile,
        'obj_User': obj_User,
        'order_Med': order_Med,
        'obj_Medicine': obj_Medicine,
        'obj_cart': obj_cart,
        'obj_about': obj_about,
        'obj_OrderMedicine': obj_OrderMedicine,
    }
    return HttpResponse(template.render(context, request))


# ***********************************   *Admin DataTable*   ***************************************************
def admin_dataTable(request):  
    template = loader.get_template('Admin/admin_DataTable.html')   
    medicine_show = db_Medicine.objects.all()
    image_med = medicine_Image.objects.all()
    obj_Option = OptionList.objects.filter().all()  
    timeSet = Pharma_TimeTable.objects.all()
    obj_about = about_Pharma.objects.all()
    obj_OrderMedicine = med_OrderMedicine.objects.all()
    context = {
        'timeSet': timeSet,
        'show_medicine' : medicine_show,
        'med_image' : image_med,
        'obj_Option': obj_Option, 
        'obj_about': obj_about,
        'obj_OrderMedicine': obj_OrderMedicine,
    }
    return HttpResponse(template.render(context, request))

# ***********************************   *add Medicine*   ***************************************************
def add_Medicine(request):  
    template = loader.get_template('Admin/admin_Control.html')
    auth_token = str(uuid.uuid4())
    if request.method == 'POST':  
        Medicine_ID = auth_token 
        var_Med_LabelName = request.POST.get('medName') 
        var_Med_CompanyName = request.POST.get('companyName') 
        var_Med_FormulaName = request.POST.get('formulaName') 
        var_Med_Purchase_Price = request.POST.get('medPurchasePrice') 
        var_Med_Sell_Price = request.POST.get('medSellPrice') 
        var_Med_Type = request.POST.get('medType') 
        var_Med_UsedFor  = request.POST.get('medUsedFor') 
        var_Med_Describtion = request.POST.get('medDecribe') 
        var_Med_ProductionDate  = request.POST.get('productionDate') 
        var_Med_ExpireDate  = request.POST.get('exp-Date')

        var_Med_Size  = request.POST.get('medSize')
        var_Med_Quantity  = request.POST.get('medQuantity')
        var_Med_Remain_Quantity  = var_Med_Quantity

        if len(request.FILES) != 0:
            var_img_display = request.FILES['UploadImg']
        
        if var_Med_LabelName == "" or var_Med_CompanyName  is None or var_img_display == "" or var_Med_FormulaName == "" or var_Med_ExpireDate == "" or var_Med_Type  is None or var_Med_Purchase_Price == ""  or var_Med_Size == "" or var_Med_Quantity == ""  :
            messages.error(request,"Medicine all field are required to filled*")
            return redirect('admin_control')
        if var_Med_UsedFor == "" or var_Med_Describtion == "":
            var_Med_UsedFor = "N/A"
            var_Med_Describtion = "N/A"
        if int(var_Med_Quantity) == 0:
            var_Status = "Not NAvailable"
        if int(var_Med_Quantity) >= 11:
            var_Status = "Available" 
        if int(var_Med_Quantity) >= 1 and int(var_Med_Quantity) <= 10:
            var_Status = "Limited Medicine"
    try:
        obj_Medicine = db_Medicine.objects.create(Medicine_ID = Medicine_ID , Med_LabelName = var_Med_LabelName, 
                Med_CompanyName = var_Med_CompanyName, Med_FormulaName = var_Med_FormulaName,
                Med_Purchase_Price = var_Med_Purchase_Price, Med_Sell_Price = var_Med_Sell_Price, Med_Type = var_Med_Type,
                Med_UsedFor  = var_Med_UsedFor, Med_Describtion = var_Med_Describtion, Med_ProductionDate  = var_Med_ProductionDate,
                Med_photo = var_img_display, Med_ExpireDate  = var_Med_ExpireDate , 
                Med_Status = var_Status, Med_Size = var_Med_Size , # ml, mg ,mm , cc
                Med_Quantity = var_Med_Quantity, Med_Remain_Quantity = var_Med_Remain_Quantity
                )
        obj_Medicine.save()
        messages.success(request, 'Your Medicine are Successfully Added!')
        return redirect('admin_control')
    except Exception as e:
            print(e)

    context = {}
    return HttpResponse(template.render(context, request))

# ***********************************   *Update Control*   ***************************************************
def update_Medicine(request): 
    if request.method == 'POST': 
        get_id =  request.POST.get('id_get')  
        var_Med_LabelName = request.POST.get('medName') 
        var_Med_CompanyName = request.POST.get('companyName') 
        var_Med_FormulaName = request.POST.get('formulaName')
        var_Med_Purchase_Price = request.POST.get('medPurchasePrice') 
        var_Med_Sell_Price = request.POST.get('medSellPrice') 
        var_Med_Type = request.POST.get('medType') 
        var_Med_UsedFor  = request.POST.get('medUsedFor') 
        var_Med_Describtion = request.POST.get('medDecribe') 
        var_Med_ProductionDate  = request.POST.get('productionDate') 
        var_Med_ExpireDate  = request.POST.get('exp-Date')
        var_img_Check  = request.POST.get('UploadImg') 
        var_Med_Size  = request.POST.get('medSize')
        var_Med_Quantity  = request.POST.get('medQuantity')
        var_Med_Remain_Quantity  = var_Med_Quantity

        
        medicine_update = db_Medicine.objects.get(Medicine_ID = get_id) 
 
        if len(request.FILES) != 0:
            var_img_display = request.FILES['UploadImg'] 
        if var_Med_Quantity == "":
            var_Med_Quantity = medicine_update.Med_Quantity 
            var_Med_Remain_Quantity = medicine_update.Med_Remain_Quantity
        if var_Med_Quantity != "":
            var_Med_Quantity = medicine_update.Med_Quantity + var_Med_Quantity
            var_Med_Remain_Quantity = medicine_update.Med_Remain_Quantity + var_Med_Remain_Quantity
        if var_img_Check == "":
            var_img_display = medicine_update.Med_photo 
        if var_Med_LabelName == "":
            var_Med_LabelName = medicine_update.Med_LabelName
        if var_img_display == "":
            var_img_display = medicine_update.Med_photo
        if var_Med_CompanyName is None:
            var_Med_CompanyName = medicine_update.Med_CompanyName
        if var_Med_FormulaName == "":
            var_Med_FormulaName = medicine_update.Med_FormulaName
        if var_Med_Purchase_Price == "":
            var_Med_Purchase_Price = medicine_update.Med_Purchase_Price
        if var_Med_Sell_Price == "":
            var_Med_Sell_Price = medicine_update.Med_Sell_Price
        if var_Med_Type is None:
            var_Med_Type = medicine_update.Med_Type
        if var_Med_UsedFor == "":
             var_Med_UsedFor = medicine_update.Med_UsedFor
        if var_Med_Describtion == "":
            var_Med_Describtion = medicine_update.Med_Describtion
        if var_Med_ProductionDate == "2024-01-01":
            var_Med_ProductionDate = medicine_update.Med_ProductionDate
        if var_Med_ExpireDate == "2024-01-01":
            var_Med_ExpireDate = medicine_update.Med_ExpireDate
        if var_Med_Size == "":
            var_Med_Size = medicine_update.Med_Size
            
        else:
            try: 
                if int(var_Med_Quantity) == 0:
                    var_Status = "Not NAvailable"
                if int(var_Med_Quantity) >= 11:
                    var_Status = "Available" 
                if int(var_Med_Quantity) >= 1 or int(var_Med_Quantity) <= 10:
                    var_Status = "Limited Medicine"
                medicine_update.Med_LabelName = var_Med_LabelName
                medicine_update.Med_CompanyName = var_Med_CompanyName
                medicine_update.Med_FormulaName = var_Med_FormulaName 
                medicine_update.Med_Purchase_Price = var_Med_Purchase_Price 
                medicine_update.Med_Sell_Price = var_Med_Sell_Price
                medicine_update.Med_Type = var_Med_Type
                medicine_update.Med_UsedFor  = var_Med_UsedFor
                medicine_update.Med_Describtion = var_Med_Describtion
                medicine_update.Med_ProductionDate   = var_Med_ProductionDate
                medicine_update.Med_ExpireDate   = var_Med_ExpireDate 
                medicine_update.Med_photo = var_img_display
                
                medicine_update.Med_Status = var_Status
                medicine_update.Med_Size = var_Med_Size # ml, mg ,mm , cc
                medicine_update.Med_Quantity = var_Med_Quantity 
                medicine_update.Med_Remain_Quantity = var_Med_Remain_Quantity  
                medicine_update.save()
                messages.success(request, 'Your Medicine is Successfully Updated ! \" ' + get_id + ' \"')
            except Exception as e:
                print(e)
    context = { } 
    return redirect('admin_control')


# ***********************************   *Add Image Control*   ***************************************************
def AddImg_Medicine(request): 
    if request.method == 'POST': 
        Img_id =  request.POST.get('id_Img') 

        check_img = medicine_Image.objects.filter(Med_ID_Img = Img_id).first()
        Img_1 =  request.POST.get('UploadImg1')
        Img_2 =  request.POST.get('UploadImg2')
        Img_3 =  request.POST.get('UploadImg3')
        Img_4 =  request.POST.get('UploadImg4')


        if len(request.FILES) != 0:
            if Img_1 is None :
                var_Img_list1 = request.FILES['UploadImg1'] 
            else:  
                if medicine_Image.objects.filter(Med_ID_Img = Img_id).exists() == True :
                    var_Img_list1 = check_img.list1_img
                else:
                    var_Img_list1 = "Medicine/ImgIcon.jfif"
            if Img_2 is None :
                var_Img_list2 = request.FILES['UploadImg2']
            else:
                if medicine_Image.objects.filter(Med_ID_Img = Img_id).exists() == True :
                    var_Img_list2 = check_img.list2_img
                else:
                    var_Img_list2 = "Medicine/ImgIcon.jfif"
            if Img_3 is None :
                var_Img_list3 = request.FILES['UploadImg3']
            else:
                if medicine_Image.objects.filter(Med_ID_Img = Img_id).exists() == True :
                    var_Img_list3 = check_img.list3_img
                else:
                    var_Img_list3 = "Medicine/ImgIcon.jfif" 
            if Img_4 is None :
                var_Img_list4 = request.FILES['UploadImg4']
            else:
                if medicine_Image.objects.filter(Med_ID_Img = Img_id).exists() == True :
                    var_Img_list4 = check_img.list4_img
                else:
                    var_Img_list4 = "Medicine/ImgIcon.jfif"  
        
        if medicine_Image.objects.filter(Med_ID_Img = Img_id).exists() == True :
            Img_obj = medicine_Image.objects.get(Med_ID_Img = Img_id) 
            try: 
                Img_obj.list1_img = var_Img_list1
                Img_obj.list2_img = var_Img_list2
                Img_obj.list3_img = var_Img_list3
                Img_obj.list4_img = var_Img_list4
                Img_obj.save()
                messages.success(request, 'Your Medicine Image is Successfully Updated ! \" ' + Img_id + ' \"')
            except Exception as e:
                print(e)
        else:
            Img_obj = medicine_Image.objects.create(Med_ID_Img =  Img_id,
                list1_img = var_Img_list1,
                list2_img = var_Img_list2,
                list3_img = var_Img_list3,
                list4_img = var_Img_list4
            )
            Img_obj.save()
            messages.success(request, 'Your Medicine Image is Successfully Added ! \" ' + Img_id + ' \"')
            
    context = { } 
    return redirect('admin_control')

# ***********************************   *delete Control*   ***************************************************
def delete_Medicine(request, id):    
    medicine_del = db_Medicine.objects.filter(Medicine_ID = id)
    medicine_del.delete()
    messages.success(request, 'Your Medicine is Successfully Deleted ! \" ' + id + ' \"')
    return redirect('admin_control')

# ***********************************   *MENU*   ***************************************************
def loaderPage(request):  
    template = loader.get_template('Menu/loaderPage.html')  
    context = {  }
    return HttpResponse(template.render(context, request))

def header(request):  
    template = loader.get_template('Menu/header.html') 
    timeSet = Pharma_TimeTable.objects.all()
    context = { 
        'timeSet': timeSet,
    }
    return HttpResponse(template.render(context, request))

def footer(request):  
    template = loader.get_template('Menu/footer.html')
    timeSet = Pharma_TimeTable.objects.all()   
    obj_about = about_Pharma.objects.all()    
    context = {  
        'timeSet': timeSet,
        'obj_about': obj_about,
    }
    return HttpResponse(template.render(context, request))


# ***********************************   *Search*   ***************************************************
# @login_required
def search(request):
    template = loader.get_template('Search.html')    
    search = request.GET['search']   
    obj_Option = OptionList.objects.filter().all()
    mySearch = (db_Medicine.objects.filter(Med_LabelName__contains = search ) | db_Medicine.objects.filter(Med_FormulaName__contains = search).values() | db_Medicine.objects.filter(Med_UsedFor__contains = search  ).values() | db_Medicine.objects.filter(Med_Describtion__contains = search).values() | db_Medicine.objects.filter(Med_ProductionDate__contains = search  ).values() | db_Medicine.objects.filter(Med_ExpireDate__contains = search).values())
    timeSet = Pharma_TimeTable.objects.all()
    obj_about = about_Pharma.objects.all()
    context = {
        'timeSet': timeSet,
        'mySearch': mySearch,    
        'obj_Option': obj_Option,  
        'obj_about': obj_about,
        } 
    return HttpResponse(template.render(context, request))


# ***********************************   *Cart List*   ***************************************************

# @login_required
def cart_list(request):
    template = loader.get_template('User/cart.html')  
    user_email = request.user.email
    mycart = med_Cart_list.objects.filter(cart_email = user_email)
    medicine_show = db_Medicine.objects.all() 
    obj_Option = OptionList.objects.filter().all() 
    timeSet = Pharma_TimeTable.objects.all()
    obj_about = about_Pharma.objects.all()
    auth_token = str(uuid.uuid4())
    if request.method == "POST":
        var_cart_ID = request.POST.get('input_cart_ID') 
        var_Med_Quantity  = request.POST.get('medQuantity') 

        med_check = db_Medicine.objects.filter(Medicine_ID = var_cart_ID).first()
        remain_Quantity = int(med_check.Med_Remain_Quantity) 
         
        if remain_Quantity < int(var_Med_Quantity):
            messages.success(request, 'Your Value must be less then given field "Quantity" ') 
            return redirect('cart_list') 
        if remain_Quantity == 0:
            messages.success(request, 'Your Value must be less then greater then 0 ') 
            return redirect('cart_list') 
        else:
            try:
                add_cart = med_Cart_list.objects.create(Pk_Cart_ID = auth_token, cart_email = user_email, med_Cart_ID = var_cart_ID, 
                    Med_Cart_Quantity = var_Med_Quantity, )
                add_cart.save()
                messages.success(request, 'Your item added in Cart')
                return redirect('cart_list')
            except Exception as e:
                print(e) 
        return redirect('cart_list')
    context = {
            'timeSet':timeSet,
            'mycart' : mycart,
            'show_medicine' : medicine_show, 
            'obj_Option': obj_Option,
            'obj_about': obj_about,
        } 
    return HttpResponse(template.render(context, request))


# ***********************************   *Billing Order Report*   ***************************************************
def bill_report(request):
    user_email = request.user.email
    auth_token = str(uuid.uuid4())
    if request.method == "POST":
        bill_ID = auth_token
        med_list = request.POST.getlist('Med_list') 
        # var_med_ID = request.POST.getlist('Med_ID') 
 
        for med_id in med_list:
            med_Cart = med_Cart_list.objects.filter(cart_email = user_email, Pk_Cart_ID = med_id).first()
            med_id_carted = med_Cart.med_Cart_ID 
            obj_Medicine = db_Medicine.objects.filter(Medicine_ID = med_id_carted).first()
            price = int(obj_Medicine.Med_Sell_Price)  
            Quantity = int(med_Cart.Med_Cart_Quantity) 
            Remain_Quantity = obj_Medicine.Med_Remain_Quantity

            if Quantity == 0:
                Total_item = 0 
            if Remain_Quantity == 0:
                var_Med_Status = "Not Available"
            if Remain_Quantity >= 1 and Remain_Quantity <= 10:
                var_Med_Status = "Limited Medicine" 
            if Remain_Quantity >= 11:
                var_Med_Status = "Available" 
            if User.objects.filter(is_staff = True).first():
                var_status_Cart = "Passed" 
            if User.objects.filter(is_staff = False).first():
                var_status_Cart = "Pendding"
            if Quantity > obj_Medicine.Med_Remain_Quantity:
                messages.success(request,  'Please Make Sure your Quantity less then from available Medicine! "' + obj_Medicine.Med_CompanyName + '"')
                return redirect('cart_list')
            else:
                Total_item = Quantity * price  
            Pk_ID = str(uuid.uuid4())
            try:
                if med_Order.objects.filter(order_email = user_email, Pk_order_ID = bill_ID).exists() == True:
                    obj_Order = med_Order(order_email = user_email)
                    posted_order = med_Order.objects.filter(order_email = user_email, Pk_order_ID = bill_ID).first()
                    order_get_id = get_object_or_404(db_Medicine, Medicine_ID = med_id_carted)
                    obj_Order.Pk_order_ID = posted_order.Pk_order_ID
                    obj_Order.order_email = user_email 
                    obj_Medicine.Med_Remain_Quantity = int(obj_Medicine.Med_Remain_Quantity) - Quantity
                    obj_Medicine.Med_Status =var_Med_Status
                    obj_Order.Med_Price = Total_item + posted_order.Med_Price
                    obj_Medicine.save()
                    obj_Order.status_Cart =  var_status_Cart
                    obj_Order.save() 
                    obj_Order.med_order_ID.add(order_get_id)
                    obj_OrderMedicine = med_OrderMedicine.objects.create(Pk_OrderMedicine_ID = Pk_ID,
                                                med_OrderMedicine_email = user_email, order_OrderMedicine_ID = bill_ID, 
                                                med_OrderMedicine_ID = med_id_carted, Pk_Cart_List_ID = med_id)
                    obj_OrderMedicine.save()
                else:
                    obj_Order = med_Order(order_email = user_email)
                    order_get_id = get_object_or_404(db_Medicine, Medicine_ID = med_id_carted)
                    obj_Order.Pk_order_ID = bill_ID
                    obj_Order.order_email = user_email
                    obj_Order.Med_Price = Total_item  
                    obj_Medicine.Med_Remain_Quantity = int(obj_Medicine.Med_Remain_Quantity) - Quantity
                    obj_Medicine.Med_Status =var_Med_Status
                    obj_Medicine.save()
                    obj_Order.status_Cart =  var_status_Cart
                    obj_Order.save() 
                    obj_Order.med_order_ID.add(order_get_id)
                    obj_OrderMedicine = med_OrderMedicine.objects.create(Pk_OrderMedicine_ID = Pk_ID,
                                                med_OrderMedicine_email = user_email, order_OrderMedicine_ID = bill_ID, 
                                                med_OrderMedicine_ID = med_id_carted, Pk_Cart_List_ID = med_id)
                    obj_OrderMedicine.save() 
                    messages.success(request,  'Your Billing Detail are Successfully Passed \n Now you will get Your Medicine on few working days!')
                    messages.success(request,  'Please Check Your Profile for Billing Detail!') 
            
            except Exception as e:
                print(e) 
    return redirect('cart_list')

def Fun_OrderMedicine(bill_ID, med_id_carted):
    Pk_ID = str(uuid.uuid4())
    obj_OrderMedicine = med_OrderMedicine.objects.create(Pk_OrderMedicine_ID = Pk_ID,
                            Pk_order_ID = bill_ID, med_order_ID = med_id_carted)
    obj_OrderMedicine.save()

# ***********************************   *OptionAdded*   ***************************************************
def optionAdd(request):
    user_email = request.user.email
    template = loader.get_template('Admin/add_List.html')   
    if request.method == "POST": 
        auth_token = str(uuid.uuid4())
        var_Company_list = request.POST.get('companyName') 
        var_Type_list = request.POST.get('medType') 
        if var_Company_list == "":
            var_Company_list = "N/A"
        if var_Type_list == "":
            var_Type_list = "N/A"
        if var_Company_list == "" and var_Type_list == "":
            messages.success(request,  'Company or Type Fieled Must be Filled!')
            return redirect('admin_control')
        if OptionList.objects.filter(company_List = var_Company_list).first():
            messages.error(request, 'Company Name is already Taken.')
            return redirect('admin_control')
        if OptionList.objects.filter(type_List = var_Type_list).first():
            messages.error(request, 'Type of Medicine is already Taken.')
            return redirect('admin_control')

        list_obj = OptionList.objects.create(Option_ID = auth_token, company_List = var_Company_list, type_List = var_Type_list)
        list_obj.save()
        messages.success(request,  'Company or Type Fieled are Successfully Added!')
        return redirect('admin_control')
    context = {}
    return HttpResponse(template.render(context, request))

# ***********************************   *Company Option Update*   ***************************************************
def update_list_company(request):
    template = loader.get_template('Admin/update_list_company.html') 
    if request.method == "POST":
        var_company_ID = request.POST.get("company_ID")
        var_comapny_Text =  request.POST.get("companyName")

        if OptionList.objects.filter(company_List = var_comapny_Text).first():
                messages.error(request, 'Company Name Already Exist. Try Again!!!')
                return redirect('admin_control') 
        if var_comapny_Text == "":
            messages.success(request,  'Company Name Must be Filled. Try Again!!!')
            return redirect('admin_control')
        
        try: 
            obj_Option = OptionList.objects.filter(Option_ID = var_company_ID).first()
            obj_Option.company_List = var_comapny_Text
            obj_Option.save()
            messages.success(request,  'Company Name Fieled is Successfully Added!')
            return redirect('admin_control')
        except Exception as e:
            print(e)
    context = {}
    return HttpResponse(template.render(context, request))


# ***********************************   *Type Option Update*   ***************************************************
def update_list_type(request):
    template = loader.get_template('Admin/update_list_type.html') 
    if request.method == "POST":
        var_type_ID = request.POST.get("type_ID")
        var_type_Text =  request.POST.get("medType")
        
        if OptionList.objects.filter(company_List = var_type_Text).first():
                messages.error(request, 'Type of Medicine Already Exist. Try Again!!!')
                return redirect('admin_control') 
        if var_type_Text == "":
            messages.success(request,  'type Name Must be Filled. Try Again!!!')
            return redirect('admin_control')
        
        try: 
            obj_Option = OptionList.objects.filter(Option_ID = var_type_ID).first()
            obj_Option.type_List = var_type_Text
            obj_Option.save()
            messages.success(request,  'Medicine Type Name Fieled is Successfully Added!')
            return redirect('admin_control')
        except Exception as e:
            print(e)
    context = {}
    return HttpResponse(template.render(context, request))

# ***********************************   *Setting*   ***************************************************
def setting(request):  
    template = loader.get_template('setting.html') 
    medicine_show = db_Medicine.objects.all()
    timeSet = Pharma_TimeTable.objects.all() 
    obj_about = about_Pharma.objects.all() 
    obj_blog = Blogs_Pharma.objects.all()
    context = {
        'timeSet': timeSet,
        'obj_about': obj_about,
        'obj_blog': obj_blog,
        'medicine_show': medicine_show,
    }
    return HttpResponse(template.render(context, request))

# ***********************************   *Add Bolgs Pharma*   ***************************************************
def blog_pharma(request): 
    auth_token = str(uuid.uuid4())  
    if request.method == "POST": 
        var_Pk_blog_ID = request.POST.get("blog_ID")
        var_blog_Title = request.POST.get("blog_title")
        var_blog_Describe =  request.POST.get("blog_describe") 
        var_blog_Medicine_Name = request.POST.get("blog_Medicine_Name") 
        update_blog = Blogs_Pharma.objects.filter(Pk_blog_ID = var_Pk_blog_ID).first() 

        if var_blog_Title == "":
            messages.error(request, 'Title Field must be required. Try Again!!!')
            return redirect('setting') 
        if var_blog_Describe == "":
            messages.error(request, 'Descriptional Field must be required. Try Again!!!')
            return redirect('setting') 
        if var_blog_Medicine_Name is None:
            messages.error(request, 'Medicine Name Field must be required. Try Again!!!')
            return redirect('setting') 
        if len(request.FILES) != 0:
            blog_img = request.FILES['blog_Image'] 
        else:
            blog_img = update_blog.blog_img

        if Blogs_Pharma.objects.filter(Pk_blog_ID = var_Pk_blog_ID).exists() == True:
            update_blog.blog_Title = var_blog_Title
            update_blog.blog_Describe =  var_blog_Describe
            update_blog.blog_Medicine_Name = var_blog_Medicine_Name
            update_blog.blog_img = blog_img

            update_blog.save()
            return redirect('setting')
        else:
            try:
                add_blog = Blogs_Pharma.objects.create(Pk_blog_ID = auth_token,
                    blog_Title = var_blog_Title, blog_Describe =  var_blog_Describe,
                    blog_Medicine_Name = var_blog_Medicine_Name, blog_img = blog_img
                )
                add_blog.save()
                return redirect('setting')
            except Exception as e:
                print(e)
    return redirect('setting')

# ***********************************   *Blog Delete*   ***************************************************
def delete_blog(request):
    if request.method == "POST":
        ids = request.POST.get('blog_delete_ID')
        if ids is None: 
            messages.success(request, 'Blog Pharma ID must be Choose !')
            return redirect('setting')
        else:
            blog_del = Blogs_Pharma.objects.filter(Pk_blog_ID = ids).first()
            blog_del.delete()
            messages.success(request, 'Blog Pharma is Successfully Deleted ! \" ' + ids + ' \"')
            return redirect('setting')
    return redirect('setting')

# ***********************************   *Add About Pharma*   ***************************************************
def about_pharma(request): 
    auth_token = str(uuid.uuid4())  
    if request.method == "POST": 
        var_Pk_about_ID = request.POST.get("about_ID")
        var_about_Title = request.POST.get("about_title")
        var_about_Describe =  request.POST.get("about_describe")  
        var_about_admin_email = request.POST.get("about_admin_email")
        var_about_address = request.POST.get("about_address")
        var_about_contact = request.POST.get("about_contact")
        update_about = about_Pharma.objects.filter(Pk_about_ID = var_Pk_about_ID).first() 

        if var_about_Title == "":
            messages.error(request, 'Title Field must be required. Try Again!!!')
            return redirect('setting') 
        if var_about_admin_email == "":
            messages.error(request, 'Admin Email Field must be required. Try Again!!!')
            return redirect('setting') 
        if var_about_address == "":
            messages.error(request, 'about Contact Field must be required. Try Again!!!')
            return redirect('setting') 
        if var_about_contact == "":
            messages.error(request, 'Contact Field must be required. Try Again!!!')
            return redirect('setting') 
        if var_about_Describe == "":
            messages.error(request, 'Describtional Field must be required. Try Again!!!')
            return redirect('setting') 
        if len(request.FILES) != 0:
            about_img = request.FILES['about_Image'] 
        else:
            about_img = update_about.about_img

        if about_Pharma.objects.filter(Pk_about_ID = var_Pk_about_ID).exists() == True:
            update_about.about_Title = var_about_Title
            update_about.about_Describe =  var_about_Describe 
            update_about.about_admin_email = var_about_admin_email
            update_about.about_address = var_about_address
            update_about.about_contact = var_about_contact
            update_about.about_img = about_img

            update_about.save()
            return redirect('setting')
        else:
            try:
                add_about = about_Pharma.objects.create(Pk_about_ID = auth_token,
                    about_Title = var_about_Title, about_Describe =  var_about_Describe, 
                    about_admin_email = var_about_admin_email, about_address = var_about_address,
                    about_contact = var_about_contact, about_img = about_img
                )
                add_about.save()
                return redirect('setting')
            except Exception as e:
                print(e)
    return redirect('setting')

# ***********************************   *about Pharma Delete*   ***************************************************
def delete_about(request,id):
    about_del = about_Pharma.objects.filter(Pk_about_ID = id).first()
    about_del.delete()
    messages.success(request, 'About Pharma is Successfully Deleted ! \" ' + id + ' \"')
    return redirect('setting')


# ***********************************   *Admin Time Setting Add*   ***************************************************
def time_setting(request): 
    auth_token = str(uuid.uuid4())  
    if request.method == "POST": 
        var_DateFrom = request.POST.get("input_DateFrom")
        var_DateTo = request.POST.get("input_DateTo")

        var_TimeStartHour = request.POST.get("input_TimeStartHour")
        var_TimeStartMin = request.POST.get("input_TimeStartMin")
        var_TimeToHour = request.POST.get("input_TimeToHour")
        var_TimeToMin = request.POST.get("input_TimeToMin")

        if var_DateFrom is None : 
            messages.error(request, 'Date Field must be required. Try Again!!!')
            return redirect('setting')
        if var_DateTo == var_DateFrom or var_DateTo is None : 
            var_DateTo = "N/A"
        if var_TimeStartHour is None or var_TimeStartMin is None: 
            messages.error(request, 'Starting Time Field are must be Required. Try Again!!!')
            return redirect('setting')
        if var_TimeToHour is None or var_TimeToMin is None: 
            messages.error(request, 'Finishing Time Field are must be Required. Try Again!!!')
            return redirect('setting')
        try: 
            obj_time = Pharma_TimeTable.objects.create(Pk_Time_ID = auth_token,
                        DateFrom = var_DateFrom, DateTo = var_DateTo,
                        TimeFromHour = var_TimeStartHour, TimeFromMin = var_TimeStartMin,
                        TimeToHour = var_TimeToHour, TimeToMin = var_TimeToMin
                )
            obj_time.save() 
            messages.error(request, 'Time Set Successfully!!!')
            return redirect('setting')
        except Exception as e:
            print(e) 
    return redirect('setting')
 
# ***********************************   *Admin Time Setting Update*   ***************************************************
def update_time_setting(request, id):   
    if request.method == "POST": 
        var_DateFrom = request.POST.get("input_DateFrom")
        var_DateTo = request.POST.get("input_DateTo")

        var_TimeStartHour = request.POST.get("input_TimeStartHour")
        var_TimeStartMin = request.POST.get("input_TimeStartMin")
        var_TimeToHour = request.POST.get("input_TimeToHour")
        var_TimeToMin = request.POST.get("input_TimeToMin")
        
        update_time = Pharma_TimeTable.objects.filter(Pk_Time_ID = id).first()
        if var_DateFrom is None : 
            var_DateFrom = update_time.DateFrom
        if var_DateTo is None:
            var_DateTo  = update_time.DateTo 
        if var_DateTo == var_DateFrom: 
            var_DateTo = "N/A"
        if var_TimeStartHour is None: 
            var_TimeStartHour = update_time.TimeFromHour
        if var_TimeStartMin is None: 
            var_TimeStartMin = update_time.TimeFromMin
        if var_TimeToHour is None: 
            var_TimeToHour = update_time.TimeToHour
        if var_TimeToMin is None: 
            var_TimeToMin = update_time.TimeToMin
        try: 
            update_time.DateFrom = var_DateFrom
            update_time.DateTo = var_DateTo
            update_time.TimeFromHour = var_TimeStartHour
            update_time.TimeFromMin = var_TimeStartMin
            update_time.TimeToHour = var_TimeToHour
            update_time.TimeToMin = var_TimeToMin 
            update_time.save() 
            messages.error(request, 'Time Update Set Successfully!!!')
            return redirect('setting')
        except Exception as e:
            print(e) 
    return redirect('setting')

# ***********************************   *Admin Time Setting Delete*   ***************************************************
def time_delete(request,id):
    time_del = Pharma_TimeTable.objects.filter(Pk_Time_ID = id).first()
    time_del.delete()
    messages.success(request, 'Time Set is Successfully Deleted ! \" ' + id + ' \"')
    return redirect('setting')

# ***********************************   *Order Status*   ***************************************************
def order_status(request):
    if request.method == "POST": 
        order_list = request.POST.getlist('status_list_ID') 
        orderStatus = request.POST.get('orderStatus') 
        
        if orderStatus is None:
            messages.success(request,  'Status Value field must be Choose!')
            return redirect('medicine_order')
        if order_list == [] : 
            messages.success(request,  'Status Checkbox field must be Selected!')
            return redirect('medicine_order')
        
        for med_id in order_list: 
            data_Order = med_Order.objects.filter(Pk_order_ID = med_id).first()
            data_Order.status_Cart = orderStatus
            data_Order.save()
            
        messages.success(request,  'Order Status is Successfully Change!')
        return redirect('medicine_order')
    return redirect('medicine_order')

# ***********************************   *Order delete Admin*   ***************************************************
def order_delete_admin(request, id):
    order_del = med_Order.objects.filter(Pk_order_ID = id).first()
    order_del.delete()
    messages.success(request, 'Your Order is Successfully Deleted ! \" ' + id + ' \"')
    return redirect('medicine')

# ***********************************   *Medicine Calculate*   ***************************************************

