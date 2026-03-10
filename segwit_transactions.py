from bitcoinrpc.authproxy import AuthServiceProxy
from decimal import Decimal

rpc_user = "user"
rpc_password = "password"
rpc_port = 18443

rpc = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:{rpc_port}")

print("Connected to Bitcoin regtest")

wallet_name = "segwitwallet"

# create or load wallet
try:
    rpc.createwallet(wallet_name)
    print("Wallet created")
except:
    rpc.loadwallet(wallet_name)
    print("Wallet loaded")

rpc = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:{rpc_port}/wallet/{wallet_name}")

# Generate P2SH-SegWit addresses
A = rpc.getnewaddress("", "p2sh-segwit")
B = rpc.getnewaddress("", "p2sh-segwit")
C = rpc.getnewaddress("", "p2sh-segwit")

print("\nGenerated SegWit Addresses")
print("A':", A)
print("B':", B)
print("C':", C)

# Mine blocks to fund wallet
mine_addr = rpc.getnewaddress()
if rpc.getbalance() == 0:
    rpc.generatetoaddress(101, mine_addr)
print("Balance after mining:", rpc.getbalance())

print("\nBalance after mining:", rpc.getbalance())

# Fund address A'
txid_fund_A = rpc.sendtoaddress(A, Decimal("10"))

print("\nFunding transaction to A':", txid_fund_A)

rpc.generatetoaddress(1, mine_addr)

# Get UTXO of A'
utxos = rpc.listunspent()

utxo_A = None
for u in utxos:
    if u["address"] == A:
        utxo_A = u
        break

print("\nUTXO for A'")
print(utxo_A)

# Create raw transaction A' → B'
inputs = [{"txid": utxo_A["txid"], "vout": utxo_A["vout"]}]

outputs = {
    B: Decimal("5"),
    A: Decimal("4.9999")
}

raw_tx = rpc.createrawtransaction(inputs, outputs)

print("\nRaw Transaction A'->B'")
print(raw_tx)

# sign transaction
signed_tx = rpc.signrawtransactionwithwallet(raw_tx)

signed_hex = signed_tx["hex"]

print("\nSigned Transaction HEX")
print(signed_hex)

# decode transaction
decoded_tx = rpc.decoderawtransaction(signed_hex)

print("\nDecoded Transaction A'->B'")
print(decoded_tx)

# broadcast transaction
txid_AB = rpc.sendrawtransaction(signed_hex)

print("\nBroadcasted TXID A'->B':", txid_AB)

rpc.generatetoaddress(1, mine_addr)

# Get UTXO for B'
utxos = rpc.listunspent()

utxo_B = None
for u in utxos:
    if u["address"] == B:
        utxo_B = u
        break

print("\nUTXO for B'")
print(utxo_B)

# Create transaction B' → C'
inputs = [{"txid": utxo_B["txid"], "vout": utxo_B["vout"]}]

outputs = {
    C: Decimal("4"),
    B: Decimal("0.9999")
}

raw_tx2 = rpc.createrawtransaction(inputs, outputs)

print("\nRaw Transaction B'->C'")
print(raw_tx2)


signed_tx2 = rpc.signrawtransactionwithwallet(raw_tx2)

signed_hex2 = signed_tx2["hex"]
print("\nSigned Transaction HEX")
print(signed_hex2)

decoded_tx2 = rpc.decoderawtransaction(signed_hex2)

print("\nDecoded Transaction B'->C'")
print(decoded_tx2)


txid_BC = rpc.sendrawtransaction(signed_hex2)

print("\nBroadcasted TXID B'->C':", txid_BC)

rpc.generatetoaddress(1, mine_addr)

print("\nFinal Balance:", rpc.getbalance())