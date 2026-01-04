"""Common code for tplink."""
from __future__ import annotations

from collections.abc import Awaitable, Callable, Coroutine
from typing import Any, TypeVar

from .swidgetclient.device import SwidgetDevice
from typing_extensions import Concatenate, ParamSpec

from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import SwidgetDataUpdateCoordinator

_T = TypeVar("_T", bound="CoordinatedSwidgetEntity")
_P = ParamSpec("_P")


def async_refresh_after(
    func: Callable[Concatenate[_T, _P], Awaitable[None]]  # type: ignore[misc]
) -> Callable[Concatenate[_T, _P], Coroutine[Any, Any, None]]:  # type: ignore[misc]
    """Define a wrapper to refresh after."""

    async def _async_wrap(self: _T, *args: _P.args, **kwargs: _P.kwargs) -> None:
        await func(self, *args, **kwargs)
        await self.coordinator.async_request_refresh_without_children()

    return _async_wrap


class CoordinatedSwidgetEntity(CoordinatorEntity[SwidgetDataUpdateCoordinator]):
    """Common base class for all coordinated tplink entities."""

    def __init__(
        self, device: SwidgetDevice, coordinator: SwidgetDataUpdateCoordinator
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self.device: SwidgetDevice = device
        self._attr_name = self.device.mac_address.replace(":", "").upper()
        self._attr_unique_id = self.device.id

    @property
    def device_info(self) -> DeviceInfo:
        """Return information about the device."""
        return DeviceInfo(
            connections={(dr.CONNECTION_NETWORK_MAC, self.device.mac_address)},
            identifiers={(DOMAIN, str(self.device.id))},
            manufacturer="Swidget",
            model=self.device.model,
            name=self.device.friendly_name,
            sw_version=self.device.version,
        )

    @property
    def available(self) -> bool:
        """Return True if entity is available.

        Device is considered available if:
        1. Websocket is connected, OR
        2. We've received an update recently (last 60 seconds)
        """
        import time
        from .swidgetclient.websocket import STATE_CONNECTED

        # Check websocket connection status
        if self.device.use_websockets and hasattr(self.device, '_websocket'):
            if self.device._websocket.state == STATE_CONNECTED:
                return True

        # Fallback: check if we've received a recent update
        if hasattr(self.device, '_last_update') and self.device._last_update:
            time_since_update = time.time() - self.device._last_update
            return time_since_update < 60  # Consider unavailable after 60s

        return False

    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        return bool(self.device.is_on)
