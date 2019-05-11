from __future__ import division
from PIL import Image, ImageDraw, ImageFont
from operator import itemgetter
import guiltygeardata as ggd
import os

characters = ggd.characters()
char_list = characters.char_list
hp_start = 14
hp_end = characters.base_HPbar_in_pixel + 14


def test_stuff():
    char1 = char_list[11]
    print(ggd.effectiveHP(char1))
    print( ggd.effectiveHP(char1) / characters.HP)
    im = Image.open(os.path.join("img","healthbar_only_radical.png"), mode='r')
    im.show()


def create_real_hp():
    """
    Base assumption are: unmanipulate health is 420 and is 600pixel in weight at a factor of 1.0
    We stretch the 600pixel weight image according to the factor effectiveHP/baseHP
    """
    #prepare image manipulation and composition by aggregating key variables
    char_size = len(char_list)
    base_image = Image.open(os.path.join("img","healthbar_only_radical.png"), mode='r')
    width, height= base_image.size

    #generate stretch factor, find biggest stretch factor and sort data by hp size low->high
    biggest_factor = 1.0
    image_data = [("420 base value", 1.0)]
    for char in char_list:
        factor = ggd.effectiveHP(char) / characters.HP
        image_data.append((char[0],factor))
        if factor > biggest_factor:
            biggest_factor = factor

    image_data.sort(key=itemgetter(1))

    #generate base image and text layer
    #   height = Amount of characters + base value
    #   width = equal to the biggest value of all characters
    comp_image = Image.new(mode="RGBA",size=(int(biggest_factor*width), height*char_size+1))
    text_layer = Image.new(mode="RGBA",size=(int(biggest_factor*width), height*char_size+1))
    text = ImageDraw.Draw(text_layer)
    fnt = ImageFont.truetype('C:\Windows\Fonts\chintzy.ttf', 30)



    #generate big image by pasting the base_image stretch by character factor and add character name
    offset_pic = 0
    offset_name = int(height/3)
    for data in image_data:
        scaled_width=int(data[1]*600)
        comp_image.paste(base_image.resize((scaled_width, height), Image.ANTIALIAS),(0, offset_pic))
        text.text((15,offset_name),data[0], fill=(0, 0, 0, 255), font=fnt)
        offset_name+=height
        offset_pic+=height

    #combine text layer and healthbar image and save the combination
    output = Image.alpha_composite(comp_image, text_layer)
    output.save(os.path.join("output","scaled_healthbars.png"))


def create_real_hp_seperate():

    """
    Base assumption are: unmanipulate health is 420 and is 600pixel in weight at a factor of 1.0
    We stretch the 600pixel weight image according to the factor effectiveHP/baseHP
    """
    #prepare image manipulation and composition by aggregating key variables
    char_size = len(char_list)
    base_image = Image.open(os.path.join("img","healthbar_only_radical.png"), mode='r')
    width, height= base_image.size

    #generate stretch factor, find biggest stretch factor and sort data by hp size low->high
    biggest_factor = 1.0
    image_data = [("420 base value", 1.0)]
    for char in char_list:
        factor = ggd.effectiveHP(char) / characters.HP
        image_data.append((char[0],factor))
        if factor > biggest_factor:
            biggest_factor = factor

    image_data.sort(key=itemgetter(1))

    #generate base image and text layer
    #   height = Amount of characters + base value
    #   width = equal to the biggest value of all characters
    comp_image = Image.new(mode="RGBA",size=(int(biggest_factor*width), height))

    fnt = ImageFont.truetype('C:\Windows\Fonts\chintzy.ttf', 30)

    #generate multiple images by pasting the base_image stretch by character factor and add character name
    offset_name = int(height/3)
    for data in image_data:
        scaled_width=int(data[1]*600)
        comp_image.paste(base_image.resize((scaled_width, height), Image.ANTIALIAS),(0, 0))
        text_layer = Image.new(mode="RGBA",size=(int(biggest_factor*600), height))
        text = ImageDraw.Draw(text_layer)
        text.text((15,offset_name),data[0], fill=(0, 0, 0, 255), font=fnt)
        #combine text layer and healthbar image and save the combination
        output = Image.alpha_composite(comp_image, text_layer)
        output.save(os.path.join("output","single",data[0]+".png"))


if __name__ == '__main__':
    #test_stuff()
    create_real_hp()
    create_real_hp_seperate()