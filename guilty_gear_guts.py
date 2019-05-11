"""This script creates a graph for all Guilty Gear Xrd Characters,
which shows the effective damage multiplier base on the characters health
"""
from __future__ import division
import plotly
import plotly.plotly as ply
import plotly.graph_objs as go
import guiltygeardata as ggd

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
    characters = ggd.characters()
    char_list = characters.char_list
    alldata = []
    # 1:generates and shows effective HP of each character
    # 2:generates all data and writes it into a txt withto be able compare with manual math :)
    # 3:generates the graph, needs 2 before
    # 4+: stops loop
    debug=1

    while debug<2:
        if debug==1:
            for char in char_list:
                print('{}s effective HPs are {:.5}'.format(char[0], ggd.effectiveHP(char)))
            debug+=1

        elif debug==2:
            try:
                file=open('guiltygeardata.txt', 'w')
                for char in char_list:
                    values = []
                    values.append(char[0])
                    for i in range(1,101,1):
                       values.append(ggd.getPercentageDmg(char, i-1))
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

if __name__ == '__main__':
    main()