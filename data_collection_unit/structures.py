"""
Author: Navjot Saroa
Structures of the packets received from the F1 23 game
"""

import ctypes as ct


class PacketHeader(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [('m_packetFormat', ct.c_uint16),
                ('m_gameYear', ct.c_uint8),
                ('m_gameMajorVersion', ct.c_uint8),
                ('m_gameMinorVersion', ct.c_uint8),
                ('m_packetVersion', ct.c_uint8),
                ('m_packetId', ct.c_uint8),
                ('m_sessionUID', ct.c_uint64),
                ('m_sessionTime', ct.c_float),
                ('m_frameIdentifier', ct.c_uint32),
                ('m_overallFrameIdentifier', ct.c_uint32),
                ('m_playerCarIndex', ct.c_uint8),
                ('m_secondaryPlayerCarIndex', ct.c_uint8)]
    
class CarMotionData(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_worldPositionX', ct.c_float),      # World space X position - metres
        ('m_worldPositionY', ct.c_float),      # World space Y position
        ('m_worldPositionZ', ct.c_float),      # World space Z position
        ('m_worldVelocityX', ct.c_float),      # Velocity in world space X – metres/s
        ('m_worldVelocityY', ct.c_float),      # Velocity in world space Y
        ('m_worldVelocityZ', ct.c_float),      # Velocity in world space Z
        ('m_worldForwardDirX', ct.c_int16),    # World space forward X direction (normalised)
        ('m_worldForwardDirY', ct.c_int16),    # World space forward Y direction (normalised)
        ('m_worldForwardDirZ', ct.c_int16),    # World space forward Z direction (normalised)
        ('m_worldRightDirX', ct.c_int16),      # World space right X direction (normalised)
        ('m_worldRightDirY', ct.c_int16),      # World space right Y direction (normalised)
        ('m_worldRightDirZ', ct.c_int16),      # World space right Z direction (normalised)
        ('m_gForceLateral', ct.c_float),       # Lateral G-Force component
        ('m_gForceLongitudinal', ct.c_float),  # Longitudinal G-Force component
        ('m_gForceVertical', ct.c_float),      # Vertical G-Force component
        ('m_yaw', ct.c_float),                 # Yaw angle in radians
        ('m_pitch', ct.c_float),               # Pitch angle in radians
        ('m_roll', ct.c_float)                 # Roll angle in radians
    ]

class MarshalZone(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [('m_zoneStart', ct.c_float),
                ('m_zoneFlag', ct.c_int8)]

class WeatherForecastSample(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [('m_sessionType', ct.c_uint8),
                ('m_timeOffset', ct.c_uint8),
                ('m_weather', ct.c_uint8),
                ('m_trackTemperature', ct.c_int8),
                ('m_trackTemperatureChange', ct.c_int8),
                ('m_airTemperature', ct.c_int8),
                ('m_airTemperatureChange', ct.c_int8),
                ('m_rainPercentage', ct.c_uint8)]

class LapData(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_lastLapTimeInMS', ct.c_uint32),               # Last lap time in milliseconds
        ('m_currentLapTimeInMS', ct.c_uint32),            # Current time around the lap in milliseconds
        ('m_sector1TimeInMS', ct.c_uint16),               # Sector 1 time in milliseconds
        ('m_sector1TimeMinutes', ct.c_uint8),             # Sector 1 whole minute part
        ('m_sector2TimeInMS', ct.c_uint16),               # Sector 2 time in milliseconds
        ('m_sector2TimeMinutes', ct.c_uint8),             # Sector 2 whole minute part
        ('m_deltaToCarInFrontInMS', ct.c_uint16),         # Time delta to car in front in milliseconds
        ('m_deltaToRaceLeaderInMS', ct.c_uint16),         # Time delta to race leader in milliseconds
        ('m_lapDistance', ct.c_float),                    # Distance vehicle is around current lap in metres
        ('m_totalDistance', ct.c_float),                  # Total distance travelled in session in metres
        ('m_safetyCarDelta', ct.c_float),                 # Delta in seconds for safety car
        ('m_carPosition', ct.c_uint8),                    # Car race position
        ('m_currentLapNum', ct.c_uint8),                  # Current lap number
        ('m_pitStatus', ct.c_uint8),                      # 0 = none, 1 = pitting, 2 = in pit area
        ('m_numPitStops', ct.c_uint8),                    # Number of pit stops taken in this race
        ('m_sector', ct.c_uint8),                         # 0 = sector1, 1 = sector2, 2 = sector3
        ('m_currentLapInvalid', ct.c_uint8),              # Current lap invalid - 0 = valid, 1 = invalid
        ('m_penalties', ct.c_uint8),                      # Accumulated time penalties in seconds to be added
        ('m_totalWarnings', ct.c_uint8),                  # Accumulated number of warnings issued
        ('m_cornerCuttingWarnings', ct.c_uint8),          # Accumulated number of corner cutting warnings issued
        ('m_numUnservedDriveThroughPens', ct.c_uint8),    # Num drive through pens left to serve
        ('m_numUnservedStopGoPens', ct.c_uint8),          # Num stop go pens left to serve
        ('m_gridPosition', ct.c_uint8),                   # Grid position the vehicle started the race in
        ('m_driverStatus', ct.c_uint8),                   # Status of driver - 0 = in garage, 1 = flying lap, etc.
        ('m_resultStatus', ct.c_uint8),                   # Result status - 0 = invalid, 1 = inactive, etc.
        ('m_pitLaneTimerActive', ct.c_uint8),             # Pit lane timing, 0 = inactive, 1 = active
        ('m_pitLaneTimeInLaneInMS', ct.c_uint16),         # Current time spent in the pit lane in ms
        ('m_pitStopTimerInMS', ct.c_uint16),              # Time of the actual pit stop in ms
        ('m_pitStopShouldServePen', ct.c_uint8)           # Whether the car should serve a penalty at this stop
    ]


class FastestLap(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('vehicleIdx', ct.c_uint8),
        ('lapTime', ct.c_float)
    ]

class Retirement(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('vehicleIdx', ct.c_uint8),
    ]

class TeamMateInPits(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('vehicleIdx', ct.c_uint8),
    ]

class RaceWinner(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('vehicleIdx', ct.c_uint8),
    ]

class Penalty(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('penaltyType', ct.c_uint8),
        ('infringementType', ct.c_uint8),
        ('vehicleIdx', ct.c_uint8),
        ('otherVehicleIdx', ct.c_uint8),
        ('time', ct.c_uint8),
        ('lapNum', ct.c_uint8),
        ('placesGained', ct.c_uint8)
    ]

class SpeedTrap(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('vehicleIdx', ct.c_uint8),
        ('speed', ct.c_float),
        ('isOverallFastestInSession', ct.c_uint8),
        ('isDriverFastestInSession', ct.c_uint8),
        ('fastestVehicleIdxInSession', ct.c_uint8),
        ('fastestSpeedInSession', ct.c_float)
    ]

class StartLights(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('numLights', ct.c_uint8),
    ]

class DriveThroughPenaltyServed(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('vehicleIdx', ct.c_uint8),
    ]

class StopGoPenaltyServed(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('vehicleIdx', ct.c_uint8),
    ]

class Flashback(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('flashbackFrameIdentifier', ct.c_uint32),
        ('flashbackSessionTime', ct.c_float)
    ]

class Buttons(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('buttonStatus', ct.c_uint32),
    ]

class Overtake(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('overtakingVehicleIdx', ct.c_uint8),
        ('beingOvertakenVehicleIdx', ct.c_uint8)
    ]

class EventDataDetails(ct.Union):
    _pack_ = 1
    _fields_ = [
        ('FastestLap', FastestLap),
        ('Retirement', Retirement),
        ('TeamMateInPits', TeamMateInPits),
        ('RaceWinner', RaceWinner),
        ('Penalty', Penalty),
        ('SpeedTrap', SpeedTrap),
        ('StartLights', StartLights),
        ('DriveThroughPenaltyServed', DriveThroughPenaltyServed),
        ('StopGoPenaltyServed', StopGoPenaltyServed),
        ('Flashback', Flashback),
        ('Buttons', Buttons),
        ('Overtake', Overtake)
    ]

class ParticipantData(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_aiControlled', ct.c_uint8),            # Whether the vehicle is AI (1) or Human (0) controlled
        ('m_driverId', ct.c_uint8),                # Driver id - see appendix, 255 if network human
        ('m_networkId', ct.c_uint8),               # Network id – unique identifier for network players
        ('m_teamId', ct.c_uint8),                  # Team id - see appendix
        ('m_myTeam', ct.c_uint8),                  # My team flag – 1 = My Team, 0 = otherwise
        ('m_raceNumber', ct.c_uint8),              # Race number of the car
        ('m_nationality', ct.c_uint8),             # Nationality of the driver
        ('m_name', ct.c_char * 48),                # Name of participant in UTF-8 format – null terminated
        ('m_yourTelemetry', ct.c_uint8),           # The player's UDP setting, 0 = restricted, 1 = public
        ('m_showOnlineNames', ct.c_uint8),         # The player's show online names setting, 0 = off, 1 = on
        ('m_platform', ct.c_uint8),                # 1 = Steam, 3 = PlayStation, 4 = Xbox, 6 = Origin, 255 = unknown
    ]


class CarSetupData(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_frontWing', ct.c_uint8),                # Front wing aero
        ('m_rearWing', ct.c_uint8),                 # Rear wing aero
        ('m_onThrottle', ct.c_uint8),               # Differential adjustment on throttle (percentage)
        ('m_offThrottle', ct.c_uint8),              # Differential adjustment off throttle (percentage)
        ('m_frontCamber', ct.c_float),              # Front camber angle (suspension geometry)
        ('m_rearCamber', ct.c_float),               # Rear camber angle (suspension geometry)
        ('m_frontToe', ct.c_float),                 # Front toe angle (suspension geometry)
        ('m_rearToe', ct.c_float),                  # Rear toe angle (suspension geometry)
        ('m_frontSuspension', ct.c_uint8),          # Front suspension
        ('m_rearSuspension', ct.c_uint8),           # Rear suspension
        ('m_frontAntiRollBar', ct.c_uint8),         # Front anti-roll bar
        ('m_rearAntiRollBar', ct.c_uint8),          # Rear anti-roll bar
        ('m_frontSuspensionHeight', ct.c_uint8),    # Front ride height
        ('m_rearSuspensionHeight', ct.c_uint8),     # Rear ride height
        ('m_brakePressure', ct.c_uint8),            # Brake pressure (percentage)
        ('m_brakeBias', ct.c_uint8),                # Brake bias (percentage)
        ('m_rearLeftTyrePressure', ct.c_float),     # Rear left tyre pressure (PSI)
        ('m_rearRightTyrePressure', ct.c_float),    # Rear right tyre pressure (PSI)
        ('m_frontLeftTyrePressure', ct.c_float),    # Front left tyre pressure (PSI)
        ('m_frontRightTyrePressure', ct.c_float),   # Front right tyre pressure (PSI)
        ('m_ballast', ct.c_uint8),                  # Ballast
        ('m_fuelLoad', ct.c_float)                  # Fuel load
    ]

class CarTelemetryData(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_speed', ct.c_uint16),                            # Speed of car in kilometres per hour
        ('m_throttle', ct.c_float),                          # Amount of throttle applied (0.0 to 1.0)
        ('m_steer', ct.c_float),                             # Steering (-1.0 (full lock left) to 1.0 (full lock right))
        ('m_brake', ct.c_float),                             # Amount of brake applied (0.0 to 1.0)
        ('m_clutch', ct.c_uint8),                            # Amount of clutch applied (0 to 100)
        ('m_gear', ct.c_int8),                               # Gear selected (1-8, N=0, R=-1)
        ('m_engineRPM', ct.c_uint16),                        # Engine RPM
        ('m_drs', ct.c_uint8),                               # 0 = off, 1 = on
        ('m_revLightsPercent', ct.c_uint8),                  # Rev lights indicator (percentage)
        ('m_revLightsBitValue', ct.c_uint16),                # Rev lights (bit 0 = leftmost LED, bit 14 = rightmost LED)
        ('m_brakesTemperature', ct.c_uint16 * 4),            # Brakes temperature (celsius)
        ('m_tyresSurfaceTemperature', ct.c_uint8 * 4),       # Tyres surface temperature (celsius)
        ('m_tyresInnerTemperature', ct.c_uint8 * 4),         # Tyres inner temperature (celsius)
        ('m_engineTemperature', ct.c_uint16),                # Engine temperature (celsius)
        ('m_tyresPressure', ct.c_float * 4),                 # Tyres pressure (PSI)
        ('m_surfaceType', ct.c_uint8 * 4)                    # Driving surface, see appendices
    ]

class CarStatusData(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_tractionControl', ct.c_uint8),           # Traction control - 0 (off) - 2 (high)
        ('m_antiLockBrakes', ct.c_uint8),            # 0 (off) - 1 (on)
        ('m_fuelMix', ct.c_uint8),                   # Fuel mix - 0 = lean, 1 = standard, 2 = rich, 3 = max
        ('m_frontBrakeBias', ct.c_uint8),            # Front brake bias (percentage)
        ('m_pitLimiterStatus', ct.c_uint8),          # Pit limiter status - 0 = off, 1 = on
        ('m_fuelInTank', ct.c_float),                # Current fuel mass
        ('m_fuelCapacity', ct.c_float),              # Fuel capacity
        ('m_fuelRemainingLaps', ct.c_float),         # Fuel remaining in terms of laps (value on MFD)
        ('m_maxRPM', ct.c_uint16),                   # Cars max RPM, point of rev limiter
        ('m_idleRPM', ct.c_uint16),                  # Cars idle RPM
        ('m_maxGears', ct.c_uint8),                  # Maximum number of gears
        ('m_drsAllowed', ct.c_uint8),                # 0 = not allowed, 1 = allowed, -1 = unknown
        ('m_drsActivationDistance', ct.c_uint16),    # 0 = DRS not available, non-zero - DRS will be available in [X] metres
        ('m_actualTyreCompound', ct.c_uint8),        # Actual tyre compound
        ('m_visualTyreCompound', ct.c_uint8),        # Visual tyre compound
        ('m_tyresAgeLaps', ct.c_uint8),              # Age in laps of the current set of tyres
        ('m_vehicleFiaFlags', ct.c_int8),            # -1 = invalid/unknown, 0 = none, 1 = green, 2 = blue, 3 = yellow, 4 = red
        ('m_enginePowerICE', ct.c_float),             # Engine power output of ICE (W)
        ('m_enginePowerMGUK', ct.c_float),            # Engine power output of MGU-K (W)
        ('m_ersStoreEnergy', ct.c_float),            # ERS energy store in Joules
        ('m_ersDeployMode', ct.c_uint8),             # ERS deployment mode, 0 = none, 1 = medium, 2 = hotlap, 3 = overtake
        ('m_ersHarvestedThisLapMGUK', ct.c_float),   # ERS energy harvested this lap by MGU-K
        ('m_ersHarvestedThisLapMGUH', ct.c_float),   # ERS energy harvested this lap by MGU-H
        ('m_ersDeployedThisLap', ct.c_float),        # ERS energy deployed this lap
        ('m_networkPaused', ct.c_uint8)              # Whether the car is paused in a network game
    ]

class FinalClassificationData(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_position', ct.c_uint8),                  # Finishing position
        ('m_numLaps', ct.c_uint8),                   # Number of laps completed
        ('m_gridPosition', ct.c_uint8),              # Grid position of the car
        ('m_points', ct.c_uint8),                    # Number of points scored
        ('m_numPitStops', ct.c_uint8),               # Number of pit stops made
        ('m_resultStatus', ct.c_uint8),              # Result status
        ('m_bestLapTimeInMS', ct.c_uint32),          # Best lap time of the session in milliseconds
        ('m_totalRaceTime', ct.c_double),            # Total race time in seconds without penalties
        ('m_penaltiesTime', ct.c_uint8),             # Total penalties accumulated in seconds
        ('m_numPenalties', ct.c_uint8),              # Number of penalties applied to this driver
        ('m_numTyreStints', ct.c_uint8),             # Number of tyres stints up to maximum
        ('m_tyreStintsActual', ct.c_uint8 * 8),      # Actual tyres used by this driver
        ('m_tyreStintsVisual', ct.c_uint8 * 8),      # Visual tyres used by this driver
        ('m_tyreStintsEndLaps', ct.c_uint8 * 8)      # The lap number stints end on
    ]

class LobbyInfoData(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_aiControlled', ct.c_uint8),          # Whether the vehicle is AI (1) or Human (0) controlled
        ('m_teamId', ct.c_uint8),                # Team id - see appendix
        ('m_nationality', ct.c_uint8),           # Nationality of the driver
        ('m_name', ct.c_char * 48),              # Name of participant in UTF-8 format – null terminated
        ('m_carNumber', ct.c_uint8),             # Car number of the player
        ('m_readyStatus', ct.c_uint8)            # 0 = not ready, 1 = ready, 2 = spectating
    ]

class CarDamageData(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_tyresWear', ct.c_float * 4),          # Tyre wear (percentage)
        ('m_tyresDamage', ct.c_uint8 * 4),        # Tyre damage (percentage)
        ('m_brakesDamage', ct.c_uint8 * 4),       # Brakes damage (percentage)
        ('m_frontLeftWingDamage', ct.c_uint8),    # Front left wing damage (percentage)
        ('m_frontRightWingDamage', ct.c_uint8),   # Front right wing damage (percentage)
        ('m_rearWingDamage', ct.c_uint8),         # Rear wing damage (percentage)
        ('m_floorDamage', ct.c_uint8),            # Floor damage (percentage)
        ('m_diffuserDamage', ct.c_uint8),         # Diffuser damage (percentage)
        ('m_sidepodDamage', ct.c_uint8),          # Sidepod damage (percentage)
        ('m_drsFault', ct.c_uint8),               # Indicator for DRS fault, 0 = OK, 1 = fault
        ('m_ersFault', ct.c_uint8),               # Indicator for ERS fault, 0 = OK, 1 = fault
        ('m_gearBoxDamage', ct.c_uint8),          # Gear box damage (percentage)
        ('m_engineDamage', ct.c_uint8),           # Engine damage (percentage)
        ('m_engineMGUHWear', ct.c_uint8),         # Engine wear MGU-H (percentage)
        ('m_engineESWear', ct.c_uint8),           # Engine wear ES (percentage)
        ('m_engineCEWear', ct.c_uint8),           # Engine wear CE (percentage)
        ('m_engineICEWear', ct.c_uint8),          # Engine wear ICE (percentage)
        ('m_engineMGUKWear', ct.c_uint8),         # Engine wear MGU-K (percentage)
        ('m_engineTCWear', ct.c_uint8),           # Engine wear TC (percentage)
        ('m_engineBlown', ct.c_uint8),            # Engine blown, 0 = OK, 1 = fault
        ('m_engineSeized', ct.c_uint8)            # Engine seized, 0 = OK, 1 = fault
    ]

class LapHistoryData(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_lapTimeInMS', ct.c_uint32),         # Lap time in milliseconds
        ('m_sector1TimeInMS', ct.c_uint16),     # Sector 1 time in milliseconds
        ('m_sector1TimeMinutes', ct.c_uint8),   # Sector 1 whole minute part
        ('m_sector2TimeInMS', ct.c_uint16),     # Sector 2 time in milliseconds
        ('m_sector2TimeMinutes', ct.c_uint8),   # Sector 2 whole minute part
        ('m_sector3TimeInMS', ct.c_uint16),     # Sector 3 time in milliseconds
        ('m_sector3TimeMinutes', ct.c_uint8),   # Sector 3 whole minute part
        ('m_lapValidBitFlags', ct.c_uint8)      # Lap valid bit flags
    ]

class TyreStintHistoryData(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_endLap', ct.c_uint8),                # Lap the tyre usage ends on (255 of current tyre)
        ('m_tyreActualCompound', ct.c_uint8),    # Actual tyres used by this driver
        ('m_tyreVisualCompound', ct.c_uint8)     # Visual tyres used by this driver
    ]

class TyreSetData(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_actualTyreCompound', ct.c_uint8),       # Actual tyre compound used
        ('m_visualTyreCompound', ct.c_uint8),       # Visual tyre compound used
        ('m_wear', ct.c_uint8),                     # Tyre wear (percentage)
        ('m_available', ct.c_uint8),                # Whether this set is currently available
        ('m_recommendedSession', ct.c_uint8),       # Recommended session for tyre set
        ('m_lifeSpan', ct.c_uint8),                 # Laps left in this tyre set
        ('m_usableLife', ct.c_uint8),               # Max number of laps recommended for this compound
        ('m_lapDeltaTime', ct.c_int16),             # Lap delta time in milliseconds compared to fitted set
        ('m_fitted', ct.c_uint8)                    # Whether the set is fitted or not
    ]


"""Packet Data"""    



class PacketMotionData(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_carMotionData', CarMotionData * 22)
    ]

class PacketSessionData(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_weather', ct.c_uint8),
        ('m_trackTemperature', ct.c_int8),
        ('m_airTemperature', ct.c_int8),
        ('m_totalLaps', ct.c_uint8),
        ('m_trackLength', ct.c_uint16),
        ('m_sessionType', ct.c_uint8),
        ('m_trackId', ct.c_int8),
        ('m_formula', ct.c_uint8),
        ('m_sessionTimeLeft', ct.c_uint16),
        ('m_sessionDuration', ct.c_uint16),
        ('m_pitSpeedLimit', ct.c_uint8),
        ('m_gamePaused', ct.c_uint8),
        ('m_isSpectating', ct.c_uint8),
        ('m_spectatorCarIndex', ct.c_uint8),
        ('m_sliProNativeSupport', ct.c_uint8),
        ('m_numMarshalZones', ct.c_uint8),
        ('m_marshalZones', MarshalZone * 21),
        ('m_safetyCarStatus', ct.c_uint8),
        ('m_networkGame', ct.c_uint8),
        ('m_numWeatherForecastSamples', ct.c_uint8),
        ('m_weatherForecastSamples', WeatherForecastSample * 56),
        ('m_forecastAccuracy', ct.c_uint8),
        ('m_aiDifficulty', ct.c_uint8),
        ('m_seasonLinkIdentifier', ct.c_uint32),
        ('m_weekendLinkIdentifier', ct.c_uint32),
        ('m_sessionLinkIdentifier', ct.c_uint32),
        ('m_pitStopWindowIdealLap', ct.c_uint8),
        ('m_pitStopWindowLatestLap', ct.c_uint8),
        ('m_pitStopRejoinPosition', ct.c_uint8),
        ('m_steeringAssist', ct.c_uint8),
        ('m_brakingAssist', ct.c_uint8),
        ('m_gearboxAssist', ct.c_uint8),
        ('m_pitAssist', ct.c_uint8),
        ('m_pitReleaseAssist', ct.c_uint8),
        ('m_ERSAssist', ct.c_uint8),
        ('m_DRSAssist', ct.c_uint8),
        ('m_dynamicRacingLine', ct.c_uint8),
        ('m_dynamicRacingLineType', ct.c_uint8),
        ('m_gameMode', ct.c_uint8),
        ('m_ruleSet', ct.c_uint8),
        ('m_timeOfDay', ct.c_uint32),
        ('m_sessionLength', ct.c_uint8),
        ('m_speedUnitsLeadPlayer', ct.c_uint8),
        ('m_temperatureUnitsLeadPlayer', ct.c_uint8), 
        ('m_speedUnitsSecondaryPlayer', ct.c_uint8),
        ('m_temperatureUnitsSecondaryPlayer', ct.c_uint8), 
        ('m_numSafetyCarPeriods', ct.c_uint8),
        ('m_numVirtualSafetyCarPeriods', ct.c_uint8), 
        ('m_numRedFlagPeriods', ct.c_uint8)
    ]
        
class PacketLapData(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_lapData', LapData * 22),
        ('m_timeTrialPBCarIdx', ct.c_uint8),
        ('m_timeTrialRivalCarIdx', ct.c_uint8)
    ]

class PacketEventData(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),
        ('m_eventStringCode', ct.c_uint8 * 4),
        ('m_eventDetails', EventDataDetails)
    ]

class PacketParticipantsData(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),                # Header
        ('m_numActiveCars', ct.c_uint8),           # Number of active cars in the data – should match number of cars on HUD
        ('m_participants', ParticipantData * 22),  # Array of ParticipantData for up to 22 participants
    ]

class PacketCarSetupData(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),            # Header
        ('m_carSetups', CarSetupData * 22)     # Array of CarSetupData for up to 22 participants
    ]

class PacketCarTelemetryData(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),                         # Header
        ('m_carTelemetryData', CarTelemetryData * 22),      # Array of CarTelemetryData for up to 22 participants
        ('m_mfdPanelIndex', ct.c_uint8),                    # Index of MFD panel open - 255 = MFD closed
        ('m_mfdPanelIndexSecondaryPlayer', ct.c_uint8),     # Index of MFD panel open for secondary player
        ('m_suggestedGear', ct.c_int8)                      # Suggested gear for the player (1-8), 0 if no gear suggested
    ]

class PacketCarStatusData(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),                   # Header
        ('m_carStatusData', CarStatusData * 22)       # Array of CarStatusData for up to 22 participants
    ]

class PacketFinalClassificationData(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),                          # Header
        ('m_numCars', ct.c_uint8),                           # Number of cars in the final classification
        ('m_classificationData', FinalClassificationData * 22)  # Array of FinalClassificationData for up to 22 participants
    ]

class PacketLobbyInfoData(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),                      # Header
        ('m_numPlayers', ct.c_uint8),                    # Number of players in the lobby data
        ('m_lobbyPlayers', LobbyInfoData * 22)           # Array of LobbyInfoData for up to 22 participants
    ]

class PacketCarDamageData(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),                      # Header
        ('m_carDamageData', CarDamageData * 22)          # Array of CarDamageData for up to 22 participants
    ]

class PacketSessionHistoryData(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),                           # Header
        ('m_carIdx', ct.c_uint8),                             # Index of the car this lap data relates to
        ('m_numLaps', ct.c_uint8),                            # Num laps in the data (including current partial lap)
        ('m_numTyreStints', ct.c_uint8),                      # Number of tyre stints in the data
        ('m_bestLapTimeLapNum', ct.c_uint8),                  # Lap the best lap time was achieved on
        ('m_bestSector1LapNum', ct.c_uint8),                  # Lap the best Sector 1 time was achieved on
        ('m_bestSector2LapNum', ct.c_uint8),                  # Lap the best Sector 2 time was achieved on
        ('m_bestSector3LapNum', ct.c_uint8),                  # Lap the best Sector 3 time was achieved on
        ('m_lapHistoryData', LapHistoryData * 100),           # 100 laps of data max
        ('m_tyreStintsHistoryData', TyreStintHistoryData * 8) # 8 tyre stints of data max
    ]

class PacketTyreSetsData(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),                      # Header
        ('m_carIdx', ct.c_uint8),                        # Index of the car this data relates to
        ('m_tyreSetData', TyreSetData * 20),             # 13 (dry) + 7 (wet)
        ('m_fittedIdx', ct.c_uint8)                      # Index into array of fitted tyre
    ]

class PacketMotionExData(ct.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('m_header', PacketHeader),                             # Header
        ('m_suspensionPosition', ct.c_float * 4),               # Suspension position (RL, RR, FL, FR)
        ('m_suspensionVelocity', ct.c_float * 4),               # Suspension velocity (RL, RR, FL, FR)
        ('m_suspensionAcceleration', ct.c_float * 4),           # Suspension acceleration (RL, RR, FL, FR)
        ('m_wheelSpeed', ct.c_float * 4),                       # Speed of each wheel
        ('m_wheelSlipRatio', ct.c_float * 4),                   # Slip ratio for each wheel
        ('m_wheelSlipAngle', ct.c_float * 4),                   # Slip angles for each wheel
        ('m_wheelLatForce', ct.c_float * 4),                    # Lateral forces for each wheel
        ('m_wheelLongForce', ct.c_float * 4),                   # Longitudinal forces for each wheel
        ('m_heightOfCOGAboveGround', ct.c_float),               # Height of centre of gravity above ground
        ('m_localVelocityX', ct.c_float),                       # Velocity in local space – metres/s
        ('m_localVelocityY', ct.c_float),                       # Velocity in local space
        ('m_localVelocityZ', ct.c_float),                       # Velocity in local space
        ('m_angularVelocityX', ct.c_float),                     # Angular velocity x-component – radians/s
        ('m_angularVelocityY', ct.c_float),                     # Angular velocity y-component
        ('m_angularVelocityZ', ct.c_float),                     # Angular velocity z-component
        ('m_angularAccelerationX', ct.c_float),                 # Angular acceleration x-component – radians/s/s
        ('m_angularAccelerationY', ct.c_float),                 # Angular acceleration y-component
        ('m_angularAccelerationZ', ct.c_float),                 # Angular acceleration z-component
        ('m_frontWheelsAngle', ct.c_float),                     # Current front wheels angle in radians
        ('m_wheelVertForce', ct.c_float * 4)                    # Vertical forces for each wheel
    ]