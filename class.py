from tkinter import *
from tkinter.ttk import Scale
from tkinter import colorchooser,filedialog,messagebox
import PIL.ImageGrab as ImageGrab
import cv2
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

class Draw():
    def __init__(self,root):

#Defining title and Size of the Tkinter Window GUI
        self.root =root
        self.root.state("zoomed") #maximize
        self.root.title("Copy Assignment Painter")
        #self.root.geometry("800x600")
        self.root.configure(background="white")
        self.root.resizable(False,False)
#         self.root.resizable(0,0)
 
#variables for pointer and Eraser   
        self.pointer= "white"
        self.erase="white"
        

#Widgets for Tkinter Window
    
# Configure the alignment , font size and color of the text
        text=Text(root)
        text.tag_configure("tag_name", justify='center', font=('arial',25),background='#292826',foreground='orange')

# Insert a Text
        text.insert("1.0", "Drawing Application in Python")

# Add the tag for following given text
        text.tag_add("tag_name", "1.0", "end")
        text.pack()
        
      

# Reset Button to clear the entire screen 
        self.clear_screen= Button(self.root,text="Clear Screen",bd=4,bg='yellow',command= lambda : self.background.delete('all'),width=9,relief=RIDGE)
        self.clear_screen.place(x=500,y=500)

# Save Button for saving the image in local computer
        self.save_btn= Button(self.root,text="PREDICT",bd=4,bg='green',command=self.predict,width=20,relief=RIDGE)
        self.save_btn.place(x=600,y=500)


#Defining a background color for the Canvas 
        self.background = Canvas(self.root,bg='black',bd=10,relief=GROOVE,height=200,width=200)
        self.background.place(x=545,y=150)  


#Bind the background Canvas with mouse click
        self.background.bind("<B1-Motion>",self.paint)
        
    #################### Label predict ######################
        self.LabelPred = Label(text="predict= ",font=22,bg="red")
        self.LabelPred.place(x=600,y=400)
        
    ################################## training #########################################
        digits=cv2.imread("C:/Users/persian computer/Desktop/digit/digits.png",cv2.IMREAD_GRAYSCALE)
        rows=np.vsplit(digits,50)
        cells=[]
        cells2=[]
        for row in rows :
            row_cells=np.hsplit(row,100)
            for cell in row_cells:
                cells.append(cell)
                #all in one column 
                cells2.append(cell.flatten())
        #############
        test_cells_flat = []
        test_cells_flat=np.array(test_cells_flat,dtype=np.float32)
        #cells2 is a list and in openCV we need numpy array because it is faster than list
        cells2=np.array(cells2,dtype=np.float32)
        n=np.arange(10)
        targets=np.repeat(n,500)
        
#        self.knn=KNeighborsClassifier(n_neighbors=6,metric='minkowski')
#        self.knn.fit(cells2,targets)
        
        self.knn=cv2.ml.KNearest_create()
        self.knn.train(cells2,cv2.ml.ROW_SAMPLE,targets)
    #####################################################################################

    def paint(self,event):       
        x1,y1 = (event.x-2), (event.y-2)  
        x2,y2 = (event.x+2), (event.y+2)  

        self.background.create_oval(x1,y1,x2,y2,fill=self.pointer,outline=self.pointer,width=25)

    def select_color(self,col):
        pass
    def eraser(self):
        pass
    def canvas_color(self):
        pass
    def predict(self):
        
        ############################## save image ################################
        try:
            # self.background update()
#            file_ss =filedialog.asksaveasfilename(defaultextension='jpg')
            #print(file_ss)
            x=self.root.winfo_rootx() + self.background.winfo_x()
            #print(x, self.background.winfo_x())
            y=self.root.winfo_rooty() + self.background.winfo_y()
            #print(y)

            x1= x + self.background.winfo_width() 
            #print(x1)
            y1= y + self.background.winfo_height()
            #print(y1)
            ImageGrab.grab().crop((x+5 , y+5, x1+5, y1+5)).save("C:/Users/persian computer/Desktop/test.png")
#            messagebox.showinfo('Screenshot Successfully Saved as' + str(file_ss))

        except:
            print("Error in saving the screenshot")
        
        ######################################### predict ##############################
        my_digit=cv2.imread("C:/Users/persian computer/Desktop/test.png",cv2.IMREAD_GRAYSCALE)
        my_digit = cv2.resize(my_digit, (20, 20)) 
        ####################
        my_test_flat=[]
        my_test_flat.append(my_digit.flatten())
        my_test_flat=np.array(my_test_flat,dtype=np.float32)
        
        my_predict = self.knn.predict(my_test_flat)
        ret,result,neighbours,dist=self.knn.findNearest(my_test_flat,k=3)
        print(result)
        #print(neighbours.score(my_test_flat,my_predict))
        self.LabelPred.configure(text=result)
        
        
        #####################
#        cv2.imshow("digits",my_digit)
#        cv2.waitKey(0)
#        cv2.destroyAllWindows()
        #####################
        #cv2.imshow("rtwo",my_digit)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        

###############################################################################################


if __name__ =="__main__":
    root = Tk()
    p= Draw(root)
    root.mainloop()