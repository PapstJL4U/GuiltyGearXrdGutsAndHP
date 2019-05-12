"""This py file provides GUTS values and characters"""
from __future__ import division


class Guts:
    """This class defines the guts values and is able to return the a tuple of all guts value depanding on guts rank
    Data can be found here: http://www.dustloop.com/wiki/index.php?title=GGXRD/System_Data"""

    def __init__(self):
        # guts values for < 50/40/30/20/10 % hp as damage taken
        self.guts_zero = (0.90, 0.76, 0.60, 0.50, 0.40)
        self.guts_one = (0.86, 0.72, 0.58, 0.48, 0.40)
        self.guts_two = (0.84, 0.68, 0.56, 0.46, 0.38)
        self.guts_three = (0.81, 0.66, 0.54, 0.44, 0.38)
        self.guts_four = (0.78, 0.64, 0.50, 0.42, 0.38)
        self.guts_five = (0.75, 0.60, 0.48, 0.40, 0.36)

    def getGutsValues(self, number):
        """Returns the GUts tuple based on the rank(integer of 0..5)"""
        guts = (0, 0, 0, 0, 0)
        if number == 0:
            guts = self.guts_zero
        elif number == 1:
            guts = self.guts_one
        elif number == 2:
            guts = self.guts_two
        elif number == 3:
            guts = self.guts_three
        elif number == 4:
            guts = self.guts_four
        elif number == 5:
            guts = self.guts_five
        return guts


_guts = Guts()


class characters:
    def __init__(self):
        self._hp = 420.0
        self._hp_bar_in_pixel = 600

        Chipp = ('Chipp', self._hp, 1.30, _guts.getGutsValues(4))
        Millia = ('Millia', self._hp, 1.21, _guts.getGutsValues(3))
        Zato = ('Zato', self._hp, 1.09, _guts.getGutsValues(0))
        Axl = ('Axl', self._hp, 1.06, _guts.getGutsValues(1))
        Ino = ('I-No', self._hp, 1.06, _guts.getGutsValues(1))
        Ramlethal = ('Ramlethal', self._hp, 1.06, _guts.getGutsValues(1))
        Dizzy = ('Dizzy', self._hp, 1.06, _guts.getGutsValues(1))
        Sin = ('Sin', self._hp, 1.04, _guts.getGutsValues(1))
        Venom = ('Venom', self._hp, 1.03, _guts.getGutsValues(1))
        Elphelt = ('Elphelt', self._hp, 1.00, _guts.getGutsValues(0))
        Faust = ('Faust', self._hp, 1.00, _guts.getGutsValues(0))
        May = ('May', self._hp, 1.06, _guts.getGutsValues(3))
        Jam = ('Jam', self._hp, 1.06, _guts.getGutsValues(3))
        Ky = ('Ky Kiske', self._hp, 1.03, _guts.getGutsValues(2))
        Jacko = ('Jack-O', self._hp, 1.03, _guts.getGutsValues(2))
        Sol = ('Sol Badguy', self._hp, 1.00, _guts.getGutsValues(1))
        Raven = ('Raven', self._hp, 1.10, _guts.getGutsValues(5))
        Slayer = ('Slayer', self._hp, 0.96, _guts.getGutsValues(1))
        Johnny = ('Johnny', self._hp, 1.00, _guts.getGutsValues(3))
        Leo = ('Leo', self._hp, 1.00, _guts.getGutsValues(3))
        Bedman = ('Bedman', self._hp, 0.93, _guts.getGutsValues(0))
        Haehyun = ('Haehyun', self._hp, 0.96, _guts.getGutsValues(2))
        Potemkin = ('Potemkin', self._hp, 0.93, _guts.getGutsValues(3))
        Baiken = ('Baiken', self._hp, 1.18, _guts.getGutsValues(4))
        Answer = ('Answer', self._hp, 1.03, _guts.getGutsValues(0))

        self._char_list = (Chipp, Millia, Zato, Axl, Ino, Ramlethal, Dizzy, Sin,
                           Venom, Elphelt, Faust, May, Jam, Ky, Jacko, Sol, Raven,
                           Slayer, Johnny, Leo, Bedman, Haehyun, Potemkin, Baiken, Answer)

    @property
    def char_list(self):
        return self._char_list

    @property
    def HP(self):
        """This is the games base HP for all math done"""
        return self._hp

    @property
    def base_HPbar_in_pixel(self):
        """This describes the healthbar weight in pixel on 1080p and measured by hand."""
        return self._hp_bar_in_pixel


def effectiveHP(character):
    """This function returns the effective HP a character has"""
    # Effective HP =  420 * (0.5 + 0.1(1/(Guts multiplier <50%)
    #                                   + 1/(Guts <40%)
    #                                   + 1/(Guts <30%)
    #                                   + 1/(Guts <20%)
    #                                   + 1/(Guts <10%))/ (Defense Modifier)
    return character[1] * (
                0.5 + 0.1 * (1 / character[3][0]) + 0.1 * (1 / character[3][1]) + 0.1 * (1 / character[3][2]) + 0.1 * (
                    1 / character[3][3]) + 0.1 * (1 / character[3][4])) / character[2]

def effectiveHP_2(character):
    """My own analysis of effect HP of any character."""
    firsthalf = 210 # half of the 420 base hp
    decile = 42 # guts works 1/10  of 420 parts below 420
    ehp = firsthalf / getPercentageDmg(character, 75) + \
        decile / getPercentageDmg(character, 45) + \
          decile / getPercentageDmg(character, 35) + \
          decile / getPercentageDmg(character, 25)+ \
          decile / getPercentageDmg(character, 15)+ \
          decile / getPercentageDmg(character, 5)

    return ehp

def getPercentageDmg(character, HPpercentage):
    """Returns damage modifier for a specific combination of %health remaining and character"""
    # HPpercentage should be between [1 and 100]
    # print('in getPercentageDmg:{}{}'.format(character[0],HPpercentage), end="")
    if HPpercentage < 10:
        dmgamp = character[3][4]
    elif HPpercentage < 20:
        dmgamp = character[3][3]
    elif HPpercentage < 30:
        dmgamp = character[3][2]
    elif HPpercentage < 40:
        dmgamp = character[3][1]
    elif HPpercentage < 50:
        dmgamp = character[3][0]
    elif HPpercentage >= 50:
        dmgamp = 1.00
    else:
        raise Exception
    # print('{}% : {}*{} = {}'.format(HPpercentage, character[2], dmgamp, character[2]*dmgamp))
    return character[2] * dmgamp
