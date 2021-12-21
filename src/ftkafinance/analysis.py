import talib as ta
from difflib import SequenceMatcher
# talib patterns dict
patterns = {
        'two crows':  ta.CDL2CROWS,
        'three black crows':  ta.CDL3BLACKCROWS,
        'three inside up/down':  ta.CDL3INSIDE,
        'three-line strike':  ta.CDL3LINESTRIKE,
        'three outside up/down':  ta.CDL3OUTSIDE,
        'three stars in the south':  ta.CDL3STARSINSOUTH,
        'three advancing white soldiers':  ta.CDL3WHITESOLDIERS,
        'abandoned baby':  ta.CDLABANDONEDBABY,
        'advance block':  ta.CDLADVANCEBLOCK,
        'belt-hold':  ta.CDLBELTHOLD,
        'breakaway':  ta.CDLBREAKAWAY,
        'closing marubozu':  ta.CDLCLOSINGMARUBOZU,
        'concealing baby swallow':  ta.CDLCONCEALBABYSWALL,
        'counterattack':  ta.CDLCOUNTERATTACK,
        'dark cloud cover':  ta.CDLDARKCLOUDCOVER,
        'doji':  ta.CDLDOJI,
        'doji star':  ta.CDLDOJISTAR,
        'dragonfly doji':  ta.CDLDRAGONFLYDOJI,
        'engulfing pattern':  ta.CDLENGULFING,
        'evening doji star':  ta.CDLEVENINGDOJISTAR,
        'evening star':  ta.CDLEVENINGSTAR,
        'up/down-gap side-by-side white lines':  ta.CDLGAPSIDESIDEWHITE,
        'gravestone doji':  ta.CDLGRAVESTONEDOJI,
        'hammer':  ta.CDLHAMMER,
        'hanging man':  ta.CDLHANGINGMAN,
        'harami pattern':  ta.CDLHARAMI,
        'harami cross pattern':  ta.CDLHARAMICROSS,
        'high-wave candle':  ta.CDLHIGHWAVE,
        'hikkake pattern':  ta.CDLHIKKAKE,
        'modified hikkake pattern':  ta.CDLHIKKAKEMOD,
        'homing pigeon':  ta.CDLHOMINGPIGEON,
        'identical three crows':  ta.CDLIDENTICAL3CROWS,
        'in-neck pattern':  ta.CDLINNECK,
        'inverted hammer':  ta.CDLINVERTEDHAMMER,
        'kicking':  ta.CDLKICKING,
        'ladder bottom':  ta.CDLLADDERBOTTOM,
        'long legged doji':  ta.CDLLONGLEGGEDDOJI,
        'long line candle':  ta.CDLLONGLINE,
        'marubozu':  ta.CDLMARUBOZU,
        'matching low':  ta.CDLMATCHINGLOW,
        'mat hold':  ta.CDLMATHOLD,
        'morning doji star':  ta.CDLMORNINGDOJISTAR,
        'morning star':  ta.CDLMORNINGSTAR,
        'on-neck pattern':  ta.CDLONNECK,
        'piercing pattern':  ta.CDLPIERCING,
        'rickshaw man':  ta.CDLRICKSHAWMAN,
        'rising/falling three methods':  ta.CDLRISEFALL3METHODS,
        'separating lines':  ta.CDLSEPARATINGLINES,
        'shooting star':  ta.CDLSHOOTINGSTAR,
        'short line candle':  ta.CDLSHORTLINE,
        'spinning top':  ta.CDLSPINNINGTOP,
        'stalled pattern':  ta.CDLSTALLEDPATTERN,
        'stick sandwich':  ta.CDLSTICKSANDWICH,
        'takuri (dragonfly doji with very long lower shadow)':  ta.CDLTAKURI,
        'tasuki gap':  ta.CDLTASUKIGAP,
        'thrusting pattern':  ta.CDLTHRUSTING,
        'tristar pattern':  ta.CDLTRISTAR,
        'unique 3 river':  ta.CDLUNIQUE3RIVER,
        'upside gap two crows':  ta.CDLUPSIDEGAP2CROWS,
        'upside/downside gap three methods':  ta.CDLXSIDEGAP3METHODS
}


# clean string for pattern matching
def clean_string(string):
    string = string.lower()
    return string.replace('-', '').replace('/', '').replace('(', '')\
        .replace(')', '').replace('.', '').replace('_', '')


# calculate candle stick patterns
def candle_stick_patterns(df, *input_pattern):
    """
    calculate candle stick patterns
    params:
        df: dataframe
        input_pattern: list of patterns to calculate
    """
    # if no input pattern is given, calculate all patterns
    if not input_pattern:
        for key, value in patterns.items():
            df[key] = value(df.Open, df.High, df.Low, df.Close)
    else:
        # if input pattern is given, calculate only those patterns
        for i in input_pattern:
            for p in patterns:
                # if input pattern is found, calculate it
                # find matches with 50% similarity or more
                if SequenceMatcher(None, clean_string(i), p).ratio() > 0.5:
                    df[p] = patterns[p](df.Open, df.High, df.Low, df.Close)
            else:
                print(f"no pattern found for {i}")
