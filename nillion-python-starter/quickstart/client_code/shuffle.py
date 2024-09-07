import asyncio
import py_nillion_client as nillion
import os
import json
import random

from py_nillion_client import NodeKey, UserKey
from dotenv import load_dotenv
from nillion_python_helpers import get_quote_and_pay, create_nillion_client, create_payments_config

from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

home = os.getenv("HOME")
load_dotenv(f"{home}/.config/nillion/nillion-devnet.env")

async def main():
    PLAYER_ALIAS = "GAME_MANAGER"
    
    # GET NILLION-DEVNET CREDENTIALS
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    grpc_endpoint = os.getenv("NILLION_NILCHAIN_GRPC")
    chain_id = os.getenv("NILLION_NILCHAIN_CHAIN_ID")
    
    seed = PLAYER_ALIAS
    
    user_key = UserKey.from_seed(seed)
    node_key = NodeKey.from_seed(seed)
    
    manager = create_nillion_client(user_key, node_key)
    
    party_id = manager.party_id
    user_id = manager.user_id
    
    payments_config = create_payments_config(chain_id, grpc_endpoint)
    payments_client = LedgerClient(payments_config)
    payments_wallet = LocalWallet(
        PrivateKey(bytes.fromhex(os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0"))),
        prefix="nillion",
    )
    
    SHUFFLING_PROGRAM = "unique"
    SHUFFLING_PROGRAM_PATH = f"../nada_quickstart_programs/target/{SHUFFLING_PROGRAM}.nada.bin"
    
    shuffle_program_receipt = await get_quote_and_pay(
        manager,
        nillion.Operation.store_program(SHUFFLING_PROGRAM_PATH),
        payments_wallet,
        payments_client,
        cluster_id,
    )
    
    action_id = await manager.store_program(
        cluster_id, SHUFFLING_PROGRAM, SHUFFLING_PROGRAM_PATH, shuffle_program_receipt
    )
    
    PROGRAM_ID = f'{user_id}/{SHUFFLING_PROGRAM}'    
    
    UNIQUE_NUMBERS = [5, 10, 6]
    compute_secrets_dict = {
        f"NUMBERS_{i}": nillion.SecretInteger(UNIQUE_NUMBERS[i]) for i in range(len(UNIQUE_NUMBERS))
    }
    NEW_SECRETS = nillion.NadaValues(compute_secrets_dict)
    
    print(compute_secrets_dict)
    
    permissions = nillion.Permissions.default_for_user(manager.user_id)    
    permissions.add_compute_permissions({manager.user_id: {PROGRAM_ID}})
    
    receipt_store = await get_quote_and_pay(
        manager,
        nillion.Operation.store_values(NEW_SECRETS, ttl_days=5),
        payments_wallet,
        payments_client,
        cluster_id,
    )
    
    store_id = await manager.store_values(
        cluster_id, NEW_SECRETS, permissions, receipt_store
    )
    
    compute_bindings = nillion.ProgramBindings(PROGRAM_ID)
    compute_bindings.add_input_party(PLAYER_ALIAS, party_id)
    compute_bindings.add_output_party(PLAYER_ALIAS, party_id)
    
    COMPUTE_SECRETS = nillion.NadaValues({})

    COMPUTE_RECEIPT = await get_quote_and_pay(
        manager,
        nillion.Operation.compute(PROGRAM_ID, COMPUTE_SECRETS),
        payments_wallet,
        payments_client,
        cluster_id,
    )
    
    COMPUTE_ID = await manager.compute(
        cluster_id,
        compute_bindings,
        [store_id],
        COMPUTE_SECRETS,
        COMPUTE_RECEIPT
    )
    print(COMPUTE_ID)
    
    while True:
        compute_event = await manager.next_compute_event()
        if isinstance(compute_event, nillion.ComputeFinishedEvent):
            print(f"🖥️  THE UNIFIED SYSTEM IDENTIFIER FOR HARDWARE BAN {compute_event.result.value}")
            return compute_event.result.value
    

if __name__ == "__main__":
    asyncio.run(main())