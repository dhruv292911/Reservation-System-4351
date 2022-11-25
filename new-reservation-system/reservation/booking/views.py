from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .models import *
from django.template import loader

# Create your views here.


def home(request):
    #return HttpResponse("Hello I am working")
    return render(request, "login.html")


def registration(request):
    #return HttpResponse("Hello this is registration page")

    if request.method == "POST":

        username = request.POST['username']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        mail_add = request.POST['mailingaddress']
        bill_add = request.POST['billingaddress']
        payment_type = request.POST['payment_method']
        credit_card_num = request.POST['credit_card']


        if registeredUser.objects.filter(username = username):
            return HttpResponse("Username already exist! Please reload and try again")
        
        if pass1 != pass2:
            return HttpResponse("The passwords didn't match! Please reload and try again")
        
        if not username.isalnum():
            return HttpResponse("Username must be Alpha-Numeric! Please reload and try again")
        

        new_reg_user = registeredUser()

        new_reg_user.username = username
        new_reg_user.password = pass1
        new_reg_user.mailing_address = mail_add
        new_reg_user.billing_address = bill_add
        new_reg_user.pref_payment_method = payment_type
        new_reg_user.cc_num = credit_card_num

        new_reg_user.save()

        messages.success(request, "Your Account has been successfully created.")

        return redirect('home')

    return render(request, "registration.html")


def reservation(request):
    #return HttpResponse("Hello this is the reservation page")
    
    if request.method == "POST":
        res_name = request.POST['name']
        res_phone = request.POST['phone_num']
        res_email = request.POST['email']
        res_partysize = int(request.POST['partysize'])
        res_date = request.POST['date']

        # see if the date is already registered in the date table (if it is we know that a table should be occupied(1, 2, or banquet hall) and atleast one reservation should be attached to the date object)
        set_of_reservations_same_date = Date.objects.filter(reservation_date = res_date)

        if(set_of_reservations_same_date.count() == 0):
            #first create the date object in the date table and save it
            new_res_date = Date()
            new_res_date.reservation_date = res_date
            new_res_date.save()
            
            # now create the reservation object and attach it to the date object above (1 to M relationship)
            new_reservation = Reservation(name = res_name, party_size = res_partysize, email = res_email, reservation_phone = res_phone, dates = new_res_date )
            new_reservation.save()

            set_of_tables = Table.objects.all()     # we will be using the same set of 11 tables. Since the date is not reserved we know all 11 tables are available on the specific date
            
            # if the party size is less than 10 we will only need one table. Add the corresponding table to the reservation object and add the corresponding table to the date object

            if(res_partysize <= 10):
                for table in set_of_tables:
                    if table.capacity >= res_partysize:
                        new_reservation.tables.add(table)                #pizza.toppings
                        new_res_date.table_set.add(table)                #topping.pizza_set
                        break

                return render(request, "reservationconfirmation.html")
       
            elif((res_partysize > 10) and (res_partysize <= 16)):
                # we need to combine two tables one size 10 and one <10
                table_one = set_of_tables.get(capacity = 10)
                remainder = res_partysize - 10

                for table in set_of_tables:
                    if table.capacity >= remainder:
                        new_reservation.tables.add(table_one)
                        new_reservation.tables.add(table)
                        new_res_date.table_set.add(table_one)
                        new_res_date.table_set.add(table)
                        break
                return render(request, "reservationconfirmation.html")
           
            else: # size > 16
                banquet_hall = set_of_tables.get(capacity = 200)
                new_reservation.tables.add(banquet_hall)
                new_res_date.table_set.add(banquet_hall)
                return render(request, "reservationconfirmation.html")

            
        else: # there is already a date object or a few date objects on the desired date. (set_of_reservations_same_date) > 0
            #we want to exclude the tables that are associate with date objects where the reservation_date is the desired_date


            #first create the date object in the date table and save it
            new_res_date = Date()
            new_res_date.reservation_date = res_date
            new_res_date.save()



            # now create the reservation object and attach it to the date object above (1 to M relationship)
            new_reservation = Reservation(name = res_name, party_size = res_partysize, email = res_email, reservation_phone = res_phone, dates = new_res_date )
            new_reservation.save()


            # since we know the date is already reserved we are getting the tables that are not associated with that date
            set_of_available_tables = Table.objects.exclude(dates__reservation_date = res_date)
            set_of_tables = Table.objects.all()



            if((set_of_available_tables.count() == 0) or res_partysize > 16): #if no tables available or partysize is > 16 add to banquet hall
                banquet_hall = set_of_tables.get(capacity = 200)
                new_reservation.tables.add(banquet_hall)
                new_res_date.table_set.add(banquet_hall)
                return render(request, "reservationconfirmation.html")
            
            elif (set_of_available_tables.count() == 1):  # if only one table is avaiable check if it can handle the guests else add to banquet hall
                for table in set_of_available_tables:
                    if res_partysize <= table.capacity:
                        new_reservation.tables.add(table)
                        new_res_date.table_set.add(table)
                        return render(request, "reservationconfirmation.html")
                    else:
                        banquet_hall = set_of_tables.get(capacity = 200)
                        new_reservation.tables.add(banquet_hall)
                        new_res_date.table_set.add(banquet_hall)
                        return render(request, "reservationconfirmation.html")
            
            else: # more than one table is available

                #1). First Check if 1 table is sufficient to take care of the reservation. Make sure to ignore the banquet hall cap = 200
                #if found one table to fit the party form the relationships and return the html template

                for table in set_of_available_tables:
                    if(table.capacity >= res_partysize) and (table.capacity != 200):
                        new_reservation.tables.add(table)
                        new_res_date.table_set.add(table)
                        return render(request, "reservationconfirmation.html")
                
                #2). Check if 2 tables are sufficient to take care of the reservation. Make sure to ignore the banquet hall cap = 200
                #If two tables are required that means the above for loop failed ^^. So the first table should be the biggest available table
                #and then iterate through the tables to find the smallest 2nd table 

                max = 0
                current_first_table = set_of_available_tables.first()
                
                # Search for First Table
                for table in set_of_available_tables:
                    if(table.capacity > max) and (table.capacity != 200):
                        max = table.capacity
                        current_first_table = table
                
                remainder = res_partysize - max

                #Search for Second Table. If found both tables then form the relationships and return html template

                set_of_remaining_tables = set_of_available_tables.exclude(id=current_first_table.id)



                for table in set_of_remaining_tables:
                    if(table.capacity >= remainder) and (table.capacity != 200):
                        second_table = table
                        new_reservation.tables.add(current_first_table)
                        new_reservation.tables.add(second_table)
                        new_res_date.table_set.add(current_first_table)
                        new_res_date.table_set.add(second_table)
                        return render(request, "reservationconfirmation.html")
                

                #if you can't find two tables just book them in the banquet hall and return 

                banquet_hall = set_of_tables.get(capacity = 200)
                new_reservation.tables.add(banquet_hall)
                new_res_date.table_set.add(banquet_hall)
                return render(request, "reservationconfirmation.html")



    return render(request, "reservation.html")



def login(request):
    if request.method == "POST":

        accountname = request.POST['username']

        current_user = registeredUser.objects.get(username= accountname)

        #template = loader.get_template('accountpage.html')

        # context = {
        #     'cur_user' : current_user
        # }

        return render(request, "accountpage.html", {'cur_user': current_user})  # what we call it here (lhs) is what we can call it in the template
    
    
    return HttpResponse("Hello you are logged in")