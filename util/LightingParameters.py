import math
from rbxl.data_types import *

def linearSpline(x, controlX, controlY, numControl):
    assert numControl >= 1
    
    # Off the beginning
    if numControl == 1 or x < controlX[0]:
        return controlY[0]
    
    for i in range(1, numControl):
        if x < controlX[i]:
            alpha = (controlX[i] - x) / (controlX[i] - controlX[i - 1])
            return controlY[i] * (1 - alpha) + controlY[i - 1] * alpha
    
    # Off the end
    return controlY[numControl - 1]

SECOND=1
MINUTE=60
HOUR = 60*60
DAY=24*60*60
SUNRISE=24*60*60/4
SUNSET=24*60*60*3/4
MIDNIGHT=0
METER=1
KILOMETER=1000

BROWN_UNIVERSITY_LATITUDE = 41.7333
BROWN_UNIVERSITY_LONGITUDE = 71.4333

# Initital star offset on Jan 1 1970 midnight
# Definition of a sidereal day
SIDEREAL_DAY = ((23*HOUR)+(56*MINUTE)+(4.071*SECOND))

toRadians = math.radians

"""
 @file LightingParameters.cpp

 @maintainer Morgan McGuire, matrix@graphics3d.com
 @created 2002-10-05
 @edited  2006-06-28
 """

sunRiseAndSetTime = HOUR / 2
solarYear = 365.2564*DAY
halfSolarYear = 182.6282
moonPhaseInterval = DAY*29.53

# Tilt amount from the ecliptic
earthTilt = toRadians(23.5)
moonTilt = toRadians(5)

# (very rough) Initial star offset on Jan 1 1970 midnight
initialStarRot = 1

# Initial moon phase on Jan 1 1970 midnight
initialMoonPhase = 0.75

SUN = 0
MOON = 1


dayAmbient = Color3.WHITE * 0.40
dayDiffuse = Color3.WHITE * 0.75

lightColorSeq = ColorSequence([
    ColorSequenceKeypoint(MIDNIGHT,                        Color3(0.2, 0.2, 0.2)),
    ColorSequenceKeypoint(SUNRISE - HOUR,                  Color3(0.1, 0.1, 0.1)),
    ColorSequenceKeypoint(SUNRISE,                         Color3.BLACK),
    ColorSequenceKeypoint(SUNRISE + sunRiseAndSetTime / 4, Color3(0.6, 0.6, 0)),
    ColorSequenceKeypoint(SUNRISE + sunRiseAndSetTime,     dayDiffuse),
    ColorSequenceKeypoint(SUNSET - sunRiseAndSetTime,      dayDiffuse),
    ColorSequenceKeypoint(SUNSET - sunRiseAndSetTime / 2,  Color3(0.1, 0.1, 0.075)),
    ColorSequenceKeypoint(SUNSET,                          Color3(0.1, 0.05, 0.05)),
    ColorSequenceKeypoint(SUNSET + HOUR / 2,               Color3(0.1, 0.1, 0.1)),
    ColorSequenceKeypoint(DAY,                             Color3(0.2, 0.2, 0.2))
])

ambientSeq = ColorSequence([
    ColorSequenceKeypoint(MIDNIGHT,                        Color3(0, 0.1, 0.3)),
    ColorSequenceKeypoint(SUNRISE - HOUR,                  Color3(0, 0, 0.1)),
    ColorSequenceKeypoint(SUNRISE,                         Color3.BLACK),
    ColorSequenceKeypoint(SUNRISE + sunRiseAndSetTime / 4, Color3.BLACK),
    ColorSequenceKeypoint(SUNRISE + sunRiseAndSetTime,     dayAmbient),
    ColorSequenceKeypoint(SUNSET - sunRiseAndSetTime,      dayAmbient),
    ColorSequenceKeypoint(SUNSET - sunRiseAndSetTime / 2,  Color3(0.5, 0.2, 0.2)),
    ColorSequenceKeypoint(SUNSET,                          Color3(0.05, 0.05, 0.1)),
    ColorSequenceKeypoint(SUNSET + HOUR / 2,               Color3(0, 0, 0.1)),
    ColorSequenceKeypoint(DAY,                             Color3(0, 0.1, 0.3))
])

diffuseAmbientSeq = ColorSequence([
    ColorSequenceKeypoint(MIDNIGHT,                        Color3(0.2, 0.2, 0.3)),
    ColorSequenceKeypoint(SUNRISE - HOUR,                  Color3(0.05, 0.06, 0.07)),
    ColorSequenceKeypoint(SUNRISE,                         Color3(0.08, 0.08, 0.01)),
    ColorSequenceKeypoint(SUNRISE + sunRiseAndSetTime / 2, Color3.WHITE * 0.75),
    ColorSequenceKeypoint(SUNRISE + sunRiseAndSetTime,     Color3.WHITE * 0.75),
    ColorSequenceKeypoint(SUNSET - sunRiseAndSetTime,      Color3.WHITE * 0.35),
    ColorSequenceKeypoint(SUNSET - sunRiseAndSetTime / 2,  Color3(0.5, 0.2, 0.2)),
    ColorSequenceKeypoint(SUNSET,                          Color3(0.05, 0.05, 0.1)),
    ColorSequenceKeypoint(SUNSET + HOUR / 2,               Color3(0.06, 0.06, 0.07)),
    ColorSequenceKeypoint(DAY,                             Color3(0.1, 0.1, 0.17))
])

skyAmbientSeq = ColorSequence([
    ColorSequenceKeypoint(MIDNIGHT,                     Color3.BLACK),
    ColorSequenceKeypoint(SUNRISE - HOUR,               Color3.BLACK),
    ColorSequenceKeypoint(SUNRISE - HOUR / 2,           Color3(0.2, 0.15, 0.01)),
    ColorSequenceKeypoint(SUNRISE,                      Color3(0.2, 0.15, 0.01)),
    ColorSequenceKeypoint(SUNRISE + sunRiseAndSetTime,  Color3.WHITE),
    ColorSequenceKeypoint(SUNSET - sunRiseAndSetTime,   Color3.WHITE),
    ColorSequenceKeypoint(SUNSET,                       Color3(0.4, 0.2, 0.05)),
    ColorSequenceKeypoint(SUNSET + HOUR / 3,            Color3.BLACK),
#    ColorSequenceKeypoint(DAY,                          Color3(0, 0, 0))
])

class LightingParameters:
    def __init__(self, *args):
        self.emissiveScale = Color3(0, 0, 0)
        self.skyAmbient = Color3(0, 0, 0)
        self.diffuseAmbient = Color3(0, 0, 0)
        self.lightColor = Color3(0, 0, 0)
        self.ambient = Color3(0, 0, 0)
        self.lightDirection = Vector3(0, 0, 0)
        self.source = 0
        self.physicallyCorrect = False
        self.trueSunPosition = Vector3(0, 0, 0)
        self.sunPosition = Vector3(0, 0, 0)
        self.trueMoonPosition = Vector3(0, 0, 0)
        self.moonPosition = Vector3(0, 0, 0)
        self.moonPhase = 0
        self.starFrame = CoordinateFrame.CreateEmpty()
        self.trueStarFrame = CoordinateFrame.CreateEmpty()
        self.starVec = Vector3(0, 0, 0)
        self.geoLatitude = 0
        if len(args) == 0:
            self.physicallyCorrect = True
            self.setLatitude(BROWN_UNIVERSITY_LATITUDE)
            self.setTime(0)
        else:
            _time, _physicallyCorrect, _latitude = args
            self.physicallyCorrect = _physicallyCorrect
            self.setLatitude(_latitude)
            self.setTime(_time)
    def setLatitude(self, _latitude):
        self.geoLatitude = _latitude
    def setTime(self, _time):
        # wrap to a 1 day interval
        time = _time - math.floor(_time / DAY) * DAY

        # Calculate starfield coordinate frame
        starRot = initialStarRot - (2*math.pi*(_time - (_time*math.floor(_time / SIDEREAL_DAY)))/SIDEREAL_DAY)
        #float aX, aY, aZ;
        self.starVec.x = math.cos(starRot)
        self.starVec.y = 0
        self.starVec.z = math.sin(starRot)
        
        self.starFrame.lookAt(self.starVec, Vector3.unitY)
        self.trueStarFrame.lookAt(self.starVec, Vector3.unitY)
        aaaaaa = [0, 0, 0]
        self.trueStarFrame.rotation.toEulerAnglesXYZ(aaaaaa)
        aX, aY, aZ = tuple(aaaaaa)
        aX -= self.geoLatitude;
        self.trueStarFrame.rotation = Matrix3.fromEulerAnglesXYZ(aX, aY, aZ)
        
        # sunAngle = 0 at midnight
        sourceAngle = 2 * math.pi * time / DAY;
        
        # Calculate fake solar and lunar positions
        self.sunPosition.x = math.sin(sourceAngle)
        self.sunPosition.y = -math.cos(sourceAngle)
        self.sunPosition.z = 0

        self.moonPosition.x = math.sin(sourceAngle + math.pi)
        self.moonPosition.y = -math.cos(sourceAngle + math.pi)
        self.moonPosition.z = 0

        # Calculate "true" solar and lunar positions
        # These positions will always be somewhat wrong 
        # unless _time is equal to real world GMT time,
        # and the current longitude is equal to zero. Also, 
        # I'm assuming that the equinox-solstice interval 
        # occurs exactly every 90 days, which isn't exactly
        # correct.
        # In addition, the precession of the moon's orbit is
        # not taken into account, but this should only account
        # for a 5 degree margin of error at most.
        
        dayOfYearOffset = (_time - (_time*math.floor(_time / solarYear)))/DAY
        self.moonPhase = math.floor(_time / moonPhaseInterval) + initialMoonPhase

        latRad = toRadians(self.geoLatitude)
        sunOffset = -earthTilt*math.cos(math.pi*(dayOfYearOffset-halfSolarYear)/halfSolarYear) - latRad
        moonOffset = ((-earthTilt+moonTilt)*math.sin(self.moonPhase*4)) - latRad
        curMoonPhase = (self.moonPhase*math.pi*2)

        rotMat = Matrix3.fromAxisAngle(Vector3.unitZ.cross(self.sunPosition), sunOffset)
        self.trueSunPosition = rotMat * self.sunPosition
        
        trueMoon = Vector3(math.sin(curMoonPhase + sourceAngle), -math.cos(curMoonPhase + sourceAngle), 0)
        rotMat = Matrix3.fromAxisAngle(Vector3.unitZ.cross(trueMoon), moonOffset)
        self.trueMoonPosition = rotMat * trueMoon

        # Determine which light source we observe.
        if not self.physicallyCorrect:
            if ((sourceAngle < (math.pi / 2)) or (sourceAngle > (3 * math.pi / 2))):
                self.source = MOON
                sourceAngle += math.pi
            else:
                self.source = SUN
     
            self.lightDirection.x = math.sin(sourceAngle)
            self.lightDirection.y = -math.cos(sourceAngle)
            self.lightDirection.z = 0
        elif self.trueSunPosition.y > -0.3:
            # The sun is always the stronger light source. When using
            # physically correct parameters, the sun and moon will
            # occasionally be in the visible sky at the same time.
            self.source = SUN
            self.lightDirection = self.trueSunPosition
        else:
            self.source = MOON
            self.lightDirection = self.trueMoonPosition
        
        self.lightColor = lightColorSeq.linearSpline(time)
        self.ambient = ambientSeq.linearSpline(time)
        self.diffuseAmbient = diffuseAmbientSeq.linearSpline(time)
        self.skyAmbient = skyAmbientSeq.linearSpline(time)

        self.emissiveScale = Color3.WHITE