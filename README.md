# OptionAnalysis
Requires Python3.7 because of the use of @dataclass.

Realtime quote data obtained from CBOE,  Update
global variable g_csvfile in OptionSkew.py with the 
name of the file downloaded from CBOE that contains
the option chain.

http://www.cboe.com/delayedquote/quote-table-download


Usage: python3 OptionSkew.py

- Download quote table from CBOE (link above)
- Set global variable in the code for the file name.
- Input the expiration date you're interested in.

Two plots will be displayed: 
- Implied volatility skew
- Option price ploted against the strike.
