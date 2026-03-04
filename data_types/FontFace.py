from .Content import Content
import data_types.Enum as Enum

getText = lambda x: x.text or ''

sourceSans = Content("rbxasset://fonts/families/SourceSansPro.json")
robotoMono = Content("rbxasset://fonts/families/RobotoMono.json")
arcade = Content("rbxasset://fonts/families/PressStart2P.json")
gotham = Content("rbxasset://fonts/families/GothamSSm.json")
arial = Content("rbxasset://fonts/families/Arial.json")
legacy = Content("rbxasset://fonts/families/LegacyArial.json")
bodoni = Content("rbxasset://fonts/families/AccanthisADFStd.json")
garamond = Content("rbxasset://fonts/families/Guru.json")
cartoon = Content("rbxasset://fonts/families/ComicNeueAngular.json")
code = Content("rbxasset://fonts/families/Inconsolata.json")
highway = Content("rbxasset://fonts/families/HighwayGothic.json")
scifi = Content("rbxasset://fonts/families/Zekton.json")
fantasy = Content("rbxasset://fonts/families/Balthazar.json")
antique = Content("rbxasset://fonts/families/RomanAntique.json")
amaticsc = Content("rbxasset://fonts/families/AmaticSC.json")
bangers = Content("rbxasset://fonts/families/Bangers.json")
creepster = Content("rbxasset://fonts/families/Creepster.json")
denkOne = Content("rbxasset://fonts/families/DenkOne.json")
fondamento = Content("rbxasset://fonts/families/Fondamento.json")
fredokaOne = Content("rbxasset://fonts/families/FredokaOne.json")
grenzeGotisch = Content("rbxasset://fonts/families/GrenzeGotisch.json")
indieFlower = Content("rbxasset://fonts/families/IndieFlower.json")
josefinSans = Content("rbxasset://fonts/families/JosefinSans.json")
jura = Content("rbxasset://fonts/families/Jura.json")
kalam = Content("rbxasset://fonts/families/Kalam.json")
luckiestGuy = Content("rbxasset://fonts/families/LuckiestGuy.json")
merriweather = Content("rbxasset://fonts/families/Merriweather.json")
michroma = Content("rbxasset://fonts/families/Michroma.json")
nunito = Content("rbxasset://fonts/families/Nunito.json")
oswald = Content("rbxasset://fonts/families/Oswald.json")
patrickHand = Content("rbxasset://fonts/families/PatrickHand.json")
permenantMarker = Content("rbxasset://fonts/families/PermanentMarker.json")
roboto = Content("rbxasset://fonts/families/Roboto.json")
robotoCondensed = Content("rbxasset://fonts/families/RobotoCondensed.json")
sarpanch = Content("rbxasset://fonts/families/Sarpanch.json")
specialElite = Content("rbxasset://fonts/families/SpecialElite.json")
titilliumWeb = Content("rbxasset://fonts/families/TitilliumWeb.json")
ubuntu = Content("rbxasset://fonts/families/Ubuntu.json")
builderSans = Content("rbxasset://fonts/families/BuilderSans.json")
arimo = Content("rbxasset://fonts/families/Arimo.json")





class FontFace:
    def __init__(self, family, weight, style):
        self.family = family
        self.weight = weight
        self.style = style
    @staticmethod
    def FromEnum(fontEnum):
        return fontMap.get(fontEnum, None)
    @staticmethod
    def FromXML(elem):
        family = Content.FromXML(elem.find("Family"))
        weight = int(elem.find("Weight").text)
        style = getText(elem.find("Style"))
        return FontFace(family, weight, style)
fontMap = {
    Enum.Font.Legacy:               FontFace(legacy,            Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.Arial:                FontFace(arial,             Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.ArialBold:            FontFace(arial,             Enum.FontWeight.Bold,      "Normal"),
    Enum.Font.SourceSans:           FontFace(sourceSans,        Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.SourceSansBold:       FontFace(sourceSans,        Enum.FontWeight.Bold,      "Normal"),
    Enum.Font.SourceSansLight:      FontFace(sourceSans,        Enum.FontWeight.Light,     "Normal"),
    Enum.Font.SourceSansItalic:     FontFace(sourceSans,        Enum.FontWeight.Regular,   "Italic"),
    Enum.Font.Bodoni:               FontFace(bodoni,            Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.Garamond:             FontFace(garamond,          Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.Cartoon:              FontFace(cartoon,           Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.Code:                 FontFace(code,              Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.Highway:              FontFace(highway,           Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.SciFi:                FontFace(scifi,             Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.Arcade:               FontFace(arcade,            Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.Fantasy:              FontFace(fantasy,           Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.Antique:              FontFace(antique,           Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.SourceSansSemibold:   FontFace(sourceSans,        Enum.FontWeight.SemiBold,  "Normal"),
    Enum.Font.Gotham:               FontFace(gotham,            Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.GothamMedium:         FontFace(gotham,            Enum.FontWeight.Medium,    "Normal"),
    Enum.Font.GothamBold:           FontFace(gotham,            Enum.FontWeight.Bold,      "Normal"),
    Enum.Font.GothamBlack:          FontFace(gotham,            Enum.FontWeight.Heavy,     "Normal"),
    Enum.Font.AmaticSC:             FontFace(amaticsc,          Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.Bangers:              FontFace(bangers,           Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.Creepster:            FontFace(creepster,         Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.DenkOne:              FontFace(denkOne,           Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.Fondamento:           FontFace(fondamento,        Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.FredokaOne:           FontFace(fredokaOne,        Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.GrenzeGotisch:        FontFace(grenzeGotisch,     Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.IndieFlower:          FontFace(indieFlower,       Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.JosefinSans:          FontFace(josefinSans,       Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.Jura:                 FontFace(jura,              Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.Kalam:                FontFace(kalam,             Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.LuckiestGuy:          FontFace(luckiestGuy,       Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.Merriweather:         FontFace(merriweather,      Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.Michroma:             FontFace(michroma,          Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.Nunito:               FontFace(nunito,            Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.Oswald:               FontFace(oswald,            Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.PatrickHand:          FontFace(patrickHand,       Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.PermanentMarker:      FontFace(permenantMarker,   Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.Roboto:               FontFace(roboto,            Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.RobotoCondensed:      FontFace(robotoCondensed,   Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.RobotoMono:           FontFace(robotoMono,        Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.Sarpanch:             FontFace(sarpanch,          Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.SpecialElite:         FontFace(specialElite,      Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.TitilliumWeb:         FontFace(titilliumWeb,      Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.Ubuntu:               FontFace(ubuntu,            Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.BuilderSans:          FontFace(builderSans,       Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.BuilderSansMedium:    FontFace(builderSans,       Enum.FontWeight.Medium,    "Normal"),
    Enum.Font.BuilderSansBold:      FontFace(builderSans,       Enum.FontWeight.Bold,      "Normal"),
    Enum.Font.BuilderSansExtraBold: FontFace(builderSans,       Enum.FontWeight.ExtraBold, "Normal"),
    Enum.Font.Arimo:                FontFace(arimo,             Enum.FontWeight.Regular,   "Normal"),
    Enum.Font.ArimoBold:            FontFace(arimo,             Enum.FontWeight.Bold,      "Normal")
}

