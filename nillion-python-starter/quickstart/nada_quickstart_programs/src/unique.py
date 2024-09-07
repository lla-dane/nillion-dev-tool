from nada_dsl import *
import os
import json

def load_num(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            creds = json.load(file)
            return (creds.get("Number", 0))
    return 0

def is_guess_in_target(array: List[SecretInteger], value: Integer) -> SecretBoolean:
    result = Integer(0)
    for element in array:
        result += (value == element).if_else(Integer(1), Integer(0))
    return (result > Integer(0))

def nada_main():
    CRED_STORE = "../client_code/credential_store.json"
    len_unique_num = load_num(CRED_STORE)
    game = Party(name="GAME_MANAGER")
    
    secret_numbers  = [
        SecretInteger(Input(name=f"NUMBERS_{i}", party=game)) for i in range(len_unique_num)
    ]
    
    new_random_number = SecretInteger.random() % Integer(52)
    condition = is_guess_in_target(secret_numbers, new_random_number)
    new_random_number = condition.if_else(new_random_number, new_random_number)
    
    return [Output(new_random_number, "NEW_NUMBER", game)]
