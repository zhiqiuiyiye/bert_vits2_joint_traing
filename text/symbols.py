""" from https://github.com/keithito/tacotron """

"""
Defines the set of symbols used in text input to the model.
"""
_pad = "_"
_punctuation = ';:,.!?¡¿—…"«»“” '
_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
_letters_ipa = "ɑɐɒæɓʙβɔɕçɗɖðʤəɘɚɛɜɝɞɟʄɡɠɢʛɦɧħɥʜɨɪʝɭɬɫɮʟɱɯɰŋɳɲɴøɵɸθœɶʘɹɺɾɻʀʁɽʂʃʈʧʉʊʋⱱʌɣɤʍχʎʏʑʐʒʔʡʕʢǀǁǂǃˈˌːˑʼʴʰʱʲʷˠˤ˞↓↑→↗↘'̩'ᵻ"


# Export all symbols:
symbols = [_pad] + list(_punctuation) + list(_letters) + list(_letters_ipa)

# Special symbol ids
SPACE_ID = symbols.index(" ")


HAITIAN_backup = ['sil','!', '"', '*', '+', ',', '.', '/', ':', '?',
          'I0', 'I1', 'J', 'N', 'E0', 'E1', 
          'O0', 'O1', 'S', 'U0', 'U1', 'a0', 'a1', 'aj0', 'aj1', 'aw0', 'aw1', 'b', 'd', 'd_Z', '@0', '@1', 'e0', 'e1', 'f', 'g', 'h', 'i0', 'i1', 'j',
          'k', 'l', 'm', 'n', 'o0', 'o1', 'oj0', 'oj1', 'p', 'r', 's', 't_S', 't_d', 'u0', 'u1', 'w', 'x', 'z',
          'EAA0', 'EAA1', 'EAA13', 'EAA2', 'EAE0', 'EAE1', 'EAE13', 'EAE2', 'EAH0', 'EAH03', 'EAH1',
          'EAH2', 'EAO0', 'EAO1', 'EAO13', 'EAO2', 'EAW0', 'EAW1', 'EAW13', 'EAW2', 'EAW23', 'EAX0', 'EAY0', 'EAY1', 
          'EAY13', 'EAY2', 'EAY23', 'EB', 'EB3', 'ECH', 'ECH3', 'ED', 'ED3', 'EDH', 'EDH3', 'EEH0', 'EEH1', 'EEH2',
          'EEH23', 'EER0', 'EER03', 'EER1', 'EER13', 'EER2', 'EEY0', 'EEY1', 'EEY13', 'EEY2', 'EEY23', 'EF', 'EF3', 'EG', 'EG3',
          'EHH', 'EIH0', 'EIH1', 'EIH2', 'EIY0', 'EIY03', 'EIY1', 'EIY13', 'EIY2', 'EIY23', 'EJH', 'EJH3', 'EK', 'EK3', 'EL', 'EL3',
          'EM', 'EM3', 'EN', 'EN3', 'ENG', 'ENG3', 'EOW0', 'EOW03', 'EOW1', 'EOW13', 'EOW2', 'EOW23', 'EOY0', 'EOY1', 'EOY13', 'EOY2',
          'EOY23', 'EP', 'EP3', 'ER', 'ER3', 'ES', 'ES3', 'ESH', 'ESH3', 'ET', 'ET3', 'ETH', 'ETH3', 'EUH0', 'EUH1', 'EUH2', 'EUW0', 'EUW03',
          'EUW1', 'EUW13', 'EUW2', 'EUW23', 'EV', 'EV3', 'EW', 'EY', 'EZ', 'EZ3', 'EZH']

HAITIAN = [_pad] + HAITIAN_backup

MyEn_list=['!', '"', '&', '(', ')', '*', '+', ',', '-', '.', '/', ':', '?', 
          'AA0', 'AA1', 'AA2', 'AE0', 'AE1', 'AE2', 'AH0', 'AH1', 'AH2', 'AO0', 
          'AO1', 'AO2', 'AW0', 'AW1', 'AW2', 'AY0', 'AY1', 'AY2', 'B', 'CH', 'D', 
          'DH', 'EH0', 'EH1', 'EH2', 'ER0', 'ER1', 'ER2', 'EY0', 'EY1', 'EY2', 'F',
           'G', 'HH', 'IH0', 'IH1', 'IH2', 'IY0', 'IY1', 'IY2', 'JH', 'K', 'L', 'M',
            'N', 'NG', 'OW0', 'OW1', 'OW2', 'OY0', 'OY1', 'OY2', 'P', 'R', 'S', 'SH', 
            'T', 'TH', 'UH0', 'UH1', 'UH2', 'UW0', 'UW1', 'UW2', 'V', 'W', 'Y', 'Z', 
            'ZH', 'a', 'b', 'd', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 
            'r', 's', 't', 'u', 'v', 'w', 'z', 'ŋ', 'ə', 'ɲ', 'ʃ', 'ʒ', 'ʔ', ';', 'e', '”']
MyEn_list = [_pad] + MyEn_list