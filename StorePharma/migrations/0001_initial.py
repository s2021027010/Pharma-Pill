# Generated by Django 4.2.1 on 2024-02-28 09:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="about_Pharma",
            fields=[
                (
                    "Pk_about_ID",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("about_Title", models.TextField(max_length=255)),
                ("about_Describe", models.TextField(max_length=1000)),
                ("about_admin_email", models.TextField(max_length=255)),
                ("about_address", models.TextField(max_length=255)),
                ("about_contact", models.TextField(max_length=255)),
                (
                    "about_img",
                    models.ImageField(blank=True, max_length=255, upload_to="Profile/"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Blogs_Pharma",
            fields=[
                (
                    "Pk_blog_ID",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("blog_Title", models.TextField(max_length=255)),
                ("blog_Medicine_Name", models.TextField(max_length=255)),
                ("blog_Describe", models.TextField(max_length=1000)),
                (
                    "blog_img",
                    models.ImageField(blank=True, max_length=255, upload_to="Profile/"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="db_Medicine",
            fields=[
                (
                    "Medicine_ID",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("Med_LabelName", models.TextField(max_length=500)),
                ("Med_CompanyName", models.TextField(max_length=500)),
                ("Med_FormulaName", models.TextField(max_length=500)),
                ("Med_Purchase_Price", models.FloatField()),
                ("Med_Sell_Price", models.FloatField()),
                ("Med_Type", models.TextField(max_length=500)),
                ("Med_UsedFor", models.TextField(max_length=1000)),
                ("Med_Describtion", models.TextField(max_length=1000)),
                ("Med_ProductionDate", models.DateField(blank=True)),
                ("Med_ExpireDate", models.DateField(blank=True)),
                (
                    "Med_photo",
                    models.ImageField(
                        blank=True, max_length=255, upload_to="Medicine/"
                    ),
                ),
                ("Med_Status", models.TextField(max_length=500)),
                ("Med_Size", models.TextField(max_length=500)),
                ("Med_Quantity", models.IntegerField()),
                ("Med_Remain_Quantity", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="med_Cart_list",
            fields=[
                (
                    "Pk_Cart_ID",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("cart_email", models.CharField(max_length=255)),
                ("med_Cart_ID", models.CharField(max_length=100)),
                ("Med_Cart_Quantity", models.IntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="med_OrderMedicine",
            fields=[
                (
                    "Pk_OrderMedicine_ID",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("order_OrderMedicine_ID", models.CharField(max_length=100)),
                ("med_OrderMedicine_email", models.CharField(max_length=255)),
                ("med_OrderMedicine_ID", models.CharField(max_length=255)),
                ("Pk_Cart_List_ID", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="medicine_Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Med_ID_Img", models.CharField(max_length=100)),
                (
                    "list1_img",
                    models.ImageField(blank=True, max_length=255, upload_to="MedList/"),
                ),
                (
                    "list2_img",
                    models.ImageField(blank=True, max_length=255, upload_to="MedList/"),
                ),
                (
                    "list3_img",
                    models.ImageField(blank=True, max_length=255, upload_to="MedList/"),
                ),
                (
                    "list4_img",
                    models.ImageField(blank=True, max_length=255, upload_to="MedList/"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="OptionList",
            fields=[
                (
                    "Option_ID",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("company_List", models.TextField(max_length=255)),
                ("type_List", models.TextField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Pharma_TimeTable",
            fields=[
                (
                    "Pk_Time_ID",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("DateFrom", models.CharField(max_length=100)),
                ("DateTo", models.CharField(max_length=100)),
                ("TimeFromHour", models.CharField(max_length=100)),
                ("TimeFromMin", models.CharField(max_length=100)),
                ("TimeToHour", models.CharField(max_length=100)),
                ("TimeToMin", models.CharField(max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="med_Order",
            fields=[
                (
                    "Pk_order_ID",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("order_email", models.CharField(max_length=255)),
                ("status_Cart", models.TextField(max_length=100)),
                ("Med_Price", models.FloatField()),
                (
                    "created_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "med_order_ID",
                    models.ManyToManyField(default=True, to="StorePharma.db_medicine"),
                ),
            ],
        ),
    ]
