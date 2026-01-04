# Swidget Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

Home Assistant integration for Swidget smart outlets, switches, and dimmers with modular insert support.

## Overview

[Swidget](https://www.swidget.com/) devices are smart outlets and switches that feature removable inserts for additional functionality like motion sensors, USB charging, ambient light sensors, and more. This integration brings full control of Swidget devices to Home Assistant.

## Features

- **Real-time Control**: Turn outlets and switches on/off instantly
- **WebSocket Support**: Live state updates without polling
- **Multi-Device Support**: Control outlets, switches, dimmers, and timer switches
- **Insert Support**: Access functionality from Swidget inserts (USB, sensors, etc.)
- **Power Monitoring**: Track power consumption on supported devices
- **Automatic Discovery**: Devices are discovered via SSDP and DHCP
- **Availability Tracking**: Know when devices are offline or unreachable

## Supported Devices

- Swidget Outlets (Standard and 20A)
- Swidget Switches
- Swidget Dimmers
- Swidget Timer Switches
- USB Inserts
- Sensor Inserts (motion, ambient light, etc.)

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots in the top right
4. Select "Custom repositories"
5. Add this repository URL and select "Integration" as the category
6. Click "Install"
7. Restart Home Assistant

### Manual Installation

1. Download the latest release
2. Copy the `custom_components/swidget` folder to your Home Assistant `config/custom_components/` directory
3. Restart Home Assistant

## Configuration

### Automatic Discovery

Swidget devices are automatically discovered via SSDP and DHCP. After installation:

1. Go to **Settings** → **Devices & Services**
2. Look for discovered Swidget devices
3. Click **Configure** and follow the prompts
4. Enter the device password if required

### Manual Configuration

If automatic discovery doesn't work:

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for "Swidget"
4. Enter the device IP address and password

## Usage

### Entities

Each Swidget device creates the following entities:

- **Switch/Light**: Main outlet or switch control
- **USB Switch**: Control USB insert (if present)
- **Sensors**: Power consumption, RSSI, and insert sensors
- **Binary Sensors**: Insert-specific sensors (motion, occupancy, etc.)

### Services

Standard Home Assistant services are supported:
- `switch.turn_on` / `switch.turn_off`
- `light.turn_on` / `light.turn_off` (for dimmers)

Timer switches also support:
- `swidget.set_countdown_timer` - Set a countdown timer (1-1440 minutes)

### Automations

Example automation to turn on an outlet:

```yaml
automation:
  - alias: "Turn on patio heater"
    trigger:
      - platform: sun
        event: sunset
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.swidget_patio_heater
```

## Troubleshooting

### Device Not Discovered

1. Ensure your Swidget device is on the same network as Home Assistant
2. Check that SSDP/mDNS is not blocked by your router or firewall
3. Try manual configuration with the device IP address

### Device Unavailable

The integration shows devices as unavailable when:
- WebSocket connection is lost
- No updates received for 60 seconds

Check:
- Device is powered on and connected to WiFi
- Network connectivity between Home Assistant and device
- Home Assistant logs for connection errors

### Excessive Logging

If you see too many debug messages, check your Home Assistant logging level:

```yaml
logger:
  default: info
  logs:
    custom_components.swidget: warning
```

Set to `debug` only when troubleshooting.

## Development

### Recent Improvements

This fork includes several reliability and performance improvements:

- **Reduced Logging**: Fixed excessive ERROR-level logging (now uses appropriate levels)
- **Optimized Polling**: Reduced polling from 0.5s to 30s (WebSockets handle real-time updates)
- **Better Error Handling**: Specific exception handling instead of bare `except` clauses
- **Availability Tracking**: Devices correctly show as unavailable when disconnected
- **Safe Defaults**: State properties default to OFF when state is unclear
- **Audit Trail**: INFO-level logging for critical state changes

### Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with clear commit messages
4. Test thoroughly
5. Submit a pull request

## License

This integration is provided as-is under the MIT License.

## Credits

- Original integration by [@michaelkkehoe](https://github.com/michaelkkehoe)
- Improvements and reliability fixes by [@irvintim](https://github.com/irvintim)

## Support

- **Issues**: [GitHub Issues](https://github.com/irvintim/haswidget2/issues)
- **Swidget Support**: [www.swidget.com](https://www.swidget.com)
- **Home Assistant Community**: [Home Assistant Forums](https://community.home-assistant.io/)

---

**Swidget** - Power to Live Smart
