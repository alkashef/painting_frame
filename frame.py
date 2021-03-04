
# Preamble
import streamlit as st
import os
from PIL import Image, ImageFont, ImageDraw

#------------------------------------------------------------------------------

# Constants
title = "Art Work Picture Frame"
subtitle = "Frame a picture of your art work and add a label."

black = (0  , 0  , 0)
white = (255, 255, 255)
grey  = (170, 170, 170)
red   = (178, 34,  34)

frame_style_dark  = {'frame_color' : black, 'text_color' : white}
frame_style_light = {'frame_color' : white, 'text_color' : black}
frame_style_grey  = {'frame_color' : grey,  'text_color' : black}
frame_style_red   = {'frame_color' : red,   'text_color' : white}

config = {'min_bottom'      : 200,
          'min_font'        : 12,
          'font_ratio'      : 0.07,
          'frame_ratio'     : 0.1,
          'label_in_bottom' : 0.66,
          'label_vspace'    : 9}

thumbnail_width = 285

#------------------------------------------------------------------------------

def add_margin(pil_img, top, right, bottom, left, frame_style):
    width, height = pil_img.size

    min_bottom = config['min_bottom']
    if bottom < min_bottom:
        bottom = min_bottom
    new_width = width + right + left
    new_height = height + top + bottom
    
    result = Image.new(pil_img.mode, (new_width, new_height), frame_style['frame_color'])
    result.paste(pil_img, (left, top))
    
    min_font = config['min_font']
    font_size = int(bottom * config['font_ratio'])
    if font_size < min_font:
        font_size = min_font
    #print(font_size)
    
    frame_style['font'] = ImageFont.truetype('arial.ttf', size = font_size)
    frame_style['bold'] = ImageFont.truetype('arialbd.ttf', size = font_size + 1)
    
    return result, bottom

def add_text(artwork, label, frame_style, bottom):
    draw = ImageDraw.Draw(artwork)

    text_color = frame_style['text_color']
    font = frame_style['font']
    bold = frame_style['bold']
    
    left = int(artwork.width / ((1 / config['frame_ratio']) + 2 ))
    vspace = int(bottom/config['label_vspace'])
    
    top1 = int(artwork.height - (bottom * config['label_in_bottom']))
    line1 = label['artist']
    draw.text((left, top1), line1, fill = text_color, font = bold)
    
    top2 = top1 + vspace
    line2 = label['title'] + ' (' + label['date'] + ')' 
    draw.text((left, top2), line2, fill = text_color, font = bold)

    top3 = top2 + vspace
    line3 = label['material'] + ', ' + label['size']
    draw.text((left, top3), line3, fill = text_color, font = font)

    top4 = top3 + vspace
    line4 = label['comment']
    draw.text((left, top4), line4, fill = text_color, font = font)
    
    return artwork

def frame(uploaded, label, frame_style):
    img = Image.open(uploaded)
    
    r = config['frame_ratio']
    
    top = int(img.size[1] * r)
    right = int(img.size[0] * r)
    if top < right:
        top = right
    else:
        right = top
    left = int(img.size[0] * r)
    bottom = int(top * 2)
    
    framed, bottom = add_margin(img, top, right , bottom, left, frame_style)
    framed_labeled = add_text(framed, label, frame_style, bottom)
    
    return framed_labeled

#------------------------------------------------------------------------------

# Headers
st.title(title)
st.text(subtitle)

# Picture
st.sidebar.subheader("Picture")
uploaded = st.sidebar.file_uploader("")
if (uploaded is not None):
    thumbnail_image = Image.open(uploaded) #.thumbnail(thumbnail_size)
    st.sidebar.image(thumbnail_image, width=thumbnail_width, caption='Thumbnail of the Loaded Picture')

# Label
st.sidebar.subheader("Label")

artist   = st.sidebar.text_input("Artist")
title    = st.sidebar.text_input("Title")
material = st.sidebar.text_input("Material")
size     = st.sidebar.text_input("Size")
date     = st.sidebar.text_input("Date")
comment  = st.sidebar.text_input("Comment")

label = {
    'artist'    : artist,
    'title'     : title,
    'material'  : material,
    'size'      : size,
    'date'      : date,
    'comment'   : comment
}

# Frame
st.sidebar.subheader("Frame")
frame_selection = st.sidebar.selectbox('', ['Dark', 'Light', 'Grey', 'Red'])
if frame_selection == 'Dark':
    frame_style = frame_style_dark
elif frame_selection == 'Light':
    frame_style = frame_style_light
elif frame_selection == 'Grey':
    frame_style = frame_style_grey
elif frame_selection == 'Red':
    frame_style = frame_style_red

# Framed Picture
framed = None
clicked = st.sidebar.button("Frame and Label")
if (clicked) and (uploaded is not None):
    framed = frame(uploaded, label, frame_style)
    
    # Display result
    #copy = framed.copy()
    st.image(framed, caption='', use_column_width=True)
    
    # Save framed picture
    saved_file = (uploaded.name.split('.')[0] + " - Framed." + uploaded.name.split('.')[1])
    framed.save(saved_file, quality=100)
    framed.close()
    message = "Framed picture saved to " + saved_file
    st.success(message)
