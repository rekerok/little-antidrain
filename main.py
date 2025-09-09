import asyncio
import random

from loguru import logger
from web3 import AsyncHTTPProvider, AsyncWeb3, Web3
from web3.middleware import async_geth_poa_middleware
import eth_utils
from eth_account import Account

from token_amount import Token_Amount

CHECK_INTERVAL = 0  # как часто чекать кошель в секундах
TOKEN_ABI = '[{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"address","name":"_lzEndpoint","type":"address"},{"internalType":"address","name":"_delegate","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"target","type":"address"}],"name":"AddressEmptyCode","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"AddressInsufficientBalance","type":"error"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"allowance","type":"uint256"},{"internalType":"uint256","name":"needed","type":"uint256"}],"name":"ERC20InsufficientAllowance","type":"error"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"uint256","name":"balance","type":"uint256"},{"internalType":"uint256","name":"needed","type":"uint256"}],"name":"ERC20InsufficientBalance","type":"error"},{"inputs":[{"internalType":"address","name":"approver","type":"address"}],"name":"ERC20InvalidApprover","type":"error"},{"inputs":[{"internalType":"address","name":"receiver","type":"address"}],"name":"ERC20InvalidReceiver","type":"error"},{"inputs":[{"internalType":"address","name":"sender","type":"address"}],"name":"ERC20InvalidSender","type":"error"},{"inputs":[{"internalType":"address","name":"spender","type":"address"}],"name":"ERC20InvalidSpender","type":"error"},{"inputs":[],"name":"FailedInnerCall","type":"error"},{"inputs":[],"name":"InvalidDelegate","type":"error"},{"inputs":[],"name":"InvalidEndpointCall","type":"error"},{"inputs":[],"name":"InvalidLocalDecimals","type":"error"},{"inputs":[{"internalType":"bytes","name":"options","type":"bytes"}],"name":"InvalidOptions","type":"error"},{"inputs":[],"name":"LzTokenUnavailable","type":"error"},{"inputs":[{"internalType":"uint32","name":"eid","type":"uint32"}],"name":"NoPeer","type":"error"},{"inputs":[{"internalType":"uint256","name":"msgValue","type":"uint256"}],"name":"NotEnoughNative","type":"error"},{"inputs":[{"internalType":"address","name":"addr","type":"address"}],"name":"OnlyEndpoint","type":"error"},{"inputs":[{"internalType":"uint32","name":"eid","type":"uint32"},{"internalType":"bytes32","name":"sender","type":"bytes32"}],"name":"OnlyPeer","type":"error"},{"inputs":[],"name":"OnlySelf","type":"error"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"OwnableInvalidOwner","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"OwnableUnauthorizedAccount","type":"error"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"SafeERC20FailedOperation","type":"error"},{"inputs":[{"internalType":"bytes","name":"result","type":"bytes"}],"name":"SimulationResult","type":"error"},{"inputs":[{"internalType":"uint256","name":"amountLD","type":"uint256"},{"internalType":"uint256","name":"minAmountLD","type":"uint256"}],"name":"SlippageExceeded","type":"error"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"components":[{"internalType":"uint32","name":"eid","type":"uint32"},{"internalType":"uint16","name":"msgType","type":"uint16"},{"internalType":"bytes","name":"options","type":"bytes"}],"indexed":false,"internalType":"struct EnforcedOptionParam[]","name":"_enforcedOptions","type":"tuple[]"}],"name":"EnforcedOptionSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"inspector","type":"address"}],"name":"MsgInspectorSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"guid","type":"bytes32"},{"indexed":false,"internalType":"uint32","name":"srcEid","type":"uint32"},{"indexed":true,"internalType":"address","name":"toAddress","type":"address"},{"indexed":false,"internalType":"uint256","name":"amountReceivedLD","type":"uint256"}],"name":"OFTReceived","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"guid","type":"bytes32"},{"indexed":false,"internalType":"uint32","name":"dstEid","type":"uint32"},{"indexed":true,"internalType":"address","name":"fromAddress","type":"address"},{"indexed":false,"internalType":"uint256","name":"amountSentLD","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amountReceivedLD","type":"uint256"}],"name":"OFTSent","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint32","name":"eid","type":"uint32"},{"indexed":false,"internalType":"bytes32","name":"peer","type":"bytes32"}],"name":"PeerSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"preCrimeAddress","type":"address"}],"name":"PreCrimeSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"SEND","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"SEND_AND_CALL","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"uint32","name":"srcEid","type":"uint32"},{"internalType":"bytes32","name":"sender","type":"bytes32"},{"internalType":"uint64","name":"nonce","type":"uint64"}],"internalType":"struct Origin","name":"origin","type":"tuple"}],"name":"allowInitializePath","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"approvalRequired","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint32","name":"_eid","type":"uint32"},{"internalType":"uint16","name":"_msgType","type":"uint16"},{"internalType":"bytes","name":"_extraOptions","type":"bytes"}],"name":"combineOptions","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimalConversionRate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"endpoint","outputs":[{"internalType":"contract ILayerZeroEndpointV2","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint32","name":"eid","type":"uint32"},{"internalType":"uint16","name":"msgType","type":"uint16"}],"name":"enforcedOptions","outputs":[{"internalType":"bytes","name":"enforcedOption","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"uint32","name":"srcEid","type":"uint32"},{"internalType":"bytes32","name":"sender","type":"bytes32"},{"internalType":"uint64","name":"nonce","type":"uint64"}],"internalType":"struct Origin","name":"","type":"tuple"},{"internalType":"bytes","name":"","type":"bytes"},{"internalType":"address","name":"_sender","type":"address"}],"name":"isComposeMsgSender","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint32","name":"_eid","type":"uint32"},{"internalType":"bytes32","name":"_peer","type":"bytes32"}],"name":"isPeer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"uint32","name":"srcEid","type":"uint32"},{"internalType":"bytes32","name":"sender","type":"bytes32"},{"internalType":"uint64","name":"nonce","type":"uint64"}],"internalType":"struct Origin","name":"_origin","type":"tuple"},{"internalType":"bytes32","name":"_guid","type":"bytes32"},{"internalType":"bytes","name":"_message","type":"bytes"},{"internalType":"address","name":"_executor","type":"address"},{"internalType":"bytes","name":"_extraData","type":"bytes"}],"name":"lzReceive","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"components":[{"internalType":"uint32","name":"srcEid","type":"uint32"},{"internalType":"bytes32","name":"sender","type":"bytes32"},{"internalType":"uint64","name":"nonce","type":"uint64"}],"internalType":"struct Origin","name":"origin","type":"tuple"},{"internalType":"uint32","name":"dstEid","type":"uint32"},{"internalType":"address","name":"receiver","type":"address"},{"internalType":"bytes32","name":"guid","type":"bytes32"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"address","name":"executor","type":"address"},{"internalType":"bytes","name":"message","type":"bytes"},{"internalType":"bytes","name":"extraData","type":"bytes"}],"internalType":"struct InboundPacket[]","name":"_packets","type":"tuple[]"}],"name":"lzReceiveAndRevert","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"uint32","name":"srcEid","type":"uint32"},{"internalType":"bytes32","name":"sender","type":"bytes32"},{"internalType":"uint64","name":"nonce","type":"uint64"}],"internalType":"struct Origin","name":"_origin","type":"tuple"},{"internalType":"bytes32","name":"_guid","type":"bytes32"},{"internalType":"bytes","name":"_message","type":"bytes"},{"internalType":"address","name":"_executor","type":"address"},{"internalType":"bytes","name":"_extraData","type":"bytes"}],"name":"lzReceiveSimulate","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"msgInspector","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint32","name":"","type":"uint32"},{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"nextNonce","outputs":[{"internalType":"uint64","name":"nonce","type":"uint64"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"oApp","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"oAppVersion","outputs":[{"internalType":"uint64","name":"senderVersion","type":"uint64"},{"internalType":"uint64","name":"receiverVersion","type":"uint64"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"oftVersion","outputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"},{"internalType":"uint64","name":"version","type":"uint64"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint32","name":"eid","type":"uint32"}],"name":"peers","outputs":[{"internalType":"bytes32","name":"peer","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"preCrime","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"uint32","name":"dstEid","type":"uint32"},{"internalType":"bytes32","name":"to","type":"bytes32"},{"internalType":"uint256","name":"amountLD","type":"uint256"},{"internalType":"uint256","name":"minAmountLD","type":"uint256"},{"internalType":"bytes","name":"extraOptions","type":"bytes"},{"internalType":"bytes","name":"composeMsg","type":"bytes"},{"internalType":"bytes","name":"oftCmd","type":"bytes"}],"internalType":"struct SendParam","name":"_sendParam","type":"tuple"}],"name":"quoteOFT","outputs":[{"components":[{"internalType":"uint256","name":"minAmountLD","type":"uint256"},{"internalType":"uint256","name":"maxAmountLD","type":"uint256"}],"internalType":"struct OFTLimit","name":"oftLimit","type":"tuple"},{"components":[{"internalType":"int256","name":"feeAmountLD","type":"int256"},{"internalType":"string","name":"description","type":"string"}],"internalType":"struct OFTFeeDetail[]","name":"oftFeeDetails","type":"tuple[]"},{"components":[{"internalType":"uint256","name":"amountSentLD","type":"uint256"},{"internalType":"uint256","name":"amountReceivedLD","type":"uint256"}],"internalType":"struct OFTReceipt","name":"oftReceipt","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"uint32","name":"dstEid","type":"uint32"},{"internalType":"bytes32","name":"to","type":"bytes32"},{"internalType":"uint256","name":"amountLD","type":"uint256"},{"internalType":"uint256","name":"minAmountLD","type":"uint256"},{"internalType":"bytes","name":"extraOptions","type":"bytes"},{"internalType":"bytes","name":"composeMsg","type":"bytes"},{"internalType":"bytes","name":"oftCmd","type":"bytes"}],"internalType":"struct SendParam","name":"_sendParam","type":"tuple"},{"internalType":"bool","name":"_payInLzToken","type":"bool"}],"name":"quoteSend","outputs":[{"components":[{"internalType":"uint256","name":"nativeFee","type":"uint256"},{"internalType":"uint256","name":"lzTokenFee","type":"uint256"}],"internalType":"struct MessagingFee","name":"msgFee","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"uint32","name":"dstEid","type":"uint32"},{"internalType":"bytes32","name":"to","type":"bytes32"},{"internalType":"uint256","name":"amountLD","type":"uint256"},{"internalType":"uint256","name":"minAmountLD","type":"uint256"},{"internalType":"bytes","name":"extraOptions","type":"bytes"},{"internalType":"bytes","name":"composeMsg","type":"bytes"},{"internalType":"bytes","name":"oftCmd","type":"bytes"}],"internalType":"struct SendParam","name":"_sendParam","type":"tuple"},{"components":[{"internalType":"uint256","name":"nativeFee","type":"uint256"},{"internalType":"uint256","name":"lzTokenFee","type":"uint256"}],"internalType":"struct MessagingFee","name":"_fee","type":"tuple"},{"internalType":"address","name":"_refundAddress","type":"address"}],"name":"send","outputs":[{"components":[{"internalType":"bytes32","name":"guid","type":"bytes32"},{"internalType":"uint64","name":"nonce","type":"uint64"},{"components":[{"internalType":"uint256","name":"nativeFee","type":"uint256"},{"internalType":"uint256","name":"lzTokenFee","type":"uint256"}],"internalType":"struct MessagingFee","name":"fee","type":"tuple"}],"internalType":"struct MessagingReceipt","name":"msgReceipt","type":"tuple"},{"components":[{"internalType":"uint256","name":"amountSentLD","type":"uint256"},{"internalType":"uint256","name":"amountReceivedLD","type":"uint256"}],"internalType":"struct OFTReceipt","name":"oftReceipt","type":"tuple"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"_delegate","type":"address"}],"name":"setDelegate","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"uint32","name":"eid","type":"uint32"},{"internalType":"uint16","name":"msgType","type":"uint16"},{"internalType":"bytes","name":"options","type":"bytes"}],"internalType":"struct EnforcedOptionParam[]","name":"_enforcedOptions","type":"tuple[]"}],"name":"setEnforcedOptions","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_msgInspector","type":"address"}],"name":"setMsgInspector","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint32","name":"_eid","type":"uint32"},{"internalType":"bytes32","name":"_peer","type":"bytes32"}],"name":"setPeer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_preCrime","type":"address"}],"name":"setPreCrime","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"sharedDecimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"token","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
LEGASY_TRANSACTION = False

RPCS = []
TOKEN_CONTRACT_ADDRESS = ""
NETWORK_SCAN = ""
TOKEN_SYMBOL = ""
TOKEN_DECIMALS = ""


async def read_file_lines(path: str) -> list[str]:
    try:
        with open(path, "r") as file:
            lines = [i.strip() for i in file.readlines()]
            return lines
    except:
        return []


async def create_web3_instance():
    while True:
        w3 = AsyncWeb3(
            AsyncHTTPProvider(
                endpoint_uri=random.choice(RPCS),
            )
        )
        w3.middleware_onion.inject(async_geth_poa_middleware, layer=0)
        if await w3.is_connected():
            return w3
    return None


async def get_eip1559_tx(self, tx_params: dict, increase_gas: float = 1.0):
    last_block = await self.w3.eth.get_block("latest")
    base_fee = int(last_block["baseFeePerGas"] * increase_gas)
    max_priority_fee_per_gas = await self.w3.eth.max_priority_fee
    tx_params["maxFeePerGas"] = int(base_fee + max_priority_fee_per_gas)
    tx_params["maxPriorityFeePerGas"] = max_priority_fee_per_gas
    return tx_params


async def sign_transaction(w3, private: str, tx: dict):
    signed_tx = w3.eth.account.sign_transaction(tx, private)
    raw_tx_hash = await w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_hash = w3.to_hex(raw_tx_hash)
    return tx_hash


async def get_eip1559_tx(w3, tx_params: dict, increase_gas: float = 1.5):
    last_block = await w3.eth.get_block("latest")
    base_fee = int(last_block["baseFeePerGas"] * increase_gas)
    max_priority_fee_per_gas = await w3.eth.max_priority_fee
    tx_params["maxFeePerGas"] = int(base_fee + max_priority_fee_per_gas)
    tx_params["maxPriorityFeePerGas"] = max_priority_fee_per_gas
    return tx_params


async def verifi_tx(w3, tx_hash):
    try:
        data = await w3.eth.wait_for_transaction_receipt(tx_hash, timeout=400)
        if "status" in data and data["status"] == 1:
            return True
        else:
            return False
    except Exception as error:
        logger.error(error)
        return False


async def send_transaction(
    w3,
    private: str,
    from_address: str,
    to_address: str,
    value: Token_Amount = None,
    data: str = None,
):
    try:
        logger.info("Begin transactction")
        tx_params = {
            "from": eth_utils.address.to_checksum_address(from_address),
            "chainId": await w3.eth.chain_id,
            "nonce": await w3.eth.get_transaction_count(
                eth_utils.address.to_checksum_address(from_address)
            ),
        }

        if to_address:
            tx_params["to"] = eth_utils.address.to_checksum_address(to_address)
        if data:
            tx_params["data"] = data

        if value is None or value == 0:
            tx_params["value"] = 0
        else:
            tx_params["value"] = value.WEI

        if not LEGACY_TRANSACTION:
            tx_params = await get_eip1559_tx(w3=w3, tx_params=tx_params)
        else:
            tx_params["gasPrice"] = await w3.eth.gas_price

        tx_params["gas"] = int(await w3.eth.estimate_gas(tx_params) * 1.5)

        tx_hash = await sign_transaction(w3=w3, tx=tx_params, private=private)
        verify = await verifi_tx(w3=w3, tx_hash=tx_hash)
        if verify:
            logger.success(f"LINK {NETWORK_SCAN}/tx/{tx_hash}")
            return True
        else:
            logger.success(f"LINK {NETWORK_SCAN}/tx/{tx_hash}")
            return False
    except Exception as error:
        logger.error(error)
        return False


async def get_allowance(contract, owner: str, spender: str) -> Token_Amount:
    try:
        amount_allowance = await contract.functions.allowance(
            eth_utils.address.to_checksum_address(owner),
            eth_utils.address.to_checksum_address(spender),
        ).call()
        amount_allowance = Token_Amount(
            amount=amount_allowance,
            decimals=await contract.functions.decimals().call(),
            wei=True,
        )
        return amount_allowance
    except Exception as error:
        logger.error(f"{error}")
        return None


async def approve(
    w3, contract, private: str, owner: str, spender: str, amount: Token_Amount
):
    try:
        logger.info(f"check approve {owner} for {TOKEN_SYMBOL} token")
        allowanced: Token_Amount = await get_allowance(
            contract=contract, owner=owner, spender=spender
        )

        if allowanced.ETHER > amount.ETHER:
            logger.info(f"approve not need")
            return True
        else:
            logger.info(f"approve need")
            value_approove = Token_Amount(
                amount=amount.WEI + amount.WEI * random.uniform(0.01, 0.05),
                decimals=amount.DECIMAL,
                wei=True,
            )
            logger.info(f"make approve for {value_approove.ETHER} {TOKEN_SYMBOL}")
            return await send_transaction(
                w3=w3,
                private=private,
                from_address=owner,
                to_address=spender,
                data=contract.encodeABI(
                    "approve",
                    args=(
                        eth_utils.address.to_checksum_address(spender),
                        int(value_approove.WEI),
                    ),
                ),
            )
    except Exception as error:
        logger.error(error)
        return False


async def transfer(
    w3, private: str, contract, from_address: str, to_address: str, amount: Token_Amount
):
    try:
        data = contract.encodeABI(
            "transfer",
            args=(
                eth_utils.address.to_checksum_address(to_address),
                int(amount.WEI),
            ),
        )
        logger.info(
            f"transfer from {from_address} {amount.ETHER} {TOKEN_SYMBOL} to {to_address}"
        )
        return await send_transaction(
            w3=w3,
            private=private,
            from_address=from_address,
            to_address=contract.address,
            data=data,
            value=0,
        )
    except Exception as error:
        logger.error(error)
        return False

async def work_wallet(pair):
    while True:
        try:
            w3 = await create_web3_instance()
            if w3 is None:
                logger.error("not w3 instance")
                continue
            contract = w3.eth.contract(
                address=eth_utils.address.to_checksum_address(TOKEN_CONTRACT_ADDRESS),
                abi=TOKEN_ABI,
            )
            wallet_address = Account.from_key(pair[0]).address
            balance_clear = await contract.functions.balanceOf(
                    eth_utils.address.to_checksum_address(wallet_address)
                ).call()
            balance = Token_Amount(
                amount=balance_clear,
                decimals=TOKEN_DECIMALS,
                wei=True,
            )
            if balance.WEI > 1:
                logger.info(
                    f"balance {wallet_address} = {balance.ETHER} {TOKEN_SYMBOL}"
                )
                if not await approve(
                    w3=w3,
                    contract=contract,
                    private=pair[0],
                    owner=wallet_address,
                    spender=pair[1],
                    amount=balance,
                ):
                    continue
                if await transfer(
                    w3=w3,
                    private=pair[0],
                    contract=contract,
                    from_address=wallet_address,
                    to_address=pair[1],
                    amount=balance,
                ):
                    break
            await asyncio.sleep(CHECK_INTERVAL)

        except Exception as error:
            logger.error(error)


async def main():
    wallets = await read_file_lines("wallets.txt")
    recipients = await read_file_lines("recipients.txt")
    pairs = zip(wallets, recipients)
    logger.info("start")
    tasks = [work_wallet(pair) for pair in pairs]
    await asyncio.gather(*tasks)
    logger.info("finish")


if __name__ == "__main__":
    asyncio.run(main())
