"""Component to embed TP-Link smart home devices."""
from __future__ import annotations

from datetime import timedelta
import logging

from .swidgetclient.device import SwidgetDevice
from .swidgetclient.exceptions import SwidgetException

from homeassistant.core import HomeAssistant
from homeassistant.helpers.debounce import Debouncer
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

REQUEST_REFRESH_DELAY = 0.35


class SwidgetDataUpdateCoordinator(DataUpdateCoordinator):
    """DataUpdateCoordinator to gather data for a specific Swidget device."""

    def __init__(
        self,
        hass: HomeAssistant,
        device: SwidgetDevice,
    ) -> None:
        """Initialize DataUpdateCoordinator to gather data for specific device"""
        self.device = device
        # Since we're using websockets for real-time updates, we only need occasional
        # polling as a fallback to detect connection issues
        update_interval = timedelta(seconds=30)
        super().__init__(
            hass,
            _LOGGER,
            name=device.ip_address,
            update_interval=update_interval,
            # We don't want an immediate refresh since the device
            # takes a moment to reflect the state change
            request_refresh_debouncer=Debouncer(
                hass, _LOGGER, cooldown=REQUEST_REFRESH_DELAY, immediate=False
            ),
        )

    async def async_request_refresh_without_children(self) -> None:
        """Request a refresh without the children."""
        # If the children do get updated this is ok as this is an
        # optimization to reduce the number of requests on the device
        # when we do not need it.
        await self.async_request_refresh()

    async def _async_update_data(self) -> None:
        """Fetch all device and sensor data from api."""
        # Since we're using websockets for real-time updates, this polling
        # is just a fallback. The websocket callbacks handle state updates.
        # We don't need to fetch data here as it would be redundant.
        return
