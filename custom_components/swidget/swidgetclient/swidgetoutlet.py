import logging

from .device import (
    DeviceType,
    SwidgetDevice
)

_LOGGER = logging.getLogger(__name__)


class SwidgetOutlet(SwidgetDevice):

    def __init__(self, host,  secret_key: str, ssl: bool) -> None:
        super().__init__(host=host, secret_key=secret_key, ssl=ssl)
        self._device_type = DeviceType.Outlet

    @property  # type: ignore
    def is_on(self) -> bool:
        """Return whether device is on.

        Returns False if state cannot be determined (better safe than sorry for heaters).
        """
        try:
            dimmer_state = self.assemblies['host'].components["0"].functions['toggle']["state"]
            return dimmer_state == "on"
        except (KeyError, TypeError, AttributeError) as ex:
            _LOGGER.warning(f"Could not determine device state, assuming OFF: {ex}")
            return False  # Default to OFF for safety (heaters should not default to ON)

    async def turn_on(self):
        """Turn the device on."""
        _LOGGER.info(f"Turning ON outlet at {self.ip_address}")
        await self.send_command(
            assembly="host", component="0", function="toggle", command={"state": "on"}
        )

    async def turn_off(self):
        """Turn the device off."""
        _LOGGER.info(f"Turning OFF outlet at {self.ip_address}")
        await self.send_command(
            assembly="host", component="0", function="toggle", command={"state": "off"}
        )

    async def turn_on_usb_insert(self):
        """Turn the USB insert on."""
        _LOGGER.info(f"Turning ON USB insert at {self.ip_address}")
        await self.send_command(
            assembly="insert", component="usb", function="toggle", command={"state": "on"}
        )

    async def turn_off_usb_insert(self):
        """Turn the USB insert off."""
        _LOGGER.info(f"Turning OFF USB insert at {self.ip_address}")
        await self.send_command(
            assembly="insert", component="usb", function="toggle", command={"state": "off"}
        )

    @property  # type: ignore
    def usb_is_on(self) -> bool:
        """Return whether USB is on.

        Returns False if state cannot be determined.
        """
        try:
            usb_state = self.assemblies['insert'].components["usb"].functions['toggle']["state"]
            return usb_state == "on"
        except (KeyError, TypeError, AttributeError) as ex:
            _LOGGER.warning(f"Could not determine USB state, assuming OFF: {ex}")
            return False  # Default to OFF for safety