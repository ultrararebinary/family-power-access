"""Shared Home Assistant fixtures for Family Power Access."""

import pytest


@pytest.fixture(autouse=True)
def load_custom_integrations(enable_custom_integrations: None) -> None:
    """Permit Home Assistant to load this repository's custom integration."""
