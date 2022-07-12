#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# source 1: https://stackoverflow.com/questions/596216/formula-to-determine-perceived-brightness-of-rgb-color
# source 2: https://stackoverflow.com/questions/6442118/python-measuring-pixel-brightness

def get_image_brightness(image_list):
    global bright_list
    bright_list = []
    for i, j in enumerate(image_list):
        try:
            imag = Image.open(urlopen(j))
            #Convert the image te RGB if it is a .gif for example
            imag = imag.convert ('RGB')
            #coordinates of the pixel
            X,Y = 0,0
            #Get RGB
            pixelRGB = imag.getpixel((X,Y))
            R,G,B = pixelRGB 

            brightness = (0.2126*R) + (0.7152*G) + (0.0722*B)
            bright_list.append(brightness)
        except:
            bright_list.append(np.nan)
        print(i)
    return(bright_list)

def get_dominant_color(image_list):
    colors = ['red', 'green', 'blue']
    global color_list
    color_list = []
    for i, j in enumerate(image_list):
        try:
            imag = Image.open(urlopen(j))
            #Convert the image te RGB if it is a .gif for example
            imag = imag.convert ('RGB')
            #coordinates of the pixel
            X,Y = 0,0
            #Get RGB
            pixelRGB = imag.getpixel((X,Y))
            R,G,B = pixelRGB 

            dominant_color = colors[np.argmax([R, G, B])]
            color_list.append(dominant_color)
        except:
            color_list.append(np.nan)
        print(i)
    return(color_list)



