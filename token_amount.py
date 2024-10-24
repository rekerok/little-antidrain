from typing import Union

from loguru import logger


class Token_Amount:
    def __init__(
        self, amount: Union[float, int], decimals: int = 18, wei: bool = False
    ) -> None:
        if wei:
            self.WEI = int(amount)
            self.ETHER = float(amount / pow(10, decimals))
        else:
            self.WEI = int(amount * pow(10, decimals))
            self.ETHER = float(amount)
        self.DECIMAL = decimals
