from bitcoinrpc.authproxy import AuthServiceProxy

# RPC credentials
rpc_user = "user"
rpc_password = "password"
rpc_port = 18443

rpc = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:{rpc_port}")

print("Connected to Bitcoin regtest")

# Create or load wallet
wallet_name = "legacywall"

try:
    rpc.createwallet(wallet_name)
    print("Wallet created")
except:
    rpc.loadwallet(wallet_name)
    print("Wallet loaded")

rpc = AuthServiceProxy(
    f"http://{rpc_user}:{rpc_password}@127.0.0.1:{rpc_port}/wallet/{wallet_name}"
)

# Generate legacy addresses
A = rpc.getnewaddress("", "legacy")
B = rpc.getnewaddress("", "legacy")
C = rpc.getnewaddress("", "legacy")

print("\nGenerated Addresses")
print("A:", A)
print("B:", B)
print("C:", C)

# Mine blocks only if needed
mine_addr = rpc.getnewaddress()
if rpc.getbalance() == 0:
    rpc.generatetoaddress(101, mine_addr)
print("Balance after mining:", rpc.getbalance())

# Send coins to A
txid_fund_A = rpc.sendtoaddress(A, 10)

print("\nFunding transaction to A:", txid_fund_A)

# confirm transaction
rpc.generatetoaddress(1, mine_addr)

# Find UTXO belonging to A
utxos = rpc.listunspent()

utxo_A = None
for u in utxos:
    if u["address"] == A:
        utxo_A = u
        break

print("\nUTXO for A")
print(utxo_A)

# Create raw transaction A -> B
inputs = [{"txid": utxo_A["txid"], "vout": utxo_A["vout"]}]
outputs = {B: 5, A: 4.9999}

raw_tx = rpc.createrawtransaction(inputs, outputs)

print("\nRaw Transaction A->B")
print(raw_tx)

# Sign transaction
signed_tx = rpc.signrawtransactionwithwallet(raw_tx)
signed_hex = signed_tx["hex"]

print("\nSigned Transaction HEX")
print(signed_hex)

# Decode raw transaction
decoded_tx = rpc.decoderawtransaction(signed_hex)

print("\nDecoded Transaction A->B")
print(decoded_tx)

# Broadcast transaction
txid_AB = rpc.sendrawtransaction(signed_hex)

print("\nBroadcasted TXID A->B:", txid_AB)

# confirm transaction
rpc.generatetoaddress(1, mine_addr)

# Get UTXO of B
utxos = rpc.listunspent()

utxo_B = None
for u in utxos:
    if u["address"] == B:
        utxo_B = u
        break

print("\nUTXO for B")
print(utxo_B)

# Create raw transaction B -> C
inputs = [{"txid": utxo_B["txid"], "vout": utxo_B["vout"]}]
outputs = {C: 4, B: 0.9999}

raw_tx2 = rpc.createrawtransaction(inputs, outputs)

print("\nRaw Transaction B->C")
print(raw_tx2)

# Sign
signed_tx2 = rpc.signrawtransactionwithwallet(raw_tx2)
signed_hex2 = signed_tx2["hex"]

print("\nSigned Transaction B->C HEX")
print(signed_hex2)

# Decode
decoded_tx2 = rpc.decoderawtransaction(signed_hex2)

print("\nDecoded Transaction B->C")
print(decoded_tx2)

# Broadcast
txid_BC = rpc.sendrawtransaction(signed_hex2)

print("\nBroadcasted TXID B->C:", txid_BC)

# confirm
rpc.generatetoaddress(1, mine_addr)

# Final Balance
print("\nFinal Balance:", rpc.getbalance())