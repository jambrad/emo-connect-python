#
# This file is part of emo-connect-python (https://github.com/0xD34D/emo-connect-python).
# Copyright (c) 2022 Clark Scheff.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
import asyncio
import json
import logging

from emoconnect.EmoConnectManager import EmoConnectManager
from emoconnect.ble.request import (
    AnimationRequest,
    PowerRequest,
    SettingRequest,
    StateRequest,
    WifiSettingRequest,
)

logging.basicConfig(format='[EMO] %(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger()
# can be changed to logging.DEBUG for debugging issues
logger.setLevel(logging.INFO)


async def sendRequest(ecm: EmoConnectManager, request: bytes):
    response = await ecm.sendRequest(request)
    print(f'{json.dumps(response, indent=4)}')


async def main():
    ecm = EmoConnectManager()
    await ecm.connectToEmo()

    preferences = await ecm.sendRequest(StateRequest.preference())
    print(preferences)

    # Enter settings mode
    await sendRequest(ecm, SettingRequest.enterSettingMode())

    # the below code will indeed set the wifi setting so feel
    # free to uncomment and play with it ;)
    # await sendRequest(ecm, WifiSettingRequest.setWifi('Groot', 'I_am_groot!'))
    # await sendRequest(ecm, StateRequest.network())
    
    await sendRequest(ecm, SettingRequest.setAutoUpdate(True))
    await sendRequest(ecm, SettingRequest.setAutoUpdate(False))
    await sendRequest(ecm, SettingRequest.setSchedule(True))
    await sendRequest(ecm, SettingRequest.setSchedule(False))
    await sendRequest(ecm, SettingRequest.setScheduleSound(True))
    await sendRequest(ecm, SettingRequest.setScheduleSound(False))
    await sendRequest(ecm, SettingRequest.setTemp(True))
    await sendRequest(ecm, SettingRequest.setTemp(False))
    await sendRequest(ecm, SettingRequest.setLength(True))
    await sendRequest(ecm, SettingRequest.setLength(False))
    await sendRequest(ecm, SettingRequest.setVolumeMute())
    await sendRequest(ecm, SettingRequest.setVolumeLow())
    await sendRequest(ecm, SettingRequest.setVolumeMedium())
    await sendRequest(ecm, SettingRequest.setVolumeHigh())

    # return settings to what they were before we messed it all up
    preferences = preferences['data']['preference']
    await sendRequest(ecm, SettingRequest.setAutoUpdate(preferences['auto_update'] == 1))
    await sendRequest(ecm, SettingRequest.setSchedule(preferences['schedule'] == 1))
    await sendRequest(ecm, SettingRequest.setScheduleSound(preferences['schedule_sound'] == 1))
    await sendRequest(ecm, SettingRequest.setLength(preferences['length'] == 0))
    await sendRequest(ecm, SettingRequest.setTemp(preferences['temperature'] == 0))
    volume = preferences['volume']
    if volume == 3:
        await sendRequest(ecm, SettingRequest.setVolumeHigh())
    elif volume == 2:
        await sendRequest(ecm, SettingRequest.setVolumeMedium())
    elif volume == 1:
        await sendRequest(ecm, SettingRequest.setVolumeLow())
    else:
        await sendRequest(ecm, SettingRequest.setVolumeMute())

    # exit settings mode
    await sendRequest(ecm, SettingRequest.exitSettingMode())

    await sendRequest(ecm, AnimationRequest.enterAnimationMode())
    for i in range(0, len(AnimationRequest.DANCE_LIST)):
        await sendRequest(ecm, AnimationRequest.playEmoDance(i))
        await asyncio.sleep(5)
    await sendRequest(ecm, AnimationRequest.exitAnimationMode())

    await sendRequest(ecm, PowerRequest.powerOff())
    await ecm.disconnect()

asyncio.run(main())
