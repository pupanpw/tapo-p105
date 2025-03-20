from flask import Flask, jsonify
from kasa import Discover, SmartPlug
import asyncio
import logging
import os

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

USERNAME = os.getenv("KASA_USERNAME")
PASSWORD = os.getenv("KASA_PASSWORD")


async def get_device():
    """ ค้นหาอุปกรณ์ Kasa ที่อยู่ในเครือข่าย """
    try:
        devices = await Discover.discover(
            username=USERNAME,
            password=PASSWORD,
            discovery_timeout=1
        )
        if devices:
            ip, device = next(iter(devices.items()))
            return {"ip": ip, "alias": device.alias, "model": device.model, "device": device}
        else:
            # หากไม่พบอุปกรณ์
            logging.warning("No device found in the network.")
            return None
    except Exception as e:
        logging.error(f"Failed to discover or update device: {e}")
        return None


@app.route('/', methods=['GET'])
def test():
    device_info = asyncio.run(get_device())
    if device_info:
        return jsonify({
            "ip": device_info['ip'],
            "user": USERNAME,
            "model": device_info['model']
        })
    return jsonify({"error": "No device found"}), 404


@app.route('/on', methods=['GET'])
def turn_on():
    device_info = asyncio.run(get_device())
    if device_info and device_info.get('device'):
        device = device_info['device']
        asyncio.run(device.turn_on())  # เปิดอุปกรณ์
        return jsonify({"status": "Device turned on"})
    return jsonify({"error": "No device found"}), 404


@app.route('/off', methods=['GET'])
def turn_off():
    device_info = asyncio.run(get_device())
    if device_info and device_info.get('device'):
        device = device_info['device']
        asyncio.run(device.turn_off())  # ปิดอุปกรณ์
        return jsonify({"status": "Device turned off"})
    return jsonify({"error": "No device found"}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
