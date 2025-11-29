from flask import Flask, jsonify, request, abort
from kasa import Discover
import asyncio
import logging
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.DEBUG)
load_dotenv()

USERNAME = os.getenv("KASA_USERNAME")
PASSWORD = os.getenv("KASA_PASSWORD")
SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)


async def get_device():
    try:
        devices = await Discover.discover(
            username=USERNAME,
            password=PASSWORD,
            discovery_timeout=1
        )
        if devices:
            ip, device = next(iter(devices.items()))
            return {"ip": ip, "alias": device.alias, "model": device.model, "device": device}
        logging.warning("No device found in the network.")
        return None
    except Exception as e:
        logging.error(f"Failed to discover device: {e}")
        return None


def check_secret():
    token = request.headers.get("X-SECRET-KEY") or request.args.get("key")
    print("Received token:", token)
    if not token or token.strip() != SECRET_KEY.strip():
        abort(401, description="Unauthorized: Invalid Secret Key")


@app.route('/', methods=['GET'])
def test():
    check_secret()
    device_info = asyncio.run(get_device())
    if device_info:
        return jsonify({
            "ip": device_info['ip'],
            "user": USERNAME,
            "alias": device_info['alias'],
            "model": device_info['model']
        })
    return jsonify({"error": "No device found"}), 404


@app.route('/on', methods=['GET'])
def turn_on():
    check_secret()
    device_info = asyncio.run(get_device())
    if device_info and device_info.get('device'):
        device = device_info['device']
        asyncio.run(device.turn_on())
        return jsonify({"status": "Device turned on"})
    return jsonify({"error": "No device found"}), 404


@app.route('/off', methods=['GET'])
def turn_off():
    check_secret()
    device_info = asyncio.run(get_device())
    if device_info and device_info.get('device'):
        device = device_info['device']
        asyncio.run(device.turn_off())
        return jsonify({"status": "Device turned off"})
    return jsonify({"error": "No device found"}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
