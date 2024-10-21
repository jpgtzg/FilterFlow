# Written by Juan Pablo Gutiérrez   

def store_uid_list(uids : list, filename="uid_store.txt"): 
    with open(filename, "w") as f:
        for uid in uids:
            f.write(f"{uid.decode()}\n")
    pass

def store_uid(uid, filename="uid_store.txt"):
    with open(filename, "a") as f:
        f.write(f"{uid.decode()}\n")
    pass

def read_uid(filename="uid_store.txt") -> list:
    try:
        with open(filename, "r") as f:
            uids = [line.strip().encode() for line in f.readlines()]
    except FileNotFoundError:
        uids = []
    return uids
