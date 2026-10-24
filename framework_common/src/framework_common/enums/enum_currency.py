"""Shared quote currencies and crypto quote units."""

from enum import Enum
from typing import Self

from framework_common.enums.enum_currency_type import EnumCurrencyType


class EnumCurrency(Enum):
    """Identify fiat and crypto quote units shared by applications."""

    # region Constants

    # region Fiat Currencies

    # Fiat currencies use ISO 4217 alphabetic codes.
    AUD: tuple[str, EnumCurrencyType] = ("AUD", EnumCurrencyType.FIAT)
    BRL: tuple[str, EnumCurrencyType] = ("BRL", EnumCurrencyType.FIAT)
    CAD: tuple[str, EnumCurrencyType] = ("CAD", EnumCurrencyType.FIAT)
    CHF: tuple[str, EnumCurrencyType] = ("CHF", EnumCurrencyType.FIAT)
    CNY: tuple[str, EnumCurrencyType] = ("CNY", EnumCurrencyType.FIAT)
    DKK: tuple[str, EnumCurrencyType] = ("DKK", EnumCurrencyType.FIAT)
    EUR: tuple[str, EnumCurrencyType] = ("EUR", EnumCurrencyType.FIAT)
    GBP: tuple[str, EnumCurrencyType] = ("GBP", EnumCurrencyType.FIAT)
    HKD: tuple[str, EnumCurrencyType] = ("HKD", EnumCurrencyType.FIAT)
    INR: tuple[str, EnumCurrencyType] = ("INR", EnumCurrencyType.FIAT)
    JPY: tuple[str, EnumCurrencyType] = ("JPY", EnumCurrencyType.FIAT)
    KRW: tuple[str, EnumCurrencyType] = ("KRW", EnumCurrencyType.FIAT)
    MXN: tuple[str, EnumCurrencyType] = ("MXN", EnumCurrencyType.FIAT)
    NOK: tuple[str, EnumCurrencyType] = ("NOK", EnumCurrencyType.FIAT)
    NZD: tuple[str, EnumCurrencyType] = ("NZD", EnumCurrencyType.FIAT)
    SEK: tuple[str, EnumCurrencyType] = ("SEK", EnumCurrencyType.FIAT)
    SGD: tuple[str, EnumCurrencyType] = ("SGD", EnumCurrencyType.FIAT)
    TWD: tuple[str, EnumCurrencyType] = ("TWD", EnumCurrencyType.FIAT)
    USD: tuple[str, EnumCurrencyType] = ("USD", EnumCurrencyType.FIAT)
    ZAR: tuple[str, EnumCurrencyType] = ("ZAR", EnumCurrencyType.FIAT)

    # endregion Fiat Currencies

    # region Cryptocurrencies

    # Crypto quote units use market symbols, not network identifiers.
    ADA: tuple[str, EnumCurrencyType] = ("ADA", EnumCurrencyType.CRYPTO)
    BCH: tuple[str, EnumCurrencyType] = ("BCH", EnumCurrencyType.CRYPTO)
    BNB: tuple[str, EnumCurrencyType] = ("BNB", EnumCurrencyType.CRYPTO)
    BTC: tuple[str, EnumCurrencyType] = ("BTC", EnumCurrencyType.CRYPTO)
    DOGE: tuple[str, EnumCurrencyType] = ("DOGE", EnumCurrencyType.CRYPTO)
    ETH: tuple[str, EnumCurrencyType] = ("ETH", EnumCurrencyType.CRYPTO)
    LTC: tuple[str, EnumCurrencyType] = ("LTC", EnumCurrencyType.CRYPTO)
    SOL: tuple[str, EnumCurrencyType] = ("SOL", EnumCurrencyType.CRYPTO)
    TRX: tuple[str, EnumCurrencyType] = ("TRX", EnumCurrencyType.CRYPTO)
    XRP: tuple[str, EnumCurrencyType] = ("XRP", EnumCurrencyType.CRYPTO)

    # endregion Cryptocurrencies

    # region Stablecoins

    DAI: tuple[str, EnumCurrencyType] = ("DAI", EnumCurrencyType.STABLE)
    USDC: tuple[str, EnumCurrencyType] = ("USDC", EnumCurrencyType.STABLE)
    USDT: tuple[str, EnumCurrencyType] = ("USDT", EnumCurrencyType.STABLE)

    # endregion Stablecoins

    # endregion Constants

    # region Properties

    @property
    def currency_type(self) -> EnumCurrencyType:
        return self._enm_currency_type

    # endregion Properties

    # region Constructor & Special Methods

    def __new__(cls, str_code: str, enm_currency_type: EnumCurrencyType) -> Self:
        _enm_member: Self = object.__new__(cls)
        _enm_member._value_ = str_code
        _enm_member._enm_currency_type: EnumCurrencyType = enm_currency_type
        return _enm_member

    # endregion Constructor & Special Methods
