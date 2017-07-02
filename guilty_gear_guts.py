"""This script creates a graph for all Guilty Gear Xrd Characters,
which shows the effective damage multiplier base on the characters health
"""
from __future__ import division
import plotly
import plotly.plotly as ply
import plotly.graph_objs as go

HP = 420.0

class Guts:
    """This class defines the guts values and is able to return the a tuple of all guts value depanding on guts rank
    Data can be found here: http://www.dustloop.com/wiki/index.php?title=GGXRD/System_Data"""
    def __init__(self):
        #guts values for 50/40/30/20/10 % hp as damage taken
        self.guts_zero  = ( 0.90, 0.76, 0.60, 0.50, 0.40)
        self.guts_one   = ( 0.86, 0.72, 0.58, 0.48, 0.40)
        self.guts_two   = ( 0.84, 0.68, 0.56, 0.46, 0.38)
        self.guts_three = ( 0.81, 0.66, 0.54, 0.44, 0.38)
        self.guts_four  = ( 0.78, 0.64, 0.50, 0.42, 0.38)
        self.guts_five  = ( 0.75, 0.60, 0.48, 0.40, 0.36)

    def getGutsValues(self, number):
        """Returns the GUts tuple based on the rank(integer of 0..5)"""
        guts = (0,0,0,0)
        if number==0:
            guts=self.guts_zero
        elif number==1:
            guts=self.guts_one
        elif number==2:
            guts=self.guts_two
        elif number==3:
            guts=self.guts_three
        elif number==4:
            guts=self.guts_four
        elif number==5:
            guts=self.guts_five
        return guts

guts = Guts()

Chipp       = ( 'Chipp', HP, 1.30 , guts.getGutsValues(4))
Millia      = ( 'Millia', HP, 1.21 , guts.getGutsValues(3))
Zato        = ( 'Zato', HP, 1.09 , guts.getGutsValues(0))
Axl         = ( 'Axl', HP, 1.06 , guts.getGutsValues(1))
Ino         = ( 'I-No', HP, 1.06 , guts.getGutsValues(1))
Ramlethal   = ( 'Ramlethal', HP, 1.06 , guts.getGutsValues(1))
Dizzy       = ( 'Dizzy', HP, 1.06 , guts.getGutsValues(1))
Sin         = ( 'Sin', HP, 1.04 , guts.getGutsValues(1))
Venom       = ( 'Venom', HP, 1.03 , guts.getGutsValues(1))
Elphelt     = ( 'Elphelt', HP, 1.00 , guts.getGutsValues(0))
Faust       = ( 'Faust', HP, 1.00 , guts.getGutsValues(0))
May         = ( 'May', HP, 1.06 , guts.getGutsValues(3))
Jam         = ( 'Jam', HP, 1.06 , guts.getGutsValues(3))
Ky          = ( 'Ky Kiske', HP, 1.03 , guts.getGutsValues(2))
Jacko       = ( 'Jack-O', HP, 1.03 , guts.getGutsValues(2))
Sol         = ( 'Sol Badguy', HP, 1.00 , guts.getGutsValues(1))
Raven       = ( 'Raven', HP, 1.10 , guts.getGutsValues(5))
Slayer      = ( 'Slayer', HP, 0.96 , guts.getGutsValues(1))
Johnny      = ( 'Johnny', HP, 1.00 , guts.getGutsValues(3))
Leo         = ( 'Leo', HP, 1.00 , guts.getGutsValues(3))
Bedman      = ( 'Bedman', HP, 0.93 , guts.getGutsValues(0))
Haehyun     = ( 'Haehyun', HP, 0.96 , guts.getGutsValues(2))
Potemkin    = ( 'Potemkin', HP, 0.93 , guts.getGutsValues(3))
Baiken      = ( 'Baiken', HP, 1.18, guts.getGutsValues(4))
Answer      = ( 'Answer', HP, 1.03, guts.getGutsValues(0))

def effectiveHP(character):
    """This function returns the effective HP a character has"""
    #Effective HP =  420 * (0.5 + 0.1(1/(Guts multiplier <50%) 
    #                                   + 1/(Guts <40%) 
    #                                   + 1/(Guts <30%) 
    #                                   + 1/(Guts <20%) 
    #                                   + 1/(Guts <10%))/ (Defense Modifier)  
    return character[1] * (0.5 + 0.1*( 1 / character[3][0]) + 0.1*( 1 / character[3][1]) + 0.1*( 1 / character[3][2]) + 0.1*( 1 / character[3][3]) + 0.1*( 1 / character[3][4]))/character[2]

def getPercentageDmg(character, HPpercentage):
    """Returns damage modifier for a specific combination of %health remaining and character"""
    #HPpercentage should be between [1 and 100]
    #print('in getPercentageDmg:{}{}'.format(character[0],HPpercentage), end="")
    if HPpercentage<10:
        dmgamp=character[3][4]
    elif HPpercentage<20:
        dmgamp=character[3][3]
    elif HPpercentage<30:
        dmgamp=character[3][2]
    elif HPpercentage<40:
        dmgamp=character[3][1]
    elif HPpercentage<50:
        dmgamp=character[3][0]
    elif HPpercentage>=50:
        dmgamp=1.00
    else:
        return -1.00
    #print('{}% : {}*{} = {}'.format(HPpercentage, character[2], dmgamp, character[2]*dmgamp))
    return character[2]*dmgamp


def generateTrace(charactervalues, xvalues):
    """This function generates all values for a character graph and is based on the plotly web example"""
    #this is one tuple of 101 values, where [0]=charater name and[1...100]= dmg modifier
    return go.Scatter(
        x = xvalues,
        y = charactervalues[1:],
        mode = 'lines',
        name = str(charactervalues[0])
        )

def main():
    """Can be used to debug other functions as well es generate the plotly graph"""
    #Generates an offline html if False, otherwise tries to publish the graph online on the plotl website.
    #Login and PW must be configered according to plotly
    publishOnline = False 
    char_list = ( Chipp, Millia, Zato, Axl, Ino, Ramlethal, Dizzy, Sin,
                  Venom, Elphelt, Faust, May, Jam, Ky, Jacko, Sol, Raven,
                  Slayer, Johnny, Leo, Bedman, Haehyun, Potemkin, Baiken, Answer)
    alldata = []
    # 1:generates and shows effective HP of each character
    # 2:generates all data and writes it into a txt withto be able compare with manual math :)
    # 3:generates the graph, needs 2 before
    # 4+: stops loop
    debug=2

    while debug<4:
        if debug==1:
            for char in char_list:
                print('{}s effective HPs are {:.5}'.format(char[0], effectiveHP(char)))
            debug+=1

        elif debug==2:
            try:
                file=open('guiltygeardata.txt', 'w')
                for char in char_list:
                    values = []
                    values.append(char[0])
                    for i in range(1,101,1):
                       values.append(getPercentageDmg(char, i-1))
                    file.write('{}\n'.format(values))
                    alldata.append(values[:])
            except Exception:
                raise
            finally:
                file.close()
                debug+=1

        elif debug==3:
            xv = [i for i in range(0,101)]
            data=[]
            for char in alldata:
                trace = generateTrace(char,xv)
                data.append(trace)
            layout = dict(title ='Guts and Defensive Modifier for Guilty Gear Xrd Rev 2',
            xaxis = dict(title = 'Health Value in Percentage', mirror = True),
            yaxis = dict(title = 'Damage Multiplier as an absolute Value' )
            )
            fig = dict(data=data, layout=layout)
            if publishOnline:
                ply.iplot(fig, filename='gg-graph-online')
            else:
                plotly.offline.plot(fig, filename='gg-graph.html')
            debug+=1

#access main function
if __name__ == '__main__':
    main()