import re
import aiohttp
import asyncio
from aiohttp import ClientSession, TCPConnector
from vehicle.models import Vehicle

TRACCAR_URL = 'https://gps.ojar.asia/api'
TRACCAR_USER = 's.taganov@amatly-chozgut.biz'
TRACCAR_PASSWORD = 'ManGusT_6767'


def get_registration_number(device_name):
    match = re.match(r'^(\S+ \S+)', device_name)
    return match.group(1) if match else None


async def fetch_json(session, url):
    async with session.get(url, auth=aiohttp.BasicAuth(TRACCAR_USER, TRACCAR_PASSWORD), ssl=False) as response:
        return await response.json()


async def process_position(session, position):
    device_id = position['deviceId']
    total_distance = position['attributes'].get('totalDistance', 0)

    device_url = f'{TRACCAR_URL}/devices/{device_id}'
    device = await fetch_json(session, device_url)

    registration_number = get_registration_number(device['name'])

    if registration_number:
        try:
            vehicle = await Vehicle.objects.aget(registration_number=registration_number)
            print(vehicle)
            vehicle.total_distance = total_distance / 1000
            await vehicle.asave()
        except Vehicle.DoesNotExist:
            print(f'Vehicle with registration number {registration_number} not found')


async def update_vehicle_distances():
    async with ClientSession(connector=TCPConnector(ssl=False)) as session:
        positions_url = f'{TRACCAR_URL}/positions'
        positions = await fetch_json(session, positions_url)

        tasks = [process_position(session, position) for position in positions]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(update_vehicle_distances())
