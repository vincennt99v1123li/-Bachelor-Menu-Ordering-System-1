import sys

from tkinter import ttk
import tkinter as tk
import tkinter.scrolledtext as tkst
from tkinter.constants import ACTIVE, DISABLED, NORMAL
from tkinter.constants import LEFT, BOTTOM
from tkinter import Button, Frame, Tk
from faulthandler import disable
import datetime
import time
from tkinter import END
import cx_Oracle
import login_loop
import clock



class Gui:
    def last_page(self,page):

        if page     == "table_sub" :
            self.left_frame.pack_forget()
            self.main_page(1,[],'')
            self.table_id_nm = ""

        elif page == "address_page":
            self.left_frame.pack_forget()
            self.address_list = []
            self.main_page(1,[],'')

        elif page == "check_order":
            self.left_frame.pack_forget()
            self.middle_frame.pack_forget()
            self.main_page(1,[],'')
        else:
            self.address_list = ''
            self.add_pd_list = []
            self.add_qty_list = []
            self.add_link_list=[]
            self.add_link_price_list=[]
            self.table_id_nm = ""
            self.delivery_list=[]


    def last_page_tb(self,page,table_no):
        if page=="set_tb":
            self.left_frame.pack_forget()

            self.add_pd_list = []
            self.add_qty_list = []
            self.add_link_list = []
            self.add_link_price_list = []
            self.table_sub(self.table_id_nm, table_no)



        else:
            self.left_frame.pack_forget()
            self.middle_frame.pack_forget()
            self.add_pd_list = []
            self.add_qty_list = []
            self.add_link_list = []
            self.add_link_price_list = []
            self.address_list = ''
            self.table_sub(self.table_id_nm,table_no)
            self.delivery_list=[]


    def last_page_switch(self, table_id,number):
        self.left_frame.pack_forget()

        self.add_pd_list = []
        self.add_qty_list = []
        self.add_link_list = []
        self.add_link_price_list = []
        print(table_id)
        print(number)
        self.table_sub(table_id, int(number))


    def home_page(self,page):

        if page == "add_order":
            self.left_frame.pack_forget()
            self.middle_frame.pack_forget()
            self.add_pd_list = []
            self.add_qty_list = []
            self.add_link_list = []
            self.add_link_price_list = []
            self.table_id_nm=""
            self.main_page(1,[],'')



        elif page == "check_order":
            self.left_frame.pack_forget()
            self.middle_frame.pack_forget()
            self.main_page(1,[],'')


        elif page == "del_order":
            self.left_frame.pack_forget()
            self.middle_frame.pack_forget()
            self.add_pd_list = []
            self.add_qty_list = []
            self.add_link_list = []
            self.add_link_price_list = []
            self.table_id_nm = ""
            self.main_page(1,[],'')
            self.delivery_list = []
            self.address_list = ''

        else:
            self.left_frame.pack_forget()
            self.add_pd_list = []
            self.add_qty_list = []
            self.add_link_list = []
            self.add_link_price_list = []
            self.table_id_nm = ""
            self.main_page(1,[],'')
            self.delivery_list=[]
            self.address_list = ''

    def check_page(self,page):
        self.left_frame.pack_forget()
        self.middle_frame.pack_forget()
        self.add_pd_list = []
        self.add_qty_list = []
        self.add_link_list = []
        self.add_link_price_list = []
        self.table_id_nm = ""
        self.check_deli_take_away()

    def confirm_order(self,order_id,table_no,section):


        if (self.add_pd_list != []) and (self.add_qty_list != []):
            t_stop=[]
            for e in range(0,len(self.add_pd_list)):
                stop=False
                i=0
                count=0
                while not stop:
                    if self.add_pd_list[e][i]=="'":
                        count+=1
                    if count==2:
                        stop=True
                        t_stop.append(i)
                    i += 1

            loop_times = len(self.add_qty_list)

            str_order_id = str(order_id)[2:-3]

            price_list=[]

            new_pd_id_link=''

            for i in range(0,loop_times):
                cur = self.conn.cursor()
                cur.execute(
                    "Select product_price from product where product_id = '"+str(self.add_pd_list[i][2:t_stop[i]])+"'")
                for row in cur.fetchall():
                    price_list.append(row)


            print(self.add_link_list)
            print(self.add_link_price_list)
            for i in range(0,loop_times):

                latest_order_pd_id=[]
                new_pd_id = 0
                cur = self.conn.cursor()
                cur.execute("select max(order_product_id) from order_product ")
                for row in cur.fetchall():
                    latest_order_pd_id.append(row)

                if (str(latest_order_pd_id[0])[1:-2]) != 'None':
                    new_pd_id = int(str(latest_order_pd_id[0])[1:-2]) + 1
                else:
                    new_pd_id=1
                if str(self.add_link_list[i]) == '/':
                    new_pd_id_list=str(new_pd_id)
                else:
                    pass

                #print(str_order_id)
                #print(str(self.add_pd_list[i][2:t_stop[i]]))
                #print(str(self.add_qty_list[i]))
                #print((str(price_list[i])[1:-2]))
                #print(str(new_pd_id))
                #print(new_pd_id_list)

                if str(self.add_link_price_list[i]) == "Y":
                    sql=("insert into order_product (order_id,product_id,quantity,price,order_date, order_product_id, link_product) values ( " +str_order_id+",'"+str(self.add_pd_list[i][2:t_stop[i]])+"',"+str(self.add_qty_list[i])+","+(str(price_list[i])[1:-2])+",sysdate,"+str(new_pd_id)+",'"+new_pd_id_list+"')")
                else:
                    sql = ("insert into order_product (order_id,product_id,quantity,price,order_date, order_product_id, link_product) values ( " + str_order_id + ",'" + str(self.add_pd_list[i][2:t_stop[i]]) + "'," + str(self.add_qty_list[i]) + "," + '0' + ",sysdate," + str(new_pd_id) + ",'" + new_pd_id_list + "')")

                self.cur.execute(sql)
                self.cur.execute('commit')
            if section == 'member' or section == "Add_pd":
                self.last_page_tb("add_order", table_no)
            elif section == "Add_pd_p_t" or section == "Add_pd_check" or section == "member_check":
                self.check_page("add_order")


        else:
            pass


    def add_to_cart(self,category,section):
        if self.add_list == "":
            pass
        elif self.add_pd_list != "":
            length_pd_list = len(self.add_pd_list)
            length_add_qty_list = len(self.add_qty_list)


            for i in range(0,(length_pd_list-length_add_qty_list)):
                self.add_qty_list.append(self.add_list)

            self.add_list = ""
            self.editAreaTable2.delete("1.0", END)
            self.editAreaTable.delete("1.0", END)
            for i in range(0,length_pd_list):
                self.editAreaTable.insert(tk.INSERT, self.add_pd_list[i][2:10]+self.add_pd_list[i][14:-2]+"\n"+" Qty: "+self.add_qty_list[i]+"\n")
            self.editAreaTable.see("end")
            self.add_order_pizza(section)

    def add_to_cart_member(self,category):

        length_pd_list = len(self.add_pd_list)
        length_add_qty_list = len(self.add_qty_list)


        for i in range(0,(length_pd_list-length_add_qty_list)):
            self.add_qty_list.append('1')

        self.add_list = ""
        self.editAreaTable2.delete("1.0", END)
        self.editAreaTable.delete("1.0", END)
        for i in range(0,length_pd_list):
            self.editAreaTable.insert(tk.INSERT, self.add_pd_list[i][2:10]+self.add_pd_list[i][14:-2]+"\n"+" Qty: "+self.add_qty_list[i]+"\n")
        self.editAreaTable.see("end")

        member_point = []
        cur = self.conn.cursor()
        cur.execute(
            "Select membership_points from membership where member_id = '" + str(self.member_id) + "'")
        for row in cur.fetchall():
            member_point.append(row)

        #str(member_point[0])[1:-2]

        comma_location = 0
        pid=''
        #print(str(self.add_pd_list[length_pd_list-1])[2])
        #print(str(self.add_pd_list[length_pd_list-2]))

        if str(self.add_pd_list[length_pd_list-1])[2] == 'C':

            for i in range(0,len(str(self.add_pd_list[length_pd_list-2]))):
                if str(self.add_pd_list[length_pd_list-2])[i] == ',':
                    comma_location = i

            pid = str(self.add_pd_list[length_pd_list - 2])[2:comma_location - 1]


        else:
            for i in range(0, len(str(self.add_pd_list[length_pd_list - 1]))):
                if str(self.add_pd_list[length_pd_list - 1])[i] == ',':
                    comma_location = i
            pid = str(self.add_pd_list[length_pd_list - 1])[2:comma_location - 1]

        product_point=[]
        cur = self.conn.cursor()
        cur.execute(
            "Select point from member_product where product_id = '" + str(pid) + "'")
        for row in cur.fetchall():
            product_point.append(row)


        new_member_point=int(str(member_point[0])[1:-2])-int(str(product_point[0])[1:-2])
        #print(new_member_point)

        cur = self.conn.cursor()
        sql = ("update membership set membership_points = "+str(new_member_point)+"where member_id  ='"+ str(self.member_id) + "'")

        self.cur.execute(sql)
        self.cur.execute('commit')

        #print(str(self.add_pd_list[length_pd_list - 2])[2:comma_location-1])
        self.add_order_pizza_member()

    def add_page_editarea(self,choice):
        if choice == "del" and self.add_list != "":

            self.add_list = self.add_list[:-1]
            self.editAreaTable2.delete("1.0", END)
            self.editAreaTable2.insert(tk.INSERT, self.add_list)
        elif choice == "del":
            pass
        elif choice == "Clear":
            """
            self.add_list = ""
            self.editAreaTable2.delete("1.0", END)
            """
            pass
        else :
            self.add_list+=choice
            self.editAreaTable2.insert(tk.INSERT, choice)

    def add_pd(self, choice, category,section):
        if section == "Add_pd":
            self.btnTR1.config(text='Starter', background="dark slate gray", command=lambda: self.add_order_starter(section))

            self.btnTR2.config(text='Pizza', background="dark slate gray", command=lambda: self.add_order_pizza(section))

            self.btnTR3.config(text='Pasta/Rice', background="dark slate gray", command=lambda: self.add_order_rice_pasta(section))

            self.btnTR4.config(text="Dessert", background="dark slate gray", command=lambda: self.add_order_dessert(section))

            self.btnTR5.config(text="Drinks", background="dark slate gray", command=lambda: self.add_order_drink(section))

            self.btnTR6.config(text="Special", background="dark slate gray", command=lambda: self.add_order_special(section))

            self.btnTR7.config(text='Set', background="dark slate gray", command=lambda: self.add_order_set(section))

            self.btnTR8.config(text='Pizza Creator', background="dark slate gray",
                           command=lambda: self.add_order_pizza_creator(section))

        elif section == "Add_pd_p_t" or section == "Add_pd_check" :
            self.btnTR1.config(text='Starter', background="dark slate gray",
                               command=lambda: self.add_order_starter(section))

            self.btnTR2.config(text='Pizza', background="dark slate gray",
                               command=lambda: self.add_order_pizza(section))

            self.btnTR3.config(text='Pasta/Rice', background="dark slate gray",
                               command=lambda: self.add_order_rice_pasta(section))

            self.btnTR4.config(text="Dessert", background="dark slate gray",
                               command=lambda: self.add_order_dessert(section))

            self.btnTR5.config(text="Drinks", background="dark slate gray",
                               command=lambda: self.add_order_drink(section))

            self.btnTR6.config(text="Special", background="dark slate gray",
                               command=lambda: self.add_order_special(section))

            self.btnTR7.config(text='Set', background="dark slate gray", command=lambda: self.add_order_set(section))

            self.btnTR8.config(text='', background="grey20",
                               command='')

        self.set_option_count = 0
        self.creator_option_count = 0
        id_end = ''
        name_start = ''
        count = 0
        for e in range(0, len(choice)):
            if choice[e] == "'":
                count += 1
            if id_end == '' and count == 2:
                id_end = e
            if name_start == '' and count == 3:
                name_start = e
        print(category)
        if category=='pizza' :
            choice_id = choice[2:id_end]
            choice_name = choice[name_start + 1:-2]
            self.add_link_list.append(str(len(self.add_pd_list)-1))
            self.add_link_price_list.append('Y')
            self.add_pd_list.append(choice)

            self.editAreaTable.insert(tk.INSERT, choice_id + " "+choice_name + "\n")


        elif  category == 'drink':
            print(choice)
            choice_id = choice[2:id_end]
            choice_name = choice[name_start + 1:-2]
            self.add_link_list.append(str(len(self.add_pd_list) - 1))
            self.add_link_price_list.append('Y')
            self.add_pd_list.append(choice)
            self.add_pd_location=''
            self.editAreaTable.insert(tk.INSERT, choice_id + " "+ choice_name + "\n")

        elif category == 'set':
            choice_id = choice[2:id_end]
            choice_name = choice[name_start + 1:-2]
            self.add_link_list.append(self.add_pd_location)
            self.add_link_price_list.append('Y')
            self.add_pd_list.append(choice)

            self.editAreaTable.insert(tk.INSERT, choice_id + " "+ choice_name + "\n")

        elif category == 'creator':
            self.add_pd_location=''
            pass

        elif category != '':
            choice_id = choice[2:id_end]
            choice_name = choice[name_start + 1:-2]
            self.add_pd_list.append(choice)
            self.add_link_list.append('/')
            self.add_link_price_list.append('Y')
            self.editAreaTable.insert(tk.INSERT, choice_id +" "+ choice_name + "\n")

        self.editAreaTable.insert(tk.INSERT, "\n" + "Quantity?" + "\n")
        self.editAreaTable.see("end")
        self.lable_pd.config(text='')

        for i in range(0, 45):
            self.btn_pd[0][i].config(text=" ", command='')

    def add_pd_member(self, choice, category):

        self.btnTR1.config(text='Starter', background="dark slate gray",
                           command=lambda: self.add_order_starter_member())

        self.btnTR2.config(text='Pizza', background="dark slate gray", command=lambda: self.add_order_pizza_member())

        self.btnTR3.config(text='Pasta/Rice', background="dark slate gray",
                           command=lambda: self.add_order_rice_pasta_member())

        self.btnTR4.config(text="Dessert", background="dark slate gray",
                           command=lambda: self.add_order_dessert_member())

        self.btnTR5.config(text="Drinks", background="dark slate gray", command=lambda: self.add_order_drink_member())

        self.btnTR6.config(text='', background="grey20", command='')

        self.btnTR7.config(text='', background="grey20", command='')

        self.btnTR8.config(text='', background="grey20", command='')
        self.set_option_count = 0
        self.creator_option_count = 0
        id_end = ''
        name_start = ''
        count = 0
        for e in range(0, len(choice)):
            if choice[e] == "'":
                count += 1
            if id_end == '' and count == 2:
                id_end = e
            if name_start == '' and count == 3:
                name_start = e
        print(category)
        choice_id = choice[2:id_end]
        choice_name = choice[name_start + 1:-2]
        if category == 'pizza' or  category == 'drink':
            self.add_link_list.append(str(len(self.add_pd_list) - 1))
            self.add_link_price_list.append('Y')
            self.add_pd_list.append(choice)
            self.editAreaTable.insert(tk.INSERT, "\n" + "Confirm?" + "\n")
            for i in range(0, 45):
                self.btn_pd[0][i].config(text=" ", command='')
        else:
            member_point = []
            cur = self.conn.cursor()
            cur.execute(
                "Select membership_points from membership where member_id = '" + str(self.member_id) + "'")
            for row in cur.fetchall():
                member_point.append(row)

            print(str(member_point[0])[1:-2])
            print(choice_id)
            product_point = []
            cur = self.conn.cursor()
            cur.execute(
                "Select point from member_product where product_id = '" + str(choice_id) + "'")
            for row in cur.fetchall():
                product_point.append(row)

            if int(str(member_point[0])[1:-2]) >= int(str(product_point[0])[1:-2]):
                self.add_pd_list.append(choice)
                self.add_link_list.append('/')
                self.add_link_price_list.append('N')
                self.editAreaTable.insert(tk.INSERT, choice_id + " "+ choice_name + "\n")
                self.editAreaTable.insert(tk.INSERT, "\n" + "Confirm?" + "\n")
                for i in range(0, 45):
                    self.btn_pd[0][i].config(text=" ", command='')
            else:
                self.editAreaTable.insert(tk.INSERT, '\nNot enough points')
                self.editAreaTable.see("end")


        self.editAreaTable.see("end")
        self.lable_pd.config(text='')




    def crust(self, choice,section):
        self.btnTR1.config(text='', command='', bg='grey20')

        self.btnTR2.config(text='', command='', bg='grey20')

        self.btnTR3.config(text='', command='', bg='grey20')

        self.btnTR4.config(text='', command='', bg='grey20')

        self.btnTR5.config(text='', command='', bg='grey20')

        self.btnTR6.config(text='', command='', bg='grey20')

        self.btnTR7.config(text='', command='', bg='grey20')

        self.btnTR8.config(text='', command='', bg='grey20')
        choice_id = choice[2:6]
        choice_name = choice[10:-2]
        #print(choice_id)
        #print(choice_name)
        self.add_pd_list.append(choice)
        self.add_link_list.append('/')
        self.add_link_price_list.append('Y')

        crust_list = []
        self.editAreaTable.insert(tk.INSERT, choice_id+" "+choice_name+"\n")
        self.editAreaTable.see("end")
        cur = self.conn.cursor()
        cur.execute(
            "Select product_id, product_name from product where product_category = 'CRUST' order by product_id")
        for row in cur.fetchall():
            crust_list.append(row)



        self.lable_pd.config( text='Crust')

        length_data = len(crust_list)


        for i in range (0,45):

            self.btn_pd[0][i].config(text=" ", command='')


        for i in range (0,int(length_data)):
            t_id = str(crust_list[i])
            t_name = str(crust_list[i])
            self.btn_pd[0][i].config(text=(t_id[2:6] + "\n" + t_name[10:-2]), command=lambda i=i: self.add_pd(str(crust_list[i]),"pizza",section))

    def add_order_pizza(self,section):
        '''
        when button clicked
        '''

        pizza_list = []
        cur = self.conn.cursor()
        cur.execute("Select product_id, product_name from product where product_category = 'PIZZA' order by product_id")
        for row in cur.fetchall():
            pizza_list.append(row)

        self.lable_pd.config(text='Pizza')

        length_data = len(pizza_list)
        for i in range(0,length_data):

            t_id = str(pizza_list[i])
            t_name = str(pizza_list[i])
            self.btn_pd[0][i].config(text=(t_id[2:6] + "\n" + t_name[10:-2]),command=lambda i=i: self.crust(str(pizza_list[i]),section))

        for i in range(length_data,45):

            self.btn_pd[0][i].config(text=( "\n" ), command='')

    def add_order_starter(self,section):
        '''
        when button clicked
        '''
        t_id=[]
        t_name=[]
        starter_list = []
        cur = self.conn.cursor()
        cur.execute(
            "Select product_id, product_name from product where product_category = 'STARTER' and product_id not like 'C%' order by product_id")
        for row in cur.fetchall():
            starter_list.append(row)
            t_id.append(row[0])
            t_name.append(row[1])
        self.lable_pd.config(text='Starter')

        length_data = len(starter_list)
        for i in range(0, length_data):

            self.btn_pd[0][i].config(text=(t_id[i] + "\n" + t_name[i]),
                                     command=lambda i=i: self.add_pd(str(starter_list[i]), "starter",section))
        for i in range(length_data,45):

            self.btn_pd[0][i].config(text=( "\n" ), command='')

    def add_order_dessert(self,section):
        '''
        when button clicked
        '''
        t_id=[]
        t_name=[]
        starter_list = []
        cur = self.conn.cursor()
        cur.execute(
            "Select product_id, product_name from product where product_category = 'DESSERT' and product_id not like 'C%' order by product_id")
        for row in cur.fetchall():
            starter_list.append(row)
            t_id.append(row[0])
            t_name.append(row[1])
        self.lable_pd.config(text='Dessert')

        length_data = len(starter_list)
        for i in range(0, length_data):

            self.btn_pd[0][i].config(text=(t_id[i] + "\n" + t_name[i]),
                                     command=lambda i=i: self.add_pd(str(starter_list[i]), "dessert",section))
        for i in range(length_data,45):

            self.btn_pd[0][i].config(text=( "\n" ), command='')

    def add_order_special(self,section):
        '''
        when button clicked
        '''
        t_id=[]
        t_name=[]
        starter_list = []
        cur = self.conn.cursor()
        cur.execute(
            "Select product_id, product_name from product where product_category = 'SPECIAL' and product_id not like 'C%' order by product_id")
        for row in cur.fetchall():
            starter_list.append(row)
            t_id.append(row[0])
            t_name.append(row[1])
        self.lable_pd.config(text='Special')

        length_data = len(starter_list)
        for i in range(0, length_data):

            self.btn_pd[0][i].config(text=(t_id[i] + "\n" + t_name[i]),
                                     command=lambda i=i: self.add_pd(str(starter_list[i]), "special",section))
        for i in range(length_data,45):

            self.btn_pd[0][i].config(text=( "\n" ), command='')

    def add_order_rice_pasta(self,section):
        '''
        when button clicked
        '''
        t_id=[]
        t_name=[]
        rice_pasta_list = []
        cur = self.conn.cursor()
        cur.execute(
            "Select product_id, product_name from product where product_category = 'RICE/PASTA' and product_id not like 'C%' order by product_id")
        for row in cur.fetchall():
            rice_pasta_list.append(row)
            t_id.append(row[0])
            t_name.append(row[1])
        self.lable_pd.config(text='Rice/ pasta')

        length_data = len(rice_pasta_list)
        for i in range(0, length_data):

            self.btn_pd[0][i].config(text=(t_id[i] + "\n" + t_name[i]),
                                     command=lambda i=i: self.add_pd(str(rice_pasta_list[i]), "rice_pasta",section))
        for i in range(length_data,45):

            self.btn_pd[0][i].config(text=( "\n" ), command='')

    def add_order_drink_option(self, choice,section):
        self.btnTR1.config(text='', command='', bg='grey20')

        self.btnTR2.config(text='', command='', bg='grey20')

        self.btnTR3.config(text='', command='', bg='grey20')

        self.btnTR4.config(text='', command='', bg='grey20')

        self.btnTR5.config(text='', command='', bg='grey20')

        self.btnTR6.config(text='', command='', bg='grey20')

        self.btnTR7.config(text='', command='', bg='grey20')

        self.btnTR8.config(text='', command='', bg='grey20')
        choice_id = choice[2:6]
        choice_name = choice[10:-2]
        print(choice)
        self.add_pd_list.append(choice)
        self.add_link_list.append('/')
        self.add_link_price_list.append('Y')

        drink_option_list = []
        self.editAreaTable.insert(tk.INSERT, choice_id+" "+choice_name+"\n")
        self.editAreaTable.see("end")
        cur = self.conn.cursor()
        cur.execute(
            "Select product_id, product_name from product where product_id like '400%' order by product_id")
        for row in cur.fetchall():
            drink_option_list.append(row)



        self.lable_pd.config( text='Drink Option')

        length_data = len(drink_option_list)


        for i in range (0,45):

            self.btn_pd[0][i].config(text=" ", command='')


        for i in range (0,int(length_data)):
            t_id = str(drink_option_list[i])
            t_name = str(drink_option_list[i])
            self.btn_pd[0][i].config(text=(t_id[2:6] + "\n" + t_name[10:-2]), command=lambda i=i: self.add_pd(str(drink_option_list[i]),"drink",section))

    def add_order_drink(self,section):
        '''
        when button clicked
        '''

        t_id = []
        t_name = []
        drink_list = []
        cur = self.conn.cursor()
        cur.execute(
            "Select product_id, product_name from product where product_category = 'DRINK' and product_id not like '400%' order by product_id")
        for row in cur.fetchall():
            drink_list.append(row)
            t_id.append(row[0])
            t_name.append(row[1])
        self.lable_pd.config(text='Drink')

        length_data = len(drink_list)
        for i in range(0, length_data):
            self.btn_pd[0][i].config(text=(t_id[i] + "\n" + t_name[i]),
                                     command=lambda i=i: self.add_order_drink_option(str(drink_list[i]),section))
        for i in range(length_data, 45):
            self.btn_pd[0][i].config(text=("\n"), command='')

    def set_option(self, choice,section):
        self.btnTR1.config(text='', command='', bg='grey20')

        self.btnTR2.config(text='', command='', bg='grey20')

        self.btnTR3.config(text='', command='', bg='grey20')

        self.btnTR4.config(text='', command='', bg='grey20')

        self.btnTR5.config(text='', command='', bg='grey20')

        self.btnTR6.config(text='', command='', bg='grey20')

        self.btnTR7.config(text='', command='', bg='grey20')

        self.btnTR8.config(text='', command='', bg='grey20')
        self.set_option_count += 1
        id_end=''
        name_start=''

        count = 0
        for e in range(0,len(choice)):
            if choice[e]=="'":
                count+=1
            if id_end=='' and count==2:
                id_end = e
            if name_start=='' and count==3:
                name_start = e

        choice_id = choice[2:id_end]
        choice_name = choice[name_start+1:-2]

        #print(choice)
        self.add_pd_list.append(choice)

        print(choice[2])
        if self.set_option_count == 1:
            self.add_pd_location = str(len(self.add_pd_list) - 1)
            self.add_link_list.append('/')

        else:
            self.add_link_list.append(self.add_pd_location)

        if choice[2] == 'C' and choice[3]!= '1':
            self.add_link_price_list.append('Y')

        elif  self.set_option_count == 1:
            self.add_link_price_list.append('Y')
        else:
            self.add_link_price_list.append('N')

        self.editAreaTable.insert(tk.INSERT, choice_id +" "+ choice_name + "\n")
        self.editAreaTable.see("end")

        if self.set_option_count==1:
            self.set=choice_id
            self.lable_pd.config(text='Set Starter')
            starter_list = []
            cur = self.conn.cursor()
            cur.execute("Select b.product_id1 , a.product_name from product a join set_product b on a.product_id=b.product_id1 where b.product_id='{0}' and a.product_category='STARTER' order by b.product_id1 ".format(self.set))
            for row in cur.fetchall():
                starter_list.append(row)

            for i in range(0, 45):
                self.btn_pd[0][i].config(text=" ", command='')
            for e in range(0, len(starter_list)):
                self.btn_pd[0][e].config(text=(starter_list[e][0] + "\n" + starter_list[e][1]),
                                         command=lambda e=e: self.set_option(str(starter_list[e]),section))


        if self.set_option_count == 2:
            self.lable_pd.config(text='Set Pizza')
            PIZZA_list = []
            cur = self.conn.cursor()
            cur.execute(
                "Select b.product_id1 , a.product_name from product a join set_product b on a.product_id=b.product_id1 where b.product_id='{0}' and a.product_category='PIZZA' order by b.product_id1 ".format(self.set))
            for row in cur.fetchall():
                PIZZA_list.append(row)
            for i in range(0, 45):
                self.btn_pd[0][i].config(text=" ", command='')

            for e in range(0, len(PIZZA_list)):
                self.btn_pd[0][e].config(text=(PIZZA_list[e][0] + "\n" + PIZZA_list[e][1]),
                                         command=lambda e=e: self.set_option(str(PIZZA_list[e]),section))

        if self.set_option_count == 3:
            self.lable_pd.config(text='Set Crust')
            CRUST_list = []
            cur = self.conn.cursor()
            cur.execute(
                "Select b.product_id1 , a.product_name from product a join set_product b on a.product_id=b.product_id1 where b.product_id='{0}' and a.product_category='CRUST' order by b.product_id1 ".format(self.set))
            for row in cur.fetchall():
                CRUST_list.append(row)

            for i in range(0, 45):
                self.btn_pd[0][i].config(text=" ", command='')

            for e in range(0, len(CRUST_list)):
                self.btn_pd[0][e].config(text=(CRUST_list[e][0] + "\n" + CRUST_list[e][1]),
                                         command=lambda e=e: self.set_option(str(CRUST_list[e]),section))

        if self.set_option_count == 4:
            self.lable_pd.config(text='Set Rice/ Pizza')
            RICE_PASTA_list = []
            cur = self.conn.cursor()
            cur.execute(
                "Select b.product_id1 , a.product_name from product a join set_product b on a.product_id=b.product_id1 where b.product_id='{0}' and a.product_category='RICE/PASTA' order by b.product_id1 ".format(self.set))
            for row in cur.fetchall():
                RICE_PASTA_list.append(row)

            for i in range(0, 45):
                self.btn_pd[0][i].config(text=" ", command='')

            for e in range(0, len(RICE_PASTA_list)):
                self.btn_pd[0][e].config(text=(RICE_PASTA_list[e][0] + "\n" + RICE_PASTA_list[e][1]),
                                         command=lambda e=e: self.set_option(str(RICE_PASTA_list[e]),section))

        if self.set_option_count == 5:
            self.lable_pd.config(text='Set Drink')
            DRINK_list = []
            cur = self.conn.cursor()
            cur.execute(
                "Select b.product_id1 , a.product_name from product a join set_product b on a.product_id=b.product_id1 where b.product_id='{0}' and a.product_category='DRINK' order by b.product_id1 ".format(self.set))
            for row in cur.fetchall():
                DRINK_list.append(row)

            for i in range(0, 45):
                self.btn_pd[0][i].config(text=" ", command='')

            for e in range(0, len(DRINK_list)):
                self.btn_pd[0][e].config(text=(DRINK_list[e][0] + "\n" + DRINK_list[e][1]),
                                         command=lambda e=e: self.set_option(str(DRINK_list[e]),section))

        if self.set_option_count == 6:
            self.set_option_count = 0
            self.lable_pd.config(text='Set Drink Option')
            DRINK_option_list = []
            cur = self.conn.cursor()
            cur.execute("Select product_id,product_name from product where product_id like '400%'  order by product_id")
            for row in cur.fetchall():
                DRINK_option_list.append(row)
            for i in range(0, 45):
                self.btn_pd[0][i].config(text=" ", command='')
            for e in range(0, len(DRINK_option_list)):
                self.btn_pd[0][e].config(text=(DRINK_option_list[e][0] + "\n" + DRINK_option_list[e][1]),
                                         command=lambda e=e: self.add_pd(str(DRINK_option_list[e]), "set",section))

    def add_order_set(self,section):
        '''
        when button clicked
        '''

        set_list = []
        cur = self.conn.cursor()
        cur.execute(
            "Select product_id, product_name from product where product_category = 'SET' order by product_id")
        for row in cur.fetchall():
            set_list.append(row)

        self.lable_pd.config(text='set')


        length_data = len(set_list)
        for i in range(0,length_data):

            t_id = str(set_list[i])
            t_name = str(set_list[i])
            self.btn_pd[0][i].config(text=(t_id[2:6] + "\n" + t_name[10:-2]),command=lambda i=i: self.set_option(str(set_list[i]),section))

        for i in range(length_data,45):

            self.btn_pd[0][i].config(text=( "\n" ), command='')

    def add_order_pizza_creator_option(self, choice,section):
        self.btnTR1.config(text='', command='', bg='grey20')

        self.btnTR2.config(text='', command='', bg='grey20')

        self.btnTR3.config(text='', command='', bg='grey20')

        self.btnTR4.config(text='', command='', bg='grey20')

        self.btnTR5.config(text='', command='', bg='grey20')

        self.btnTR6.config(text='', command='', bg='grey20')

        self.btnTR7.config(text='', command='', bg='grey20')

        self.btnTR8.config(text='', command='', bg='grey20')
        self.creator_option_count+=1

        id_end=''
        name_start=''
        count = 0
        for e in range(0,len(choice)):
            if choice[e]=="'":
                count+=1
            if id_end=='' and count==2:
                id_end = e
            if name_start=='' and count==3:
                name_start = e

        choice_id = choice[2:id_end]
        choice_name = choice[name_start+1:-2]
        self.add_pd_list.append(choice)

        if self.creator_option_count == 1:
            self.add_pd_location = str(len(self.add_pd_list) - 1)
            self.add_link_list.append('/')
            self.add_link_price_list.append('Y')
        else:
            self.add_link_list.append(self.add_pd_location)
            self.add_link_price_list.append('Y')

        self.editAreaTable.insert(tk.INSERT, choice_id + " " +choice_name + "\n")
        self.editAreaTable.see("end")
        self.lable_pd.config(text='creator_option')

        if self.creator_option_count ==1:
            CRUST_list = []
            cur = self.conn.cursor()
            cur.execute(
                "Select product_id , product_name from product  where product_category='CRUST' order by product_id ")
            for row in cur.fetchall():
                CRUST_list.append(row)
            for i in range(0, 45):
                self.btn_pd[0][i].config(text=" ", command='')

            for e in range(0, len(CRUST_list)):
                self.btn_pd[0][e].config(text=(CRUST_list[e][0] + "\n" + CRUST_list[e][1]),
                                         command=lambda e=e: self.add_order_pizza_creator_option(str(CRUST_list[e]),section))

        elif self.creator_option_count>=2 and self.creator_option_count< 8:
            creator_option_list = []
            cur = self.conn.cursor()
            cur.execute("Select product_id, product_name from product where product_category = 'CREATECHOICE'  order by product_id")
            for row in cur.fetchall():
                found=False
                for e in range(0,len(self.add_pd_list)):
                    if str(row)==str(self.add_pd_list[e]) :
                        found=True
                if not found:
                    creator_option_list.append(row)
                    found=True

            for i in range(0, 45):
                self.btn_pd[0][i].config(text=" ", command='')
            for e in range(0, len(creator_option_list)):
                self.btn_pd[0][e].config(text=(creator_option_list[e][0] + "\n" + creator_option_list[e][1]),
                                         command=lambda e=e: self.add_order_pizza_creator_option(str(creator_option_list[e]),section))

            self.btn_pd[0][e+1].config(text=('[END]'),command=lambda : self.add_pd(" ", "creator",section))
        else:
            self.set_option_count = 0
            creator_option_list = []
            cur = self.conn.cursor()
            cur.execute("Select product_id, product_name from product where product_category = 'CREATECHOICE'  order by product_id")
            for row in cur.fetchall():
                found=False
                for e in range(0,len(self.add_pd_list)):
                    if str(row)==str(self.add_pd_list[e]) :
                        found=True
                if not found:
                    creator_option_list.append(row)
                    found=True
            for i in range(0, 45):
                self.btn_pd[0][i].config(text=" ", command='')
            for e in range(0, len(creator_option_list)):
                self.btn_pd[0][e].config(text=(creator_option_list[e][0] + "\n" + creator_option_list[e][1]),command=lambda e=e: self.add_pd(str(creator_option_list[e]), "creator",section))
            self.btn_pd[0][e + 1].config(text=('[END]'), command=lambda: self.add_pd(" ", "creator",section))

    def add_order_pizza_creator(self,section):
        '''
        when button clicked
        '''
        self.creator_option_count = 0

        t_id = []
        t_name = []
        pizza_creator_list = []
        cur = self.conn.cursor()
        cur.execute(
            "Select product_id, product_name from product where product_category = 'CREATE'  order by product_id")
        for row in cur.fetchall():
            pizza_creator_list.append(row)
            t_id.append(row[0])
            t_name.append(row[1])
        self.lable_pd.config(text='pizza_creator')

        length_data = len(pizza_creator_list)
        for i in range(0, length_data):
            self.btn_pd[0][i].config(text=(t_id[i] + "\n" + t_name[i]),
                                     command=lambda i=i: self.add_order_pizza_creator_option(str(pizza_creator_list[i]),section))
        for i in range(length_data, 45):
            self.btn_pd[0][i].config(text=("\n"), command='')


    def crust_member (self, choice):
        self.btnTR1.config(text='', command='', bg='grey20')

        self.btnTR2.config(text='', command='', bg='grey20')

        self.btnTR3.config(text='', command='', bg='grey20')

        self.btnTR4.config(text='', command='', bg='grey20')

        self.btnTR5.config(text='', command='', bg='grey20')

        self.btnTR6.config(text='', command='', bg='grey20')

        self.btnTR7.config(text='', command='', bg='grey20')

        self.btnTR8.config(text='', command='', bg='grey20')
        choice_id = choice[2:6]
        choice_name = choice[10:-2]
        #print(choice)

        member_point = []
        cur = self.conn.cursor()
        cur.execute(
            "Select membership_points from membership where member_id = '" + str(self.member_id) + "'")
        for row in cur.fetchall():
            member_point.append(row)

        print(str(member_point[0])[1:-2])
        print(choice_id)
        product_point = []
        cur = self.conn.cursor()
        cur.execute(
            "Select point from member_product where product_id = '" + str(choice_id) + "'")
        for row in cur.fetchall():
            product_point.append(row)

        if int(str(member_point[0])[1:-2]) >= int(str(product_point[0])[1:-2]):

            self.add_pd_list.append(choice)
            self.add_link_list.append('/')
            self.add_link_price_list.append('N')

            crust_list = []
            self.editAreaTable.insert(tk.INSERT, choice_id+" "+choice_name+"\n")
            self.editAreaTable.see("end")
            cur = self.conn.cursor()
            cur.execute(
                "Select product_id, product_name from product where product_category = 'CRUST' order by product_id")
            for row in cur.fetchall():
                crust_list.append(row)



            self.lable_pd.config( text='Crust')

            length_data = len(crust_list)


            for i in range (0,45):

                self.btn_pd[0][i].config(text=" ", command='')


            for i in range (0,int(length_data)):
                t_id = str(crust_list[i])
                t_name = str(crust_list[i])
                self.btn_pd[0][i].config(text=(t_id[2:6] + "\n" + t_name[10:-2]), command=lambda i=i: self.add_pd_member(str(crust_list[i]),"pizza"))

        else:
            self.editAreaTable.insert(tk.INSERT,'\nNot enough points')
            self.editAreaTable.see("end")

    def add_order_pizza_member(self):
        '''
        when button clicked
        '''

        pizza_list = []
        cur = self.conn.cursor()
        cur.execute(
            "Select member_product.product_id, product.product_name from member_product inner join product on member_product.product_id = product.product_id where product.product_category = 'PIZZA' order by product.product_id")
        for row in cur.fetchall():
            pizza_list.append(row)

        self.lable_pd.config(text='Pizza')

        length_data = len(pizza_list)
        for i in range(0, length_data):
            t_id = str(pizza_list[i])
            t_name = str(pizza_list[i])
            self.btn_pd[0][i].config(text=(t_id[2:6] + "\n" + t_name[10:-2]),
                                     command=lambda i=i: self.crust_member(str(pizza_list[i])))

        for i in range(length_data, 45):
            self.btn_pd[0][i].config(text=("\n"), command='')

    def add_order_starter_member(self):
        t_id = []
        t_name=[]
        starter_list=[]
        cur = self.conn.cursor()
        cur.execute(
            "Select member_product.product_id, product.product_name from member_product inner join product on member_product.product_id = product.product_id where product.product_category = 'STARTER' order by product.product_id")
        for row in cur.fetchall():
            t_id.append(row[0])
            t_name.append(row[1])
            starter_list.append((row))

        self.lable_pd.config(text='Starter')

        for i in range(0, len(t_id)):
            self.btn_pd[0][i].config(text=(t_id[i] + "\n" + t_name[i]),
                                     command=lambda i=i: self.add_pd_member(str(starter_list[i]),"starter"))

        for i in range(len(t_id), 45):
            self.btn_pd[0][i].config(text=("\n"), command='')

    def add_order_rice_pasta_member(self):
        t_id = []
        t_name = []
        rice_pasta_list = []
        cur = self.conn.cursor()
        cur.execute(
            "Select member_product.product_id, product.product_name from member_product inner join product on member_product.product_id = product.product_id where product.product_category = 'RICE/PASTA' order by product.product_id")
        for row in cur.fetchall():
            t_id.append(row[0])
            t_name.append(row[1])
            rice_pasta_list.append((row))

        self.lable_pd.config(text='Rice/Pasta')

        for i in range(0, len(t_id)):
            self.btn_pd[0][i].config(text=(t_id[i] + "\n" + t_name[i]),
                                     command=lambda i=i: self.add_pd_member(str(rice_pasta_list[i]), "rice_pasta"))

        for i in range(len(t_id), 45):
            self.btn_pd[0][i].config(text=("\n"), command='')

    def add_order_dessert_member(self):
        t_id = []
        t_name = []
        dessert_list = []
        cur = self.conn.cursor()
        cur.execute(
            "Select member_product.product_id, product.product_name from member_product inner join product on member_product.product_id = product.product_id where product.product_category = 'DESSERT' order by product.product_id")
        for row in cur.fetchall():
            t_id.append(row[0])
            t_name.append(row[1])
            dessert_list.append((row))

        self.lable_pd.config(text='Dessert')

        for i in range(0, len(t_id)):
            self.btn_pd[0][i].config(text=(t_id[i] + "\n" + t_name[i]),
                                     command=lambda i=i: self.add_pd_member(str(dessert_list[i]), "dessert"))

        for i in range(len(t_id), 45):
            self.btn_pd[0][i].config(text=("\n"), command='')

    def add_order_drink_option_member(self, choice):
        self.btnTR1.config(text='', command='', bg='grey20')

        self.btnTR2.config(text='', command='', bg='grey20')

        self.btnTR3.config(text='', command='', bg='grey20')

        self.btnTR4.config(text='', command='', bg='grey20')

        self.btnTR5.config(text='', command='', bg='grey20')

        self.btnTR6.config(text='', command='', bg='grey20')

        self.btnTR7.config(text='', command='', bg='grey20')

        self.btnTR8.config(text='', command='', bg='grey20')
        choice_id = choice[2:6]
        choice_name = choice[10:-2]
        # print(choice)

        member_point = []
        cur = self.conn.cursor()
        cur.execute(
            "Select membership_points from membership where member_id = '" + str(self.member_id) + "'")
        for row in cur.fetchall():
            member_point.append(row)

        print(str(member_point[0])[1:-2])
        print(choice_id)
        product_point = []
        cur = self.conn.cursor()
        cur.execute(
            "Select point from member_product where product_id = '" + str(choice_id) + "'")
        for row in cur.fetchall():
            product_point.append(row)

        if int(str(member_point[0])[1:-2]) >= int(str(product_point[0])[1:-2]):

            self.add_pd_list.append(choice)
            self.add_link_list.append('/')
            self.add_link_price_list.append('N')

            drink_option_list = []
            self.editAreaTable.insert(tk.INSERT, choice_id +" "+ choice_name + "\n")
            self.editAreaTable.see("end")
            cur = self.conn.cursor()
            cur.execute(
                "Select product_id, product_name from product where product_id like '400%' order by product_id")
            for row in cur.fetchall():
                drink_option_list.append(row)

            self.lable_pd.config(text='Drink')

            length_data = len(drink_option_list)

            for i in range(0, 45):
                self.btn_pd[0][i].config(text=" ", command='')

            for i in range(0, int(length_data)):
                t_id = str(drink_option_list[i])
                t_name = str(drink_option_list[i])
                self.btn_pd[0][i].config(text=(t_id[2:6] + "\n" + t_name[10:-2]),
                                         command=lambda i=i: self.add_pd_member(str(drink_option_list[i]), "drink"))

        else:
            self.editAreaTable.insert(tk.INSERT, '\nNot enough points')
            self.editAreaTable.see("end")

    def add_order_drink_member(self):
        '''
        when button clicked
        '''

        drink_list = []
        cur = self.conn.cursor()
        cur.execute(
            "Select member_product.product_id, product.product_name from member_product inner join product on member_product.product_id = product.product_id where product.product_category = 'DRINK' order by product.product_id")
        for row in cur.fetchall():
            drink_list.append(row)

        self.lable_pd.config(text='Drink')

        length_data = len(drink_list)
        for i in range(0, length_data):
            t_id = str(drink_list[i])
            t_name = str(drink_list[i])
            self.btn_pd[0][i].config(text=(t_id[2:6] + "\n" + t_name[10:-2]),
                                     command=lambda i=i: self.add_order_drink_option_member(str(drink_list[i])))

        for i in range(length_data, 45):
            self.btn_pd[0][i].config(text=("\n"), command='')

    def add_order_template(self,order_id,table_no,section):
        '''
        when button clicked
        '''

        print(table_no)
        print(order_id)


        self.left_frame.pack_forget()

        if section == "Add_pd":

            self.btnTR1.config(text='Starter',background="dark slate gray", command=lambda: self.add_order_starter(section))

            self.btnTR2.config(text='Pizza',background="dark slate gray", command=lambda: self.add_order_pizza(section))

            self.btnTR3.config(text='Pasta/Rice',background="dark slate gray", command=lambda: self.add_order_rice_pasta(section))

            self.btnTR4.config(text= "Dessert",background="dark slate gray", command=lambda: self.add_order_dessert(section))

            self.btnTR5.config(text="Drinks",background="dark slate gray", command=lambda: self.add_order_drink(section))

            self.btnTR6.config(text="Special", background="dark slate gray", command=lambda: self.add_order_special(section))

            self.btnTR7.config(text='Set',background="dark slate gray",command=lambda: self.add_order_set(section))

            self.btnTR8.config(text='Pizza Creator',background="dark slate gray", command=lambda: self.add_order_pizza_creator(section))


        elif section == "Add_pd_p_t" or section == "Add_pd_check":

            self.btnTR1.config(text='Starter',background="dark slate gray", command=lambda: self.add_order_starter(section))

            self.btnTR2.config(text='Pizza',background="dark slate gray", command=lambda: self.add_order_pizza(section))

            self.btnTR3.config(text='Pasta/Rice',background="dark slate gray", command=lambda: self.add_order_rice_pasta(section))

            self.btnTR4.config(text= "Dessert",background="dark slate gray", command=lambda: self.add_order_dessert(section))

            self.btnTR5.config(text="Drinks",background="dark slate gray", command=lambda: self.add_order_drink(section))

            self.btnTR6.config(text="Special", background="dark slate gray", command=lambda: self.add_order_special(section))

            self.btnTR7.config(text='Set',background="dark slate gray",command=lambda: self.add_order_set(section))

            self.btnTR8.config(text='',background="grey20", command='')


        elif section =='member' or section =='member_check' :

            self.btnTR1.config(text='Starter', background="dark slate gray", command=lambda: self.add_order_starter_member())

            self.btnTR2.config(text='Pizza', background="dark slate gray", command=lambda: self.add_order_pizza_member())

            self.btnTR3.config(text='Pasta/Rice', background="dark slate gray",command=lambda: self.add_order_rice_pasta_member())

            self.btnTR4.config(text="Dessert", background="dark slate gray", command=lambda: self.add_order_dessert_member())

            self.btnTR5.config(text="Drinks", background="dark slate gray", command=lambda: self.add_order_drink_member())

            self.btnTR6.config(text='', background="grey20", command='')

            self.btnTR7.config(text='', background="grey20", command='')

            self.btnTR8.config(text='', background="grey20", command='')


        if section == 'member' or section == "Add_pd":
            self.btnBack.config(command=lambda: self.last_page_tb("add_order", table_no))

        elif section == "Add_pd_p_t":
            self.btnBack.config(command=lambda: self.home_page("add_order"))

        elif section == "Add_pd_check" or section =="member_check":
            self.btnBack.config(command=lambda: self.check_page("add_order"))

        self.btnHome.config(command=lambda: self.home_page("add_order"))


        self.left_frame = Frame(self.root, background="black",
                                    borderwidth=5, relief="ridge",
                                    width=600)
        self.left_frame.pack(side="left",
                                 fill="both",
                                 expand="yes",
                                 )



        self.middle_frame = Frame(self.root, background="black",
                                    borderwidth=5, relief="ridge",
                                   )
        self.middle_frame.pack(side="left",
                                 fill="both",

                                 )

        self.frameL1 = tk.Frame(self.left_frame)
        self.frameL1.pack()
        self.frameL2 = tk.Frame(self.left_frame)
        self.frameL2.pack()
        self.frameL3 = tk.Frame(self.left_frame)
        self.frameL3.pack()
        self.frameL4 = tk.Frame(self.left_frame)
        self.frameL4.pack()
        self.frameL5 = tk.Frame(self.left_frame)
        self.frameL5.pack()
        self.frameL6 = tk.Frame(self.left_frame)
        self.frameL6.pack()
        self.frameL7 = tk.Frame(self.left_frame)
        self.frameL7.pack()
        self.frameL8 = tk.Frame(self.left_frame)
        self.frameL8.pack()
        self.frameL9 = tk.Frame(self.left_frame)
        self.frameL9.pack()
        self.frameL10 = tk.Frame(self.left_frame)
        self.frameL10.pack()
        self.frameL11 = tk.Frame(self.left_frame)
        self.frameL11.pack()

        self.lable_pd = tk.Label(self.frameL1, bg='black', text='',
                                 font=("Helvetica", 20, "bold "), fg="white", borderwidth=5)
        self.lable_pd.pack()



        self.btn_pd=[[0 for x in range(45)] for y in range(1)]
        for i in range(0,5):

            self.btn_pd[0][i]=tk.Button(self.frameL3, text=" ",font=("Helvetica", 10, "bold "),fg= "white",bg="grey20", width=20, height=4,command='')
            self.btn_pd[0][i].pack(side=tk.LEFT)

        for i in range(5,10):
            self.btn_pd[0][i] = tk.Button(self.frameL4, text=" ", font=("Helvetica", 10, "bold "),fg= "white",bg="grey20", width=20,
                                              height=4, command='')
            self.btn_pd[0][i].pack(side=tk.LEFT)
        for i in range(10,15):
            self.btn_pd[0][i] = tk.Button(self.frameL5, text=" ", font=("Helvetica", 10, "bold "),fg= "white",bg="grey20", width=20,
                                              height=4, command='')
            self.btn_pd[0][i].pack(side=tk.LEFT)
        for i in range(15,20):
            self.btn_pd[0][i] = tk.Button(self.frameL6, text=" ", font=("Helvetica", 10, "bold "),fg= "white",bg="grey20", width=20,
                                              height=4, command='')
            self.btn_pd[0][i].pack(side=tk.LEFT)
        for i in range(20,25):
            self.btn_pd[0][i] = tk.Button(self.frameL7, text=" ", font=("Helvetica", 10, "bold "),fg= "white",bg="grey20", width=20,
                                              height=4, command='')
            self.btn_pd[0][i].pack(side=tk.LEFT)
        for i in range(25,30):
            self.btn_pd[0][i] = tk.Button(self.frameL8, text=" ", font=("Helvetica", 10, "bold "),fg= "white",bg="grey20", width=20,
                                              height=4, command='')
            self.btn_pd[0][i].pack(side=tk.LEFT)
        for i in range(30,35):
            self.btn_pd[0][i] = tk.Button(self.frameL9, text=" ", font=("Helvetica", 10, "bold "),fg= "white",bg="grey20", width=20,
                                              height=4, command='')
            self.btn_pd[0][i].pack(side=tk.LEFT)
        for i in range(35,40):
            self.btn_pd[0][i] = tk.Button(self.frameL10, text=" ", font=("Helvetica", 10, "bold "),fg= "white",bg="grey20", width=20,
                                              height=4, command='')
            self.btn_pd[0][i].pack(side=tk.LEFT)
        for i in range(40, 45):
            self.btn_pd[0][i] = tk.Button(self.frameL11, text=" ", font=("Helvetica", 10, "bold "),fg= "white",bg="grey20", width=20,
                                              height=4, command='')
            self.btn_pd[0][i].pack(side=tk.LEFT)

        self.frameM1 = tk.Frame(self.middle_frame)
        self.frameM1.pack()

        if section == "Add_pd" or section == "Add_pd_p_t" or section == "Add_pd_check" :
            tk.Label(self.frameM1, bg='black', text='+Add Order - Table '+str(table_no),
                     font=("Helvetica", 20, "bold "), fg="white", borderwidth=5).pack()

        if section == "member"or section =='member_check' :
            tk.Label(self.frameM1, bg='black', text='+Member - Table '+str(table_no),
                     font=("Helvetica", 20, "bold "), fg="white", borderwidth=5).pack()


        self.frameM1 = tk.Frame(self.middle_frame)
        self.frameM1.pack()
        self.frameM2 = tk.Frame(self.middle_frame)
        self.frameM2.pack()
        self.frameM3 = tk.Frame(self.middle_frame)
        self.frameM3.pack()
        self.frameM4 = tk.Frame(self.middle_frame)
        self.frameM4.pack()
        self.frameM5 = tk.Frame(self.middle_frame)
        self.frameM5.pack()
        self.frameM6 = tk.Frame(self.middle_frame)
        self.frameM6.pack()
        self.frameM7 = tk.Frame(self.middle_frame)
        self.frameM7.pack()
        self.frameM8 = tk.Frame(self.middle_frame)
        self.frameM8.pack()
        self.frameM9 = tk.Frame(self.middle_frame)
        self.frameM9.pack()

        self.editAreaTable = tkst.ScrolledText(self.frameM1, height=8, width=40, background="black", fg="white",
                                                   font=("courier new", 15, "bold"))
        self.editAreaTable.pack(fill="both", expand="yes", side="left")

        self.editAreaTable2 = tkst.ScrolledText(self.frameM2, height=2, width=40, background="black", fg="white",
                                                   font=("courier new", 15, "bold"))
        self.editAreaTable2.pack(fill="both", expand="yes", side="left")

        tk.Button(self.frameM3, text="", font=("Helvetica", 20, "bold "), fg="white", bg="grey20", width=4, height=2,
                  command='').pack(
            side=tk.LEFT)
        tk.Button(self.frameM3, text="", font=("Helvetica", 20, "bold "), fg="white", bg="grey20", width=4, height=2,
                  command='').pack(
            side=tk.LEFT)
        tk.Button(self.frameM3, text="", font=("Helvetica", 20, "bold "),fg= "white",bg="grey20", width=4, height=2, command='').pack(
                side=tk.LEFT)
        tk.Button(self.frameM3, text="Finish", font=("Helvetica", 20, "bold "),fg= "white",bg="dark orange3", width=8, height=2, command=lambda: self.confirm_order(order_id,table_no,section)).pack(
                side=tk.LEFT)




        tk.Button(self.frameM5, text="7", font=("Helvetica", 20, "bold "),fg= "white",bg="slate blue", width=4, height=2, command=lambda: self.add_page_editarea("7")).pack(
                side=tk.LEFT)
        tk.Button(self.frameM5, text="8", font=("Helvetica", 20, "bold "),fg= "white",bg="slate blue", width=4, height=2, command=lambda: self.add_page_editarea("8")).pack(
                side=tk.LEFT)
        tk.Button(self.frameM5, text="9", font=("Helvetica", 20, "bold "),fg= "white",bg="slate blue", width=4, height=2, command=lambda: self.add_page_editarea("9")).pack(
                side=tk.LEFT)
        tk.Button(self.frameM5, text="<[X]", font=("Helvetica", 20, "bold "),fg= "white",bg="dark red", width=4, height=2, command=lambda: self.add_page_editarea("del")).pack(
                side=tk.LEFT)
        tk.Button(self.frameM5, text="", font=("Helvetica", 20, "bold "),fg= "white",bg="grey20", width=4, height=2, command='').pack(
                side=tk.LEFT)

        tk.Button(self.frameM6, text="4", font=("Helvetica", 20, "bold "),fg= "white",bg="slate blue", width=4, height=2, command=lambda: self.add_page_editarea("4")).pack(
                side=tk.LEFT)
        tk.Button(self.frameM6, text="5", font=("Helvetica", 20, "bold "),fg= "white",bg="slate blue", width=4, height=2, command=lambda: self.add_page_editarea("5")).pack(
                side=tk.LEFT)
        tk.Button(self.frameM6, text="6", font=("Helvetica", 20, "bold "),fg= "white",bg="slate blue", width=4, height=2, command=lambda: self.add_page_editarea("6")).pack(
                side=tk.LEFT)
        tk.Button(self.frameM6, text="", font=("Helvetica", 20, "bold "), fg="white", bg="grey20", width=4, height=2,
                  command='').pack(
            side=tk.LEFT)
        tk.Button(self.frameM6, text="", font=("Helvetica", 20, "bold "),fg= "white",bg="grey20", width=4, height=2, command='').pack(
                side=tk.LEFT)

        tk.Button(self.frameM7, text="1", font=("Helvetica", 20, "bold "),fg= "white",bg="slate blue", width=4, height=2, command=lambda: self.add_page_editarea("1")).pack(
                side=tk.LEFT)
        tk.Button(self.frameM7, text="2", font=("Helvetica", 20, "bold "),fg= "white",bg="slate blue", width=4, height=2, command=lambda: self.add_page_editarea("2")).pack(
                side=tk.LEFT)
        tk.Button(self.frameM7, text="3", font=("Helvetica", 20, "bold "),fg= "white",bg="slate blue", width=4, height=2, command=lambda: self.add_page_editarea("3")).pack(
                side=tk.LEFT)
        tk.Button(self.frameM7, text="", font=("Helvetica", 20, "bold "),fg= "white",bg="grey20", width=4, height=2, command='').pack(
                side=tk.LEFT)
        tk.Button(self.frameM7, text="", font=("Helvetica", 20, "bold "),fg= "white",bg="grey20", width=4, height=2, command='').pack(
                side=tk.LEFT)

        tk.Button(self.frameM8, text="0", font=("Helvetica", 20, "bold "),fg= "white",bg="slate blue", width=4, height=2, command=lambda: self.add_page_editarea("0")).pack(
                side=tk.LEFT)
        tk.Button(self.frameM8, text="", font=("Helvetica", 20, "bold "),fg= "white",bg="slate blue", width=4, height=2, command='').pack(
                side=tk.LEFT)
        tk.Button(self.frameM8, text="", font=("Helvetica", 20, "bold "),fg= "white",bg="slate blue", width=4, height=2, command='').pack(
                side=tk.LEFT)
        if section == "Add_pd" or section == "Add_pd_p_t" or section == "Add_pd_check":
            tk.Button(self.frameM8, text="+Add", font=("Helvetica", 20, "bold "),fg="white",bg="dark green", width=8, height=2, command=lambda: self.add_to_cart("pizza",section)).pack(
                side=tk.LEFT)
        elif section == "member"or section =='member_check' :
            tk.Button(self.frameM8, text="+Add", font=("Helvetica", 20, "bold "), fg="white", bg="dark green", width=8,
                      height=2,command=lambda: self.add_to_cart_member("pizza")).pack(
                side=tk.LEFT)

        if section == "Add_pd" or section == "Add_pd_p_t" or section == "Add_pd_check":
            self.add_order_pizza(section)
        elif section == 'member'or section =='member_check' :
            self.add_order_pizza_member()


    def del_page_editarea(self, choice):
        if choice == "del":
            self.del_list = self.del_list[:-1]
            self.editAreaTable3.delete("1.0", END)
            self.editAreaTable3.insert(tk.INSERT, self.del_list)

        elif choice == "Clear":
            pass
        else:
            self.del_list += choice
            self.editAreaTable3.insert(tk.INSERT, choice)
            self.editAreaTable3.see("end")

    def delete_from_order(self, order_id):
        if self.del_pd_id == '':
            cur = self.conn.cursor()
            cur.execute("select  * from order_product where order_id = {0} order by order_product_id".format(str(order_id[0][0])))
            found = False
            for row in cur.fetchall():
                if str(self.editAreaTable3.get("1.0", END)[0:-1]) == str(row[5]):
                    found = True
                else:
                    pass

            if not found:
                self.editAreaTable2.insert(tk.INSERT, self.del_pd_id)
                self.editAreaTable2.insert(tk.INSERT, '\nNot Found. Try Again:')
                self.editAreaTable3.delete("1.0", END)
                self.editAreaTable3.see("end")
                self.del_list=''
            else:
                self.del_pd_id = self.editAreaTable3.get("1.0", END)
                self.editAreaTable2.insert(tk.INSERT, self.del_pd_id)
                self.editAreaTable3.delete("1.0", END)
                self.editAreaTable3.see("end")
                self.del_list=''
        else:
            self.del_pd_qty = self.editAreaTable3.get("1.0", END)
            self.editAreaTable2.insert(tk.INSERT, self.del_pd_qty)
            self.editAreaTable3.delete("1.0", END)
            self.editAreaTable3.see("end")
            self.del_list=''

        if self.del_pd_id != '' and self.del_pd_qty == '':
            self.editAreaTable2.insert(tk.INSERT, 'Quantity:')

        if self.del_pd_id != '' and self.del_pd_qty != '':
            link=False
            cur = self.conn.cursor()
            sql = (
                "update order_product set quantity=((select quantity from order_product where order_product_id={0})-{1})  where order_product_id={0} or link_product=(select link_product from order_product where order_product_id={0})").format(
                str(self.del_pd_id[0:-1]), int(self.del_pd_qty[0:-1]))

            self.cur.execute(sql)
            cur.execute('DELETE FROM order_product WHERE quantity<=0')
            self.cur.execute('commit')
            self.editAreaTable2.insert(tk.INSERT, 'Done!')
            self.editAreaTable2.insert(tk.INSERT, '\n')
            self.editAreaTable2.insert(tk.INSERT, 'Other id to delete:')
            self.del_pd_id = ''
            self.del_pd_qty = ''

            order_item = []
            order_created_time = []
            order_product_id = []
            product_id = []
            product_name = []
            order_time = []
            order_quantity = []
            order_price = []
            order_link = []

            self.editAreaTable.config(state="normal")
            self.editAreaTable.delete("1.0", END)
            cur = self.conn.cursor()
            cur.execute("select  * from order_product where order_id = {0}".format(str(order_id[0][0])))
            for row in cur.fetchall():
                order_item.append(row)



            if order_item == []:
                self.editAreaTable.insert(tk.INSERT, "No product is ordered")
            else:
                self.editAreaTable.insert(tk.INSERT, "Order id: ")
                self.editAreaTable.insert(tk.INSERT, order_id)



                cur = self.conn.cursor()
                cur.execute("select order_product_id from order_product where order_id = " + str(order_id[0])[
                                                                                             1:-2] + " order by order_product_id")
                for row in cur.fetchall():
                    order_product_id.append(row)

                cur = self.conn.cursor()
                cur.execute("select  product_id from order_product where order_id = " + str(order_id[0])[
                                                                                        1:-2] + " order by order_product_id")
                for row in cur.fetchall():
                    product_id.append(row)

                cur = self.conn.cursor()
                cur.execute(
                    "select  product.product_name from order_product inner join product on product.product_id = order_product.product_id where order_id = " + str(
                        order_id[0])[
                                                                                                                                                              1:-2] + " order by order_product_id")
                for row in cur.fetchall():
                    product_name.append(row)

                cur = self.conn.cursor()
                cur.execute("select  quantity from order_product where order_id = " + str(order_id[0])[
                                                                                      1:-2] + " order by order_product_id")
                for row in cur.fetchall():
                    order_quantity.append(row)

                cur = self.conn.cursor()
                cur.execute("select  price from order_product where order_id = " + str(order_id[0])[
                                                                                   1:-2] + " order by order_product_id")
                for row in cur.fetchall():
                    order_price.append(row)

                cur = self.conn.cursor()
                cur.execute("select  link_product from order_product where order_id = " + str(order_id[0])[
                                                                                          1:-2] + " order by order_product_id")
                for row in cur.fetchall():
                    order_link.append(row)

                self.editAreaTable.insert(tk.INSERT,
                                          "\n\n" + '%-8s  %-5s  %-30s  %3s  %5s' % (
                                              "O_PID", "PID", "Name", "Qty", "$/1"))

                total_price = 0
                for e in range(0, len(order_price)):
                    total_price += (float(order_price[e][0]) * float(order_quantity[e][0]))

                for i in range(0, len(order_product_id)):
                    if str(order_link[i])[2:-3] == str(order_product_id[i])[1:-2]:
                        self.editAreaTable.insert(tk.INSERT,
                                                  "\n" + '%-8s  %-5s  %-30s  %3s  %5s' % (
                                                      str(order_product_id[i])[1:-2], str(product_id[i])[2:-3], str(
                                                          product_name[i])[2:-3], str(order_quantity[i])[1:-2], str(
                                                          order_price[i])[1:-2]))
                    else:
                        self.editAreaTable.insert(tk.INSERT,
                                                  "\n" + '%-8s  %-5s  %-30s  %3s  %5s' % (
                                                      '', " " + str(product_id[i])[2:-3], " " + str(
                                                          product_name[i])[2:-3], str(order_quantity[i])[1:-2], str(
                                                          order_price[i])[1:-2]))

                self.editAreaTable.insert(tk.INSERT, "\n\n\n" + '%-46s  %5s' % ('', 'Total : ' + str(total_price)))

            self.editAreaTable.config(state="disabled")

        pass

    def del_order_template(self, order_id, table_no, section):
        '''
        when button clicked
        '''
        self.left_frame.pack_forget()
        self.del_list=''
        self.del_pd_id = ''
        self.del_pd_qty = ''

        if section == "del_pd" or section == "del_check" :
            self.btnTR1.config(text='', command='',bg='grey20')

            self.btnTR2.config(text='', command='',bg='grey20')

            self.btnTR3.config(text='', command='',bg='grey20')

            self.btnTR4.config(text='', command='',bg='grey20')

            self.btnTR5.config(text='', command='',bg='grey20')

            self.btnTR6.config(text='', command='',bg='grey20')

            self.btnTR7.config(text='', command='',bg='grey20')

            self.btnTR8.config(text='', command='',bg='grey20')


        if section == "del_pd":
            self.btnBack.config(command=lambda: self.last_page_tb("del_order", table_no))
        elif section == "del_check":
            self.btnBack.config(command=lambda: self.check_page("add_order"))

        self.btnHome.config(command=lambda: self.home_page("del_order"))

        self.left_frame = Frame(self.root, background="black",
                                borderwidth=5, relief="ridge",
                                width=600)
        self.left_frame.pack(side="left",
                             fill="both",
                             expand="yes",
                             )

        self.middle_frame = Frame(self.root, width=20, background="black",
                                  borderwidth=5, relief="ridge",
                                  )
        self.middle_frame.pack(side="left",
                               fill="both",

                               )
        self.editAreaTable = tkst.ScrolledText(self.left_frame, height=8, width=69, background="black", fg="white",
                                               font=("courier new", 15, "bold"))
        self.editAreaTable.pack(fill="both", expand="yes", side="left")

        order_item = []
        order_created_time = []
        order_product_id = []
        product_id = []
        product_name = []
        order_time = []
        order_quantity = []
        order_price = []
        order_link = []

        if order_id == []:
            self.editAreaTable.insert(tk.INSERT, "There is no order")
        else:
            cur = self.conn.cursor()
            cur.execute("select  * from order_product where order_id = {0}".format(str(order_id[0][0])))
            for row in cur.fetchall():
                order_item.append(row)


            if order_item == []:
                self.editAreaTable.insert(tk.INSERT, "No product is ordered")
            else:
                self.editAreaTable.insert(tk.INSERT, "Order id: ")
                self.editAreaTable.insert(tk.INSERT, order_id)


                cur = self.conn.cursor()
                cur.execute("select order_product_id from order_product where order_id = " + str(order_id[0])[
                                                                                             1:-2] + " order by order_product_id")
                for row in cur.fetchall():
                    order_product_id.append(row)

                cur = self.conn.cursor()
                cur.execute("select  product_id from order_product where order_id = " + str(order_id[0])[
                                                                                        1:-2] + " order by order_product_id")
                for row in cur.fetchall():
                    product_id.append(row)

                cur = self.conn.cursor()
                cur.execute(
                    "select  product.product_name from order_product inner join product on product.product_id = order_product.product_id where order_id = " + str(
                        order_id[0])[
                                                                                                                                                              1:-2] + " order by order_product_id")
                for row in cur.fetchall():
                    product_name.append(row)

                cur = self.conn.cursor()
                cur.execute("select  quantity from order_product where order_id = " + str(order_id[0])[
                                                                                      1:-2] + " order by order_product_id")
                for row in cur.fetchall():
                    order_quantity.append(row)

                cur = self.conn.cursor()
                cur.execute("select  price from order_product where order_id = " + str(order_id[0])[
                                                                                   1:-2] + " order by order_product_id")
                for row in cur.fetchall():
                    order_price.append(row)

                cur = self.conn.cursor()
                cur.execute("select  link_product from order_product where order_id = " + str(order_id[0])[
                                                                                          1:-2] + " order by order_product_id")
                for row in cur.fetchall():
                    order_link.append(row)


                self.editAreaTable.insert(tk.INSERT,
                                          "\n\n" + '%-8s  %-5s  %-30s  %3s  %5s' % (
                                          "O_PID", "PID", "Name", "Qty", "$/1"))

                total_price = 0
                for e in range(0, len(order_price)):
                    total_price += (float(order_price[e][0]) * float(order_quantity[e][0]))

                for i in range(0, len(order_product_id)):
                    if str(order_link[i])[2:-3] == str(order_product_id[i])[1:-2]:
                        self.editAreaTable.insert(tk.INSERT,
                                                  "\n" + '%-8s  %-5s  %-30s  %3s  %5s' % (
                                                  str(order_product_id[i])[1:-2], str(product_id[i])[2:-3], str(
                                                      product_name[i])[2:-3], str(order_quantity[i])[1:-2], str(
                                                      order_price[i])[1:-2]))
                    else:
                        self.editAreaTable.insert(tk.INSERT,
                                                  "\n" + '%-8s  %-5s  %-30s  %3s  %5s' % (
                                                      '', " " + str(product_id[i])[2:-3], " " + str(
                                                          product_name[i])[2:-3], str(order_quantity[i])[1:-2], str(
                                                          order_price[i])[1:-2]))

                self.editAreaTable.insert(tk.INSERT, "\n\n\n" + '%-46s  %5s' % ('', 'Total : ' + str(total_price)))

        self.editAreaTable.config(state="disabled")

        self.frameM1 = tk.Frame(self.middle_frame)
        self.frameM1.pack()

        if section == "del_pd" or section == "del_check":
            tk.Label(self.frameM1, bg='black', text='-Delete Order - Table ' + str(table_no),
                     font=("Helvetica", 20, "bold "), fg="white", borderwidth=5).pack()

        self.frameM1 = tk.Frame(self.middle_frame)
        self.frameM1.pack()
        self.frameM2 = tk.Frame(self.middle_frame)
        self.frameM2.pack()
        self.frameM3 = tk.Frame(self.middle_frame)
        self.frameM3.pack()
        self.frameM4 = tk.Frame(self.middle_frame)
        self.frameM4.pack()
        self.frameM5 = tk.Frame(self.middle_frame)
        self.frameM5.pack()
        self.frameM6 = tk.Frame(self.middle_frame)
        self.frameM6.pack()
        self.frameM7 = tk.Frame(self.middle_frame)
        self.frameM7.pack()
        self.frameM8 = tk.Frame(self.middle_frame)
        self.frameM8.pack()
        self.frameM9 = tk.Frame(self.middle_frame)
        self.frameM9.pack()

        self.editAreaTable2 = tkst.ScrolledText(self.frameM1, height=10, width=40, background="black", fg="white",
                                                font=("courier new", 15, "bold"))
        self.editAreaTable2.pack(fill="both", expand="yes", side="left")

        self.editAreaTable3 = tkst.ScrolledText(self.frameM2, height=2, width=40, background="black", fg="white",
                                                font=("courier new", 15, "bold"))
        self.editAreaTable3.pack(fill="both", expand="yes", side="left")



        tk.Button(self.frameM5, text="7", font=("Helvetica", 20, "bold "), fg="white", bg="slate blue", width=4,
                  height=2, command=lambda: self.del_page_editarea("7")).pack(
            side=tk.LEFT)
        tk.Button(self.frameM5, text="8", font=("Helvetica", 20, "bold "), fg="white", bg="slate blue", width=4,
                  height=2, command=lambda: self.del_page_editarea("8")).pack(
            side=tk.LEFT)
        tk.Button(self.frameM5, text="9", font=("Helvetica", 20, "bold "), fg="white", bg="slate blue", width=4,
                  height=2, command=lambda: self.del_page_editarea("9")).pack(
            side=tk.LEFT)
        tk.Button(self.frameM5, text="<[X]", font=("Helvetica", 20, "bold "), fg="white", bg="dark red", width=4,
                  height=2, command=lambda: self.del_page_editarea("del")).pack(
            side=tk.LEFT)
        tk.Button(self.frameM5, text="", font=("Helvetica", 20, "bold "),fg= "white",bg="grey20", width=4, height=2, command='').pack(
            side=tk.LEFT)

        tk.Button(self.frameM6, text="4", font=("Helvetica", 20, "bold "), fg="white", bg="slate blue", width=4,
                  height=2, command=lambda: self.del_page_editarea("4")).pack(
            side=tk.LEFT)
        tk.Button(self.frameM6, text="5", font=("Helvetica", 20, "bold "), fg="white", bg="slate blue", width=4,
                  height=2, command=lambda: self.del_page_editarea("5")).pack(
            side=tk.LEFT)
        tk.Button(self.frameM6, text="6", font=("Helvetica", 20, "bold "), fg="white", bg="slate blue", width=4,
                  height=2, command=lambda: self.del_page_editarea("6")).pack(
            side=tk.LEFT)
        tk.Button(self.frameM6, text="", font=("Helvetica", 20, "bold "), fg="white", bg="grey20", width=4, height=2,
                  command='').pack(
            side=tk.LEFT)
        tk.Button(self.frameM6, text="", font=("Helvetica", 20, "bold "),fg= "white",bg="grey20", width=4, height=2, command='').pack(
            side=tk.LEFT)

        tk.Button(self.frameM7, text="1", font=("Helvetica", 20, "bold "), fg="white", bg="slate blue", width=4,
                  height=2, command=lambda: self.del_page_editarea("1")).pack(
            side=tk.LEFT)
        tk.Button(self.frameM7, text="2", font=("Helvetica", 20, "bold "), fg="white", bg="slate blue", width=4,
                  height=2, command=lambda: self.del_page_editarea("2")).pack(
            side=tk.LEFT)
        tk.Button(self.frameM7, text="3", font=("Helvetica", 20, "bold "), fg="white", bg="slate blue", width=4,
                  height=2, command=lambda: self.del_page_editarea("3")).pack(
            side=tk.LEFT)
        tk.Button(self.frameM7, text="", font=("Helvetica", 20, "bold "),fg= "white",bg="grey20", width=4, height=2, command='').pack(
            side=tk.LEFT)
        tk.Button(self.frameM7, text="", font=("Helvetica", 20, "bold "),fg= "white",bg="grey20", width=4, height=2, command='').pack(
            side=tk.LEFT)
        tk.Button(self.frameM8, text="0", font=("Helvetica", 20, "bold "), fg="white", bg="slate blue", width=4,
                  height=2, command=lambda: self.del_page_editarea("0")).pack(
            side=tk.LEFT)
        tk.Button(self.frameM8, text="", font=("Helvetica", 20, "bold "), fg="white", bg="slate blue", width=4,
                  height=2, command='').pack(
            side=tk.LEFT)
        tk.Button(self.frameM8, text="", font=("Helvetica", 20, "bold "), fg="white", bg="slate blue", width=4,
                  height=2, command='').pack(
            side=tk.LEFT)

        if section == "del_pd" or section == "del_check":
            tk.Button(self.frameM8, text="-Delete", font=("Helvetica", 20, "bold "), fg="white", bg="dark green",
                      width=8, height=2, command=lambda: self.delete_from_order(order_id)).pack(
                side=tk.LEFT)

        self.editAreaTable2.insert(tk.INSERT, 'Input Order_product_id to delete: ')


    def set_table(self,table_id):

        table_current=[]
        cur = self.conn.cursor()
        cur.execute("select count(table_id) from order_ where table_id = '" + table_id + "' and order_status = 0")
        for row in cur.fetchall():
            table_current.append(row)
        if (int(str(table_current)[2:-3])) == 0:
            latest_order_no = []
            new_order_id=0
            cur = self.conn.cursor()
            cur.execute("select max(order_id) from order_ ")
            for row in cur.fetchall():
                latest_order_no.append(row)

            #print(str(latest_order_no[0])[1:-2])
            if str(latest_order_no[0]) != '(None,)':
                new_order_id=int(str(latest_order_no[0])[1:-2])+1
            else:
                new_order_id=1

            sql= ("insert into order_ (order_id,order_date_time,order_status,shop_id,table_id) values ("+str( new_order_id)+" ,sysdate,'0','"+str(self.id)+"','"+str(table_id)+"')")
            self.cur.execute(sql)
            self.editAreaTable.delete("1.0", END)
            self.cur.execute('commit')

            self.last_page_tb("set_tb",int(str(table_id[6:])))

    def checkout(self,order_id,table_id):

        sql = ("Update order_ set order_status = 1 where order_id = '"+str(order_id)[2:-3]+"'")
        self.cur.execute(sql)

        self.cur.execute('commit')
        self.last_page_tb("set_tb", int(str(table_id[6:])))

    def transition_switch_tb(self,order_id,table_id):
        self.left_frame.pack_forget()
        self.main_page(2,order_id,table_id)

    def table_sub(self,table_id, number):
        '''
        when button clicked
        '''

        if number in range( 0,121):
            self.table_id_nm=table_id
            self.left_frame.pack_forget()


            self.left_frame = Frame(self.root, background="black",
                                    borderwidth=5, relief="ridge",
                                    width=1000)
            self.left_frame.pack(side="left",
                                 fill="both",
                                 expand="yes",
                                 )


            self.frameL1 = tk.Frame(self.left_frame)
            self.frameL1.pack()

            self.frameL2 = tk.Frame(self.left_frame)
            self.frameL2.pack()

            tk.Label(self.frameL1, bg='black', text=('Table '+str(number)),
                     font=("Helvetica", 20, "bold "), fg="white", borderwidth=5).pack()

            order_id= []
            order_created_time=[]
            order_item=[]
            order_product_id=[]
            product_id=[]
            product_name=[]
            order_time=[]
            order_quantity=[]
            order_price=[]
            order_link=[]
            cur = self.conn.cursor()
            cur.execute("select order_id from order_ where table_id = '"+table_id+"' and order_status = '0'")

            for row in cur.fetchall():
                order_id.append(row)


            cur = self.conn.cursor()
            cur.execute("select  order_date_time from order_ where table_id = '" + table_id + "' and order_status = 0")
            for row in cur.fetchall():
                order_created_time.append(row)

            self.editAreaTable2 = tkst.ScrolledText(self.frameL2, height=1, width=100, background="black", fg="white",
                                                    font=("courier new", 15, "bold"))
            self.editAreaTable2.pack(fill="both")
            self.editAreaTable2.delete("1.0", END)

            self.editAreaTable = tkst.ScrolledText(self.frameL2, height=50,width=100, background="black" ,fg="white",font=("courier new",15, "bold"))
            self.editAreaTable.pack(fill="both")
            self.editAreaTable.delete("1.0", END)

            if order_id == []:
                max_seat=[]
                cur = self.conn.cursor()
                cur.execute(
                    "select  max_seat_available from table_ where table_id = '" + table_id + "'")
                for row in cur.fetchall():
                    max_seat.append(row)
                self.editAreaTable.insert(tk.INSERT,  "Please set table")
                self.editAreaTable.insert(tk.INSERT, "\nMax seat: "+str(max_seat[0])[1:-2])

                self.btnTR1.config(text='Set Table', font=("Helvetica", 20, "bold "), bg="royalblue3",
                                   command=lambda: self.set_table(table_id))
                self.btnTR2.config(text='', font=("Helvetica", 20, "bold "), bg="grey20")
                self.btnTR3.config(text='', font=("Helvetica", 20, "bold "), bg="grey20")
                self.btnTR4.config(text='', font=("Helvetica", 20, "bold "), bg="grey20")
                self.btnTR5.config(text='', font=("Helvetica", 20, "bold "), bg="grey20")
                self.btnTR6.config(text='', font=("Helvetica", 20, "bold "), bg="grey20")
                self.btnTR7.config(text='', font=("Helvetica", 20, "bold "), bg="grey20")
                self.btnTR8.config(text='', font=("Helvetica", 20, "bold "), bg="grey20")

            else:

                cur = self.conn.cursor()
                cur.execute("select order_product_id from order_product where order_id = " + str(order_id[0])[1:-2] + " order by order_product_id")
                for row in cur.fetchall():
                    order_product_id.append(row)

                cur = self.conn.cursor()
                cur.execute("select  product_id from order_product where order_id = " + str(order_id[0])[
                                                                               1:-2] + " order by order_product_id")
                for row in cur.fetchall():
                    product_id.append(row)

                cur = self.conn.cursor()
                cur.execute("select  product.product_name from order_product inner join product on product.product_id = order_product.product_id where order_id = " + str(order_id[0])[
                                                                               1:-2] + " order by order_product_id")
                for row in cur.fetchall():
                    product_name.append(row)

                cur = self.conn.cursor()
                cur.execute("select  quantity from order_product where order_id = " + str(order_id[0])[
                                                                                        1:-2] + " order by order_product_id")
                for row in cur.fetchall():
                    order_quantity.append(row)

                cur = self.conn.cursor()
                cur.execute("select  price from order_product where order_id = " + str(order_id[0])[
                                                                                        1:-2] + " order by order_product_id")
                for row in cur.fetchall():
                    order_price.append(row)

                cur = self.conn.cursor()
                cur.execute(
                    "select  to_char(order_date,'DD-MM-YYYY HH24:SS:MM') from order_product where order_id = " + str(
                        order_id[0])[
                                                                                                                 1:-2] + " order by order_product_id")
                for row in cur.fetchall():
                    order_time.append(row)

                cur = self.conn.cursor()
                cur.execute( "select  link_product from order_product where order_id = " + str(order_id[0])[1:-2] + " order by order_product_id")
                for row in cur.fetchall():
                    order_link.append(row)

                total_price = 0
                for e in range(0,len(order_price)):
                    total_price += (float(order_price[e][0])*float(order_quantity[e][0]))

                self.editAreaTable.insert(tk.INSERT, "Order id: ")
                self.editAreaTable.insert(tk.INSERT, order_id)
                self.editAreaTable.insert(tk.INSERT, "\n"+"Order time created: ")
                self.editAreaTable.insert(tk.INSERT, order_created_time)

                self.editAreaTable.insert(tk.INSERT,
                                          "\n\n"+'%-8s  %-5s  %-30s  %3s  %5s  %-20s'%("O_PID", "PID", "Name", "Qty", "$/1", "Date&Time")  )



                for i in range(0,len(order_product_id)):
                    if str(order_link[i])[2:-3] == str(order_product_id[i])[1:-2]:
                        self.editAreaTable.insert(tk.INSERT,
                                        "\n" + '%-8s  %-5s  %-30s  %3s  %5s  %-20s' %(str(order_product_id[i])[1:-2], str(product_id[i])[2:-3], str(
                                            product_name[i])[2:-3], str(order_quantity[i])[1:-2], str(
                                            order_price[i])[1:-2], str(order_time[i])[2:-3]))
                    else:
                        self.editAreaTable.insert(tk.INSERT,
                                                  "\n" + '%-8s  %-5s  %-30s  %3s  %5s  %-20s' % (
                                                  '', " "+str(product_id[i])[2:-3], " "+str(
                                                      product_name[i])[2:-3], str(order_quantity[i])[1:-2], str(
                                                      order_price[i])[1:-2], str(order_time[i])[2:-3]))

                self.editAreaTable.insert(tk.INSERT,"\n\n\n" + '%-46s  %5s' % ('', 'Total : ' + str(total_price)))

                self.btnTR1.config(text='', font=("Helvetica", 20, "bold "), bg="grey20")

                self.btnTR2.config(text='Switch Table', bg="deepskyblue3",
                                   command=lambda: self.transition_switch_tb(order_id, table_id))

                self.btnTR3.config(text='+Add Order', font=("Helvetica", 20, "bold "), bg="forest green",
                                   command=lambda: self.add_order_template(order_id, number, "Add_pd"))

                self.btnTR4.config(text='+Member', font=("Helvetica", 20, "bold "), bg="chartreuse4",
                                   command=lambda: self.member_page(order_id, number,"table_sub"))

                self.btnTR5.config(text='-Delete Order', font=("Helvetica", 20, "bold "), bg="orangered3",
                                   command=lambda: self.del_order_template(order_id, number, "del_pd"))

                self.btnTR6.config(text='', font=("Helvetica", 20, "bold "), bg="grey20")

                self.btnTR7.config(text='Checkout', font=("Helvetica", 20, "bold "), bg="firebrick3",
                                   command=lambda: self.checkout(order_id, table_id))

                self.btnTR8.config(text='Export', bg="darkorange3",
                                   command=lambda: self.export("order", str(order_id[0])[1:-2]))

            self.editAreaTable.config(state="disabled")



            self.btnBack.config( command=lambda: self.last_page("table_sub"))
            self.btnHome.config(command=lambda: self.home_page("table_sub"))


    def address_page_editarea(self,choice):

        if choice == "del" and self.address_list != "":

            self.address_list = self.address_list[:-1]
            self.editAreaAddress2.delete("1.0", END)
            self.editAreaAddress2.insert(tk.INSERT, self.address_list)

        else :
            self.address_list+=choice
            self.editAreaAddress2.insert(tk.INSERT, choice)

    def member_verify (self,order_id,number,section):
        self.editAreaAddress2.delete("1.0", END)

        self.delivery_list.append(self.address_list)
        self.address_list = ''
        self.editAreaAddress.delete("1.0", END)
        print(str(self.delivery_list[1]))

        phone_number_list=[]

        cur = self.conn.cursor()
        cur.execute("Select phone_number from membership where member_id = '"+str(self.delivery_list[0])+"'")
        for row in cur.fetchall():
            phone_number_list.append(row)

        if str(phone_number_list[0])[2:-3] == str(self.delivery_list[1]):
            self.member_id = str(self.delivery_list[0])
            if section == "table_sub":
                self.add_order_template(order_id,number,'member')
            elif section == "check_deli":
                self.add_order_template(order_id, number, 'member_check')
        else:
            self.editAreaAddress.insert(tk.INSERT, 'Not found')

    def member_phone(self,order_id,number,section):

        self.editAreaAddress2.delete("1.0", END)

        self.delivery_list.append(self.address_list)
        self.address_list = ''
        self.editAreaAddress.delete("1.0", END)
        self.editAreaAddress.insert(tk.INSERT, 'Member id: ')
        self.editAreaAddress.insert(tk.INSERT, self.delivery_list[0])

        self.editAreaAddress.insert(tk.INSERT, '\n' + 'Input Phone Number:')
        self.btn_ap_enter.config(command=lambda: self.member_verify(order_id,number,section))

    def member_page(self,order_id,number,section):
        self.address_list = ''
        self.delivery_list=[]
        #print(order_id)
        self.left_frame.pack_forget()
        self.left_frame = Frame(self.root, background="black",
                                borderwidth=5, relief="ridge",
                                width=600)
        self.left_frame.pack(side="left",
                             fill="both",
                             expand="yes",
                             )

        self.frameL1 = tk.Frame(self.left_frame)
        self.frameL1.pack()
        self.frameL2 = tk.Frame(self.left_frame)
        self.frameL2.pack()
        self.frameL3 = tk.Frame(self.left_frame)
        self.frameL3.pack()
        self.frameL4 = tk.Frame(self.left_frame)
        self.frameL4.pack()
        self.frameL5 = tk.Frame(self.left_frame)
        self.frameL5.pack()
        self.frameL6 = tk.Frame(self.left_frame)
        self.frameL6.pack()
        self.frameL7 = tk.Frame(self.left_frame)
        self.frameL7.pack()

        if section == "table_sub":
            self.btnBack.config(command=lambda: self.last_page_tb("set_tb",number))
        elif section == "check_deli":
            self.btnBack.config(command=lambda: self.check_page("add_order"))
        self.editAreaAddress = tkst.ScrolledText(self.frameL1, height=7, background="black", fg="white",
                                                 font=("courier new", 15, "bold"))
        self.editAreaAddress.pack(fill="both", expand="yes", side="left")

        self.editAreaAddress.insert(tk.INSERT, 'Input member id::')

        self.editAreaAddress2 = tkst.ScrolledText(self.frameL2, height=5, background="black", fg="white",
                                                  font=("courier new", 15, "bold"))
        self.editAreaAddress2.pack(fill="both", expand="yes", side="left")

        keyboardlist = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O',
                        'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', "'", 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',',
                        '/']

        self.btn_ap = [[0 for x in range(121)] for y in range(1)]
        for i in range(0, 10):
            self.btn_ap[0][i] = tk.Button(self.frameL3, text=keyboardlist[i], font=("Helvetica", 20, "bold "),
                                          fg="white", bg="grey20", width=4, height=2,
                                          command=lambda i=i: self.address_page_editarea(keyboardlist[i]))
            self.btn_ap[0][i].pack(side=tk.LEFT)
        self.btn_ap_bk = tk.Button(self.frameL3, text='<[X]', font=("Helvetica", 20, "bold "), fg="white",
                                   bg="dark red", width=6,
                                   height=2,
                                   command=lambda: self.address_page_editarea("del"))
        self.btn_ap_bk.pack(side=tk.LEFT)
        for i in range(10, 20):
            self.btn_ap[0][i] = tk.Button(self.frameL4, text=keyboardlist[i], font=("Helvetica", 20, "bold "),
                                          fg="white", bg="grey20", width=4, height=2,
                                          command=lambda i=i: self.address_page_editarea(keyboardlist[i]))
            self.btn_ap[0][i].pack(side=tk.LEFT)

        for i in range(20, 30):
            self.btn_ap[0][i] = tk.Button(self.frameL5, text=keyboardlist[i], font=("Helvetica", 20, "bold "),
                                          fg="white", bg="grey20", width=4, height=2,
                                          command=lambda i=i: self.address_page_editarea(keyboardlist[i]))
            self.btn_ap[0][i].pack(side=tk.LEFT)

        for i in range(30, 39):
            self.btn_ap[0][i] = tk.Button(self.frameL6, text=keyboardlist[i], font=("Helvetica", 20, "bold "),
                                          fg="white", bg="grey20", width=4, height=2,
                                          command=lambda i=i: self.address_page_editarea(keyboardlist[i]))
            self.btn_ap[0][i].pack(side=tk.LEFT)

        self.btn_ap_space = tk.Button(self.frameL7, text='Spacebar', font=("Helvetica", 20, "bold "), fg="white",
                                      bg="grey20", width=40, height=2,
                                      command=lambda: self.address_page_editarea(' '))
        self.btn_ap_space.pack(side=tk.LEFT)

        self.btn_ap_enter = tk.Button(self.frameL7, text='ENTER', font=("Helvetica", 20, "bold "), fg="white",
                                      bg="dark orange3", width=6,
                                      height=2,
                                      command='')
        self.btn_ap_enter.pack(side=tk.LEFT)

        self.btn_ap_enter.config(command=lambda: self.member_phone(order_id,number,section))

        self.btnTR1.config(text='', font=("Helvetica", 20, "bold "), bg="grey20", command='')
        self.btnTR2.config(text='', font=("Helvetica", 20, "bold "), bg="grey20", command='')
        self.btnTR3.config(text='', font=("Helvetica", 20, "bold "), bg="grey20", command='')
        self.btnTR4.config(text='', font=("Helvetica", 20, "bold "), bg="grey20", command='')
        self.btnTR5.config(text='', font=("Helvetica", 20, "bold "), bg="grey20", command='')
        self.btnTR6.config(text='', font=("Helvetica", 20, "bold "), bg="grey20", command='')
        self.btnTR7.config(text='', font=("Helvetica", 20, "bold "), bg="grey20", command='')
        self.btnTR8.config(text='', font=("Helvetica", 20, "bold "), bg="grey20", command='')


    def delivery_set_table(self):
        self.delivery_list.append(self.address_list)
        self.address_list = ''
        latest_order_no = []
        new_order_id = 0
        cur = self.conn.cursor()
        cur.execute("select max(order_id) from order_ ")
        for row in cur.fetchall():
            latest_order_no.append(row)

        #print(str(latest_order_no[0]))
        if str(latest_order_no[0]) != '(None,)':
            new_order_id = int(str(latest_order_no[0])[1:-2]) + 1
        else:
            new_order_id = 1
        #print(new_order_id)
        #print(str(self.delivery_list[1]))
        sql = ("insert into order_ (order_id,order_date_time,order_status,shop_id,phone_number,table_id) values (" + str(new_order_id) + ",sysdate,'0','" +str(self.id) + "','" + str(self.delivery_list[2]) + "','0')")
        self.cur.execute(sql)
        self.cur.execute('commit')

        sql2 = ("insert into delivery (order_id, delivery_location,surname) values (" + str(new_order_id) + ",'" + str(self.delivery_list[0]) + "','"+str(self.delivery_list[1])+"')")
        self.cur.execute(sql2)
        self.cur.execute('commit')

        cur = self.conn.cursor()
        cur.execute("select order_id from order_ where order_id = '" + str(new_order_id) + "' ")
        order_id=[]
        for row in cur.fetchall():
            order_id.append(row)

        self.add_order_template(order_id,'Delivery','Add_pd_p_t')

    def delivery_phone_number(self):
        self.editAreaAddress2.delete("1.0", END)

        self.delivery_list.append(self.address_list)
        self.address_list = ''
        self.editAreaAddress.delete("1.0", END)
        self.editAreaAddress.insert(tk.INSERT, 'Address: ')
        self.editAreaAddress.insert(tk.INSERT, self.delivery_list[0])

        self.editAreaAddress.insert(tk.INSERT, '\n'+'Surname: ')
        self.editAreaAddress.insert(tk.INSERT, self.delivery_list[1])


        self.editAreaAddress.insert(tk.INSERT, '\n' + 'Input Phone Number:')
        self.btn_ap_enter.config(command=lambda: self.delivery_set_table())
        for i in range(10, 39):
            self.btn_ap[0][i].config(text='',command='')

    def delivery_surname(self):
        self.editAreaAddress2.delete("1.0", END)

        self.delivery_list.append(self.address_list)
        self.address_list=''
        self.editAreaAddress.delete("1.0", END)
        self.editAreaAddress.insert(tk.INSERT, 'Address: ')
        self.editAreaAddress.insert(tk.INSERT, self.delivery_list[0])
        self.editAreaAddress.insert(tk.INSERT, '\n'+'Input Surname:')
        self.btn_ap_enter.config(command=lambda: self.delivery_phone_number())
        pass


    def logout(self):
        pw=[]
        cur = self.conn.cursor()
        cur.execute("select shop_password from shop where shop_id = '" + str(self.id) + "'")

        for row in cur.fetchall():
            pw.append(row)
        print(pw)
        print(str(self.address_list))
        if str(pw[0])[2:-3] == str(self.address_list):
            login_loop.main(self.root)
        else:
            self.editAreaAddress.insert(tk.INSERT, 'wrong pw ')


    def update_address(self):
        #print(str(self.update_order_id[0])[1:-2])
        cur = self.conn.cursor()
        sql = ("update delivery set delivery_location = '" + str(self.address_list) + "' where order_id  =" + str(self.update_order_id[0])[1:-2] )

        self.cur.execute(sql)
        self.cur.execute('commit')
        #print(str(self.address_list))
        self.check_deli_take_away()

    def update_surname(self):
        #print(str(self.update_order_id[0])[1:-2])
        cur = self.conn.cursor()
        sql = ("update delivery set surname = '" + str(self.address_list) + "' where order_id  =" + str(self.update_order_id[0])[1:-2] )

        self.cur.execute(sql)
        self.cur.execute('commit')
        #print(str(self.address_list))
        self.check_deli_take_away()

    def update_phone(self):
        #print(str(self.update_order_id[0])[1:-2])
        cur = self.conn.cursor()
        sql = ("update order_ set phone_number = '" + str(self.address_list) + "' where order_id  =" + str(self.update_order_id[0])[1:-2] )

        self.cur.execute(sql)
        self.cur.execute('commit')
        #print(str(self.address_list))
        self.check_deli_take_away()

    def address_page(self,mode):
        #---
        self.address_list=''
        self.left_frame.pack_forget()
        self.left_frame = Frame(self.root, background="black",
                                borderwidth=5, relief="ridge",
                                width=600)
        self.left_frame.pack(side="left",
                             fill="both",
                             expand="yes",
                             )

        self.frameL1 = tk.Frame(self.left_frame)
        self.frameL1.pack()
        self.frameL2 = tk.Frame(self.left_frame)
        self.frameL2.pack()
        self.frameL3 = tk.Frame(self.left_frame)
        self.frameL3.pack()
        self.frameL4 = tk.Frame(self.left_frame)
        self.frameL4.pack()
        self.frameL5 = tk.Frame(self.left_frame)
        self.frameL5.pack()
        self.frameL6 = tk.Frame(self.left_frame)
        self.frameL6.pack()
        self.frameL7 = tk.Frame(self.left_frame)
        self.frameL7.pack()

        if mode == 'update_address' or mode == 'update_surname' or mode == 'update_phone':
            self.btnBack.config(command=lambda: self.check_page("address_page_update"))
        else:
            self.btnBack.config(command=lambda: self.last_page("address_page"))
        self.btnHome.config(command=lambda: self.home_page("address_page"))



        self.editAreaAddress = tkst.ScrolledText(self.frameL1, height=7, background="black", fg="white",
                                               font=("courier new", 15, "bold"))
        self.editAreaAddress.pack(fill="both", expand="yes", side="left")
        if mode == 'delivery' or mode == 'update_address':
            self.editAreaAddress.insert(tk.INSERT, 'Input address:')

        elif mode == 'logout':
            self.editAreaAddress.insert(tk.INSERT, 'Input password:')

        elif mode=='clean_data1':
            self.middle_frame.pack_forget()
            self.editAreaAddress.insert(tk.INSERT, 'Input password:')

        elif mode == 'clean_data2':
            self.editAreaAddress.insert(tk.INSERT, 'Input password:')

        elif mode == 'member':
            self.editAreaAddress.insert(tk.INSERT, 'Input member id:')

        elif mode == 'update_surname':
            self.editAreaAddress.insert(tk.INSERT, 'Input surname:')

        elif mode == 'update_phone':
            self.editAreaAddress.insert(tk.INSERT, 'Input phone no:')

        self.editAreaAddress2 = tkst.ScrolledText(self.frameL2, height=5, background="black", fg="white",
                                                font=("courier new", 15, "bold"))
        self.editAreaAddress2.pack(fill="both", expand="yes", side="left")

        keyboardlist=['1','2','3','4','5','6','7','8','9','0','Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L',"'",'Z','X','C','V','B','N','M',',','/','+']

        self.btn_ap = [[0 for x in range(121)] for y in range(1)]


        if mode == 'logout':
            for i in range(0, 10):
                self.btn_ap[0][i] = tk.Button(self.frameL3, text=keyboardlist[i], font=("Helvetica", 20, "bold "),
                                              fg="white", bg="grey20", width=4, height=2,
                                              command=lambda i=i: self.address_page_editarea(keyboardlist[i]))
                self.btn_ap[0][i].pack(side=tk.LEFT)

            for i in range(10, 20):
                self.btn_ap[0][i] = tk.Button(self.frameL4, text=keyboardlist[i], font=("Helvetica", 20, "bold "),
                                              fg="white", bg="grey20", width=4, height=2,
                                              command=lambda i=i: self.address_page_editarea(keyboardlist[i]))
                self.btn_ap[0][i].pack(side=tk.LEFT)

            for i in range(20, 30):
                self.btn_ap[0][i] = tk.Button(self.frameL5, text=keyboardlist[i], font=("Helvetica", 20, "bold "),
                                              fg="white", bg="grey20", width=4, height=2,
                                              command=lambda i=i: self.address_page_editarea(keyboardlist[i]))
                self.btn_ap[0][i].pack(side=tk.LEFT)

            for i in range(30, 39):
                self.btn_ap[0][i] = tk.Button(self.frameL6, text=keyboardlist[i], font=("Helvetica", 20, "bold "),
                                              fg="white", bg="grey20", width=4, height=2,
                                              command=lambda i=i: self.address_page_editarea(keyboardlist[i]))
                self.btn_ap[0][i].pack(side=tk.LEFT)

        else:
            for i in range(0, 10):
                self.btn_ap[0][i] = tk.Button(self.frameL3, text=keyboardlist[i], font=("Helvetica", 20, "bold "),fg= "white",bg="grey20", width=4, height=2,
                                          command= lambda i=i: self.address_page_editarea(keyboardlist[i]))
                self.btn_ap[0][i].pack(side=tk.LEFT)

            for i in range(10, 20):
                self.btn_ap[0][i] = tk.Button(self.frameL4, text=keyboardlist[i], font=("Helvetica", 20, "bold "),fg= "white",bg="grey20", width=4, height=2,
                                          command=lambda i=i: self.address_page_editarea(keyboardlist[i]))
                self.btn_ap[0][i].pack(side=tk.LEFT)

            for i in range(20, 30):
                self.btn_ap[0][i] = tk.Button(self.frameL5, text=keyboardlist[i], font=("Helvetica", 20, "bold "),fg= "white",bg="grey20", width=4, height=2,
                                          command=lambda i=i: self.address_page_editarea(keyboardlist[i]))
                self.btn_ap[0][i].pack(side=tk.LEFT)

            for i in range(30, 40):
                self.btn_ap[0][i] = tk.Button(self.frameL6, text=keyboardlist[i], font=("Helvetica", 20, "bold "),fg= "white",bg="grey20", width=4, height=2,
                                          command=lambda i=i: self.address_page_editarea(keyboardlist[i]))
                self.btn_ap[0][i].pack(side=tk.LEFT)


        if mode == 'update_phone':
            for i in range(10, 39):
                self.btn_ap[0][i].config(text='', command='')


        self.btn_ap_bk = tk.Button(self.frameL3, text='<[X]', font=("Helvetica", 20, "bold "), fg="white",
                                   bg="dark red", width=6,
                                   height=2,
                                   command=lambda: self.address_page_editarea("del"))
        self.btn_ap_bk.pack(side=tk.LEFT)

        self.btn_ap_space= tk.Button(self.frameL7, text='Spacebar', font=("Helvetica", 20, "bold "),fg= "white",bg="grey20", width=40, height=2,
                                          command=lambda: self.address_page_editarea(' '))
        self.btn_ap_space.pack(side=tk.LEFT)

        self.btn_ap_enter = tk.Button(self.frameL7, text='ENTER', font=("Helvetica", 20, "bold "), fg="white", bg="dark orange3", width=6,
                                      height=2,
                                      command='')
        self.btn_ap_enter.pack(side=tk.LEFT)
        if mode == 'delivery':
            self.btn_ap_enter.config(command=lambda: self.delivery_surname())

        elif mode == 'logout':
            self.btn_ap_enter.config(command=lambda: self.logout())


        elif mode == 'clean_data1' or mode == 'clean_data2':
            self.btn_ap_enter.config(command=lambda: self.clean())

        elif mode == 'member':
            self.btn_ap_enter.config(command=lambda: self.member_surname())

        elif mode == 'update_address':
            self.btn_ap_enter.config(command=lambda: self.update_address())

        elif mode == 'update_surname':
            self.btn_ap_enter.config(command=lambda: self.update_surname())

        elif mode == 'update_phone':
            self.btn_ap_enter.config(command=lambda: self.update_phone())

        self.btnTR1.config(text='', font=("Helvetica", 20, "bold "),bg="grey20", command='')
        self.btnTR2.config(text='', font=("Helvetica", 20, "bold "),bg="grey20", command='')
        self.btnTR3.config(text='', font=("Helvetica", 20, "bold "),bg="grey20", command='')
        self.btnTR4.config(text='', font=("Helvetica", 20, "bold "),bg="grey20", command='')
        self.btnTR5.config(text='', font=("Helvetica", 20, "bold "),bg="grey20", command='')
        self.btnTR6.config(text='', font=("Helvetica", 20, "bold "),bg="grey20", command='')
        self.btnTR7.config(text='', font=("Helvetica", 20, "bold "),bg="grey20", command='')
        self.btnTR8.config(text='', font=("Helvetica", 20, "bold "),bg="grey20", command='')

    def take_away(self):
        latest_order_no = []
        new_order_id = 0
        cur = self.conn.cursor()
        cur.execute("select max(order_id) from order_ ")
        for row in cur.fetchall():
            latest_order_no.append(row)


        if str(latest_order_no[0]) != '(None,)':
            new_order_id = int(str(latest_order_no[0])[1:-2]) + 1
        else:
            new_order_id = 1



        sql = ("insert into order_ (order_id,order_date_time,order_status,shop_id,table_id) values (" + str(
            new_order_id) + ",sysdate,'0','"+str(self.id)+"','1')")
        self.cur.execute(sql)

        self.cur.execute('commit')

        cur = self.conn.cursor()
        cur.execute("select order_id from order_ where order_id = '" + str(new_order_id) + "' ")
        order_id = []
        for row in cur.fetchall():
            order_id.append(row)

        self.add_order_template(order_id,'Take away','Add_pd_p_t')

        pass


    def transition_check_member_order(self, order_id, number):
        # print(order_id)
        self.left_frame.pack_forget()
        self.middle_frame.pack_forget()

        self.member_page(order_id, number,"check_deli")

    def transition_check_order(self, order_id, number, section):
        # print(order_id)
        self.left_frame.pack_forget()
        self.middle_frame.pack_forget()

        self.add_order_template(order_id, number,section)

    def transition_check_del(self, order_id, number, section):
        # print(order_id)
        self.left_frame.pack_forget()
        self.middle_frame.pack_forget()

        self.del_order_template(order_id, number,section)

    def transition_update(self,order_id,mode):
        self.left_frame.pack_forget()
        self.middle_frame.pack_forget()
        self.update_order_id=order_id
        self.address_page(mode)

    def checkall(self):

        self.btnTR1.config(text='List', bg="royalblue3", command=lambda: self.checkall())

        self.btnTR2.config(text='', command='', bg="grey20")
        #---
        self.btnTR3.config(text='Clear Data', font=("Helvetica", 20, "bold "), bg="firebrick3", command=lambda: self.address_page("clean_data1"))

        self.btnTR4.config(text='', command='', bg="grey20")

        self.btnTR5.config(text='', command='', bg="grey20")

        self.btnTR6.config(text='', command='', bg="grey20")

        self.btnTR7.config(text='', command='', bg="grey20")

        self.btnTR8.config(text='', command='', bg="grey20")

        self.editAreaTable2.config(state="normal")
        self.editAreaTable2.delete("1.0", END)
        self.editAreaTable2.insert(tk.INSERT, "Input Order_id to Search: ")
        self.editAreaTable2.config(state="disabled")


        self.editAreaTable.config(state="normal")
        self.editAreaTable.delete("1.0", END)

        self.editAreaTable.insert(tk.INSERT,"Shop :"+self.id+'\n')


        self.editAreaTable.insert(tk.INSERT,
                                  "\n" + '%-5s %-5s %-5s  %-30s  %3s  %5s %5s ' % (
                                  "OID","O_PID", "PID", "Name", "Qty", "$/1","Remark")+"\n")

        cur = self.conn.cursor()
        sql = "select a.order_id,a.order_product_id,a.product_id,c.product_name,a.quantity, a.price,a.link_product,b.table_id from order_product a join order_ b on a.order_id =b.order_id join product c on a.product_id=c.product_id where b.shop_id='{0}' and (b.table_id ='0' or b.table_id ='1') and b.days is null order by  a.order_id DESC,a.order_product_id".format(
            self.id)
        cur.execute(sql)

        order_id=[]
        order_product_id=[]
        product_id=[]
        product_name=[]
        order_quantity=[]
        order_price=[]
        order_link=[]
        DT=[]


        for row in cur.fetchall():
            order_id.append(row[0])
            order_product_id.append(row[1])
            product_id.append(row[2])
            product_name.append(row[3])
            order_quantity.append(row[4])
            order_price.append(row[5])
            order_link.append(row[6])
            if str(row[7])==str(0):
                DT.append('deli.')
            elif str(row[7])==str(1):
                DT.append('take.')
            else:
                DT.append(' ')

        for i in range(0, len(order_product_id)):

            if str(order_id[i]) ==str(order_id[i-1]):
                if str(order_link[i]) == str(order_product_id[i]):
                    self.editAreaTable.insert(tk.INSERT,
                                              "\n" + '%-5s %-5s %-5s  %-30s  %3s  %5s %5s ' % (
                                              ' ', str(order_product_id[i]),
                                          str(product_id[i]), str(
                                              product_name[i]), str(order_quantity[i]), str(
                                              order_price[i]),''))
                else:
                    self.editAreaTable.insert(tk.INSERT,
                                              "\n" + '%-5s %-5s %-5s  %-30s  %3s  %5s %5s '% (
                                                  ' ', ' ',
                                          ' '+str(product_id[i]), ' '+str(
                                              product_name[i]), str(order_quantity[i]), str(
                                              order_price[i]),''))
            else:
                self.editAreaTable.insert(tk.INSERT,
                                          "\n" +  '%-5s %-5s %-5s  %-30s  %3s  %5s %5s ' % (
                                              str(order_id[i]), str(order_product_id[i]),
                                              str(product_id[i]), str(
                                                  product_name[i]), str(order_quantity[i]), str(
                                                  order_price[i]),str(DT[i])))


        self.editAreaTable.insert(tk.INSERT,"\n---END---")

        self.editAreaTable.config(state="disabled")
        self.btnTR2.config(text='', command='', bg="grey20")
        self.btnTR3.config(text='Clear Data', font=("Helvetica", 20, "bold "), bg="firebrick3", command='')
        self.btnTR4.config(text='', command='', bg="grey20")
        self.btnTR5.config(text='', command='', bg="grey20")
        self.btnTR6.config(text='', command='', bg="grey20")
        self.btnTR7.config(text='', command='', bg="grey20")

    def check_deli_take_away(self):
        '''
        when button clicked
        '''
        self.left_frame.pack_forget()

        self.del_pd_id = ''
        self.del_pd_qty = ''


        self.btnTR1.config(text='List',bg="royalblue3",command=lambda: self.checkall())

        self.btnTR2.config(text='', command='',bg="grey20")
        #---
        self.btnTR3.config(text='Clear Data', font=("Helvetica", 20, "bold "), bg="firebrick3", command=lambda: self.address_page("clean_data1"))

        self.btnTR4.config(text='', command='',bg="grey20")

        self.btnTR5.config(text='', command='',bg="grey20")

        self.btnTR6.config(text='', command='',bg="grey20")

        self.btnTR7.config(text='', command='',bg="grey20")

        self.btnTR8.config(text='', command='', bg="grey20")


        self.btnBack.config(command=lambda: self.home_page("check_order"))
        self.btnHome.config(command=lambda: self.home_page("check_order"))

        self.left_frame = Frame(self.root, background="black",
                                borderwidth=5, relief="ridge",
                                width=600)
        self.left_frame.pack(side="left",
                             fill="both",
                             expand="yes",
                             )

        self.middle_frame = Frame(self.root, width=20, background="black",
                                  borderwidth=5, relief="ridge",
                                  )
        self.middle_frame.pack(side="left",
                               fill="both",

                               )
        self.editAreaTable = tkst.ScrolledText(self.left_frame, height=5, width=69, background="black", fg="white",
                                               font=("courier new", 15, "bold"))
        self.editAreaTable.pack(fill="both", expand="yes", side="left")

        self.editAreaTable.insert(tk.INSERT, "Shop :" + self.id + '\n')

        self.editAreaTable.insert(tk.INSERT,
                                  "\n" +  '%-5s %-5s %-5s  %-30s  %3s  %5s %5s ' % (
                                      "OID", "O_PID", "PID", "Name", "Qty", "$/1", "Remark") + "\n")

        cur = self.conn.cursor()
        sql = "select a.order_id,a.order_product_id,a.product_id,c.product_name,a.quantity, a.price,a.link_product,b.table_id from order_product a join order_ b on a.order_id =b.order_id join product c on a.product_id=c.product_id where b.shop_id='{0}' and (b.table_id ='0' or b.table_id ='1') and b.days is null order by  a.order_id DESC,a.order_product_id".format(
            self.id)
        cur.execute(sql)

        order_id = []
        order_product_id = []
        product_id = []
        product_name = []
        order_quantity = []
        order_price = []
        order_link = []
        DT = []

        for row in cur.fetchall():
            order_id.append(row[0])
            order_product_id.append(row[1])
            product_id.append(row[2])
            product_name.append(row[3])
            order_quantity.append(row[4])
            order_price.append(row[5])
            order_link.append(row[6])
            if str(row[7]) == str(0):
                DT.append('deli.')
            elif str(row[7]) == str(1):
                DT.append('take.')
            else:
                DT.append(' ')

        for i in range(0, len(order_product_id)):
            if str(order_id[i]) == str(order_id[i - 1]):
                if str(order_link[i]) == str(order_product_id[i]):
                    self.editAreaTable.insert(tk.INSERT,
                                              "\n" + '%-5s %-5s %-5s  %-30s  %3s  %5s %5s ' % (
                                                  ' ', str(order_product_id[i]),
                                                  str(product_id[i]), str(
                                                      product_name[i]), str(order_quantity[i]), str(
                                                      order_price[i]), ''))
                else:
                    self.editAreaTable.insert(tk.INSERT,
                                              "\n" + '%-5s %-5s %-5s  %-30s  %3s  %5s %5s ' % (
                                                  ' ', ' ',
                                                  ' ' + str(product_id[i]), ' ' + str(
                                                      product_name[i]), str(order_quantity[i]), str(
                                                      order_price[i]), ''))
            else:
                self.editAreaTable.insert(tk.INSERT,
                                          "\n" + '%-5s %-5s %-5s  %-30s  %3s  %5s %5s ' % (
                                              str(order_id[i]), str(order_product_id[i]),
                                              str(product_id[i]), str(
                                                  product_name[i]), str(order_quantity[i]), str(
                                                  order_price[i]), str(DT[i])))

        self.editAreaTable.insert(tk.INSERT, "\n---END---")

        self.editAreaTable.config(state="disabled")

        self.frameM1 = tk.Frame(self.middle_frame)
        self.frameM1.pack()


        tk.Label(self.frameM1, bg='black', text='Check Deli./T.Away' ,font=("Helvetica", 20, "bold "), fg="white", borderwidth=5).pack()

        self.frameM1 = tk.Frame(self.middle_frame)
        self.frameM1.pack()
        self.frameM2 = tk.Frame(self.middle_frame)
        self.frameM2.pack()
        self.frameM3 = tk.Frame(self.middle_frame)
        self.frameM3.pack()
        self.frameM4 = tk.Frame(self.middle_frame)
        self.frameM4.pack()
        self.frameM5 = tk.Frame(self.middle_frame)
        self.frameM5.pack()
        self.frameM6 = tk.Frame(self.middle_frame)
        self.frameM6.pack()
        self.frameM7 = tk.Frame(self.middle_frame)
        self.frameM7.pack()
        self.frameM8 = tk.Frame(self.middle_frame)
        self.frameM8.pack()
        self.frameM9 = tk.Frame(self.middle_frame)
        self.frameM9.pack()

        self.editAreaTable2 = tkst.ScrolledText(self.frameM1, height=10, width=40, background="black", fg="white",
                                                font=("courier new", 15, "bold"))
        self.editAreaTable2.pack(fill="both", expand="yes", side="left")

        self.editAreaTable3 = tkst.ScrolledText(self.frameM2, height=3, width=40, background="black", fg="white",
                                                font=("courier new", 15, "bold"))
        self.editAreaTable3.pack(fill="both", expand="yes", side="left")


        tk.Button(self.frameM5, text="7", font=("Helvetica", 20, "bold "), fg="white", bg="slate blue", width=4,
                  height=2, command=lambda: self.del_page_editarea("7")).pack(
            side=tk.LEFT)
        tk.Button(self.frameM5, text="8", font=("Helvetica", 20, "bold "), fg="white", bg="slate blue", width=4,
                  height=2, command=lambda: self.del_page_editarea("8")).pack(
            side=tk.LEFT)
        tk.Button(self.frameM5, text="9", font=("Helvetica", 20, "bold "), fg="white", bg="slate blue", width=4,
                  height=2, command=lambda: self.del_page_editarea("9")).pack(
            side=tk.LEFT)
        tk.Button(self.frameM5, text="<[X]", font=("Helvetica", 20, "bold "),fg= "white",bg="dark red", width=4,
                  height=2, command=lambda: self.del_page_editarea("del")).pack(
            side=tk.LEFT)
        tk.Button(self.frameM5, text="", font=("Helvetica", 20, "bold "),fg= "white",bg="grey20", width=4, height=2, command='').pack(
            side=tk.LEFT)

        tk.Button(self.frameM6, text="4", font=("Helvetica", 20, "bold "), fg="white", bg="slate blue", width=4,
                  height=2, command=lambda: self.del_page_editarea("4")).pack(
            side=tk.LEFT)
        tk.Button(self.frameM6, text="5", font=("Helvetica", 20, "bold "), fg="white", bg="slate blue", width=4,
                  height=2, command=lambda: self.del_page_editarea("5")).pack(
            side=tk.LEFT)
        tk.Button(self.frameM6, text="6", font=("Helvetica", 20, "bold "), fg="white", bg="slate blue", width=4,
                  height=2, command=lambda: self.del_page_editarea("6")).pack(
            side=tk.LEFT)
        tk.Button(self.frameM6, text="", font=("Helvetica", 20, "bold "),fg= "white",bg="grey20", width=4, height=2, command='').pack(
            side=tk.LEFT)
        tk.Button(self.frameM6, text="", font=("Helvetica", 20, "bold "),fg= "white",bg="grey20", width=4, height=2, command='').pack(
            side=tk.LEFT)

        tk.Button(self.frameM7, text="1", font=("Helvetica", 20, "bold "), fg="white", bg="slate blue", width=4,
                  height=2, command=lambda: self.del_page_editarea("1")).pack(
            side=tk.LEFT)
        tk.Button(self.frameM7, text="2", font=("Helvetica", 20, "bold "), fg="white", bg="slate blue", width=4,
                  height=2, command=lambda: self.del_page_editarea("2")).pack(
            side=tk.LEFT)
        tk.Button(self.frameM7, text="3", font=("Helvetica", 20, "bold "), fg="white", bg="slate blue", width=4,
                  height=2, command=lambda: self.del_page_editarea("3")).pack(
            side=tk.LEFT)
        tk.Button(self.frameM7, text="", font=("Helvetica", 20, "bold "),fg= "white",bg="grey20", width=4, height=2, command='').pack(
            side=tk.LEFT)
        tk.Button(self.frameM7, text="", font=("Helvetica", 20, "bold "),fg= "white",bg="grey20", width=4, height=2, command='').pack(
            side=tk.LEFT)
        tk.Button(self.frameM8, text="0", font=("Helvetica", 20, "bold "), fg="white", bg="slate blue", width=4,
                  height=2, command=lambda: self.del_page_editarea("0")).pack(
            side=tk.LEFT)
        tk.Button(self.frameM8, text="", font=("Helvetica", 20, "bold "), fg="white", bg="slate blue", width=4,
                  height=2, command='').pack(
            side=tk.LEFT)
        tk.Button(self.frameM8, text="", font=("Helvetica", 20, "bold "), fg="white", bg="slate blue", width=4,
                  height=2, command='').pack(
            side=tk.LEFT)


        tk.Button(self.frameM8, text="Search", font=("Helvetica", 20, "bold "), fg="white", bg="dark green",
                      width=8, height=2, command=lambda: self.search()).pack(
                side=tk.LEFT)

        self.editAreaTable2.insert(tk.INSERT, 'Input Order_id to Search: ')

    def search(self):

        order_id = self.editAreaTable3.get("1.0", END)[0:-1]
        self.editAreaTable2.config(state="normal")
        self.editAreaTable2.delete("1.0", END)
        self.editAreaTable2.insert(tk.INSERT, "The Order_id you input:")
        self.order_id=order_id
        cur = self.conn.cursor()
        cur.execute("select  * from order_ where order_id = '"+ str(order_id)+"'and shop_id = '"+str(self.id)+"'and (table_id ='0' or table_id ='1') and days is null order by order_id")
        found = False
        for row in cur.fetchall():
            if str(self.editAreaTable3.get("1.0", END)[0:-1])== str(row[0]):
                found = True
            else:
                pass
        if not found:
            self.editAreaTable2.insert(tk.INSERT, order_id)
            self.editAreaTable2.insert(tk.INSERT, '\nNot Found. Try Again:')
            self.editAreaTable3.delete("1.0", END)
            self.editAreaTable3.see("end")
        else:

            self.editAreaTable.config(state="normal")
            self.editAreaTable2.config(state="normal")

            self.editAreaTable.delete("1.0", END)
            self.editAreaTable2.insert(tk.INSERT, order_id)


            order_item = []
            order_created_time = []
            order_product_id = []
            product_id = []
            product_name = []
            order_quantity = []
            order_price = []
            order_link = []

            cur = self.conn.cursor()
            cur.execute("select  * from order_product where order_id = {0}".format(int(order_id)))
            for row in cur.fetchall():
                order_item.append(row)

            self.editAreaTable.insert(tk.INSERT, "Order id: ")
            self.editAreaTable.insert(tk.INSERT, order_id)

            cur = self.conn.cursor()
            cur.execute("select to_char(order_date_time,'DD-MM-YYYY HH24:MM:SS') from order_ where order_id = {0}".format(int(order_id)))
            order_time= cur.fetchall()

            self.editAreaTable.insert(tk.INSERT, "\nOrder Date/Time: ")
            self.editAreaTable.insert(tk.INSERT, order_time[0])
            self.editAreaTable.insert(tk.INSERT, '\n')

            cur = self.conn.cursor()
            cur.execute("select  Table_id from order_ where order_id = {0}".format(int(order_id)))
            order_status=cur.fetchall()


            if order_status[0][-1] == str(1):
                self.editAreaTable.insert(tk.INSERT, "Take Away ")


            elif order_status[0][-1] == str(0):
                cur = self.conn.cursor()
                cur.execute("select  delivery_location from delivery where order_id = {0}".format(int(order_id)))
                self.editAreaTable.insert(tk.INSERT, "Delivery: ")
                self.editAreaTable.insert(tk.INSERT, cur.fetchall())
                cur = self.conn.cursor()
                cur.execute("select  surname from delivery where order_id = {0}".format(int(order_id)))
                self.editAreaTable.insert(tk.INSERT, "\nSurname: ")
                self.editAreaTable.insert(tk.INSERT, cur.fetchall())
                cur = self.conn.cursor()
                cur.execute("select  phone_number from order_ where order_id = {0}".format(int(order_id)))
                self.editAreaTable.insert(tk.INSERT, "\nPhone number: ")
                self.editAreaTable.insert(tk.INSERT, cur.fetchall())



            else:
                self.editAreaTable.insert(tk.INSERT, "Shop/Table:  ")
                self.editAreaTable.insert(tk.INSERT, order_status)

            self.editAreaTable.insert(tk.INSERT,'\n')

            if order_item == []:
                self.editAreaTable.insert(tk.INSERT, "\n\nNo product is ordered")
            else:

                cur = self.conn.cursor()
                cur.execute("select order_product_id from order_product where order_id = " + order_id + " order by order_product_id")
                for row in cur.fetchall():
                    order_product_id.append(row)

                cur = self.conn.cursor()
                cur.execute("select  product_id from order_product where order_id = " + order_id + " order by order_product_id")
                for row in cur.fetchall():
                    product_id.append(row)

                cur = self.conn.cursor()
                cur.execute(
                    "select  product.product_name from order_product inner join product on product.product_id = order_product.product_id where order_id = " + order_id + " order by order_product_id")
                for row in cur.fetchall():
                    product_name.append(row)

                cur = self.conn.cursor()
                cur.execute("select  quantity from order_product where order_id = " + order_id + " order by order_product_id")
                for row in cur.fetchall():
                    order_quantity.append(row)

                cur = self.conn.cursor()
                cur.execute("select  price from order_product where order_id = " + order_id + " order by order_product_id")
                for row in cur.fetchall():
                    order_price.append(row)

                cur = self.conn.cursor()
                cur.execute("select  link_product from order_product where order_id = " + order_id + " order by order_product_id")
                for row in cur.fetchall():
                    order_link.append(row)

                total_price=0
                if len(order_price)!=0:
                    for e in range(0,len(order_price)):
                        total_price += (float(order_price[e][0])*float(order_quantity[e][0]))

                self.editAreaTable.insert(tk.INSERT,"\n\n" + '%-8s  %-5s  %-30s  %3s  %5s' % ("O_PID", "PID", "Name", "Qty", "$/1"))

                for i in range(0, len(order_product_id)):
                    if str(order_link[i])[2:-3] == str(order_product_id[i])[1:-2]:
                        self.editAreaTable.insert(tk.INSERT,
                                              "\n" + '%-8s  %-5s  %-30s  %3s  %5s' % (
                                                  str(order_product_id[i])[1:-2], str(product_id[i])[2:-3], str(
                                                      product_name[i])[2:-3], str(order_quantity[i])[1:-2], str(
                                                      order_price[i])[1:-2]))
                    else:
                        self.editAreaTable.insert(tk.INSERT,
                                                  "\n" + '%-8s  %-5s  %-30s  %3s  %5s' % (
                                                      '', ' '+str(product_id[i])[2:-3], ' '+str(
                                                          product_name[i])[2:-3], str(order_quantity[i])[1:-2], str(
                                                          order_price[i])[1:-2]))
                self.editAreaTable.insert(tk.INSERT,"\n\n\n" +  '%-43s  %5s' % ('','Total : '+str(total_price)))

            self.editAreaTable.config(state="disabled")
            self.editAreaTable2.config(state="disabled")
            self.editAreaTable3.delete("1.0", END)
            self.editAreaTable3.see("end")
            print(order_id)

            tranfer_order_id=[]
            cur = self.conn.cursor()
            cur.execute("select order_id from order_ where order_id = '" + str(order_id) + "' and order_status = '0'")

            for row in cur.fetchall():
                tranfer_order_id.append(row)

            if order_status[0][-1] == str(1):
                self.btnTR2.config(text='', command='', bg="grey20")

                self.btnTR3.config(text='', command='', bg="grey20")

                self.btnTR4.config(text='', command='', bg="grey20")

            elif order_status[0][-1] == str(0):
                self.btnTR2.config(text='^Update\nAddress', font=("Helvetica", 20, "bold "), bg="dark violet",
                                   command=lambda: self.transition_update(tranfer_order_id, 'update_address'))

                self.btnTR3.config(text='^Update\nSurname', bg="blue violet",
                                   command=lambda: self.transition_update(tranfer_order_id, 'update_surname'))
                self.btnTR4.config(text='^Update\nPhone', font=("Helvetica", 20, "bold "), bg="dark orchid",
                                   command=lambda: self.transition_update(tranfer_order_id, 'update_phone'))

            else:
                self.btnTR2.config(text='', command='', bg="grey20")

                self.btnTR3.config(text='', command='', bg="grey20")

                self.btnTR4.config(text='', command='', bg="grey20")

            self.btnTR5.config(text='+Add Order', font=("Helvetica", 20, "bold "), bg="forest green",
                               command=lambda: self.transition_check_order(tranfer_order_id, '0', "Add_pd_check"))

            self.btnTR6.config( text='+Member', bg="chartreuse4",command=lambda: self.transition_check_member_order(tranfer_order_id,'0'))
            self.btnTR7.config(text='-Delete Order', font=("Helvetica", 20, "bold "), bg="orangered3",
                               command=lambda: self.transition_check_del(tranfer_order_id, '0', "del_check"))

            self.btnTR8.config(text='Export', bg="darkorange3", command=lambda: self.export("order", self.order_id))

        pass

    def report(self):
        self.left_frame.pack_forget()
        self.left_frame = Frame(self.root, background="black",
                                borderwidth=5, relief="ridge",
                                width=600)
        self.left_frame.pack(side="left",
                             fill="both",
                             expand="yes",
                             )

        self.frameL1 = tk.Frame(self.left_frame)
        self.frameL1.pack()
        self.frameL2 = tk.Frame(self.left_frame)
        self.frameL2.pack()

        self.btnBack.config(command=lambda: self.home_page("report_page"))
        self.btnHome.config(command=lambda: self.home_page("report_page"))

        self.editArea = tkst.ScrolledText(self.frameL1, height=2, background="black", fg="white",
                                               font=("courier new", 15, "bold"))
        self.editArea.pack(fill="both", expand="yes", side="left")

        self.editArea2 = tkst.ScrolledText(self.frameL2, height=50, background="black", fg="white",
                                                font=("courier new", 15, "bold"))
        self.editArea2.pack(fill="both", expand="yes", side="left")
        #---
        self.btnTR1.config(text='', font=("Helvetica", 20, "bold "),bg="grey20", command='')
        self.btnTR2.config(text='', font=("Helvetica", 20, "bold "),bg="grey20", command='')
        self.btnTR3.config(text='Clear Data', font=("Helvetica", 20, "bold "), bg="firebrick3", command=lambda: self.address_page("clean_data2"))
        self.btnTR4.config(text='', font=("Helvetica", 20, "bold "),bg="grey20", command='')
        self.btnTR5.config(text='', font=("Helvetica", 20, "bold "),bg="grey20", command='')
        self.btnTR6.config(text='', font=("Helvetica", 20, "bold "), bg="grey20", command='')
        self.btnTR7.config(text='Refresh', font=("Helvetica", 20, "bold "),bg="forest green", command=lambda: self.report())
        self.btnTR8.config(text='Export', font=("Helvetica", 20, "bold "),bg="darkorange3", command=lambda: self.export('report',''))

        self.editArea2.insert(tk.INSERT, 'Summary of Shop:'+str(self.id))

        product_id = []
        product_name = []
        unit_price = []
        total_quantity = []

        cur = self.conn.cursor()
        cur.execute(
            "select a.product_id,c.product_name,a.price, sum(a.quantity) from order_product a inner join order_ b on a.order_id = b.order_id join product c on a.product_id=c.product_id where b.shop_id = '{0}' and b.days is null GROUP BY a.product_id,a.price,c.product_name order by a.product_id".format(
                self.id))
        for row in cur.fetchall():
            product_id.append(row[0])
            product_name.append(row[1])
            unit_price.append(row[2])
            total_quantity.append(row[3])

        total_price=0
        for e in range(0,len(unit_price)):
            total_price += (float(unit_price[e]) * float(total_quantity[e]))

        self.editArea2.insert(tk.INSERT, "\n\nTotal income: " + str(total_price)+'\n\n'+'-'*50)

        self.editArea2.insert(tk.INSERT,"\n\nThe sale of each product (0 will not be showed):\n\n" + '%-5s  %-30s  %5s  %15s' % ("PID", "Name", "Unit_price", "Quantity")+'\n')

        for i in range(0, len(product_name)):
            self.editArea2.insert(tk.INSERT,"\n" + '%-5s  %-35s  %5s  %15s' % (
                                          str(product_id[i]),str(product_name[i]), str(unit_price[i]), str(total_quantity[i])))

        self.editArea2.insert(tk.INSERT, '\n\n---END---\n')

    def export(self,type,id):
        date_string = datetime.datetime.now()
        file_full = ''
        for e in str(date_string):
            if e == ':':
                e = '_'
            file_full += e

        if type=='report':
            self.editArea.delete("1.0", END)

            fileIn = open('Summary report ' + file_full + '.txt', 'w')
            fileIn.write('Created ' + str(date_string.strftime('%Y/%m/%d %H:%M:%S')))
            fileIn.write('\n')
            fileIn.write('\n')
            if str(self.editArea2.get("1.0", END))!='':
                fileIn.write(str(self.editArea2.get("1.0", END))+ '\n')
            else:
                fileIn.write('No data!')
            fileIn.write('\n')
            fileIn.write('---------------------------------------------------------------------------------------------------------------')
            fileIn.close()

            self.editArea.insert(tk.INSERT,"The report '{0}' is printed.".format('Summary report ' + file_full + '.txt'))

        elif type=='order':
            if str(self.editAreaTable.get("1.0", END))[0:-1] == '':
                self.editAreaTable2.config(state="normal")
                self.editAreaTable2.insert(tk.INSERT,'\nPlease input a order_id first.\n')
            elif str(self.editAreaTable.get("1.0", END))[0:-1] != '':
                fileIn = open('Order '+id+' on '+ file_full + '.txt', 'w')
                fileIn.write('Created ' + str(date_string.strftime('%Y/%m/%d %H:%M:%S')))
                fileIn.write('\n')
                fileIn.write('\n')
                fileIn.write(str(self.editAreaTable.get("1.0", END)) + '\n')
                fileIn.write('\n')
                fileIn.write(
                    '---------------------------------------------------------------------------------------------------------------')
                fileIn.close()
                self.editAreaTable2.config(state="normal")
                self.editAreaTable2.insert(tk.INSERT,"\nThe report '{0}' is printed.\n ".format('Order_id'+id+' (' + file_full + ').txt'))

    def clean(self):
        #---
        pw = []
        cur = self.conn.cursor()
        cur.execute("select shop_password from shop where shop_id = '" + str(self.id) + "'")

        for row in cur.fetchall():
            pw.append(row)
        print(pw)
        print(str(self.address_list))
        if str(pw[0])[2:-3] == str(self.address_list):
            cur = self.conn.cursor()
            cur.execute("update order_ set days=1")
            cur.execute("commit")
            self.home_page("report_page")

        else:
            self.editAreaAddress.insert(tk.INSERT, 'wrong pw ')

    def diff(self,list1, list2):
        c = set(list1).union(set(list2))  # or c = set(list1) | set(list2)
        d = set(list1).intersection(set(list2))  # or d = set(list1) & set(list2)
        return list(c - d)



    def switch_implement(self, order_id, table_no):
        #print(str(order_id)[1:-2])
        #print(table_no)
        cur = self.conn.cursor()
        sql=("update order_ set table_id = '"+str(table_no)+"' where order_id = "+str(order_id)[2:-3])
        self.cur.execute(sql)
        self.cur.execute('commit')
        self.home_page("set_tb")


    def switch_table(self,order_id,table_no):

        self.btnBack.config(command=lambda: self.last_page_switch( table_no,table_no[6:]))
        self.btnHome.config(command=lambda: self.home_page("set_tb"))

        table_name_list = []
        new_table_id_list = []
        table_occupy_List = []
        new_name_list = []

        cur = self.conn.cursor()
        cur.execute(
            "select table_.table_name from table_ inner join order_ on order_.table_id = table_.table_id where table_.table_id like '"+str(self.id) +"-%' "+" and order_.order_status = '0' order by table_.table_name")
        for row in cur.fetchall():
            table_occupy_List.append(row)

        print(table_occupy_List)



        cur = self.conn.cursor()
        cur.execute("select table_name from table_ where table_id like '" + str(self.id) + "-%' order by table_name")
        for row in cur.fetchall():
            table_name_list.append(row)

        new_name_list = self.diff(table_occupy_List,table_name_list)
        print(new_name_list)

        for i in range(0,len(new_name_list)):
            new_table_id_list.append(str(self.id)+"-"+str(new_name_list[i])[2:-3])


        print(new_table_id_list)
        length_data = len(table_name_list)


        for i in range(0, length_data):

            self.btn_tb[0][i].config(text=(str(new_name_list[i])[2:-3]),command=lambda i=i: self.switch_implement(order_id,str(new_table_id_list[i]) ))

    def main_page_table(self):
        table_name_list = []
        table_id_list=[]

        cur = self.conn.cursor()
        cur.execute("select table_name from table_ where table_id like '"+str(self.id)+"-%' order by table_name")
        for row in cur.fetchall():
            table_name_list.append(row)

        cur = self.conn.cursor()
        cur.execute("select table_id from table_ where table_id like '"+str(self.id)+"-%' order by table_name")
        for row in cur.fetchall():
            table_id_list.append(row)


        length_data = len(table_name_list)

        t_name_list=[]
        t_id_list=[]
        for i in range(0,length_data):


            t_name = str(table_name_list[i])
            t_id = str(table_id_list[i])


            t_name_list.append(t_name[2:-3])
            t_id_list.append(t_id[2:-3])
            self.btn_tb[0][i].config(text=(t_name[2:-3]),command=lambda i=i: self.table_sub(str(t_id_list[i]),int(str(t_name_list[i]))))

    def main_page(self,section,order_id,table_id):
        #print(self.id)
        self.left_frame = Frame(self.root, background="black",
                                borderwidth=5, relief="ridge",
                                width=1000)
        self.left_frame.pack(side="left",
                             fill="both",
                             expand="yes",
                             )

        self.frameL1 = tk.Frame(self.left_frame)

        self.frameL1.pack()

        self.frameL2 = tk.Frame(self.left_frame)

        self.frameL2.pack()

        self.frameL3 = tk.Frame(self.left_frame)

        self.frameL3.pack()

        self.frameL4 = tk.Frame(self.left_frame)

        self.frameL4.pack()

        self.frameL5 = tk.Frame(self.left_frame)

        self.frameL5.pack()

        self.frameL6 = tk.Frame(self.left_frame)

        self.frameL6.pack()

        self.frameL7 = tk.Frame(self.left_frame)

        self.frameL7.pack()

        self.frameL8 = tk.Frame(self.left_frame)

        self.frameL8.pack()

        self.frameL9 = tk.Frame(self.left_frame)

        self.frameL9.pack()

        self.frameL10 = tk.Frame(self.left_frame)

        self.frameL10.pack()

        self.frameTablelabel = tk.Frame(self.left_frame)
        self.frameTablelabel.pack()

        if section == 1:
            tk.Label(self.frameL1, bg='black', text='Table list',
                    font=("Helvetica", 20, "bold "), fg="white", borderwidth=5).pack()

        elif section == 2:
            tk.Label(self.frameL1, bg='black', text='Switch table',
                     font=("Helvetica", 20, "bold "), fg="white", borderwidth=5).pack()

        self.btn_tb = [[0 for x in range(121)] for y in range(1)]
        for i in range(0, 15):
            self.btn_tb[0][i] = tk.Button(self.frameL3, text='', font=("Helvetica", 20, "bold "),background="grey20",fg='white', width=4, height=2,
                      command='')
            self.btn_tb[0][i].pack(side=tk.LEFT)

        for i in range(15, 30):
            self.btn_tb[0][i] = tk.Button(self.frameL4, text='', font=("Helvetica", 20, "bold "),background="grey20",fg='white', width=4, height=2,
                                          command='')
            self.btn_tb[0][i].pack(side=tk.LEFT)
        for i in range(30, 45):
            self.btn_tb[0][i] = tk.Button(self.frameL5, text='', font=("Helvetica", 20, "bold "),background="grey20",fg='white', width=4, height=2,
                                          command='')
            self.btn_tb[0][i].pack(side=tk.LEFT)
        for i in range(45, 60):
            self.btn_tb[0][i] = tk.Button(self.frameL6, text='', font=("Helvetica", 20, "bold "),background="grey20",fg='white', width=4, height=2,
                                          command='')
            self.btn_tb[0][i].pack(side=tk.LEFT)
        for i in range(60, 75):
            self.btn_tb[0][i] = tk.Button(self.frameL7, text='', font=("Helvetica", 20, "bold "),background="grey20",fg='white', width=4, height=2,
                                          command='')
            self.btn_tb[0][i].pack(side=tk.LEFT)
        for i in range(75, 90):
            self.btn_tb[0][i] = tk.Button(self.frameL8, text='', font=("Helvetica", 20, "bold "),background="grey20",fg='white', width=4, height=2,
                                          command='')
            self.btn_tb[0][i].pack(side=tk.LEFT)
        for i in range(90, 105):
            self.btn_tb[0][i] = tk.Button(self.frameL9, text='', font=("Helvetica", 20, "bold "),background="grey20",fg='white', width=4, height=2,
                                          command='')
            self.btn_tb[0][i].pack(side=tk.LEFT)
        for i in range(105, 120):
            self.btn_tb[0][i] = tk.Button(self.frameL10, text='', font=("Helvetica", 20, "bold "),background="grey20",fg='white', width=4, height=2,
                                          command='')
            self.btn_tb[0][i].pack(side=tk.LEFT)



        self.btnTR1.config(text='Delivery', font=("Helvetica", 20, "bold "),bg='sea green', command=lambda: self.address_page('delivery') )

        self.btnTR2.config(text='Take Away', font=("Helvetica", 20, "bold "),bg='sea green',command=lambda: self.take_away())

        self.btnTR3.config(text='Check \n Deli./T.Away', font=("Helvetica", 20, "bold "),bg='darkorange3',command=lambda:self.check_deli_take_away())

        self.btnTR4.config(text='Report', font=("Helvetica", 20, "bold "),bg='darkorange3', command=lambda:self.report())

        self.btnTR5.config(text='',background="grey20", font=("Helvetica", 20, "bold "),command='')

        self.btnTR6.config(text='',background="grey20",command='')

        self.btnTR7.config(text='',background="grey20",command='')

        self.btnTR8.config(text='LogOut',bg='red4', command=lambda:self.address_page('logout'))

        self.btnHome.config(command="")

        self.btnBack.config (command = "")

        if section == 1:
            self.main_page_table()

        elif section == 2:
            self.switch_table(order_id,table_id)

    def __init__(self, root,id):
        self.root = root
        self.root.geometry('1920x1080')
        self.root.title("PizzaHut_Menu_Ordering_System")

        self.conn = cx_Oracle.connect('G2_team03/Abc12345@144.214.177.102/xe')
        self.cur = self.conn.cursor()

        self.frameRt = tk.Frame(self.root ,background="black")
        self.frameRt.pack(fill="both")

        self.id=str(id)
        #print(self.id)
        shop_name=[]
        cur = self.conn.cursor()
        cur.execute("select shop_name from shop where shop_id = '" + str(self.id) + "'")
        for row in cur.fetchall():
            shop_name.append(row)

        self.date = datetime.datetime.now()
        self.date_label = tk.Label(self.frameRt, text='PizzaHut - '+str(shop_name[0])[2:-3]+'      ' + str(self.date.strftime('%Y/%m/%d')+'      '),font=("courier new", 20, "bold"),bg='black',fg = "white" )
        self.date_label.pack(side=tk.LEFT)

        self.clock1 = clock.Clock(self.frameRt)
        self.clock1.pack(side=tk.LEFT)
        self.clock1.configure(font=("courier new", 20, "bold"),bg='black',fg = "white")




        self.bottom_nvaigation = Frame(self.root, background="black",borderwidth=5,
                                       relief="ridge", height=35)
        self.bottom_nvaigation.pack(side="bottom",fill="both",
                                    )



        self.right_frame = Frame(self.root, background="black",
                                 borderwidth=5, relief="ridge")
        self.right_frame.pack(side="right",fill="both",
                              )

        self.frame_bottom_nvaigation = tk.Frame(self.bottom_nvaigation)
        self.frame_bottom_nvaigation.pack()

        self.btnBack = tk.Button(self.frame_bottom_nvaigation, text='< BACK', font=("Helvetica", 10, "bold "), width=88, height=1,bg="black",fg="white")
        self.btnBack.pack(side=tk.LEFT)

        self.btnHome = tk.Button(self.frame_bottom_nvaigation, text='O HOME', font=("Helvetica", 10, "bold "), width=88, height=1,bg="black",fg="white",command=lambda: self.home_page())
        self.btnHome.pack(side=tk.LEFT)



        self.frameR1 = tk.Frame(self.right_frame)

        self.frameR1.pack()

        self.frameR2 = tk.Frame(self.right_frame)

        self.frameR2.pack()

        self.frameR3 = tk.Frame(self.right_frame)

        self.frameR3.pack()

        self.frameR4 = tk.Frame(self.right_frame)

        self.frameR4.pack()

        self.frameR5 = tk.Frame(self.right_frame)

        self.frameR5.pack()

        self.frameR6 = tk.Frame(self.right_frame)

        self.frameR6.pack()

        self.frameR7 = tk.Frame(self.right_frame)

        self.frameR7.pack()

        self.frameR8 = tk.Frame(self.right_frame)

        self.frameR8.pack()

        self.btnTR1 = tk.Button(self.frameR1, text='', font=("Helvetica", 20, "bold "),background="grey20",fg='white', width=10, height=2)
        self.btnTR1.pack(side=tk.LEFT)
        self.btnTR2 = tk.Button(self.frameR2, text='', font=("Helvetica", 20, "bold "),background="grey20",fg='white', width=10, height=2)
        self.btnTR2.pack(side=tk.LEFT)
        self.btnTR3 = tk.Button(self.frameR3, text='', font=("Helvetica", 20, "bold "),background="grey20",fg='white', width=10, height=2)
        self.btnTR3.pack(side=tk.LEFT)
        self.btnTR4 = tk.Button(self.frameR4, text='', font=("Helvetica", 20, "bold "),background="grey20",fg='white', width=10, height=2)
        self.btnTR4.pack(side=tk.LEFT)
        self.btnTR5 = tk.Button(self.frameR5, text='', font=("Helvetica", 20, "bold "),background="grey20",fg='white', width=10, height=2)
        self.btnTR5.pack(side=tk.LEFT)
        self.btnTR6 = tk.Button(self.frameR6, text='', font=("Helvetica", 20, "bold "),background="grey20",fg='white', width=10, height=2)
        self.btnTR6.pack(side=tk.LEFT)
        self.btnTR7 = tk.Button(self.frameR7, text='', font=("Helvetica", 20, "bold "),background="grey20",fg='white', width=10, height=2)
        self.btnTR7.pack(side=tk.LEFT)
        self.btnTR8 = tk.Button(self.frameR8, text='', font=("Helvetica", 20, "bold "),background="grey20",fg='white', width=10, height=2)
        self.btnTR8.pack(side=tk.LEFT)




        self.table_id_nm=""
        self.add_list=""
        self.del_list =''
        self.address_list = ""
        self.delivery_list=[]
        self.add_pd_list=[]
        self.add_qty_list=[]
        self.add_link_list=[]
        self.add_link_price_list=[]
        self.set_option_count=0
        self.creator_option_count = 0
        self.add_pd_location=''
        self.table_people_no=''
        self.member_id=''
        self.update_order_id=[]

        self.main_page(1,[],'')

def main(id, window):
    root = tk.Tk()
    Gui(root,id)
    window.destroy()
    root.mainloop()


if __name__ == '__main__':
    sys.exit(main())

