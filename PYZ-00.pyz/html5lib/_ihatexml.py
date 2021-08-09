# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\html5lib\_ihatexml.py
from __future__ import absolute_import, division, unicode_literals
import re, warnings
from .constants import DataLossWarning
baseChar = '\n[#x0041-#x005A] | [#x0061-#x007A] | [#x00C0-#x00D6] | [#x00D8-#x00F6] |\n[#x00F8-#x00FF] | [#x0100-#x0131] | [#x0134-#x013E] | [#x0141-#x0148] |\n[#x014A-#x017E] | [#x0180-#x01C3] | [#x01CD-#x01F0] | [#x01F4-#x01F5] |\n[#x01FA-#x0217] | [#x0250-#x02A8] | [#x02BB-#x02C1] | #x0386 |\n[#x0388-#x038A] | #x038C | [#x038E-#x03A1] | [#x03A3-#x03CE] |\n[#x03D0-#x03D6] | #x03DA | #x03DC | #x03DE | #x03E0 | [#x03E2-#x03F3] |\n[#x0401-#x040C] | [#x040E-#x044F] | [#x0451-#x045C] | [#x045E-#x0481] |\n[#x0490-#x04C4] | [#x04C7-#x04C8] | [#x04CB-#x04CC] | [#x04D0-#x04EB] |\n[#x04EE-#x04F5] | [#x04F8-#x04F9] | [#x0531-#x0556] | #x0559 |\n[#x0561-#x0586] | [#x05D0-#x05EA] | [#x05F0-#x05F2] | [#x0621-#x063A] |\n[#x0641-#x064A] | [#x0671-#x06B7] | [#x06BA-#x06BE] | [#x06C0-#x06CE] |\n[#x06D0-#x06D3] | #x06D5 | [#x06E5-#x06E6] | [#x0905-#x0939] | #x093D |\n[#x0958-#x0961] | [#x0985-#x098C] | [#x098F-#x0990] | [#x0993-#x09A8] |\n[#x09AA-#x09B0] | #x09B2 | [#x09B6-#x09B9] | [#x09DC-#x09DD] |\n[#x09DF-#x09E1] | [#x09F0-#x09F1] | [#x0A05-#x0A0A] | [#x0A0F-#x0A10] |\n[#x0A13-#x0A28] | [#x0A2A-#x0A30] | [#x0A32-#x0A33] | [#x0A35-#x0A36] |\n[#x0A38-#x0A39] | [#x0A59-#x0A5C] | #x0A5E | [#x0A72-#x0A74] |\n[#x0A85-#x0A8B] | #x0A8D | [#x0A8F-#x0A91] | [#x0A93-#x0AA8] |\n[#x0AAA-#x0AB0] | [#x0AB2-#x0AB3] | [#x0AB5-#x0AB9] | #x0ABD | #x0AE0 |\n[#x0B05-#x0B0C] | [#x0B0F-#x0B10] | [#x0B13-#x0B28] | [#x0B2A-#x0B30] |\n[#x0B32-#x0B33] | [#x0B36-#x0B39] | #x0B3D | [#x0B5C-#x0B5D] |\n[#x0B5F-#x0B61] | [#x0B85-#x0B8A] | [#x0B8E-#x0B90] | [#x0B92-#x0B95] |\n[#x0B99-#x0B9A] | #x0B9C | [#x0B9E-#x0B9F] | [#x0BA3-#x0BA4] |\n[#x0BA8-#x0BAA] | [#x0BAE-#x0BB5] | [#x0BB7-#x0BB9] | [#x0C05-#x0C0C] |\n[#x0C0E-#x0C10] | [#x0C12-#x0C28] | [#x0C2A-#x0C33] | [#x0C35-#x0C39] |\n[#x0C60-#x0C61] | [#x0C85-#x0C8C] | [#x0C8E-#x0C90] | [#x0C92-#x0CA8] |\n[#x0CAA-#x0CB3] | [#x0CB5-#x0CB9] | #x0CDE | [#x0CE0-#x0CE1] |\n[#x0D05-#x0D0C] | [#x0D0E-#x0D10] | [#x0D12-#x0D28] | [#x0D2A-#x0D39] |\n[#x0D60-#x0D61] | [#x0E01-#x0E2E] | #x0E30 | [#x0E32-#x0E33] |\n[#x0E40-#x0E45] | [#x0E81-#x0E82] | #x0E84 | [#x0E87-#x0E88] | #x0E8A |\n#x0E8D | [#x0E94-#x0E97] | [#x0E99-#x0E9F] | [#x0EA1-#x0EA3] | #x0EA5 |\n#x0EA7 | [#x0EAA-#x0EAB] | [#x0EAD-#x0EAE] | #x0EB0 | [#x0EB2-#x0EB3] |\n#x0EBD | [#x0EC0-#x0EC4] | [#x0F40-#x0F47] | [#x0F49-#x0F69] |\n[#x10A0-#x10C5] | [#x10D0-#x10F6] | #x1100 | [#x1102-#x1103] |\n[#x1105-#x1107] | #x1109 | [#x110B-#x110C] | [#x110E-#x1112] | #x113C |\n#x113E | #x1140 | #x114C | #x114E | #x1150 | [#x1154-#x1155] | #x1159 |\n[#x115F-#x1161] | #x1163 | #x1165 | #x1167 | #x1169 | [#x116D-#x116E] |\n[#x1172-#x1173] | #x1175 | #x119E | #x11A8 | #x11AB | [#x11AE-#x11AF] |\n[#x11B7-#x11B8] | #x11BA | [#x11BC-#x11C2] | #x11EB | #x11F0 | #x11F9 |\n[#x1E00-#x1E9B] | [#x1EA0-#x1EF9] | [#x1F00-#x1F15] | [#x1F18-#x1F1D] |\n[#x1F20-#x1F45] | [#x1F48-#x1F4D] | [#x1F50-#x1F57] | #x1F59 | #x1F5B |\n#x1F5D | [#x1F5F-#x1F7D] | [#x1F80-#x1FB4] | [#x1FB6-#x1FBC] | #x1FBE |\n[#x1FC2-#x1FC4] | [#x1FC6-#x1FCC] | [#x1FD0-#x1FD3] | [#x1FD6-#x1FDB] |\n[#x1FE0-#x1FEC] | [#x1FF2-#x1FF4] | [#x1FF6-#x1FFC] | #x2126 |\n[#x212A-#x212B] | #x212E | [#x2180-#x2182] | [#x3041-#x3094] |\n[#x30A1-#x30FA] | [#x3105-#x312C] | [#xAC00-#xD7A3]'
ideographic = '[#x4E00-#x9FA5] | #x3007 | [#x3021-#x3029]'
combiningCharacter = '\n[#x0300-#x0345] | [#x0360-#x0361] | [#x0483-#x0486] | [#x0591-#x05A1] |\n[#x05A3-#x05B9] | [#x05BB-#x05BD] | #x05BF | [#x05C1-#x05C2] | #x05C4 |\n[#x064B-#x0652] | #x0670 | [#x06D6-#x06DC] | [#x06DD-#x06DF] |\n[#x06E0-#x06E4] | [#x06E7-#x06E8] | [#x06EA-#x06ED] | [#x0901-#x0903] |\n#x093C | [#x093E-#x094C] | #x094D | [#x0951-#x0954] | [#x0962-#x0963] |\n[#x0981-#x0983] | #x09BC | #x09BE | #x09BF | [#x09C0-#x09C4] |\n[#x09C7-#x09C8] | [#x09CB-#x09CD] | #x09D7 | [#x09E2-#x09E3] | #x0A02 |\n#x0A3C | #x0A3E | #x0A3F | [#x0A40-#x0A42] | [#x0A47-#x0A48] |\n[#x0A4B-#x0A4D] | [#x0A70-#x0A71] | [#x0A81-#x0A83] | #x0ABC |\n[#x0ABE-#x0AC5] | [#x0AC7-#x0AC9] | [#x0ACB-#x0ACD] | [#x0B01-#x0B03] |\n#x0B3C | [#x0B3E-#x0B43] | [#x0B47-#x0B48] | [#x0B4B-#x0B4D] |\n[#x0B56-#x0B57] | [#x0B82-#x0B83] | [#x0BBE-#x0BC2] | [#x0BC6-#x0BC8] |\n[#x0BCA-#x0BCD] | #x0BD7 | [#x0C01-#x0C03] | [#x0C3E-#x0C44] |\n[#x0C46-#x0C48] | [#x0C4A-#x0C4D] | [#x0C55-#x0C56] | [#x0C82-#x0C83] |\n[#x0CBE-#x0CC4] | [#x0CC6-#x0CC8] | [#x0CCA-#x0CCD] | [#x0CD5-#x0CD6] |\n[#x0D02-#x0D03] | [#x0D3E-#x0D43] | [#x0D46-#x0D48] | [#x0D4A-#x0D4D] |\n#x0D57 | #x0E31 | [#x0E34-#x0E3A] | [#x0E47-#x0E4E] | #x0EB1 |\n[#x0EB4-#x0EB9] | [#x0EBB-#x0EBC] | [#x0EC8-#x0ECD] | [#x0F18-#x0F19] |\n#x0F35 | #x0F37 | #x0F39 | #x0F3E | #x0F3F | [#x0F71-#x0F84] |\n[#x0F86-#x0F8B] | [#x0F90-#x0F95] | #x0F97 | [#x0F99-#x0FAD] |\n[#x0FB1-#x0FB7] | #x0FB9 | [#x20D0-#x20DC] | #x20E1 | [#x302A-#x302F] |\n#x3099 | #x309A'
digit = '\n[#x0030-#x0039] | [#x0660-#x0669] | [#x06F0-#x06F9] | [#x0966-#x096F] |\n[#x09E6-#x09EF] | [#x0A66-#x0A6F] | [#x0AE6-#x0AEF] | [#x0B66-#x0B6F] |\n[#x0BE7-#x0BEF] | [#x0C66-#x0C6F] | [#x0CE6-#x0CEF] | [#x0D66-#x0D6F] |\n[#x0E50-#x0E59] | [#x0ED0-#x0ED9] | [#x0F20-#x0F29]'
extender = '\n#x00B7 | #x02D0 | #x02D1 | #x0387 | #x0640 | #x0E46 | #x0EC6 | #x3005 |\n#[#x3031-#x3035] | [#x309D-#x309E] | [#x30FC-#x30FE]'
letter = ' | '.join([baseChar, ideographic])
name = ' | '.join([letter, digit, '.', '-', '_', combiningCharacter,
 extender])
nameFirst = ' | '.join([letter, '_'])
reChar = re.compile('#x([\\d|A-F]{4,4})')
reCharRange = re.compile('\\[#x([\\d|A-F]{4,4})-#x([\\d|A-F]{4,4})\\]')

def charStringToList(chars):
    charRanges = [item.strip() for item in chars.split(' | ')]
    rv = []
    for item in charRanges:
        foundMatch = False
        for regexp in (reChar, reCharRange):
            match = regexp.match(item)
            if match is not None:
                rv.append([hexToInt(item) for item in match.groups()])
                if len(rv[(-1)]) == 1:
                    rv[-1] = rv[(-1)] * 2
                foundMatch = True
                break

        if not foundMatch:
            assert len(item) == 1
            rv.append([ord(item)] * 2)

    rv = normaliseCharList(rv)
    return rv


def normaliseCharList(charList):
    charList = sorted(charList)
    for item in charList:
        assert item[1] >= item[0]

    rv = []
    i = 0
    while i < len(charList):
        j = 1
        rv.append(charList[i])
        while i + j < len(charList) and charList[(i + j)][0] <= rv[(-1)][1] + 1:
            rv[(-1)][1] = charList[(i + j)][1]
            j += 1

        i += j

    return rv


max_unicode = int('FFFF', 16)

def missingRanges(charList):
    rv = []
    if charList[0] != 0:
        rv.append([0, charList[0][0] - 1])
    for i, item in enumerate(charList[:-1]):
        rv.append([item[1] + 1, charList[(i + 1)][0] - 1])

    if charList[(-1)][1] != max_unicode:
        rv.append([charList[(-1)][1] + 1, max_unicode])
    return rv


def listToRegexpStr(charList):
    rv = []
    for item in charList:
        if item[0] == item[1]:
            rv.append(escapeRegexp(chr(item[0])))
        else:
            rv.append(escapeRegexp(chr(item[0])) + '-' + escapeRegexp(chr(item[1])))

    return '[%s]' % ''.join(rv)


def hexToInt(hex_str):
    return int(hex_str, 16)


def escapeRegexp(string):
    specialCharacters = ('.', '^', '$', '*', '+', '?', '{', '}', '[', ']', '|', '(',
                         ')', '-')
    for char in specialCharacters:
        string = string.replace(char, '\\' + char)

    return string


nonXmlNameBMPRegexp = re.compile('[\x00-,/:-@\\[-\\^`\\{-¶¸-¿×÷Ĳ-ĳĿ-ŀŉſǄ-ǌǱ-ǳǶ-ǹȘ-ɏʩ-ʺ˂-ˏ˒-˿͆-͟͢-΅\u038b\u038d\u03a2Ϗϗ-ϙϛϝϟϡϴ-ЀЍѐѝ҂҇-ҏӅ-ӆӉ-ӊӍ-ӏӬ-ӭӶ-ӷӺ-\u0530\u0557-\u0558՚-\u0560և-\u0590ֺ֢־׀׃ׅ-\u05cf\u05eb-\u05ef׳-ؠػ-ؿٓ-ٟ٪-ٯڸ-ڹڿۏ۔۩ۮ-ۯۺ-ऀऄऺ-ऻॎ-ॐॕ-ॗ।-॥॰-ঀ\u0984\u098d-\u098e\u0991-\u0992\u09a9\u09b1\u09b3-\u09b5\u09ba-\u09bbঽ\u09c5-\u09c6\u09c9-\u09caৎ-\u09d6\u09d8-\u09db\u09de\u09e4-\u09e5৲-ਁਃ-\u0a04\u0a0b-\u0a0e\u0a11-\u0a12\u0a29\u0a31\u0a34\u0a37\u0a3a-\u0a3b\u0a3d\u0a43-\u0a46\u0a49-\u0a4a\u0a4e-\u0a58\u0a5d\u0a5f-\u0a65ੵ-\u0a80\u0a84ઌ\u0a8e\u0a92\u0aa9\u0ab1\u0ab4\u0aba-\u0abb\u0ac6\u0aca\u0ace-\u0adfૡ-\u0ae5૰-\u0b00\u0b04\u0b0d-\u0b0e\u0b11-\u0b12\u0b29\u0b31\u0b34-ଵ\u0b3a-\u0b3bୄ-\u0b46\u0b49-\u0b4a\u0b4e-\u0b55\u0b58-\u0b5b\u0b5eୢ-\u0b65୰-\u0b81\u0b84\u0b8b-\u0b8d\u0b91\u0b96-\u0b98\u0b9b\u0b9d\u0ba0-\u0ba2\u0ba5-\u0ba7\u0bab-\u0badஶ\u0bba-\u0bbd\u0bc3-\u0bc5\u0bc9\u0bce-\u0bd6\u0bd8-௦௰-ఀ\u0c04\u0c0d\u0c11\u0c29ఴ\u0c3a-ఽ\u0c45\u0c49\u0c4e-\u0c54\u0c57-\u0c5fౢ-\u0c65\u0c70-ಁ\u0c84\u0c8d\u0c91\u0ca9\u0cb4\u0cba-ಽ\u0cc5\u0cc9\u0cce-\u0cd4\u0cd7-\u0cdd\u0cdfೢ-\u0ce5\u0cf0-ഁ\u0d04\u0d0d\u0d11ഩഺ-ഽൄ-\u0d45\u0d49ൎ-ൖ൘-ൟൢ-\u0d65൰-\u0e00ฯ\u0e3b-฿๏๚-\u0e80\u0e83\u0e85-\u0e86\u0e89\u0e8b-\u0e8c\u0e8e-\u0e93\u0e98\u0ea0\u0ea4\u0ea6\u0ea8-\u0ea9\u0eacຯ\u0eba\u0ebe-\u0ebf\u0ec5\u0ec7\u0ece-\u0ecf\u0eda-༗༚-༟༪-༴༶༸༺-༽\u0f48ཪ-\u0f70྅ྌ-ྏྖ\u0f98ྮ-ྰྸྺ-႟\u10c6-\u10cfჷ-ჿᄁᄄᄈᄊᄍᄓ-ᄻᄽᄿᅁ-ᅋᅍᅏᅑ-ᅓᅖ-ᅘᅚ-ᅞᅢᅤᅦᅨᅪ-ᅬᅯ-ᅱᅴᅶ-ᆝᆟ-ᆧᆩ-ᆪᆬ-ᆭᆰ-ᆶᆹᆻᇃ-ᇪᇬ-ᇯᇱ-ᇸᇺ-᷿ẜ-ẟỺ-ỿ\u1f16-\u1f17\u1f1e-\u1f1f\u1f46-\u1f47\u1f4e-\u1f4f\u1f58\u1f5a\u1f5c\u1f5e\u1f7e-\u1f7f\u1fb5᾽᾿-῁\u1fc5῍-῏\u1fd4-\u1fd5\u1fdc-῟῭-\u1ff1\u1ff5´-\u20cf⃝-⃠⃢-℥℧-℩ℬ-ℭℯ-ⅿↃ-〄〆〈-〠〰〶-\u3040ゕ-\u3098゛-゜ゟ-゠・ヿ-\u3104ㄭ-䷿龦-\uabff\ud7a4-\uffff]')
nonXmlNameFirstBMPRegexp = re.compile('[\x00-@\\[-\\^`\\{-¿×÷Ĳ-ĳĿ-ŀŉſǄ-ǌǱ-ǳǶ-ǹȘ-ɏʩ-ʺ˂-΅·\u038b\u038d\u03a2Ϗϗ-ϙϛϝϟϡϴ-ЀЍѐѝ҂-ҏӅ-ӆӉ-ӊӍ-ӏӬ-ӭӶ-ӷӺ-\u0530\u0557-\u0558՚-\u0560և-\u05cf\u05eb-\u05ef׳-ؠػ-ـً-ٰڸ-ڹڿۏ۔ۖ-ۤۧ-ऄऺ-़ा-ॗॢ-\u0984\u098d-\u098e\u0991-\u0992\u09a9\u09b1\u09b3-\u09b5\u09ba-\u09db\u09deৢ-৯৲-\u0a04\u0a0b-\u0a0e\u0a11-\u0a12\u0a29\u0a31\u0a34\u0a37\u0a3a-\u0a58\u0a5d\u0a5f-ੱੵ-\u0a84ઌ\u0a8e\u0a92\u0aa9\u0ab1\u0ab4\u0aba-઼ા-\u0adfૡ-\u0b04\u0b0d-\u0b0e\u0b11-\u0b12\u0b29\u0b31\u0b34-ଵ\u0b3a-଼ା-\u0b5b\u0b5eୢ-\u0b84\u0b8b-\u0b8d\u0b91\u0b96-\u0b98\u0b9b\u0b9d\u0ba0-\u0ba2\u0ba5-\u0ba7\u0bab-\u0badஶ\u0bba-\u0c04\u0c0d\u0c11\u0c29ఴ\u0c3a-\u0c5fౢ-\u0c84\u0c8d\u0c91\u0ca9\u0cb4\u0cba-\u0cdd\u0cdfೢ-\u0d04\u0d0d\u0d11ഩഺ-ൟൢ-\u0e00ฯัิ-฿ๆ-\u0e80\u0e83\u0e85-\u0e86\u0e89\u0e8b-\u0e8c\u0e8e-\u0e93\u0e98\u0ea0\u0ea4\u0ea6\u0ea8-\u0ea9\u0eacຯັິ-ຼ\u0ebe-\u0ebf\u0ec5-༿\u0f48ཪ-႟\u10c6-\u10cfჷ-ჿᄁᄄᄈᄊᄍᄓ-ᄻᄽᄿᅁ-ᅋᅍᅏᅑ-ᅓᅖ-ᅘᅚ-ᅞᅢᅤᅦᅨᅪ-ᅬᅯ-ᅱᅴᅶ-ᆝᆟ-ᆧᆩ-ᆪᆬ-ᆭᆰ-ᆶᆹᆻᇃ-ᇪᇬ-ᇯᇱ-ᇸᇺ-᷿ẜ-ẟỺ-ỿ\u1f16-\u1f17\u1f1e-\u1f1f\u1f46-\u1f47\u1f4e-\u1f4f\u1f58\u1f5a\u1f5c\u1f5e\u1f7e-\u1f7f\u1fb5᾽᾿-῁\u1fc5῍-῏\u1fd4-\u1fd5\u1fdc-῟῭-\u1ff1\u1ff5´-℥℧-℩ℬ-ℭℯ-ⅿↃ-〆〈-〠〪-\u3040ゕ-゠・-\u3104ㄭ-䷿龦-\uabff\ud7a4-\uffff]')
nonPubidCharRegexp = re.compile("[^ \r\na-zA-Z0-9\\-'()+,./:=?;!*#@$_%]")

class InfosetFilter(object):
    replacementRegexp = re.compile('U[\\dA-F]{5,5}')

    def __init__(self, dropXmlnsLocalName=False, dropXmlnsAttrNs=False, preventDoubleDashComments=False, preventDashAtCommentEnd=False, replaceFormFeedCharacters=True, preventSingleQuotePubid=False):
        self.dropXmlnsLocalName = dropXmlnsLocalName
        self.dropXmlnsAttrNs = dropXmlnsAttrNs
        self.preventDoubleDashComments = preventDoubleDashComments
        self.preventDashAtCommentEnd = preventDashAtCommentEnd
        self.replaceFormFeedCharacters = replaceFormFeedCharacters
        self.preventSingleQuotePubid = preventSingleQuotePubid
        self.replaceCache = {}

    def coerceAttribute(self, name, namespace=None):
        if self.dropXmlnsLocalName and name.startswith('xmlns:'):
            warnings.warn('Attributes cannot begin with xmlns', DataLossWarning)
            return
        else:
            if self.dropXmlnsAttrNs:
                if namespace == 'http://www.w3.org/2000/xmlns/':
                    warnings.warn('Attributes cannot be in the xml namespace', DataLossWarning)
                    return
            return self.toXmlName(name)

    def coerceElement(self, name):
        return self.toXmlName(name)

    def coerceComment(self, data):
        if self.preventDoubleDashComments:
            while '--' in data:
                warnings.warn('Comments cannot contain adjacent dashes', DataLossWarning)
                data = data.replace('--', '- -')

            if data.endswith('-'):
                warnings.warn('Comments cannot end in a dash', DataLossWarning)
                data += ' '
        return data

    def coerceCharacters(self, data):
        if self.replaceFormFeedCharacters:
            for _ in range(data.count('\x0c')):
                warnings.warn('Text cannot contain U+000C', DataLossWarning)

            data = data.replace('\x0c', ' ')
        return data

    def coercePubid(self, data):
        dataOutput = data
        for char in nonPubidCharRegexp.findall(data):
            warnings.warn('Coercing non-XML pubid', DataLossWarning)
            replacement = self.getReplacementCharacter(char)
            dataOutput = dataOutput.replace(char, replacement)

        if self.preventSingleQuotePubid:
            if dataOutput.find("'") >= 0:
                warnings.warn('Pubid cannot contain single quote', DataLossWarning)
                dataOutput = dataOutput.replace("'", self.getReplacementCharacter("'"))
        return dataOutput

    def toXmlName(self, name):
        nameFirst = name[0]
        nameRest = name[1:]
        m = nonXmlNameFirstBMPRegexp.match(nameFirst)
        if m:
            warnings.warn('Coercing non-XML name', DataLossWarning)
            nameFirstOutput = self.getReplacementCharacter(nameFirst)
        else:
            nameFirstOutput = nameFirst
        nameRestOutput = nameRest
        replaceChars = set(nonXmlNameBMPRegexp.findall(nameRest))
        for char in replaceChars:
            warnings.warn('Coercing non-XML name', DataLossWarning)
            replacement = self.getReplacementCharacter(char)
            nameRestOutput = nameRestOutput.replace(char, replacement)

        return nameFirstOutput + nameRestOutput

    def getReplacementCharacter(self, char):
        if char in self.replaceCache:
            replacement = self.replaceCache[char]
        else:
            replacement = self.escapeChar(char)
        return replacement

    def fromXmlName(self, name):
        for item in set(self.replacementRegexp.findall(name)):
            name = name.replace(item, self.unescapeChar(item))

        return name

    def escapeChar(self, char):
        replacement = 'U%05X' % ord(char)
        self.replaceCache[char] = replacement
        return replacement

    def unescapeChar(self, charcode):
        return chr(int(charcode[1:], 16))