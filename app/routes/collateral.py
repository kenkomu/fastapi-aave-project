# app/routes/collateral.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.services.web3_service import execute_swap_and_repay

router = APIRouter()

class SwapAndRepayRequest(BaseModel):
    collateral_asset: str = Field(..., description="Address of the collateral asset")
    debt_asset: str = Field(..., description="Address of the debt asset")
    collateral_amount: float = Field(..., gt=0, description="Amount of collateral to swap")
    debt_repay_amount: float = Field(..., gt=0, description="Amount of debt to repay")
    user_address: str = Field(..., description="User's Ethereum address")
    private_key: str = Field(..., description="User's private key")

    class Config:
        schema_extra = {
            "example": {
                "collateral_asset": "0x4e65fE4DbA92790696d040ac24Aa414708F5c0AB",
                "debt_asset": "0xBdb9300b7CDE636d9cD4AFF00f6F009fFBBc8EE6",
                "collateral_amount": 1.0,
                "debt_repay_amount": 1.0,
                "user_address": "0x000000f6d9a0C099b24046333A4E1F37d61E12B7",
                "private_key": "3fb035a776d12cb6b7475b0d9ef6e3d7561059eda95617fdd58335c3cfa54a68"
            }
        }

@router.post(
    "/swap-and-repay/",
    responses={
        200: {
            "description": "Transaction Successful",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Collateral switch transaction sent successfully",
                        "approve_tx_hash": "0xMockedApproveTransactionHash",
                        "switch_tx_hash": "0xMockedSwitchTransactionHash",
                        "approve_gas_consumed": 2000000,
                        "switch_gas_consumed": 2500000
                    }
                }
            }
        },
        400: {"description": "Validation Error"},
        500: {"description": "Internal Server Error"}
    }
)
async def swap_and_repay_endpoint(request: SwapAndRepayRequest):
    """
    Execute a swap and repay transaction on AAVE
    - Swaps collateral asset for debt asset
    - Repays the specified debt amount
    """
    try:
        # Mocked response structure
        mocked_response = {
            "message": "Collateral switch transaction sent successfully",
            "approve_tx_hash": "0xMockedApproveTransactionHash",
            "switch_tx_hash": "0xMockedSwitchTransactionHash",
            "approve_gas_consumed": 2000000,
            "switch_gas_consumed": 2500000
        }

        # Uncomment this line if you want to return mock responses without calling the real service
        # return mocked_response

        # Execute the swap and repay transaction
        tx_hash = execute_swap_and_repay(
            collateral_asset=request.collateral_asset,
            debt_asset=request.debt_asset,
            collateral_amount=request.collateral_amount,
            debt_repay_amount=request.debt_repay_amount,
            user_address=request.user_address,
            private_key=request.private_key
        )

        # Return success response
        return {
            "message": "Swap and repay transaction executed successfully",
            "tx_hash": tx_hash,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to execute swapAndRepay: {str(e)}")