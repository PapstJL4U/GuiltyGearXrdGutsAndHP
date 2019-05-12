from __future__ import division
from PIL import Image, ImageDraw, ImageFont
from operator import itemgetter
from math import floor
import guiltygeardata as ggd
import os

characters = ggd.characters()
char_list = characters.char_list
hp_start = 14
hp_end = characters.base_HPbar_in_pixel + 14


def test_stuff():
    char1 = char_list[11]
    print(ggd.effectiveHP(char1))
    print(ggd.effectiveHP(char1) / characters.HP)
    im = Image.open(os.path.join("img", "healthbar_only_radical.png"), mode='r')
    im.show()


def create_real_hp():
    """
    Base assumption are: unmanipulate health is 420 and is 600pixel in weight at a factor of 1.0
    We stretch the 600pixel weight image according to the factor effectiveHP/baseHP
    """
    # prepare image manipulation and composition by aggregating key variables
    char_size = len(char_list)
    base_image = Image.open(os.path.join("img", "healthbar_only_radical.png"), mode='r')
    width, height = base_image.size

    # generate stretch factor, find biggest stretch factor and sort data by hp size low->high
    biggest_factor = 1.0
    image_data = [("420 base value", 1.0)]
    for char in char_list:
        factor = ggd.effectiveHP(char) / characters.HP
        image_data.append((char[0], factor))
        if factor > biggest_factor:
            biggest_factor = factor

    image_data.sort(key=itemgetter(1))

    # generate base image and text layer
    #   height = Amount of characters + base value
    #   width = equal to the biggest value of all characters
    comp_image = Image.new(mode="RGBA", size=(int(biggest_factor * width), height * char_size + 1))
    text_layer = Image.new(mode="RGBA", size=(int(biggest_factor * width), height * char_size + 1))
    text = ImageDraw.Draw(text_layer)
    fnt = ImageFont.truetype('C:\Windows\Fonts\chintzy.ttf', 30)

    # generate big image by pasting the base_image stretch by character factor and add character name
    offset_pic = 0
    offset_name = int(height / 3)
    for data in image_data:
        scaled_width = int(data[1] * 600)
        comp_image.paste(base_image.resize((scaled_width, height), Image.ANTIALIAS), (0, offset_pic))
        text.text((15, offset_name), data[0], fill=(0, 0, 0, 255), font=fnt)
        offset_name += height
        offset_pic += height

    # combine text layer and healthbar image and save the combination
    output = Image.alpha_composite(comp_image, text_layer)
    output.save(os.path.join("output", "scaled_healthbars.png"))


def create_real_hp_seperate():
    """
    Base assumption are: unmanipulate health is 420 and is 600pixel in weight at a factor of 1.0
    We stretch the 600pixel weight image according to the factor effectiveHP/baseHP
    """
    # prepare image manipulation and composition by aggregating key variables
    base_image = Image.open(os.path.join("img", "healthbar_only_radical.png"), mode='r')
    width, height = base_image.size

    # generate stretch factor, find biggest stretch factor and sort data by hp size low->high
    biggest_factor = 1.0
    image_data = [("420 base value", 1.0)]
    for char in char_list:
        factor = ggd.effectiveHP(char) / characters.HP
        image_data.append((char[0], factor))
        if factor > biggest_factor:
            biggest_factor = factor

    image_data.sort(key=itemgetter(1))

    # generate base image and text layer
    #   height = Amount of characters + base value
    #   width = equal to the biggest value of all characters
    comp_image = Image.new(mode="RGBA", size=(int(biggest_factor * width), height))

    fnt = ImageFont.truetype('C:\Windows\Fonts\chintzy.ttf', 30)

    # generate multiple images by pasting the base_image stretch by character factor and add character name
    offset_name = int(height / 3)
    for data in image_data:
        scaled_width = int(data[1] * 600)
        comp_image.paste(base_image.resize((scaled_width, height), Image.ANTIALIAS), (0, 0))
        text_layer = Image.new(mode="RGBA", size=(int(biggest_factor * 600), height))
        text = ImageDraw.Draw(text_layer)
        text.text((15, offset_name), data[0], fill=(0, 0, 0, 255), font=fnt)
        # combine text layer and healthbar image and save the combination
        output = Image.alpha_composite(comp_image, text_layer)
        output.save(os.path.join("output", "single", data[0] + ".png"))


def linear_health():
    """calculate absolute health values for all relevant %hp parts"""
    health = characters.HP
    decile = characters.HP / 10
    # list of format [ NAME, health >=50 health <50, health <40, health <30, health <20, health <10, sum ]
    char_health = []
    for char in char_list:
        name = char[0]
        highHP = health / 2 / char[2]
        temp = []
        temp.append(name)
        temp.append(highHP)

        hp = highHP
        guts = char[3]
        percentage = 55
        for _ in guts:
            percentage -= 10
            temp.append(decile / ggd.getPercentageDmg(char, percentage))
            hp += decile / ggd.getPercentageDmg(char, percentage)

        temp.append(hp)
        char_health.append(temp)
        # print(char[0],hp, ggd.effectiveHP(char), ggd.effectiveHP_2(char))
    # print(char_health)
    return char_health


def create_comp_img(character, char_health):
    name = character[0]
    if name != char_health[0]:
        print (name, char_health)
        return "wrong characters"

    base = Image.open(os.path.join("img", "healthbar_only_radical.png"), mode='r')
    scaled = Image.open(os.path.join("img", "healthbar_only_radical.png"), mode='r')
    width = max(base.width, scaled.width)
    margin = 25
    height = base.height + scaled.height + margin
    comp_image = Image.new(mode="RGBA", size=(width, height))
    fnt = ImageFont.truetype('C:\Windows\Fonts\chintzy.ttf', 30)
    fntsmall = ImageFont.truetype('C:\Windows\Fonts\chintzy.ttf', 15)

    diagonals_start = []
    diagonals_end = []
    # draw vertial lines across base image at 50/40/30/20/10%
    i, j = 50, 0
    while i > 0:
        iip = i / 100
        draw = ImageDraw.Draw(base)
        draw.line([base.width - base.width * iip, 0, base.width - base.width * iip, base.height],
                  fill=(128, 128, 128, 128), width=3)

        draw.text((15, base.height / 3), name, fill=(0, 0, 0, 255), font=fnt)
        draw.text((5 + base.width - base.width * iip, base.height / 2), str(i)+"%", fill=(0, 0, 0, 255), font=fntsmall)
        diagonals_start.append((floor(base.width - base.width * iip), base.height))
        i -= 10
        j += 1

    base.save(os.path.join("output", "comp", "sub", name + ".png"))

    sum , percentage = 0 ,0
    for i in range(1,len(char_health)-1):
        ehealth = char_health[i]
        percentage += ehealth / char_health[7]
        sum += ehealth
        # print(ehealth, percentage, sum)
        draw = ImageDraw.Draw(scaled)
        draw.line([scaled.width * percentage, 0, scaled.width * percentage, scaled.height],
                  fill=(128, 128, 128, 128), width=3)
        draw.text([scaled.width * percentage - 35, scaled.height/2], str(floor(char_health[i])), \
                  fill=(0, 0, 0, 255), font=fntsmall)
        draw.text((15, scaled.height / 2), "EHP appr. "+str(floor(char_health[-1])), fill=(0, 0, 0, 255), font=fntsmall)
        diagonals_end.append((floor(scaled.width * percentage), base.height + margin))

    scaled.save(os.path.join("output", "comp", "sub", name +"_scaled"+ ".png"))

    comp_image.paste(base, (0, 0))
    comp_image.paste(scaled,(0,(base.height + margin)))
    for pair in zip(diagonals_start, diagonals_end):
        list = pair[0] + pair[1]
        draw = ImageDraw.Draw(comp_image)
        draw.line(list , fill=(255, 255, 255, 128), width=3)
    comp_image.save(os.path.join("output", "comp", name +"_comp"+ ".png"))

def draw_comp():

    ch = linear_health()

    for i, characters in enumerate(char_list):
        create_comp_img(char_list[i], ch[i])

if __name__ == '__main__':
    # test_stuff()
    #create_real_hp()
    #create_real_hp_seperate()
    draw_comp()
