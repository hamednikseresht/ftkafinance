import talib as ta
import numpy as np
import pandas as pd

pattern = {
ta.CDL2CROWS : 'Two Crows',
ta.CDL3BLACKCROWS : 'Three Black Crows',
ta.CDL3INSIDE : 'Three Inside Up/Down',
ta.CDL3LINESTRIKE : 'Three-Line Strike',
ta.CDL3OUTSIDE : 'Three Outside Up/Down',
ta.CDL3STARSINSOUTH : 'Three Stars In The South',
ta.CDL3WHITESOLDIERS : 'Three Advancing White Soldiers',
ta.CDLABANDONEDBABY : 'Abandoned Baby',
ta.CDLADVANCEBLOCK : 'Advance Block',
ta.CDLBELTHOLD : 'Belt-hold',
ta.CDLBREAKAWAY : 'Breakaway',
ta.CDLCLOSINGMARUBOZU : 'Closing Marubozu',
ta.CDLCONCEALBABYSWALL : 'Concealing Baby Swallow',
ta.CDLCOUNTERATTACK : 'Counterattack',
ta.CDLDARKCLOUDCOVER : 'Dark Cloud Cover',
ta.CDLDOJI : 'Doji',
ta.CDLDOJISTAR : 'Doji Star',
ta.CDLDRAGONFLYDOJI : 'Dragonfly Doji',
ta.CDLENGULFING : 'Engulfing Pattern',
ta.CDLEVENINGDOJISTAR : 'Evening Doji Star',
ta.CDLEVENINGSTAR : 'Evening Star',
ta.CDLGAPSIDESIDEWHITE : 'Up/Down-gap side-by-side white lines',
ta.CDLGRAVESTONEDOJI : 'Gravestone Doji',
ta.CDLHAMMER : 'Hammer',
ta.CDLHANGINGMAN : 'Hanging Man',
ta.CDLHARAMI : 'Harami Pattern',
ta.CDLHARAMICROSS : 'Harami Cross Pattern',
ta.CDLHIGHWAVE : 'High-Wave Candle',
ta.CDLHIKKAKE : 'Hikkake Pattern',
ta.CDLHIKKAKEMOD : 'Modified Hikkake Pattern',
ta.CDLHOMINGPIGEON : 'Homing Pigeon',
ta.CDLIDENTICAL3CROWS : 'Identical Three Crows',
ta.CDLINNECK : 'In-Neck Pattern',
ta.CDLINVERTEDHAMMER : 'Inverted Hammer',
ta.CDLKICKING : 'Kicking',
ta.CDLKICKINGBYLENGTH : 'Kicking - bull/bear determined by the longer marubozu',
ta.CDLLADDERBOTTOM : 'Ladder Bottom',
ta.CDLLONGLEGGEDDOJI : 'Long Legged Doji',
ta.CDLLONGLINE : 'Long Line Candle',
ta.CDLMARUBOZU : 'Marubozu',
ta.CDLMATCHINGLOW : 'Matching Low',
ta.CDLMATHOLD : 'Mat Hold',
ta.CDLMORNINGDOJISTAR : 'Morning Doji Star',
ta.CDLMORNINGSTAR : 'Morning Star',
ta.CDLONNECK : 'On-Neck Pattern',
ta.CDLPIERCING : 'Piercing Pattern',
ta.CDLRICKSHAWMAN : 'Rickshaw Man',
ta.CDLRISEFALL3METHODS : 'Rising/Falling Three Methods',
ta.CDLSEPARATINGLINES : 'Separating Lines',
ta.CDLSHOOTINGSTAR : 'Shooting Star',
ta.CDLSHORTLINE : 'Short Line Candle',
ta.CDLSPINNINGTOP : 'Spinning Top',
ta.CDLSTALLEDPATTERN : 'Stalled Pattern',
ta.CDLSTICKSANDWICH : 'Stick Sandwich',
ta.CDLTAKURI : 'Takuri (Dragonfly Doji with very long lower shadow)',
ta.CDLTASUKIGAP : 'Tasuki Gap',
ta.CDLTHRUSTING : 'Thrusting Pattern',
ta.CDLTRISTAR : 'Tristar Pattern',
ta.CDLUNIQUE3RIVER : 'Unique 3 River',
ta.CDLUPSIDEGAP2CROWS : 'Upside Gap Two Crows',
ta.CDLXSIDEGAP3METHODS : 'Upside/Downside Gap Three Methods'
}

# calculate candle stick patterns
def candle_stick_patterns(df):
    # itreate on dict
    for key, value in pattern.items():
        df[value] = key(df.Open, df.High, df.Low, df.Close)