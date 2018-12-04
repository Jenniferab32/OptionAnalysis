'''
OptionSkew.py  - Python 3.7

Plot volatility skew for given security at a realtime IV.
Realtime quote data obtained from CBOE
http://www.cboe.com/delayedquote/quote-table-download

Written by Jennifer Stopka 
First release - 12/2/2018

Please give me a mention if code is
useful to you. Please let me know if
you have any suggestionsi for the code.

https://www.linkedin.com/in/jenniferstopka/


Usage: python3 OptionSkew.py

- Download quote table from CBOE (link above)
- Set global variable in the code for the file name.
- Input the expiration date you're interested in.

Two plots will be displayed: 
- Implied volatility skew
- Option price ploted against the strike.

'''
import pandas as pd
from decimal import Decimal
from dataclasses import dataclass
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

global g_csvfile 
g_csvfile = 'msft1130.csv'

@dataclass
class Underlying:
    name:       str
    bid:        Decimal 
    ask:        Decimal 
    size:       str 
    last_sale:  Decimal
    change:     Decimal
    vol:        Decimal

class CBOEFormater:
 def getUnderlying(f):
     with open(f) as file:
         x = next(file)
         name = x.split(',')[0]
         last_sale = x.split(',')[1]
         change = x.split(',')[2]

         x = next(file)
         date = x.split(',')[0]
         bid = x.split(',')[2]
         ask = x.split(',')[4]
         size = x.split(',')[6]
         vol = x.split(',')[8]

     underlying = Underlying(name, Decimal(bid), Decimal(ask), \
             size, Decimal(last_sale), Decimal(change), Decimal(vol)) 
     return underlying

 def getCalls(df):
    calls = pd.DataFrame(
        {'Expiration Date': [], 'Strike': [], 'Last Sale': [], 
            'Net': [], 'Bid': [], 'Ask': [], 'Vol': [], 'IV': [], 
            'Delta': [], 'Gamma': [], 'Open Int': []}) 
     
    for i in range(0,len(df)):
            calls = calls.append(
            {'Expiration Date': df.at[i,'Expiration Date'], 
                'Strike': df.at[i,'Strike'], 'Last Sale': df.at[i,'Last Sale'], 
                'Net': df.at[i,'Net'], 'Bid': df.at[i,'Bid'], 'Ask': df.at[i,'Ask'],
                'Vol': df.at[i,'Vol'], 'IV': df.at[i,'IV'], 'Delta': df.at[i,'Delta'],
                'Gamma': df.at[i,'Gamma'], 'Open Int': df.at[i,'Open Int']}, ignore_index=True)
    return calls

 def getPuts(df):
    puts  = pd.DataFrame(
        {'Expiration Date': [], 'Strike': [], 'Last Sale': [], 
            'Net': [], 'Bid': [], 'Ask': [], 'Vol': [], 'IV': [], 
            'Delta': [], 'Gamma': [], 'Open Int': []}) 
    
    for i in range(0,len(df)):
            puts = puts.append(
            {'Expiration Date': df.at[i,'Expiration Date'], 
                'Strike': df.at[i,'Strike'], 'Last Sale': df.at[i,'Last Sale.1'], 
                'Net': df.at[i,'Net.1'], 'Bid': df.at[i,'Bid.1'], 'Ask': df.at[i,'Ask.1'],
                'Vol': df.at[i,'Vol.1'], 'IV': df.at[i,'IV.1'], 'Delta': df.at[i,'Delta.1'],
                'Gamma': df.at[i,'Gamma.1'], 'Open Int': df.at[i,'Open Int.1']}, ignore_index=True)
    return puts 

 @classmethod
 def loadOptionChain(cls,f):
     df  = pd.read_csv(f, skiprows=2)
     return cls.getUnderlying(f), cls.getCalls(df), cls.getPuts(df)

expiration = input("Expiration Date (mm/dd/yyyy): ")
underlying, calls, puts = CBOEFormater.loadOptionChain(g_csvfile)

call = calls[(calls['Expiration Date']==expiration)]             
put  = puts[(calls['Expiration Date']==expiration)] 

plt.figure('Volatility', [12,12])
plt.plot(call['Strike'],call['IV'], color='b') #call
plt.plot(put ['Strike'], put['IV'], color='r') #put
plt.xlabel('Strike Price', fontsize=10)
plt.ylabel('Implied Volitility', fontsize=10)
plt.axvline(underlying.last_sale, color='g')
plt.title(underlying.name + ' - ' + "Volatility\n", fontsize=12)

red_patch = mpatches.Patch(color='r', label = "Put Volatility")
blue_patch = mpatches.Patch(color='b', label = "Call Volatility")
green_patch = mpatches.Patch(color='g', label = "Underlying: " + str(underlying.last_sale))
plt.legend(handles=[blue_patch,red_patch,green_patch])


plt.figure('Price',[12,12])
plt.plot(call['Strike'],call['Last Sale'], color='b') #call
plt.plot(put['Strike'],put['Last Sale'], color='r') #put
plt.xlabel('Strike Price', fontsize=10)
plt.ylabel('Option Price', fontsize=10)
plt.axvline(underlying.last_sale, color='g')
plt.title(underlying.name + ' - ' + "Option Price\n", fontsize=12)

red_patch = mpatches.Patch(color='r', label = "Put Price")
blue_patch = mpatches.Patch(color='b', label = "Call Price")
green_patch = mpatches.Patch(color='g', label = "Underlying: " + str(underlying.last_sale))
plt.legend(handles=[blue_patch,red_patch,green_patch])

plt.show()

print(underlying)

