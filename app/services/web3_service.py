# app/services/web3_service.py
import os
from dotenv import load_dotenv
from web3 import Web3
import json

# Load environment variables
load_dotenv()

# Connect to BASE L2 Network
BASE_RPC_URL = "https://mainnet.base.org"
web3 = Web3(Web3.HTTPProvider(BASE_RPC_URL))

# Check connection
if web3.is_connected():
    print("Connected to BASE L2 Network")
else:
    raise ConnectionError("Failed to connect to BASE L2 Network")

# Load ABI
with open("app/abi/aave_lending_pool.json", "r") as abi_file:
    lending_pool_abi = json.load(abi_file)

# Contract address
LENDING_POOL_ADDRESS = "0x63dfa7c09Dc2Ff4030d6B8Dc2ce6262BF898C8A4"

# Initialize contract instance
lending_pool_contract = web3.eth.contract(
    address=web3.to_checksum_address(LENDING_POOL_ADDRESS),
    abi=lending_pool_abi
)

def execute_swap_and_repay(
    collateral_asset: str,
    debt_asset: str,
    collateral_amount: float,
    debt_repay_amount: float,
    user_address: str,
    private_key: str
) -> dict:
    """
    Executes the swapAndRepay function.
    """
    try:
        # Convert addresses to checksum format
        collateral_asset = web3.to_checksum_address(collateral_asset)
        debt_asset = web3.to_checksum_address(debt_asset)
        user_address = web3.to_checksum_address(user_address)

        # Convert amounts to Wei
        collateral_amount_wei = web3.to_wei(collateral_amount, 'ether')
        debt_repay_amount_wei = web3.to_wei(debt_repay_amount, 'ether')

        print(f"Collateral Asset: {collateral_asset}")
        print(f"Debt Asset: {debt_asset}")
        print(f"Collateral Amount: {collateral_amount_wei}")
        print(f"Debt Repay Amount: {debt_repay_amount_wei}")
        print(f"User Address: {user_address}")

        # Get nonce
        nonce = web3.eth.get_transaction_count(user_address)

        # Get gas price
        gas_price = web3.eth.gas_price

        # Create permit signature tuple
        permit_signature = (
            0,  # amount
            0,  # deadline
            0,  # v
            b'\x00' * 32,  # r
            b'\x00' * 32   # s
        )

        # Prepare the transaction
        params = {
            'from': user_address,
            'nonce': nonce,
            'gas': 3000000,  # Update as per estimation
            'gasPrice': gas_price,
        }

        # Build the contract function call
        contract_function = lending_pool_contract.functions.swapAndRepay(
            collateral_asset,
            debt_asset,
            collateral_amount_wei,
            debt_repay_amount_wei,
            2,  # debtRateMode
            0,  # buyAllBalanceOffset
            b'',  # paraswapData
            permit_signature  # permitSignature tuple
        )

        # Estimate gas (optional, but recommended)
        try:
            estimated_gas = contract_function.estimate_gas(params)
            params['gas'] = estimated_gas
            print(f"Estimated Gas: {estimated_gas}")
        except Exception as e:
            raise ValueError(f"Gas estimation failed: {e}")

        # Build the transaction
        transaction = contract_function.build_transaction(params)

        # Sign the transaction
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)

        # Send the transaction
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        # Wait for transaction receipt
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        if receipt['status'] == 1:
            return {
                "success": True,
                "tx_hash": web3.to_hex(tx_hash),
                "gas_used": receipt['gasUsed'],
                "block_number": receipt['blockNumber'],
            }
        else:
            raise ValueError("Transaction failed: Receipt indicates failure.")

    except ValueError as e:
        raise ValueError(f"Value error in transaction process: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error in execute_swap_and_repay: {str(e)}")
