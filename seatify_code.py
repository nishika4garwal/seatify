from tkinter import * #for creating a GUI platform
import mysql.connector 
from PIL import ImageTk,Image #to display images on the tkinter window
import random
import pymysql


######################CONNECTING SQL AND PYTHON#############################################
mydb=mysql.connector.connect(host="localhost",user="root",passwd="gibberish@1234")
mycursor=mydb.cursor()


#######################DEFINING OTHER USEFUL FUNCTIONS######################################
def clear_current_page():
    # Destroy all widgets inside the root window
    for widget in window.winfo_children():
        widget.destroy()

def switch_to_nextpg(next_page_function):
    global current_page
    # Clear the current page
    clear_current_page()
    # Call the next page function
    next_page_function()
    # Update current page
    current_page = "next_page"

def switch_to_previouspg(previous_page_function):
    global current_page
    # Clear the current page
    clear_current_page()
    # Call the previous page function
    previous_page_function()
    # Update current page
    current_page = "previous_page"


#####################CREATING TKINTER WINDOW#####################################
window = Tk()
window.title('Seatify: book tickets at one go!')
window.geometry("992x556")
window.minsize(width=992, height=556)
window.maxsize(width=992, height=556)
window.configure(bg = "#ffffff")
######################CREATING A FUNTION FOR CANVAS##############################
def canvasdefinition():
    global canvas
    canvas = Canvas(window,bg = "#ffffff",height = 600,width = 1000,bd = 0,highlightthickness = 0,relief = "ridge")
    canvas.place(x = 0, y = 0)

########################################### checkout page #############################################
def checkout():
    global bgimg,pay_button_img,backbtnimg
    canvasdefinition()
    
    try:
        bgimg = PhotoImage(file="imgs/bg-after.png")
        canvas.create_image(496.0, 278.0, image=bgimg)
    except Exception as e:
        print("Error loading background image:", e)

    def click():
        switch_to_previouspg(seatmatrix)

    def payment_completed():
        popup_window = Toplevel(window)
        popup_window.geometry("400x100")
        popup_window.title("Payment Completed")
        popup_window.geometry("+550+190")
        label = Label(popup_window, text="Your payment has been completed!")
        label.pack()
        popup_window.focus_set()

    def goto():
        switch_to_nextpg(homepage)

    def combine():
        payment_completed()
        window.after(1000, goto)

    try:
        pay_button_img = PhotoImage(file="imgs/pay_button.png")
        pay_button = Button(image=pay_button_img, borderwidth=0, highlightthickness=0, relief="flat",
                            cursor="hand2", activebackground="white", bg="white", command=combine)
        pay_button.place(x=395, y=418, width=229, height=40)
    except Exception as e:
        print("Error loading payment button image:", e)

    try:
        backbtnimg = PhotoImage(file="imgs/backbtn.png")
        backbtn = Button(image=backbtnimg, borderwidth=0, highlightthickness=0, relief="flat",
                         cursor="hand2", activebackground="black", bg="black", command=click)
        backbtn.place(x=903, y=12, width=73, height=27)
    except Exception as e:
        print("Error loading back button image:", e)


     # Calculate payment and create labels
    per_seat_cost = 500
    gst_per_seat = 90
    num_of_seats_selected = len(selected_seats)
    pay = per_seat_cost * num_of_seats_selected
    gst_pay = gst_per_seat * num_of_seats_selected
    total_pay = pay + gst_pay

    pay_str = f"Pay Rs.{total_pay}"
    pay_label = Label(window, text=pay_str, bg="#A11B1B", fg="white", font=("Arial", 10, "bold"))
    pay_label.place(x=470, y=426)

    gst_pay_str = f"Rs.{gst_pay}"
    gst_pay_label = Label(window, text=gst_pay_str, bg="white", fg="grey")
    gst_pay_label.place(x=553, y=240)

    total_pay_str = f"Rs.{pay}"
    total_pay_label = Label(window, text=total_pay_str, bg="white", fg="black")
    total_pay_label.place(x=553, y=146)

    sub_total_pay_str = f"Rs.{total_pay}"
    sub_total_pay_label = Label(window, text=sub_total_pay_str, bg="white", fg="black")
    sub_total_pay_label.place(x=553, y=283)

    # Define the string for selected seats
    seat_names_str = "Seats Selected:\n"

    # Iterate through the list of selected seats
    for seat in selected_seats:
        # Extract the row and column from the seat tuple
        seat_row = seat[0]
        seat_col = seat[1]

        # Convert column to string
        seat_col_str = str(seat_col)

        # Append the row and column to the seat_names_str
        seat_names_str += f"{seat_row}-{seat_col_str}\n"

    # Create a label with the constructed string and place it in the new window
    seat_names_label = Label(window, text=seat_names_str, bg="white", fg="black")
    seat_names_label.place(x=350, y=146)


######################################### seat matrix ######################################
def seatmatrix():
    canvasdefinition()

    def click():
        switch_to_previouspg(func)
    def goto():
        switch_to_nextpg(checkout)

    # Load and set the background image
    seats_img = PhotoImage(file="imgs\\seat_bg_final.png")
    background = canvas.create_image(496.0, 278.0, image=seats_img)


    # defining back button
    backbtnimg=PhotoImage(file="imgs\\backbtn.png")
    backbtn=Button(image = backbtnimg,borderwidth = 0,highlightthickness = 0,relief = "flat",cursor="hand2",activebackground="white",bg="white",
                   command=click)
    backbtn.place(x=820, y=12, width= 73 ,height=27)


    # defining next button
    nextbtnimg=PhotoImage(file="imgs\\next.png")
    nextbtn=Button(image = nextbtnimg,borderwidth = 0,highlightthickness = 0,relief = "flat",cursor="hand2",activebackground="white",bg="white",
                   command=goto)
    nextbtn.place(x=903, y=12, width= 73 ,height=27)

    def select_seat(row, col):
        """Select a seat in the seating arrangement."""
        # Convert row to a character and form the seat key
        seat_key = (chr(row), col)
    
        # Retrieve the button corresponding to the seat
        btn = seat_states.get(seat_key)
    
        if btn:
            # Define the file path for the green seat image
            import os
            file_path = os.path.join("imgs", f"seat_{col}green.png")
        
            try:
                # Load the green seat image
                img = PhotoImage(file=file_path)
            
                # Update the button state and image
                btn.config(state=DISABLED, image=img)
            
                # Keep a reference to the new image to prevent garbage collection
                btn.image = img
            
                # Add the seat key to the selected seats list
                selected_seats.append(seat_key)
            except Exception as e:
                print(f"Error loading image: {file_path}\n{e}")
        else:
            print(f"Seat key {seat_key} not found in seat_states.")

    
        # Define seat button positions and states
    seat_states = {}
    global selected_seats
    selected_seats=[]

    def create_seat_button(row, col, x, y):
        """Create a seat button at the specified location."""
        # Define file path for seat image
        file_path = f"imgs/seat_{col}white.png"
    
        # Try to load the seat image
        try:
            seat_img = PhotoImage(file=file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {file_path}\n{e}")
            return None
    
        # Create the seat button
        seat_btn = Button(window, image=seat_img, borderwidth=0, highlightthickness=0, relief="flat", cursor="hand2",command=lambda:select_seat(row,col))
        seat_btn.place(x=x, y=y, width=61, height=56)
    
        # Keep a reference to the button and its image to prevent garbage collection
        seat_btn.image = seat_img
    
        # Return the seat button
        return seat_btn

    # Create seat buttons in a grid
    x_start = 91
    y_start = 75
    row_range = range(69, 64, -1)
    col_range = range(1,6)

    for row in row_range:
        for col in col_range:
            # Calculate seat button position
            x = x_start + (col - 1) * 78
            y = y_start + (69 - row) * 71
        
            # Create seat button and save its state
            seat_button = create_seat_button(row, col, x, y)
            if seat_button:
             seat_key = (chr(row), col)
             seat_states[seat_key] = seat_button


    x_start=528
    y_start=75
    row_range=range(69,64,-1)
    col_range=range(6,11)


    for row in row_range:
        for col in col_range:
            # Calculate seat button position
            x = x_start + (col - 6) * 78
            y = y_start + (69 - row) * 71
        
            # Create seat button and save its state
            seat_button = create_seat_button(row, col, x, y)
            if seat_button:
                seat_key = (chr(row), col)
                seat_states[seat_key] = seat_button


    # Selecting Random Seats
    randomly_selected_seats=[]

    def randomly_select():
        # Define the range of seats to randomly select
        num_of_seats = random.randint(1, 10)
    
        # Get a list of available seats
        available_seats = list(seat_states.keys())
    
        # Select random seats from available seats
        selected_random_seats = random.sample(available_seats, num_of_seats)
    
   

        for seat in selected_random_seats:
            # Add the randomly selected seat to the list
            randomly_selected_seats.append(seat)
        
            # Retrieve the seat button
            seat_button = seat_states[seat]
        
            # Extract the column from the seat key
            seat_col = seat[1]
        
            # Define the file path for the red seat image
            file_path = f"imgs/seat_{seat_col}red.png"
        
            try:
                # Load the red seat image
                red_img = PhotoImage(file=file_path)
            
                # Update the seat button to be disabled and set the new image
                seat_button.config(state=DISABLED, image=red_img)
            
                # Keep a reference to the new image to prevent garbage collection
                seat_button.image = red_img
            
            except Exception as e:
                print(f"Failed to load image: {file_path}\n{e}")

    randomly_select()   
    # Run the application
    window.mainloop()


#################################### timings page ###########################################
global func

def idiots_3():
    global idiot3_page,time1,time2,time3,backbtn,func
   
    canvasdefinition()

    def click():
        switch_to_previouspg(mov["3idiots"].display)
    def goto():
        global func
        func=idiots_3
        switch_to_nextpg(seatmatrix)

        
    backbtn=PhotoImage(file=f"imgs\\backbtn.png")
    back=Button(image = backbtn,borderwidth = 0,highlightthickness = 0,relief = "flat",cursor="hand2",command=click)
    back.place(x=898, y=12, width= 73 ,height=27 )
   
    idiot3_page = PhotoImage(file=f"imgs\\Desktop - 9.png")
    background = canvas.create_image(496.0, 278.0,image=idiot3_page)

    time1= PhotoImage(file = f"imgs\\3_35.png")
    time_1= Button(image = time1,borderwidth = 0,highlightthickness = 0,relief = "flat",cursor="hand2",command=goto)
    time_1.place(x =33.09, y = 161.21,width = 81.04,height = 34.28,)

    time2= PhotoImage(file = f"imgs\\12_45.png")
    time_2= Button(image = time2,borderwidth = 0,highlightthickness = 0,relief = "flat",cursor="hand2",command=goto)
    time_2.place(x =33.09, y = 311.21,width = 81.04,height = 34.28)

    time3= PhotoImage(file = f"imgs\\4_55.png")
    time_3= Button(image = time3,borderwidth = 0,highlightthickness = 0,relief = "flat",cursor="hand2",command=goto)
    time_3.place(x =149.09, y = 161.21,width = 81.04,height = 34.28)

def avengers():
   global avn_page,pvr_1,background,pvr_2,pvr_3,pvr_4,pvr_5,backbtn,func
   
   canvasdefinition()

   def click():
        switch_to_previouspg(mov["Avengers"].display)
   def goto():
       global func
       func=avengers
       switch_to_nextpg(seatmatrix)

   backbtn=PhotoImage(file=f"imgs\\backbtn.png")
   back=Button(image = backbtn,borderwidth = 0,highlightthickness = 0,relief = "flat",cursor="hand2",command=click)
   back.place(x=898, y=12, width= 73 ,height=27 )
   
   avn_page = PhotoImage(file=f"imgs\\Desktop - 10.png")
   background = canvas.create_image(496.0, 278.0,image=avn_page)
   
   pvr_1=PhotoImage(file=f"imgs\\Group 31.png")
   pvr_11 = Button(image = pvr_1,borderwidth = 0,highlightthickness = 0,relief = "flat",cursor="hand2",command=goto)
   pvr_11.place(x =33, y =161 ,width = 81.22,height = 35)
   
   pvr_2=PhotoImage(file=f"imgs\\Group 14.png")
   pvr_12 = Button(image = pvr_2,borderwidth = 0,highlightthickness = 0,relief = "flat",cursor="hand2",command=goto)
   pvr_12.place(x =144, y =161 ,width = 81.22,height = 34.7)
   
   pvr_3=PhotoImage(file=f"imgs\\Group 17.png")
   pvr_13 = Button(image = pvr_3,borderwidth = 0,highlightthickness = 0,relief = "flat",cursor="hand2",command=goto)
   pvr_13.place(x =247, y =311 ,width = 81.22,height = 35.7)
   
   pvr_5=PhotoImage(file=f"imgs\\Group 16.png")
   pvr_15 = Button(image = pvr_5,borderwidth = 0,highlightthickness = 0,relief = "flat",cursor="hand2",command=goto)
   pvr_15.place(x =33, y =311 ,width = 81.22,height = 34.7)
   
   pvr_4=PhotoImage(file=f"imgs\\Group 15.png")
   pvr_14 = Button(image = pvr_4,borderwidth = 0,highlightthickness = 0,relief = "flat",cursor="hand2",command=goto)
   pvr_14.place(x =140, y =311 ,width = 81.22,height = 34.7)
   
def star():
   global star_page,pvr_1,background,pvr_2,pvr_3,pvr_4,pvr_5,backbtn,func
   
   canvasdefinition()

   def click():
        switch_to_previouspg(mov["A Star is Born"].display)
   def goto():
       global func
       func=star
       switch_to_nextpg(seatmatrix)

   backbtn=PhotoImage(file=f"imgs\\backbtn.png")
   back=Button(image = backbtn,borderwidth = 0,highlightthickness = 0,relief = "flat",cursor="hand2",command=click)
   back.place(x=898, y=12, width= 73 ,height=27 )
   
   star_page = PhotoImage(file=f"imgs\\Desktop - 11.png")
   background = canvas.create_image(496.0, 278.0,image=star_page)
   
   pvr_1=PhotoImage(file=f"imgs\\Group 19.png")
   pvr_11 = Button(image = pvr_1,borderwidth = 0,highlightthickness = 0,relief = "flat",cursor="hand2",command=goto)
   pvr_11.place(x =33, y =161 ,width = 81.22,height = 34.7)
   
   pvr_2=PhotoImage(file=f"imgs\\Group 20.png")
   pvr_12 = Button(image = pvr_2,borderwidth = 0,highlightthickness = 0,relief = "flat",cursor="hand2",command=goto)
   pvr_12.place(x =144, y =161 ,width = 81.22,height = 34.7)
   
   pvr_3=PhotoImage(file=f"imgs\\Group 21.png")
   pvr_13 = Button(image = pvr_3,borderwidth = 0,highlightthickness = 0,relief = "flat",cursor="hand2",command=goto)
   pvr_13.place(x =33, y =311 ,width = 81.22,height = 34.7)
   
   pvr_5=PhotoImage(file=f"imgs\\Group 22.png")
   pvr_15 = Button(image = pvr_5,borderwidth = 0,highlightthickness = 0,relief = "flat",cursor="hand2",command=goto)
   pvr_15.place(x =33, y =453 ,width = 81.22,height = 34.7)
   
   pvr_4=PhotoImage(file=f"imgs\\Group 23.png")
   pvr_14 = Button(image = pvr_4,borderwidth = 0,highlightthickness = 0,relief = "flat",cursor="hand2",command=goto)
   pvr_14.place(x =149, y =453 ,width = 81.22,height = 34.7)

def ZNMD():
    global mainimg,time1,time2,time3,time4,backbtn,func
    
    canvasdefinition()

    def click():
        switch_to_previouspg(mov["Zindagi Na Milegi Dubara"].display)
    def goto():
        global func
        func=ZNMD
        switch_to_nextpg(seatmatrix)

    backbtn=PhotoImage(file=f"imgs\\backbtn.png")
    back=Button(image = backbtn,borderwidth = 0,highlightthickness = 0,relief = "flat",cursor="hand2",command=click)
    back.place(x=898, y=12, width= 73 ,height=27 )
    
    mainimg = PhotoImage(file = f"imgs\\ZNMD_book.png")
    background = canvas.create_image(496.0, 278.0,image=mainimg)

    time1= PhotoImage(file = f"imgs\\3_35.png")
    time_1= Button(image = time1,borderwidth = 0,highlightthickness = 0,relief = "flat",cursor="hand2",command=goto)
    time_1.place(x =33.09, y = 161.21,width = 81.04,height = 34.28)

    time2= PhotoImage(file = f"imgs\\12_45.png")
    time_2= Button(image = time2,borderwidth = 0,highlightthickness = 0,relief = "flat",cursor="hand2",command=goto)
    time_2.place(x =33.09, y = 311.21,width = 81.04,height = 34.28)

    time3= PhotoImage(file = f"imgs\\12_05.png")
    time_3= Button(image = time3,borderwidth = 0,highlightthickness = 0,relief = "flat",cursor="hand2",command=goto)
    time_3.place(x =33.09, y = 453.21,width = 81.04,height = 34.28)

    time4= PhotoImage(file = f"imgs\\4_55.png")
    time_4= Button(image = time4,borderwidth = 0,highlightthickness = 0,relief = "flat",cursor="hand2",command=goto)
    time_4.place(x =149.09, y = 161.21,width = 81.04,height = 34.28)


######################################### each movie page #############################################
def switch_to_next_pg(arg):
    switch_to_nextpg(arg)    

# defining book tickets button image
global btimg
btimg=PhotoImage(file="imgs\\BOOK TICKETS.png")  
class Movies():
    global btimg
    btimg=PhotoImage(file="imgs\\BOOK TICKETS.png")
    def __init__(self,bgimage,book_tickets_fun,book_tickets_arg):
        self.bgimage=bgimage
        self.book_tickets_fun=book_tickets_fun
        self.book_tickets_arg=book_tickets_arg
    def click(self):
        switch_to_previouspg(homepage)
        

    def display(self,):
        canvasdefinition()
        # defining background image and buttons
        background = canvas.create_image(496.0, 278.0,image=self.bgimage)
        btimgbtn1=Button(image = btimg,borderwidth = 0,highlightthickness = 0,relief = "flat",cursor="hand2",activebackground="black",bg="black",
                         command=self.book_tickets)
        btimgbtn1.place(x =432, y = 297,width = 162.82,height = 45.83)

        # defining back button
        global backbtnimg
        backbtnimg=PhotoImage(file="imgs\\backbtn.png")
        backbtn=Button(image = backbtnimg,borderwidth = 0,highlightthickness = 0,relief = "flat",cursor="hand2",activebackground="black",bg="black",
                       command=self.click)
        backbtn.place(x=903, y=12, width= 73 ,height=27)

# creating book tickets function
    def book_tickets(self):
        self.book_tickets_fun(self.book_tickets_arg)
        
  
l=["3idiots","Avengers","A Star is Born","Zindagi Na Milegi Dubara"]
list_arg=[idiots_3, avengers, star, ZNMD]
mov={}

for i in range(1,5):
    global img
    img=PhotoImage(file=f"imgs\\bg-image{i}.png")
    temp=Movies(img,switch_to_next_pg,list_arg[i-1])
    mov[l[i-1]]=temp

# we can display by just name of movie
#mov["3idiots"].display()


############################################ homepage #####################################
def homepage():
    global homepageimg,box1,box2,box3,box4

    def box1_click():
        switch_to_nextpg(mov["3idiots"].display)
    def box2_click():
        switch_to_nextpg(mov["Avengers"].display)
    def box3_click():
        switch_to_nextpg(mov["A Star is Born"].display)
    def box4_click():
        switch_to_nextpg(mov["Zindagi Na Milegi Dubara"].display)
        
    
    canvasdefinition()


    homepageimg = PhotoImage(file = f"imgs\\homepage.png")
    background = canvas.create_image(496.0, 278.0,image=homepageimg)
    
    box1= PhotoImage(file = f"imgs\\3Idiots.png")
    box_1= Button(image = box1,borderwidth = 0,highlightthickness = 0,relief = "flat",cursor="hand2",command=box1_click)
    box_1.place(x =25, y = 240,width = 209,height = 300)

    box2= PhotoImage(file = f"imgs\\Avengers.png")
    box_2= Button(image = box2,borderwidth = 0,highlightthickness = 0,relief = "flat",cursor="hand2",command=box2_click)
    box_2.place(x =267, y = 240,width = 209,height = 300)

    box3= PhotoImage(file = f"imgs\\aStarIsBorn.png")
    box_3= Button(image = box3,borderwidth = 0,highlightthickness = 0,relief = "flat",cursor="hand2",command=box3_click)
    box_3.place(x =509, y = 240,width = 209,height = 300)

    box4= PhotoImage(file = f"imgs\\ZNMD.png")
    box_4= Button(image = box4,borderwidth = 0,highlightthickness = 0,relief = "flat",cursor="hand2",command=box4_click)
    box_4.place(x =751, y = 240,width = 209,height = 300)


    #the banners will change time to time
    banner1 = ImageTk.PhotoImage(Image.open("imgs\\taylorswift.png"))
    banner2 = ImageTk.PhotoImage(Image.open("imgs\\avatar.png"))
    banner3 = ImageTk.PhotoImage(Image.open("imgs\\harrypotter.png"))
    banner4 = ImageTk.PhotoImage(Image.open("imgs\\skyfall.png"))

    dots1 = ImageTk.PhotoImage(Image.open("imgs\\tsdots.png"))
    dots2 = ImageTk.PhotoImage(Image.open("imgs\\avatardots.png"))
    dots3 = ImageTk.PhotoImage(Image.open("imgs\\harrypotterdots.png"))
    dots4 = ImageTk.PhotoImage(Image.open("imgs\\skyfall dots.png"))

    l=Label(window)
    l.place(x=27,y=35,height=154,width=938)

    l1=Label(window)
    l1.place(x=449,y=203,height=19,width=86)
    
    banners=[banner1,banner2,banner3,banner4]
    dots=[dots1,dots2,dots3,dots4]
    
    def change_image(nextindex,value):
        global change
        if value=="continue":
            l.configure(image=banners[nextindex])
            l1.configure(image=dots[nextindex])
            change=window.after(2000, lambda: change_image((nextindex+1) % len(banners),"continue"))
        else:
            window.after_cancel(change)       
    change_image(0,"continue")

####################################### login and signup pages #############################
def login_pg():
    
    class login:
        def __init__(self,window):
            global log_btn
            log_btn=PhotoImage(file="imgs//loginbtn.png")
            self.window=window
            self.window.title('Seatify: book tickets at one go!')
            self.window.geometry("992x556")
            self.window.minsize(width=992, height=556)
            self.window.maxsize(width=992, height=556)
            self.window.configure(bg = "black")
            self.window.resizable(False,False)
            self.bg=PhotoImage(file="imgs//loginPage.png")
            self.bg_image=Label(self.window,image=self.bg).place(x=0,y=0,relwidth=1,relheight=1)
            self.txt_user=Entry(font=("times new roman",15),bg="white")
            self.txt_user.place(x =360.41, y = 203,width = 300,height = 48)
            login_up_btn=Button(image=log_btn,borderwidth=0,highlightthickness=0,relief="flat",activebackground="#d9d9d9",cursor="hand2",
                                bg="#d9d9d9",
                                command=self.verifykey).place(x =390, y = 283.52,width = 240.93,height = 45.24)
            sign_writeup=Button(text="Signup",fg="#bb2020",activebackground="#d9d9d9",bg="#d9d9d9",bd=0,font=("Lato",8,"bold"),
                                cursor="hand2",command=self.signup_page).place(x =537, y = 477)
        def veri(self,primary_key):
         try:
          con = pymysql.connect(host="localhost", user="root", passwd="gibberish@1234", db="userdata")
          cursor = con.cursor()
          query = f"SELECT * FROM data WHERE email='{primary_key}'"
          cursor.execute(query)
          result = cursor.fetchone()
          if result:
            return True  # Primary key exists
          else:
            return False  # Primary key does not exist
         except pymysql.Error as e:
          print("Error:", e)
          return False  # Error occurred, assume primary key does not exist
         finally:
          if con:
            con.close()

        def verifykey(self):
         primary_key = self.txt_user.get()
         if self.veri(primary_key):
           self.click()  # Call the click method if primary key exists
         else:
           messagebox.showerror('Error', 'Account does not exist')
           

        def signup_page(self):
          switch_to_previouspg(signup_pg)
        def click(self):
         switch_to_nextpg(homepage)
    
    # Assuming Signup is the class representing the signup page
    # Add any additional logic to show the signup page, e.g., signup_page.show()


    obj1=login(window)

def signup_pg():
  class signup:
    def __init__(self, window):
        global sign_btn
        sign_btn=PhotoImage(file=f"imgs//signupbtn.png")
        self.window = window
        self.window.title('Seatify: book tickets at one go!')
        self.window.geometry("992x556")
        self.window.minsize(width=992, height=556)
        self.window.maxsize(width=992, height=556)
        self.window.configure(bg="#ffffff")
        self.window.resizable(False, False)
        # bg image
        self.bg = PhotoImage(file=f"imgs//signuppage.png")
        self.bg_image = Label(self.window, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)

        self.txt_user = Entry(font=("times new roman", 15), bg="white")
        self.txt_user.place(x=76, y=178, width=293, height=48)
        self.txt_email = Entry(font=("times new roman", 15), bg="white")
        self.txt_email.place(x=76, y=256, width=293, height=48)
        self.txt_pass = Entry(font=("times new roman", 15), bg="white")
        self.txt_pass.place(x=76, y=334, width=293, height=48)
        login_in_case = Button(text="Login", fg="#bb2020", bg="#d9d9d9",activebackground="#d9d9d9", bd=0, font=("Lato", 9,"bold"),
                             cursor="hand2",command=self.login_page).place(x=253, y=455)

        sign_up_btn = Button(image=sign_btn,borderwidth=0,highlightthickness=0,relief="flat",activebackground="#d9d9d9",cursor="hand2",
                                command=self.click)
        sign_up_btn.place(x=107.1, y=412.58, width=229, height=40)
        sign_up_btn.configure(command=self.connect_database)
    def click(self):
        switch_to_nextpg(homepage)
    def login_page(self):
          switch_to_nextpg(login_pg)
    def clear(self):
        self.txt_user.delete(0,END)
        self.txt_email.delete(0,END)
        self.txt_pass.delete(0,END)
    def connect_database(self):
        if self.txt_user.get() == '' or self.txt_email.get() == '' or self.txt_pass.get() == '':
            messagebox.showerror('Error', 'All fields are required')
        else:
            try:
                con = pymysql.connect(host="localhost", user="root", passwd="gibberish@1234")
                mycursor = con.cursor()
                query = 'create database if not exists userdata'
                mycursor.execute(query)
                query = 'use userdata'
                mycursor.execute(query)
                query = 'create table if not exists data( username varchar(100), email varchar(100) primary key, password varchar(20))'
                mycursor.execute(query)
#id int auto_increment primary key
                # Check if email already exists
                email = self.txt_email.get()
                query = f"select * from data where email='{email}'"
                mycursor.execute(query)
                result = mycursor.fetchone()
                if result:
                    messagebox.showerror('Error', 'Account already exists for this email')
                else:
                    # Insert new account details
                    username = self.txt_user.get()
                    password = self.txt_pass.get()
                    query = f"insert into data (username, email, password) values ('{username}', '{email}', '{password}')"
                    mycursor.execute(query)
                    self.click()
                    
                    con.commit()
                   
            except Exception as e:
                messagebox.showerror('Error', 'Database connectivity issues: ' + str(e))
            finally:
                if con:
                    con.close()
            self.clear()
  obj=signup(window)
signup_pg()
window.mainloop()


