#APOD Viewer
import tkinter, requests,webbrowser
from tkinter import filedialog
from tkcalendar import DateEntry
from PIL import ImageTk,Image
from io import BytesIO

#Defining our window
root = tkinter.Tk()
root.title('APOD Photo Viewer')
root.iconbitmap('rocket.ico')

#Defining fonts and colors
text_font = ('Times New Roman', 14)
nasa_blue = "#043c93"
nasa_light_blue = "#7aa5d3"
nasa_red = "#ff1923"
nasa_white = "#ffffff"
root.config(bg=nasa_blue)

#Defining Functions
def get_request():
    '''Getting our request data from NASA API'''
    global response

    #Setting parameters for request
    #url= "https://api.nasa.gov/planetary/apod?api_key=AF48RXSucvaPVcHzSfARTSjbhAUHKUZBMR8yNjYW"
    url= "https://api.nasa.gov/planetary/apod"
    api_key= "AF48RXSucvaPVcHzSfARTSjbhAUHKUZBMR8yNjYW"
    date= calendar.get_date()
    #print(date)
    querystring ={'api_key':api_key,'date':date}

    #Calling_a_request_and_turning_it_into_a_python_usable_format
    response=requests.request("GET", url,params=querystring)
    response=response.json()
    #print(response)
    #Update output Label
    set_info()

def set_info():
    '''Updating output labels based on API Calls'''
    #Example Response
    '''{'date': '2021-12-29', 'explanation': "What and where are these large ovals? They are rotating storm clouds on Jupiter imaged last month by NASA's Juno spacecraft. In general, higher clouds are lighter in color, and the lightest clouds visible are the relatively small clouds that dot the lower oval. At 50 kilometers across, however, even these light clouds are not small.  They are so high up that they cast shadows on the swirling oval below. The featured image has been processed to enhance 
    color and contrast. Large ovals are usually regions of high pressure that span over 1000 kilometers and can last for years. The largest oval on Jupiter is the Great 
    Red Spot (not pictured), which has lasted for at least hundreds of years. Studying cloud dynamics on Jupiter with Juno images enables a better understanding of dangerous typhoons and hurricanes on Earth.   Follow APOD in English on: Facebook,  Instagram, Podcast, Reddit, or Twitter", 'hdurl': 'https://apod.nasa.gov/apod/image/2112/JupiterStorms_JunoGill_1024.jpg', 'media_type': 'image', 'service_version': 'v1', 'title': 'Giant Storms and High Clouds on Jupiter', 'url': 'https://apod.nasa.gov/apod/image/2112/JupiterStorms_JunoGill_1024.jpg'}'''

    #updating the picture date and explanation
    
    picture_date.config(text=response['date'])
    picture_explanation.config(text=response['explanation'])

    #we will need 3 image in other functions: an image, a thumbnail, & a full image
    global img 
    global thumb 
    global full_img
    url = response['url']

    if response['media_type'] == 'image':
        #grab the photo i.e. stored in our response
        
        img_response = requests.get(url,stream=True)


        #getting the content of the response and using BytesIO to open it as an Image
        #keep a reference to this image as this is what you can use to save as an image.(Image not PhotoImage)
        #create a full screen image for a second window
        img_data=img_response.content
        #print(img_data)
        img = Image.open(BytesIO(img_data))
        full_img = ImageTk.PhotoImage(img)
        #creating a thubnail
        thumb_data=img_response.content
        thumb=Image.open(BytesIO(thumb_data))
        thumb.thumbnail((200,200))
        thumb = ImageTk.PhotoImage(thumb)
        #setting thumbnail
        picture_label.config(image=thumb)
    elif response['media_type'] == 'video':
        picture_label.config(text=url,image='')
        webbrowser.open(url)

def full_photo():
    '''It will open full size photo in a new window'''
    top = tkinter.Toplevel
    top.title('Full APOD Photo')
    top.iconbitmap('rocket.ico')

    #Load the full image to the top window
    img_label=tkinter.Label(top,image=full_img)
    img_label.pack()

def save_photo():
    '''Save the photo to a location on your local device'''
    save_name=filedialog.asksaveasfilename(initialdir="./",title="Save Image",filetypes=(("JPEG", "*.jpg"), ("All Files","*.*")))
    img.save(save_name + ".jpg")

#Defining our layouts
#Create frames
input_frame = tkinter.Frame(root, bg=nasa_blue)
output_frame = tkinter.Frame(root, bg=nasa_white)
input_frame.pack()
output_frame.pack(padx=50, pady=(0,25))
#layout for the input frame
calendar = DateEntry(input_frame, width=10,font=text_font,background=nasa_blue, foreground=nasa_white)
submit_button = tkinter.Button(input_frame, text="Submit",font=text_font, bg=nasa_light_blue,command=get_request)
full_button = tkinter.Button(input_frame,text="Full Photo", font=text_font,bg=nasa_light_blue,command=full_photo)
save_button = tkinter.Button(input_frame,text="Save Photo", font=text_font,bg=nasa_light_blue,command=save_photo)
exit_button = tkinter.Button(input_frame,text="Exit", font=text_font,bg=nasa_red,command=root.destroy)

calendar.grid(row=0, column=0,padx=5,pady=10)
submit_button.grid(row=0,column=1,padx=5,pady=10,ipadx=35)
full_button.grid(row=0,column=2,padx=5,pady=10,ipadx=25)
save_button.grid(row=0,column=3,padx=5,pady=10,ipadx=25)
exit_button.grid(row=0,column=4,padx=5,pady=10,ipadx=50)
#Layout_for_the_output_frame
picture_date = tkinter.Label(output_frame,font=text_font,bg=nasa_white)
picture_explanation = tkinter.Label(output_frame,font=text_font,bg=nasa_white,wraplength=600)
picture_label = tkinter.Label(output_frame)

picture_date.grid(row=1,column=1,padx=10)
picture_explanation.grid(row=0,column=0,padx=10,pady=10,rowspan=2)
picture_label.grid(row=0,column=1,padx=10,pady=10)
#Get today's photo to start with 
get_request()
#Running our main window in Loop
root.mainloop()