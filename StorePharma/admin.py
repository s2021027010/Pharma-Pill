from django.contrib import admin

from .models import db_Medicine , medicine_Image , med_Cart_list, Blogs_Pharma
from .models import med_Order , Pharma_TimeTable, OptionList, about_Pharma, med_OrderMedicine

admin.site.register(db_Medicine)
admin.site.register(medicine_Image)
admin.site.register(med_Cart_list)
admin.site.register(med_Order)
admin.site.register(med_OrderMedicine)
admin.site.register(Pharma_TimeTable)
admin.site.register(OptionList)
admin.site.register(Blogs_Pharma)
admin.site.register(about_Pharma)