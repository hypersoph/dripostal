"""Asynchronous client for Pelias Libpostal Service.

Dribia 2021/03/23, Nabil Kakeh <nabil@dribia.com>
"""

from typing import List

try:
    from aiohttp import ClientSession
except ModuleNotFoundError as e:
    msg = (
        e.msg
        + " You can install it as an optional dependency installing dripostal[aiohttp]."
    )
    raise ModuleNotFoundError(msg)

from . import DriPostal as _BaseDriPostal
from .schemas import Address

from pydantic import AnyHttpUrl

# modified so that clientsession is passed into the class

class DriPostal(_BaseDriPostal):
    """Asynchronous version of the DriPostal client."""
    
    def __init__(
        self, url: str, session, parse_method: str = "parse", expand_method: str = "expand"
    ):
        """Dripostal configuration.

        Args:
            url: URL of the Libpostal service.
            parse_method: Parse method name in the API.
            expand_method: Expand method name in the API.

        """
        self.service_url: AnyHttpUrl = self._parse_url(url)
        self._parse_method: str = parse_method
        self._expand_method: str = expand_method
        self.session = session

    async def parse(self, address: str) -> Address:  # type: ignore
        """Parse an address with Libpostal.

        Args:
            address: Address to parse, in plain text.

        Returns: Parsed address.

        """
        request_url = self._get_url(method="parse", address=address)

        async with self.session.get(request_url) as response:
            payload = await response.json()
            return Address(**{el["label"]: el["value"] for el in payload})

    async def expand(self, address: str) -> List[str]:  # type: ignore
        """Expand an address with Libpostal.

        Args:
            address: Address to expand, in plain text.

        Returns: Expanded address.

        """
        request_url = self._get_url(method="expand", address=address)

        async with self.session.get(request_url) as response:
            return await response.json()


__all__ = ["DriPostal"]

