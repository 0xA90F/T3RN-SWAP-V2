_Ah='[yellow]N/A[/yellow]'
_Ag='[red]None[/red]'
_Af='BRN_STATS'
_Ae='SET_DELAYS'
_Ad='SET_AMOUNT'
_Ac='%H:%M:%S %d-%m-%Y'
_Ab='Average per Transaction'
_Aa='Transactions Count'
_AZ='Total Estimated Value'
_AY='Total Estimated BRN'
_AX='[bold red]Invalid option.[/bold red]'
_AW='[bold red]Invalid delay value.[/bold red]'
_AV='Select an option (1-3) or press Enter to go back'
_AU='[bold red]Invalid choice.[/bold red]'
_AT='[bold red]Invalid choice. Please select 1-3.[/bold red]'
_AS='Arbitrum - OP'
_AR='OP - Arbitrum'
_AQ='Arbitrum - BASE'
_AP='BASE - Arbitrum'
_AO='BASE - OP'
_AN='OP - BASE'
_AM='data_bridge'
_AL='Parameter'
_AK='estimated_received_eth'
_AJ='brn_bonus_usd'
_AI='confirmed'
_AH='Est. BRN'
_AG='Status'
_AF='Account'
_AE='expiry'
_AD='Custom Delay'
_AC='right'
_AB='[bold red]Delay cannot be negative.[/bold red]'
_AA='bridge_amount'
_A9='Network'
_A8='total_brn_with_bonus'
_A7='bonus_brn'
_A6='base_brn_bonus'
_A5='Asia/Jakarta'
_A4='bonus'
_A3='estimate'
_A2='explorer'
_A1='block'
_A0='pending'
_z='install'
_y='pip'
_x='Bridge'
_w='delays'
_v='ether'
_u='total_usd'
_t='%d-%m-%Y'
_s='balance'
_r='red'
_q='Value'
_p='latest'
_o='blue'
_n='[bold red]Invalid input.[/bold red]'
_m='yellow'
_l='avg_usd'
_k='number'
_j='rpc_url'
_i='access'
_h='wallet'
_g='magenta'
_f='nonce'
_e='Default'
_d='between_cycles'
_c='between_bridges'
_b='between_accounts'
_a='w'
_Z='total_brn'
_Y='bonus_percentage'
_X='avg_brn'
_W='gas'
_V='Base Sepolia'
_U='OP Sepolia'
_T='Arbitrum Sepolia'
_S='config.json'
_R=False
_Q='transaction_count'
_P='brn'
_O='bridge'
_N='info'
_M='success'
_L=True
_K='time'
_J='🔵'
_I='transactions'
_H='warning'
_G='error'
_F='custom_delays'
_E='settings'
_D='bridges'
_C='cyan'
_B=None
_A='green'
import time,os,sys,logging,binascii,json,re,threading
from typing import Dict,List,Tuple,Optional,Any,Union
from web3 import Web3
from web3.exceptions import TransactionNotFound
from eth_account import Account
from eth_account.signers.local import LocalAccount
from datetime import datetime,timedelta
from decimal import Decimal
try:import pytz,requests;from rich.console import Console;from rich.table import Table;from rich.panel import Panel;from rich.progress import Progress,SpinnerColumn,TextColumn,BarColumn,TimeElapsedColumn;from rich.prompt import Prompt,Confirm;from rich.live import Live;from rich.layout import Layout;from rich.text import Text;from rich.box import ROUNDED,HEAVY,DOUBLE
except ImportError:print('Installing required packages...');import subprocess;subprocess.check_call([sys.executable,'-m',_y,_z,'rich']);subprocess.check_call([sys.executable,'-m',_y,_z,'pytz']);subprocess.check_call([sys.executable,'-m',_y,_z,'requests']);import pytz;import requests;from rich.console import Console;from rich.table import Table;from rich.panel import Panel;from rich.progress import Progress,SpinnerColumn,TextColumn,BarColumn,TimeElapsedColumn;from rich.prompt import Prompt,Confirm;from rich.live import Live;from rich.layout import Layout;from rich.text import Text;from rich.box import ROUNDED,HEAVY,DOUBLE
console=Console()
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s',handlers=[logging.FileHandler('t3rn_bot.log'),logging.StreamHandler()])
logger=logging.getLogger('t3rn-bot')
CHAIN_STYLES={_T:(_o,_J),_U:(_r,'🔴'),_V:(_C,_J)}
STATUS_ICONS={_M:'✅',_G:'❌',_H:'⚠️',_N:'ℹ️',_A0:'⏳',_AI:'✓',_s:'💰','network':'🌐',_O:'🌉',_W:'⛽',_K:'⏱️',_A1:'🧱',_h:'👛','key':'🔑',_E:'⚙️',_f:'🔢',_A2:'🔍',_i:'🔐',_P:'🪙',_A3:'📊',_A4:'🎁'}
def get_user_ip():
	"Get the user's public IP address"
	try:
		A=requests.get('https://api.ipify.org',timeout=5)
		if A.status_code==200:return A.text.strip()
		else:logger.error(f"Error getting IP: HTTP {A.status_code}");return
	except Exception as B:logger.error(f"Error getting user IP: {B}");return
def fetch_whitelist():
	'Fetch and parse IP whitelist from GitHub';B={}
	try:
		H='https://raw.githubusercontent.com/0xA90F/ip-whitelist/refs/heads/main/allow';C=requests.get(H,timeout=10)
		if C.status_code!=200:logger.error(f"Error fetching whitelist: HTTP {C.status_code}");return B
		for A in C.text.splitlines():
			A=A.strip()
			if not A or A.startswith('#'):continue
			D=A.split()
			if len(D)>=2:
				F=D[0];G=D[1]
				try:I=datetime.strptime(G,_t);B[F]=I
				except ValueError as E:logger.warning(f"Invalid date format for IP {F}: {G} - {E}")
		return B
	except Exception as E:logger.error(f"Error fetching whitelist: {E}");return B
def check_ip_access(ip):
	'Check if an IP is allowed based on the whitelist\n    \n    Returns:\n        Tuple of (is_allowed, expiry_time, message)\n    '
	if not ip:return _R,_B,'Could not determine your IP address'
	B=fetch_whitelist();D=pytz.timezone(_A5);C=datetime.now(D).replace(tzinfo=_B)
	if ip in B:
		A=B[ip]
		if A>C:return _L,A,f"Access granted until {A.strftime(_t)}"
		else:return _R,_B,f"Your IP access has expired on {A.strftime(_t)}"
	else:E=C+timedelta(hours=1);return _R,E,f"IP not in whitelist. Granting 1-hour trial."
def load_config():
	'Load configuration from config.json file'
	try:
		with open(_S,'r')as A:return json.load(A)
	except FileNotFoundError:return load_config
class NetworkManager:
	'Manages network connections and RPC endpoints'
	def __init__(A,config):B=config;A.networks=B['networks'];A.alternative_rpcs=B['alternative_rpcs'];A.explorer_urls=B[_E]['explorer_urls'];A.web3_connections={}
	def get_web3(B,network_name):
		'Get a web3 connection for the specified network, trying multiple RPCs if needed';A=network_name
		if A in B.web3_connections:
			C=B.web3_connections[A]
			try:
				if C.is_connected():C.eth.block_number;return C
			except Exception:pass
		F=B.networks[A][_j];C=B._try_rpc(A,F)
		if C:B.web3_connections[A]=C;return C
		if A in B.alternative_rpcs:
			with Progress(SpinnerColumn(),TextColumn('[bold blue]Trying alternative RPCs...'),console=console)as D:
				G=D.add_task('',total=len(B.alternative_rpcs[A]))
				for E in B.alternative_rpcs[A]:
					if E==F:D.advance(G);continue
					C=B._try_rpc(A,E);D.advance(G)
					if C:B.networks[A][_j]=E;B.web3_connections[A]=C;return C
		console.print(f"[bold red]{STATUS_ICONS[_G]} All RPC endpoints failed for {A}![/bold red]")
	def _try_rpc(P,network_name,rpc_url):
		'Try to connect to an RPC endpoint with timeout';F='timestamp';C=rpc_url;A=network_name
		try:
			console.print(f"[cyan]{STATUS_ICONS[_N]} Trying RPC for {A}: {C}[/cyan]");D=Web3(Web3.HTTPProvider(C,request_kwargs={'timeout':5}));K=5;L=time.time();G=_R
			while time.time()-L<K:
				try:
					if D.is_connected():G=_L;break
				except Exception:time.sleep(.5)
			if not G:console.print(f"[yellow]{STATUS_ICONS[_H]} Connection timeout for {A}[/yellow]");return
			try:
				console.print(f"[cyan]Checking {A} health...[/cyan]");H=threading.Event();B={_k:_B,F:_B,_M:_R}
				def M():
					try:A=D.eth.block_number;C=D.eth.get_block(_p);B[_k]=A;B[F]=C.timestamp;B[_M]=_L
					except Exception as E:console.print(f"[yellow]{STATUS_ICONS[_H]} Block retrieval failed: {E}[/yellow]")
					finally:H.set()
				I=threading.Thread(target=M);I.daemon=_L;I.start()
				if not H.wait(timeout=5):console.print(f"[yellow]{STATUS_ICONS[_H]} Block data retrieval timed out for {A}[/yellow]");return
				if B[_M]:
					N=B[_k];O=int(time.time());J=O-B[F]
					if J>300:console.print(f"[yellow]{STATUS_ICONS[_H]} Warning: {A} latest block is {J} seconds old.[/yellow]")
					console.print(f"[green]{STATUS_ICONS[_M]} Connected to {A} at {C} (block: {N})[/green]");return D
				else:return
			except Exception as E:console.print(f"[yellow]{STATUS_ICONS[_H]} Health check failed: {E}[/yellow]");return
		except Exception as E:console.print(f"[yellow]{STATUS_ICONS[_H]} RPC failed: {C} - {E}[/yellow]")
	def get_explorer_url(A,network_name,tx_hash):'Get explorer URL for a transaction';B=A.explorer_urls.get(network_name,'');return f"{B}{tx_hash}"
class BRNEstimator:
	'Estimates BRN rewards for bridge transactions'
	def __init__(A):A.api_url='https://api.t2rn.io/estimate';A.chain_codes={_T:'arbt',_U:'opst',_V:'bast'};A.total_estimated_brn=0;A.total_estimated_usd=Decimal('0');A.transaction_count=0;A.bonus_percentage=50
	def estimate_brn(A,from_chain,to_chain,amount_eth):
		S='100';R='0x0';Q='hex';P='eth';H=to_chain;G=from_chain
		try:
			I=A.chain_codes.get(G);J=A.chain_codes.get(H)
			if not I or not J:logger.error(f"Unknown chain names: {G} -> {H}");return
			T=int(amount_eth*10**18);U={'amountWei':str(T),'executorTipUSD':0,'fromAsset':P,'fromChain':I,'overpayOptionPercentage':0,'spreadOptionPercentage':0,'toAsset':P,'toChain':J};console.print(f"[cyan]{STATUS_ICONS[_A3]} Estimating BRN rewards...[/cyan]");B=requests.post(A.api_url,json=U,timeout=10)
			if B.status_code==200:C=B.json();V=int(C.get('BRNBonusWei',{}).get(Q,R),16);K=Decimal(C.get('BRNBonusUSD','0'));W=int(C.get('estimatedReceivedAmountWei',{}).get(Q,R),16);X=W/10**18;L=V/10**18;D=Decimal(str(L));M=Decimal(str(A.bonus_percentage));N=Decimal('1')+M/Decimal(S);Y=D*(M/Decimal(S));E=D*N;F=K*N;A.total_estimated_brn+=float(E);A.total_estimated_usd+=F;A.transaction_count+=1;console.print(f"[green]{STATUS_ICONS[_P]} Estimated BRN reward: {L:.8f} BRN +{A.bonus_percentage}% bonus = {float(E):.8f} BRN (${F})[/green]");return{_A6:float(D),_Y:A.bonus_percentage,_A7:float(Y),_A8:float(E),_AJ:K,'total_usd_with_bonus':F,_AK:X,'full_response':C}
			else:logger.error(f"API error: {B.status_code} - {B.text}");console.print(f"[yellow]{STATUS_ICONS[_H]} Failed to estimate BRN rewards: API returned status {B.status_code}[/yellow]");return
		except Exception as O:logger.error(f"Error estimating BRN: {O}");console.print(f"[yellow]{STATUS_ICONS[_H]} Failed to estimate BRN rewards: {O}[/yellow]");return
	def get_total_estimated_brn(A):'Get the total estimated BRN earned so far (including bonuses)';return A.total_estimated_brn
	def get_total_estimated_usd(A):'Get the total estimated USD value of BRN earned so far (including bonuses)';return A.total_estimated_usd
	def get_stats(A):
		'Get BRN reward statistics (including bonuses)';B=0;C=Decimal('0')
		if A.transaction_count>0:B=A.total_estimated_brn/A.transaction_count;C=A.total_estimated_usd/A.transaction_count
		return{_Z:A.total_estimated_brn,_u:A.total_estimated_usd,_Q:A.transaction_count,_X:B,_l:C,_Y:A.bonus_percentage}
class TransactionManager:
	'Manages transaction creation, signing, and monitoring'
	def __init__(A,network_manager):A.network_manager=network_manager;A.address_nonces={};A.successful_txs=0
	def get_nonce(B,web3,address,force_refresh=_R):
		'Get the next nonce for an address\n        \n        Args:\n            web3: Web3 instance\n            address: Account address\n            force_refresh: If True, always get fresh nonce from blockchain\n            \n        Returns:\n            Current nonce for the address\n        ';A=address
		if not force_refresh and A in B.address_nonces:return B.address_nonces[A]
		try:D=web3.eth.get_transaction_count(A,_A0);E=web3.eth.get_transaction_count(A,_p);C=max(D,E);console.print(f"[cyan]{STATUS_ICONS[_f]} Got nonce from blockchain: {C} (pending: {D}, latest: {E})[/cyan]");B.address_nonces[A]=C;return C
		except Exception as G:
			logger.error(f"Error getting nonce for {A}: {G}")
			if A in B.address_nonces:F=B.address_nonces[A];console.print(f"[yellow]{STATUS_ICONS[_H]} Using cached nonce as fallback: {F}[/yellow]");return F
			console.print(f"[yellow]{STATUS_ICONS[_H]} Using default nonce 0[/yellow]");B.address_nonces[A]=0;return 0
	def update_nonce(A,address,nonce):'Update the cached nonce for an address';A.address_nonces[address]=nonce
	def decode_error(F,error_data):
		'Decode error data from a failed transaction';A=error_data
		if not A or len(A)<10:return'Unknown error'
		try:
			if A.startswith('0x08c379a0'):C=binascii.unhexlify(A[10:].replace('0x',''));B=32;D=int.from_bytes(C[B:B+32],'big');E=C[B+32:B+32+D].decode('utf-8');return f"Contract error: {E}"
		except Exception:pass
		return f"Raw error: {A}"
	def wait_for_transaction(L,web3,tx_hash,timeout=120):
		'Wait for a transaction to be confirmed with timeout and better handling';B=tx_hash;A=timeout;D=time.time();I=D+A;J=web3.to_hex(B)if not isinstance(B,str)else B
		with Progress(SpinnerColumn(),TextColumn('[bold blue]Waiting for confirmation...'),BarColumn(),TextColumn('[bold cyan]{task.percentage:.0f}%'),TimeElapsedColumn(),console=console)as C:
			E=C.add_task('',total=A)
			while time.time()<I:
				try:
					F=web3.eth.get_transaction_receipt(B)
					if F is not _B:C.update(E,completed=A);return F
				except Exception as G:
					H=str(G)
					if'not found'not in H.lower()and'not available'not in H.lower():console.print(f"[yellow]{STATUS_ICONS[_H]} Error checking transaction: {G}[/yellow]")
				K=time.time()-D;C.update(E,completed=min(K,A));time.sleep(2)
		console.print(f"[yellow]{STATUS_ICONS[_H]} Timed out waiting for transaction {J} after {A} seconds[/yellow]")
	def send_bridge_transaction(B,network_name,account,bridge_data,value_eth=.1,max_attempts=3):
		'Send a bridge transaction with retry logic';o='blockNumber';n='maxPriorityFeePerGas';m='baseFeePerGas';e=account;d='gasPrice';c='chainId';b='maxFeePerGas';W=max_attempts;V='value';U='data';T='to';P=network_name;O='gwei';L=bridge_data;H=value_eth
		if not L:console.print(f"[bold red]{STATUS_ICONS[_G]} No bridge data available for this route. Please update config.json[/bold red]");return _B,_B
		A=B.network_manager.get_web3(P)
		if not A:console.print(f"[bold red]{STATUS_ICONS[_G]} Cannot connect to {P}[/bold red]");return _B,_B
		M=B.network_manager.networks[P]['contract_address'];C=e.address
		try:
			p=A.eth.get_balance(C);f=A.from_wei(p,_v)
			if f<H+.01:console.print(f"[yellow]{STATUS_ICONS[_H]} Insufficient balance: {f} ETH (need at least {H+.01})[/yellow]");return _B,_B
		except Exception as E:console.print(f"[yellow]{STATUS_ICONS[_H]} Could not check balance: {E}[/yellow]")
		D=B.get_nonce(A,C,force_refresh=_L);Q=A.to_wei(H,_v)
		for g in range(1,W+1):
			if g>1:console.print(Panel(f"[bold yellow]Retry attempt {g}/{W}[/bold yellow]"));D=B.get_nonce(A,C,force_refresh=_L);time.sleep(5)
			try:
				try:
					with console.status('[bold cyan]Estimating gas...[/bold cyan]'):h=A.eth.estimate_gas({T:M,'from':C,U:L,V:Q});R=h+50000
					console.print(f"[cyan]{STATUS_ICONS[_W]} Gas estimate: {h}[/cyan]")
				except Exception as E:
					console.print(f"[bold red]{STATUS_ICONS[_G]} Gas estimation failed: {E}[/bold red]")
					if isinstance(E,tuple)and len(E)>1:q=E[1];r=B.decode_error(q);console.print(f"[bold red]{STATUS_ICONS[_G]} Decoded error: {r}[/bold red]")
					console.print(f"[yellow]{STATUS_ICONS[_H]} This usually means invalid bridge data, insufficient balance, or contract changes[/yellow]");continue
				try:
					with console.status('[bold cyan]Preparing transaction...[/bold cyan]'):
						i=A.eth.get_block(_p)
						if hasattr(i,m):s=i[m];j=A.to_wei(2,O);t=2*s+j;G={_f:D,T:M,V:Q,_W:R,b:t,n:j,c:A.eth.chain_id,U:L}
						else:u=A.eth.gas_price;G={_f:D,T:M,V:Q,_W:R,d:int(u*1.1),c:A.eth.chain_id,U:L}
				except Exception as E:console.print(f"[yellow]{STATUS_ICONS[_H]} Error getting gas parameters: {E}[/yellow]");G={_f:D,T:M,V:Q,_W:R,d:A.to_wei(30,O),c:A.eth.chain_id,U:L}
				F=Table(title='Transaction Details',box=ROUNDED,border_style=_C);F.add_column(_AL,style=_g);F.add_column(_q,style=_C);F.add_row(f"{STATUS_ICONS[_O]} Contract",M);F.add_row(f"{STATUS_ICONS[_s]} Value",f"{H} ETH");F.add_row(f"{STATUS_ICONS[_f]} Nonce",f"{G[_f]}");F.add_row(f"{STATUS_ICONS[_W]} Gas Limit",f"{R}")
				if b in G:F.add_row(f"{STATUS_ICONS[_W]} Max Fee",f"{A.from_wei(G[b],O)} Gwei");F.add_row(f"{STATUS_ICONS[_W]} Priority Fee",f"{A.from_wei(G[n],O)} Gwei")
				else:F.add_row(f"{STATUS_ICONS[_W]} Gas Price",f"{A.from_wei(G[d],O)} Gwei")
				console.print(F)
				with console.status('[bold cyan]Signing and sending transaction...[/bold cyan]'):v=A.eth.account.sign_transaction(G,e.key);X=A.eth.send_raw_transaction(v.raw_transaction);N=A.to_hex(X)
				console.print(f"[green]{STATUS_ICONS[_M]} Transaction sent: {N}[/green]");k=B.network_manager.get_explorer_url(P,N);console.print(f"[blue]{STATUS_ICONS[_A2]} Explorer link: {k}[/blue]");S=B.wait_for_transaction(A,X)
				if S:console.print(Panel(f"[bold green]{STATUS_ICONS[_AI]} Transaction confirmed in block {S[o]}[/bold green]"));B.update_nonce(C,D+1);B.display_account_info(C);B.successful_txs+=1;J=Table(title='Transaction Receipt',box=ROUNDED,border_style=_A);J.add_column('Detail',style=_g);J.add_column(_q,style=_A);J.add_row(f"{STATUS_ICONS[_W]} Gas Used",f"{S['gasUsed']}");J.add_row(f"{STATUS_ICONS[_A1]} Block Number",f"{S[o]}");J.add_row(f"{STATUS_ICONS[_A2]} Explorer",k);console.print(J);return N,H
				else:
					console.print(f"[yellow]{STATUS_ICONS[_H]} Transaction not confirmed within timeout[/yellow]")
					try:
						w=A.eth.get_transaction(X)
						if w:console.print(f"[cyan]{STATUS_ICONS[_N]} Transaction still pending, may complete later[/cyan]");B.update_nonce(C,D+1);return N,H
					except Exception:console.print(f"[yellow]{STATUS_ICONS[_H]} Transaction may have been dropped[/yellow]")
			except Exception as E:
				K=str(E);console.print(f"[bold red]{STATUS_ICONS[_G]} Error sending transaction: {K}[/bold red]")
				if'nonce too low'in K.lower():
					try:Y=A.eth.get_transaction_count(C,_A0);B.update_nonce(C,Y);D=Y;console.print(f"[cyan]{STATUS_ICONS[_N]} Updated nonce to {Y} (was too low)[/cyan]")
					except Exception as Z:console.print(f"[bold red]{STATUS_ICONS[_G]} Error updating nonce: {Z}[/bold red]")
				elif'nonce too high'in K.lower():
					console.print(f"[yellow]{STATUS_ICONS[_H]} Nonce too high error detected. Resetting nonce tracking.[/yellow]")
					try:
						import re;l=re.search('state: (\\d+)',K)
						if l:a=int(l.group(1));console.print(f"[cyan]{STATUS_ICONS[_N]} Using state nonce from error message: {a}[/cyan]");D=a;B.update_nonce(C,a)
						else:I=A.eth.get_transaction_count(C,_p);console.print(f"[cyan]{STATUS_ICONS[_N]} Couldn't parse state nonce. Using latest nonce: {I}[/cyan]");D=I;B.update_nonce(C,I)
					except Exception as Z:
						console.print(f"[bold red]{STATUS_ICONS[_G]} Error handling nonce too high: {Z}[/bold red]")
						try:I=A.eth.get_transaction_count(C,_p);console.print(f"[cyan]{STATUS_ICONS[_N]} Using latest nonce as fallback: {I}[/cyan]");D=I;B.update_nonce(C,I)
						except Exception:console.print(f"[yellow]{STATUS_ICONS[_H]} Using nonce 0 as last resort[/yellow]");D=0;B.update_nonce(C,0)
				elif'replacement transaction underpriced'in K.lower():console.print(f"[yellow]{STATUS_ICONS[_H]} Transaction with same nonce pending, needs higher gas price[/yellow]");B.update_nonce(C,D+1);D+=1
				elif'already known'in K.lower():console.print(f"[yellow]{STATUS_ICONS[_H]} Transaction already submitted[/yellow]");B.update_nonce(C,D+1);return N,H
				continue
		console.print(Panel(f"[bold red]{STATUS_ICONS[_G]} All {W} attempts failed[/bold red]"));return _B,_B
	def display_account_info(F,address):
		'Display account balances across networks and BRN';G='N/A';B=address;A=Table(title=f"{STATUS_ICONS[_h]} Account Information for {B[:6]}...{B[-4:]}",box=ROUNDED,border_style=_C);A.add_column(_A9,style='bold');A.add_column('Chain ID',style=_C);A.add_column('Balance',style=_A)
		for C in F.network_manager.networks:
			D=F.network_manager.get_web3(C)
			if D:
				try:H=D.eth.get_balance(B);I=D.from_wei(H,_v);J=D.eth.chain_id;N,K=CHAIN_STYLES.get(C,(_A,_J));A.add_row(f"{K} {C}",f"{J}",f"{STATUS_ICONS[_s]} {I:.6f} ETH")
				except Exception as L:A.add_row(f"{C}",G,f"Error: {str(L)[:30]}...")
		try:
			E=Web3(Web3.HTTPProvider('https://b2n.rpc.caldera.xyz/http'))
			if E.is_connected():M=E.from_wei(E.eth.get_balance(B),_v);A.add_row('🔵 BRN Network',f"{E.eth.chain_id}",f"{STATUS_ICONS[_s]} {M:.6f} BRN")
		except Exception:A.add_row('BRN Network',G,'Could not connect')
		console.print(A)
class BridgeManager:
	'Manages bridge transactions across different networks'
	def __init__(A,config,network_manager,tx_manager):B=config;A.data_bridge=B[_AM];A.bridge_amount=B[_E][_AA];A.network_manager=network_manager;A.tx_manager=tx_manager;A.brn_estimator=BRNEstimator();A.bridge_paths={_AN:(_U,_V),_AO:(_V,_U),_AP:(_V,_T),_AQ:(_T,_V),_AR:(_U,_T),_AS:(_T,_U)}
	def get_available_bridges(A):
		'Get list of available bridges with valid data';C=[]
		for(B,(D,E))in A.bridge_paths.items():
			if B in A.data_bridge and A.data_bridge[B]:C.append((B,f"{D} to {E}"))
		return C
	def execute_bridge(B,bridge_name,account,value_eth=_B):
		'Execute a bridge transaction';E=value_eth;D=bridge_name
		if D not in B.data_bridge or not B.data_bridge[D]:console.print(f"[bold red]{STATUS_ICONS[_G]} No bridge data available for {D}[/bold red]");return _R,_B
		if D not in B.bridge_paths:console.print(f"[bold red]{STATUS_ICONS[_G]} Invalid bridge name: {D}[/bold red]");return _R,_B
		F,G=B.bridge_paths[D];H,J=CHAIN_STYLES.get(F,(_A,_J));I,K=CHAIN_STYLES.get(G,(_A,_J));console.print(Panel(f"[bold {H}]{J} {F}[/bold {H}] → [bold {I}]{K} {G}[/bold {I}]",title=f"{STATUS_ICONS[_O]} Bridge Transaction",border_style=_C))
		if E is _B:E=B.bridge_amount
		A=B.brn_estimator.estimate_brn(F,G,E)
		if A:N=A[_A6];O=A[_Y];P=A[_A7];Q=A[_A8];R=A[_AJ];S=A[_AK];C=Table(title=f"{STATUS_ICONS[_A3]} Transaction Estimation",box=ROUNDED,border_style=_m);C.add_column(_AL,style=_g);C.add_column(_q,style=_C);C.add_row('Bridge Amount',f"{E} ETH");C.add_row('Est. Received',f"{S:.6f} ETH");C.add_row(f"{STATUS_ICONS[_P]} Base BRN Reward",f"{N:.8f} BRN");C.add_row(f"{STATUS_ICONS[_A4]} Bonus (+{O}%)",f"[bold green]+{P:.8f} BRN[/bold green]");C.add_row(f"{STATUS_ICONS[_P]} Total BRN Reward",f"[bold green]{Q:.8f} BRN (${R})[/bold green]");T=B.brn_estimator.get_stats();C.add_row(f"{STATUS_ICONS[_P]} Total Est. BRN",f"[bold green]{T[_Z]:.8f} BRN[/bold green]");console.print(C)
		L,U=B.tx_manager.send_bridge_transaction(F,account,B.data_bridge[D],E)
		if L:
			M=''
			if A:M=f"\n{STATUS_ICONS[_P]} Base BRN: [green]{A[_A6]:.8f} BRN[/green]\n{STATUS_ICONS[_A4]} Bonus (+{A[_Y]}%): [green]+{A[_A7]:.8f} BRN[/green]\n{STATUS_ICONS[_P]} Total Reward: [bold green]{A[_A8]:.8f} BRN[/bold green]"
			console.print(Panel(f"[bold green]{STATUS_ICONS[_M]} Bridge transaction successful![/bold green]\nFrom: [bold {H}]{J} {F}[/bold {H}]\nTo: [bold {I}]{K} {G}[/bold {I}]\nAmount: {E} ETH{M}",border_style=_A));return _L,L
		else:console.print(Panel(f"[bold red]{STATUS_ICONS[_G]} Bridge transaction failed[/bold red]",border_style=_r));return _R,_B
	def get_bridge_delay(A,bridge_name):
		'Get the delay for a specific bridge, using custom delay if set'
		if hasattr(A,_F)and _D in A.custom_delays:return A.custom_delays[_D].get(bridge_name,A.bridge_amount)
		return A.bridge_amount
	def add_custom_bridge(A,source_network,dest_network,bridge_data):
		'Add a custom bridge to the configuration';F=bridge_data;E=dest_network;D=source_network;B=f"{D} - {E}";A.data_bridge[B]=F
		if B not in A.bridge_paths:
			G=next((A for A in A.network_manager.networks if A.startswith(D)),_B);H=next((A for A in A.network_manager.networks if A.startswith(E)),_B)
			if G and H:A.bridge_paths[B]=G,H
		try:
			with open(_S,'r')as C:I=json.load(C)
			I[_AM][B]=F
			with open(_S,_a)as C:json.dump(I,C,indent=2)
			console.print(f"[bold green]{STATUS_ICONS[_M]} Added custom bridge: {B}[/bold green]");return _L
		except Exception as J:console.print(f"[bold red]{STATUS_ICONS[_G]} Failed to save custom bridge: {J}[/bold red]");return _R
	def get_brn_stats(A):'Get BRN reward statistics';return A.brn_estimator.get_stats()
class UserInterface:
	'Handles user interaction through command line interface'
	def __init__(A,config,network_manager,tx_manager,bridge_manager,accounts,labels,trial_info=_B):
		B=config;A.config=B;A.network_manager=network_manager;A.tx_manager=tx_manager;A.bridge_manager=bridge_manager;A.accounts=accounts;A.labels=labels;A.bridge_amount=B[_E][_AA];A.trial_info=trial_info
		if _w not in B[_E]:B[_E][_w]={_b:5,_c:10,_d:30}
		A.delays=B[_E][_w]
		if _F not in B[_E]:B[_E][_F]={_D:{},_I:{}}
		A.custom_delays={_D:B[_E][_F].get(_D,{}),_I:B[_E][_F].get(_I,{})}
	def set_delay_settings(A):
		'Set custom delay times between operations and for specific bridges/transactions';A.clear_screen()
		if _F not in A.config[_E]:A.config[_E][_F]={_D:{},_I:{}}
		if not hasattr(A,_F):A.custom_delays={_D:A.config[_E][_F].get(_D,{}),_I:A.config[_E][_F].get(_I,{})}
		console.print(Panel(f"[bold cyan]Delay Settings:[/bold cyan]\n\n1. Global Delays\n2. Custom Bridge Delays\n3. Custom Transaction Delays",title=f"{STATUS_ICONS[_K]} Delay Settings",border_style=_C));C=Prompt.ask('Select which delay type to modify (1-3) or press Enter to go back',default='')
		if not C:return
		try:
			B=int(C)
			if B==1:A.set_global_delays()
			elif B==2:A.set_bridge_delays()
			elif B==3:A.set_transaction_delays()
			else:console.print(_AT);time.sleep(2)
		except ValueError:console.print(_AU);time.sleep(2)
	def set_global_delays(A):
		'Set global delay settings';A.clear_screen();console.print(Panel(f"[bold cyan]Current Global Delay Settings:[/bold cyan]\n\n1. Between accounts: {A.delays[_b]} seconds\n2. Between bridges: {A.delays[_c]} seconds\n3. Between cycles: {A.delays[_d]} seconds",title=f"{STATUS_ICONS[_K]} Global Delay Settings",border_style=_C));E=Prompt.ask('Select which delay to modify (1-3) or press Enter to go back',default='')
		if not E:return
		try:
			C=int(E)
			if C<1 or C>3:console.print(_AT);time.sleep(2);return
			G=[_b,_c,_d];H=['between accounts','between bridges','between cycles'];D=G[C-1];F=H[C-1];I=A.delays[D];B=Prompt.ask(f"Enter new delay {F} in seconds",default=str(I))
			try:
				B=int(B)
				if B<0:console.print(_AB);time.sleep(2);return
				A.delays[D]=B;A.config[_E][_w][D]=B
				with open(_S,_a)as J:json.dump(A.config,J,indent=2)
				console.print(f"[bold green]✅ {F.title()} delay updated to {B} seconds[/bold green]");time.sleep(2)
			except ValueError:console.print('[bold red]Invalid value. Please enter a number.[/bold red]');time.sleep(2)
		except(ValueError,IndexError):console.print(_AU);time.sleep(2)
	def set_bridge_delays(A):
		'Set custom delays for specific bridges';P='[bold red]Invalid bridge number.[/bold red]';A.clear_screen();C=A.bridge_manager.get_available_bridges()
		if not C:console.print(f"[bold red]{STATUS_ICONS[_G]} No bridges with valid data available[/bold red]");time.sleep(2);return
		E=Table(title='Custom Bridge Delays',box=ROUNDED,border_style=_C);E.add_column('#',style=_C,justify=_AC);E.add_column(_x,style=_g);E.add_column(_AD,style=_A)
		for(Q,(B,V))in enumerate(C,1):I=A.custom_delays[_D].get(B,_e);K,L=A.bridge_manager.bridge_paths[B];M,R=CHAIN_STYLES.get(K,(_A,_J));N,S=CHAIN_STYLES.get(L,(_A,_J));T=f"[{M}]{R} {K}[/{M}] → [{N}]{S} {L}[/{N}]";E.add_row(str(Q),T,f"{I} seconds"if I!=_e else I)
		console.print(E);console.print(Panel(f"[bold cyan]Options:[/bold cyan]\n\n1. Set custom delay for a bridge\n2. Remove custom delay for a bridge\n3. Remove all custom bridge delays",title=f"{STATUS_ICONS[_E]} Bridge Delay Options",border_style=_C));O=Prompt.ask(_AV,default='')
		if not O:return
		try:
			J=int(O)
			if J==1:
				F=Prompt.ask('Enter bridge number to set custom delay',default='')
				if not F:return
				try:
					G=int(F)-1
					if 0<=G<len(C):
						B=C[G][0];U=A.custom_delays[_D].get(B,A.delays[_c]);D=Prompt.ask(f"Enter custom delay in seconds for this bridge",default=str(U))
						try:
							D=int(D)
							if D<0:console.print(_AB);time.sleep(2);return
							A.custom_delays[_D][B]=D
							if _F not in A.config[_E]:A.config[_E][_F]={_D:{},_I:{}}
							A.config[_E][_F][_D][B]=D
							with open(_S,_a)as H:json.dump(A.config,H,indent=2)
							console.print(f"[bold green]✅ Custom delay for {B} set to {D} seconds[/bold green]");time.sleep(2)
						except ValueError:console.print(_AW);time.sleep(2)
					else:console.print(P);time.sleep(2)
				except ValueError:console.print(_n);time.sleep(2)
			elif J==2:
				F=Prompt.ask('Enter bridge number to remove custom delay',default='')
				if not F:return
				try:
					G=int(F)-1
					if 0<=G<len(C):
						B=C[G][0]
						if B in A.custom_delays[_D]:
							del A.custom_delays[_D][B]
							if B in A.config[_E][_F][_D]:
								del A.config[_E][_F][_D][B]
								with open(_S,_a)as H:json.dump(A.config,H,indent=2)
							console.print(f"[bold green]✅ Custom delay for {B} removed[/bold green]")
						else:console.print(f"[bold yellow]No custom delay exists for {B}[/bold yellow]")
						time.sleep(2)
					else:console.print(P);time.sleep(2)
				except ValueError:console.print(_n);time.sleep(2)
			elif J==3:
				if Confirm.ask('Are you sure you want to remove all custom bridge delays?'):
					A.custom_delays[_D]={};A.config[_E][_F][_D]={}
					with open(_S,_a)as H:json.dump(A.config,H,indent=2)
					console.print(f"[bold green]✅ All custom bridge delays removed[/bold green]");time.sleep(2)
			else:console.print(_AX);time.sleep(2)
		except ValueError:console.print(_n);time.sleep(2)
	def set_transaction_delays(A):
		'Set custom delays for transactions on specific networks';M='[bold red]Invalid network number.[/bold red]';A.clear_screen();D=Table(title='Custom Transaction Delays',box=ROUNDED,border_style=_C);D.add_column('#',style=_C,justify=_AC);D.add_column(_A9,style=_g);D.add_column(_AD,style=_A);E=list(A.network_manager.networks.keys())
		for(N,B)in enumerate(E,1):I=A.custom_delays[_I].get(B,_e);K,O=CHAIN_STYLES.get(B,(_A,_J));D.add_row(str(N),f"[{K}]{O} {B}[/{K}]",f"{I} seconds"if I!=_e else I)
		console.print(D);console.print(Panel(f"[bold cyan]Options:[/bold cyan]\n\n1. Set custom delay for a network\n2. Remove custom delay for a network\n3. Remove all custom transaction delays",title=f"{STATUS_ICONS[_E]} Transaction Delay Options",border_style=_C));L=Prompt.ask(_AV,default='')
		if not L:return
		try:
			J=int(L)
			if J==1:
				F=Prompt.ask('Enter network number to set custom delay',default='')
				if not F:return
				try:
					G=int(F)-1
					if 0<=G<len(E):
						B=E[G];P=5;Q=A.custom_delays[_I].get(B,P);C=Prompt.ask(f"Enter custom delay in seconds for transactions on {B}",default=str(Q))
						try:
							C=int(C)
							if C<0:console.print(_AB);time.sleep(2);return
							A.custom_delays[_I][B]=C
							if _F not in A.config[_E]:A.config[_E][_F]={_D:{},_I:{}}
							A.config[_E][_F][_I][B]=C
							with open(_S,_a)as H:json.dump(A.config,H,indent=2)
							console.print(f"[bold green]✅ Custom transaction delay for {B} set to {C} seconds[/bold green]");time.sleep(2)
						except ValueError:console.print(_AW);time.sleep(2)
					else:console.print(M);time.sleep(2)
				except ValueError:console.print(_n);time.sleep(2)
			elif J==2:
				F=Prompt.ask('Enter network number to remove custom delay',default='')
				if not F:return
				try:
					G=int(F)-1
					if 0<=G<len(E):
						B=E[G]
						if B in A.custom_delays[_I]:
							del A.custom_delays[_I][B]
							if B in A.config[_E][_F][_I]:
								del A.config[_E][_F][_I][B]
								with open(_S,_a)as H:json.dump(A.config,H,indent=2)
							console.print(f"[bold green]✅ Custom transaction delay for {B} removed[/bold green]")
						else:console.print(f"[bold yellow]No custom transaction delay exists for {B}[/bold yellow]")
						time.sleep(2)
					else:console.print(M);time.sleep(2)
				except ValueError:console.print(_n);time.sleep(2)
			elif J==3:
				if Confirm.ask('Are you sure you want to remove all custom transaction delays?'):
					A.custom_delays[_I]={};A.config[_E][_F][_I]={}
					with open(_S,_a)as H:json.dump(A.config,H,indent=2)
					console.print(f"[bold green]✅ All custom transaction delays removed[/bold green]");time.sleep(2)
			else:console.print(_AX);time.sleep(2)
		except ValueError:console.print(_n);time.sleep(2)
	def clear_screen(A):'Clear the terminal screen';os.system('cls'if os.name=='nt'else'clear')
	def display_network_info(I):
		'Display current network information with timeout protection';Q='Unknown';E='chain_id';B=Table(title=f"{STATUS_ICONS['network']} Network Status",box=ROUNDED,border_style=_o);B.add_column(_A9,style='bold');B.add_column('Chain ID',style=_C);B.add_column('Block',style=_A);B.add_column('RPC Endpoint',style=_o)
		for(A,C)in I.network_manager.networks.items():
			try:
				K=time.time();L=5;F=_B
				try:
					F=I.network_manager.get_web3(A)
					if time.time()-K>L:raise TimeoutError(f"Getting web3 for {A} timed out")
				except Exception as G:console.print(f"[yellow]Error getting web3 for {A}: {G}[/yellow]")
				if F and F.is_connected():
					try:
						M=L-(time.time()-K)
						if M<=0:raise TimeoutError('Network check timed out')
						D={_k:_B,E:_B,_M:_R};N=threading.Event()
						def R():
							try:D[_k]=F.eth.block_number;D[E]=F.eth.chain_id;D[_M]=_L
							except Exception as A:console.print(f"[yellow]Error getting block info: {A}[/yellow]")
							finally:N.set()
						O=threading.Thread(target=R);O.daemon=_L;O.start()
						if not N.wait(timeout=min(3,M)):raise TimeoutError('Block data retrieval timed out')
						if D[_M]:S=D[_k];T=D[E];J=C[_j];P,H=CHAIN_STYLES.get(A,(_A,_J));B.add_row(f"{H} {A}",f"{T}",f"{STATUS_ICONS[_A1]} {S}",f"{J[:40]}..."if len(J)>40 else J)
						else:raise Exception('Failed to get block data')
					except Exception as G:B.add_row(f"{A}",f"{C[E]}",f"Error: {str(G)[:30]}...",f"{C[_j][:40]}...")
				else:P,H=CHAIN_STYLES.get(A,(_A,_J));B.add_row(f"{H} {A}",f"{C[E]}",'[red]Not connected[/red]',f"{C[_j][:40]}...")
			except Exception as G:P,H=CHAIN_STYLES.get(A,(_A,_J));B.add_row(f"{H} {A}",f"{C.get(E,Q)}",f"[red]Error: {str(G)[:20]}...[/red]",f"{C.get(_j,Q)[:40]}...")
		I.clear_screen();console.print(B)
	def display_account_balances(C):
		'Display balances for the first account and BRN rewards with bonus info'
		if not C.accounts:console.print(Panel('[yellow]No accounts configured. Please update your config.json file.[/yellow]'));return
		D=C.accounts[0];C.tx_manager.display_account_info(D.address);B=C.bridge_manager.get_brn_stats()
		if B[_Q]>0:A=Table(title=f"{STATUS_ICONS[_P]} BRN Rewards Tracker",box=ROUNDED,border_style=_A);A.add_column('Metric',style=_g);A.add_column(_q,style=_A);A.add_row(_AY,f"[bold green]{B[_Z]:.8f} BRN[/bold green]");A.add_row(_AZ,f"[bold green]${B[_u]:.4f} USD[/bold green]");A.add_row(_Aa,f"{B[_Q]}");A.add_row(_Ab,f"{B[_X]:.8f} BRN (${B[_l]:.4f})");A.add_row('Bonus Information',f"[cyan]All rewards include +{B[_Y]}% bonus[/cyan]");console.print(A)
	def display_brn_stats(D):
		'Display BRN rewards statistics with bonus information';D.clear_screen();A=D.bridge_manager.get_brn_stats()
		if A[_Q]==0:console.print(Panel(f"[yellow]No BRN rewards estimated yet. Run some bridge transactions first.[/yellow]",title=f"{STATUS_ICONS[_P]} BRN Rewards Statistics",border_style=_m));time.sleep(3);return
		B=Table(title=f"{STATUS_ICONS[_P]} BRN Rewards Statistics",box=ROUNDED,border_style=_A);B.add_column('Metric',style=_g);B.add_column(_q,style=_A);B.add_row(_AY,f"[bold green]{A[_Z]:.8f} BRN[/bold green]");B.add_row(_AZ,f"[bold green]${A[_u]:.4f} USD[/bold green]");B.add_row(_Aa,f"{A[_Q]}");B.add_row(_Ab,f"{A[_X]:.8f} BRN (${A[_l]:.4f})");C=24*3;E=C*365;F=A[_X]*E;G=A[_l]*E;B.add_row('Estimated Daily (@ 3tx/hour)',f"{A[_X]*C:.4f} BRN (${A[_l]*C:.2f})");B.add_row('Estimated Monthly (@ 3tx/hour)',f"{A[_X]*C*30:.4f} BRN (${A[_l]*C*30:.2f})");B.add_row('Estimated Yearly (@ 3tx/hour)',f"[bold green]{F:.4f} BRN (${G:.2f})[/bold green]");console.print(B);console.print(Panel(f"[cyan]BRN rewards include a +{A[_Y]}% bonus on every transaction.\nThese estimates are based on your historical BRN earnings (with bonus) of {A[_X]:.8f} BRN per transaction.\nActual rewards may vary based on network conditions, transaction volume, and t3rn protocol changes.[/cyan]",title='Reward Information',border_style=_o));Prompt.ask('\nPress Enter to return to the main menu',default='')
	def display_main_menu(B):
		'Display the main menu and get user choice'
		if B.trial_info:
			Q=pytz.timezone(_A5);R=datetime.now(Q).replace(tzinfo=_B);F=B.trial_info[_AE].replace(tzinfo=_B);G=F-R;S,T=divmod(G.total_seconds(),3600);U,V=divmod(T,60)
			if G.total_seconds()>0:console.print(Panel(f"[bold yellow]Your IP: {B.trial_info['ip']}[/bold yellow]\nTime left in trial: [bold cyan]{int(S)}h {int(U)}m {int(V)}s[/bold cyan]\nTrial expires: {F.strftime(_Ac)} WIB",title=f"{STATUS_ICONS[_i]} Trial Access",border_style=_m))
		try:B.display_network_info();B.display_account_balances()
		except Exception as W:console.print(f"[yellow]Error loading network information: {W}. Continuing with limited data.[/yellow]")
		X=Text(f"{STATUS_ICONS[_O]} T3RN Bridge Bot by Yoake",style='bold cyan');H=''
		for(I,(J,Y))in enumerate(zip(B.accounts,B.labels)):H+=f"[bold cyan]{STATUS_ICONS[_h]} {Y}:[/bold cyan] {J.address[:6]}...{J.address[-4:]}\n"
		Z={_AN:(_U,_V),_AO:(_V,_U),_AP:(_V,_T),_AQ:(_T,_V),_AR:(_U,_T),_AS:(_T,_U)}
		for(K,a)in Z.items():
			if K not in B.bridge_manager.bridge_paths:B.bridge_manager.bridge_paths[K]=a
		b=B.bridge_manager.get_available_bridges();C='';A=[];C+='[bold cyan]Bridge Options:[/bold cyan]\n'
		for(I,(L,f))in enumerate(b,1):M,N=B.bridge_manager.bridge_paths[L];O,c=CHAIN_STYLES.get(M,(_A,_J));P,d=CHAIN_STYLES.get(N,(_A,_J));C+=f"[bold white]{I}.[/bold white] [{O}]{c} {M}[/{O}] → [{P}]{d} {N}[/{P}]\n";A.append(L)
		C+='\n[bold cyan]Utility Options:[/bold cyan]\n';C+=f"[bold white]{len(A)+1}.[/bold white] {STATUS_ICONS[_O]} Run all transactions repeatedly\n";C+=f"[bold white]{len(A)+2}.[/bold white] {STATUS_ICONS[_O]} Run custom selection of bridges\n";C+=f"[bold white]{len(A)+3}.[/bold white] {STATUS_ICONS[_E]} Set Bridge Amount (current: {B.bridge_amount} ETH)\n";C+=f"[bold white]{len(A)+4}.[/bold white] {STATUS_ICONS[_K]} Set Delay Times (between actions)\n";C+=f"[bold white]{len(A)+5}.[/bold white] {STATUS_ICONS[_P]} View BRN Rewards Stats\n";C+=f"[bold white]Q.[/bold white] {STATUS_ICONS[_N]} Quit\n";e=f"{H}\n{C}";console.print(Panel(e,title=X,border_style=_C,box=DOUBLE));E=Prompt.ask('Choose an option',default='Q')
		if E.isdigit():
			D=int(E)
			if 1<=D<=len(A):return A[D-1]
			elif D==len(A)+1:return'RUN_ALL'
			elif D==len(A)+2:return'CUSTOM'
			elif D==len(A)+3:return _Ad
			elif D==len(A)+4:return _Ae
			elif D==len(A)+5:return _Af
		return E.upper()
	def set_bridge_amount(A):
		'Set the bridge amount';A.clear_screen();console.print(Panel(f"Current bridge amount: {A.bridge_amount} ETH",title=f"{STATUS_ICONS[_E]} Bridge Amount",border_style=_C))
		try:
			B=float(Prompt.ask('Enter new amount in ETH',default=str(A.bridge_amount)))
			if B<=0:console.print(f"[bold red]{STATUS_ICONS[_G]} Amount must be greater than 0[/bold red]");time.sleep(2);return
			A.bridge_amount=B;A.bridge_manager.bridge_amount=B;A.config[_E][_AA]=B
			with open(_S,_a)as C:json.dump(A.config,C,indent=2)
			console.print(f"[bold green]{STATUS_ICONS[_M]} Bridge amount set to {A.bridge_amount} ETH[/bold green]")
		except ValueError:console.print(f"[bold red]{STATUS_ICONS[_G]} Invalid amount[/bold red]")
		time.sleep(2)
	def update_status_table_with_brn(H,status_table,bridge_label,account_label,success,bridge_amount,brn_stats):
		'Helper method to update status tables with BRN bonus information';E=success;A=brn_stats
		if E:F=f"[green]{STATUS_ICONS[_M]} Success - {bridge_amount} ETH[/green]"
		else:F=f"[red]{STATUS_ICONS[_G]} Failed[/red]"
		B=''
		if A[_Q]>0:
			if E:
				C=A[_Z]
				if A[_Q]>1:C=A[_Z]-A[_X]*(A[_Q]-1)
				D=A[_Y];G=C/(1+D/100);I=G*(D/100);B=f"[green]{G:.6f} +{D}% = {C:.6f}[/green]"
			else:B=_Ag
		else:B=_Ah
		status_table.add_row(bridge_label,account_label,F,B)
	def display_brn_summary(B,brn_stats):
		'Display a summary of BRN rewards with bonus information';A=brn_stats
		if A[_Q]>0:console.print(Panel(f"Total estimated BRN rewards: [bold green]{A[_Z]:.8f} BRN[/bold green] (${A[_u]:.4f})\nAverage per transaction: [green]{A[_X]:.8f} BRN[/green]\nBonus: [cyan]All rewards include +{A[_Y]}% bonus[/cyan]",title=f"{STATUS_ICONS[_P]} BRN Rewards Summary",border_style=_A))
	def run_custom_bridge_selection(A):
		'Run a custom selection of bridges in sequence';A.clear_screen();console.print(Panel('Select bridges to run in sequence',title=f"{STATUS_ICONS[_O]} Custom Bridge Selection",border_style=_C));O=A.bridge_manager.get_available_bridges()
		if not O:console.print(f"[bold red]{STATUS_ICONS[_G]} No bridges with valid data available[/bold red]");time.sleep(2);return
		I=Table(title='Available Bridges',box=ROUNDED,border_style=_C);I.add_column('#',style=_C,justify=_AC);I.add_column('Route',style=_A);I.add_column(_AD,style=_m)
		for(G,(B,h))in enumerate(O,1):
			J,K=A.bridge_manager.bridge_paths[B];D,L=CHAIN_STYLES.get(J,(_A,_J));E,M=CHAIN_STYLES.get(K,(_A,_J));P=_e
			if hasattr(A,_F)and _D in A.custom_delays:P=A.custom_delays[_D].get(B,_e)
			S=f"[{D}]{L} {J}[/{D}] → [{E}]{M} {K}[/{E}]";I.add_row(str(G),S,f"{P}s"if P!=_e else P)
		console.print(I);c=Prompt.ask('Enter bridge numbers to run (comma separated, e.g. 1,3,4)')
		try:
			d=[int(A.strip())-1 for A in c.split(',')];F=[]
			for T in d:
				if 0<=T<len(O):F.append(O[T][0])
				else:console.print(f"[yellow]{STATUS_ICONS[_H]} Invalid selection: {T+1}[/yellow]")
			if not F:console.print(f"[bold red]{STATUS_ICONS[_G]} No valid bridges selected[/bold red]");time.sleep(2);return
			Q=Table(title='Selected Bridges',box=ROUNDED,border_style=_A);Q.add_column(_x,style=_A);Q.add_column('Delay',style=_m)
			for B in F:
				J,K=A.bridge_manager.bridge_paths[B];D,L=CHAIN_STYLES.get(J,(_A,_J));E,M=CHAIN_STYLES.get(K,(_A,_J));C=A.delays[_c]
				if hasattr(A,_F)and _D in A.custom_delays:C=A.custom_delays[_D].get(B,C)
				S=f"[{D}]{L} {J}[/{D}] → [{E}]{M} {K}[/{E}]";Q.add_row(S,f"{C}s"if C!=_e else _e)
			console.print(Q)
			if not Confirm.ask(f"Run these {len(F)} bridges in sequence?"):return
			R=f"[cyan]Delays:[/cyan]\n- Between accounts: {A.delays[_b]} seconds\n";U=[]
			if hasattr(A,_F)and _D in A.custom_delays:
				for B in F:
					if B in A.custom_delays[_D]:U.append(f"- {B}: {A.custom_delays[_D][B]} seconds")
			if U:R+=f"[cyan]Custom Bridge Delays:[/cyan]\n"+'\n'.join(U)+'\n'
			else:R+=f"- Between bridges: {A.delays[_c]} seconds\n"
			R+=f"- Between cycles: {A.delays[_d]} seconds";console.print(Panel(f"Running {len(F)} selected bridges in sequence...\nPress Ctrl+C to stop\n\n{R}",title=f"{STATUS_ICONS[_O]} Custom Bridge Sequence",border_style=_C))
			try:
				V=0
				while _L:
					if A.trial_info:A.check_trial_expiry()
					V+=1;console.print(f"[bold cyan]{STATUS_ICONS[_N]} Starting cycle {V}[/bold cyan]");H=Table(title=f"Cycle {V} Progress",box=ROUNDED,border_style=_C);H.add_column(_x,style=_C);H.add_column(_AF,style=_C);H.add_column(_AG,style=_A);H.add_column(_AH,style=_A)
					for B in F:
						N,W=A.bridge_manager.bridge_paths[B];D,L=CHAIN_STYLES.get(N,(_A,_J));E,M=CHAIN_STYLES.get(W,(_A,_J));e=f"[{D}]{L} {N}[/{D}] → [{E}]{M} {W}[/{E}]";console.print(f"[cyan]{STATUS_ICONS[_O]} Processing bridge: {B} ({N} to {W})[/cyan]")
						for(G,f)in enumerate(A.accounts):
							Y=A.labels[G]if G<len(A.labels)else f"Account {G+1}";X=_B
							if hasattr(A,_F)and _I in A.custom_delays:X=A.custom_delays[_I].get(N)
							if X is not _B:console.print(f"[cyan]{STATUS_ICONS[_K]} Using custom transaction delay for {N}: {X}s[/cyan]")
							console.print(f"[cyan]{STATUS_ICONS[_h]} Processing account: {Y}[/cyan]");g,i=A.bridge_manager.execute_bridge(B,f,A.bridge_amount);Z=A.bridge_manager.get_brn_stats();A.update_status_table_with_brn(H,e,Y,g,A.bridge_amount,Z);a=A.delays[_b]
							if G<len(A.accounts)-1:console.print(f"[cyan]{STATUS_ICONS[_K]} Waiting {a} seconds before next account...[/cyan]");time.sleep(a)
						if B!=F[-1]:
							C=A.delays[_c]
							if hasattr(A,_F)and _D in A.custom_delays:C=A.custom_delays[_D].get(B,C)
							console.print(f"[cyan]{STATUS_ICONS[_K]} Waiting {C} seconds before next bridge...[/cyan]");time.sleep(C)
					console.print(H);A.display_brn_summary(Z);b=A.delays[_d];console.print(f"[bold cyan]{STATUS_ICONS[_K]} Completed custom selection cycle. Waiting {b} seconds before starting again...[/bold cyan]");time.sleep(b)
			except KeyboardInterrupt:console.print(f"[yellow]{STATUS_ICONS[_H]} Stopped by user[/yellow]")
			except TrialExpiredException:console.print(f"[bold red]{STATUS_ICONS[_G]} Trial period has expired[/bold red]");time.sleep(3);return
		except ValueError:console.print(f"[bold red]{STATUS_ICONS[_G]} Invalid input. Please enter comma-separated numbers.[/bold red]");time.sleep(2)
	def run_single_bridge(A,bridge_name):
		'Run a single bridge continuously';H=bridge_name;I,J=A.bridge_manager.bridge_paths[H];K,S=CHAIN_STYLES.get(I,(_A,_J));L,T=CHAIN_STYLES.get(J,(_A,_J));console.print(Panel(f"""Running [{K}]{S} {I}[/{K}] → [{L}]{T} {J}[/{L}] bridge continuously...
Press Ctrl+C to stop

[cyan]Delays:[/cyan]
- Between accounts: {A.delays[_b]} seconds
- Between cycles: {A.delays[_d]} seconds""",title=f"{STATUS_ICONS[_O]} Single Bridge Mode",border_style=_C))
		try:
			E=0
			while _L:
				if A.trial_info:A.check_trial_expiry()
				E+=1;console.print(f"[bold cyan]{STATUS_ICONS[_N]} Starting cycle {E}[/bold cyan]");C=Table(title=f"Cycle {E} Progress",box=ROUNDED,border_style=_C);C.add_column(_AF,style=_C);C.add_column(_AG,style=_A);C.add_column('Time',style=_C);C.add_column(_AH,style=_A)
				for(D,U)in enumerate(A.accounts):
					M=A.labels[D]if D<len(A.labels)else f"Account {D+1}";V=time.time();console.print(f"[cyan]{STATUS_ICONS[_h]} Processing account: {M}[/cyan]");N,Z=A.bridge_manager.execute_bridge(H,U,A.bridge_amount);W=time.time()
					if N:O=f"[green]{STATUS_ICONS[_M]} Success - {A.bridge_amount} ETH[/green]"
					else:O=f"[red]{STATUS_ICONS[_G]} Failed[/red]"
					X=W-V;B=A.bridge_manager.get_brn_stats()
					if B[_Q]>0:
						if N:
							F=B[_Z]
							if B[_Q]>1:F=B[_Z]-B[_X]*(B[_Q]-1)
							P=B[_Y];Y=F/(1+P/100);G=f"[green]{Y:.6f} +{P}% = {F:.6f}[/green]"
						else:G=_Ag
					else:G=_Ah
					C.add_row(M,O,f"{STATUS_ICONS[_K]} {X:.1f}s",G);Q=A.delays[_b]
					if D<len(A.accounts)-1:console.print(f"[cyan]{STATUS_ICONS[_K]} Waiting {Q} seconds before next account...[/cyan]");time.sleep(Q)
				console.print(C);A.display_brn_summary(B);R=A.delays[_d];console.print(f"[bold cyan]{STATUS_ICONS[_K]} Waiting {R} seconds before next cycle...[/bold cyan]");time.sleep(R)
		except KeyboardInterrupt:console.print(f"[yellow]{STATUS_ICONS[_H]} Stopped by user[/yellow]")
		except TrialExpiredException:console.print(f"[bold red]{STATUS_ICONS[_G]} Trial period has expired[/bold red]");time.sleep(3);return
	def run_all_bridges(A):
		'Run all available bridges in sequence';B=f"[cyan]Global Delays:[/cyan]\n- Between accounts: {A.delays[_b]} seconds\n";Y=[]
		if hasattr(A,_F)and _D in A.custom_delays and A.custom_delays[_D]:
			B+=f"[cyan]Custom Bridge Delays:[/cyan]\n"
			for(C,H)in A.custom_delays[_D].items():B+=f"- {C}: {H} seconds\n"
		else:B+=f"- Between bridges: {A.delays[_c]} seconds\n"
		if hasattr(A,_F)and _I in A.custom_delays and A.custom_delays[_I]:
			B+=f"[cyan]Custom Transaction Delays:[/cyan]\n"
			for(S,H)in A.custom_delays[_I].items():B+=f"- {S}: {H} seconds\n"
		B+=f"- Between cycles: {A.delays[_d]} seconds";console.print(Panel(f"Running all available bridges continuously...\nPress Ctrl+C to stop\n\n{B}",title=f"{STATUS_ICONS[_O]} All Bridges Mode",border_style=_C))
		try:
			I=0
			while _L:
				if A.trial_info:A.check_trial_expiry()
				I+=1;console.print(f"[bold cyan]{STATUS_ICONS[_N]} Starting cycle {I}[/bold cyan]");J=[A for(A,B)in A.bridge_manager.get_available_bridges()]
				if not J:console.print(f"[bold red]{STATUS_ICONS[_G]} No bridges with valid data available[/bold red]");return
				D=Table(title=f"Cycle {I} Progress",box=ROUNDED,border_style=_C);D.add_column(_x,style=_C);D.add_column(_AF,style=_C);D.add_column(_AG,style=_A);D.add_column(_AH,style=_A)
				for C in J:
					E,K=A.bridge_manager.bridge_paths[C];M,T=CHAIN_STYLES.get(E,(_A,_J));N,U=CHAIN_STYLES.get(K,(_A,_J));V=f"[{M}]{T} {E}[/{M}] → [{N}]{U} {K}[/{N}]";console.print(f"[cyan]{STATUS_ICONS[_O]} Processing bridge: {C} ({E} to {K})[/cyan]")
					for(F,W)in enumerate(A.accounts):
						O=A.labels[F]if F<len(A.labels)else f"Account {F+1}";L=_B
						if hasattr(A,_F)and _I in A.custom_delays:L=A.custom_delays[_I].get(E)
						if L is not _B:console.print(f"[cyan]{STATUS_ICONS[_K]} Using custom transaction delay for {E}: {L}s[/cyan]")
						console.print(f"[cyan]{STATUS_ICONS[_h]} Processing account: {O}[/cyan]");X,Z=A.bridge_manager.execute_bridge(C,W,A.bridge_amount);P=A.bridge_manager.get_brn_stats();A.update_status_table_with_brn(D,V,O,X,A.bridge_amount,P);Q=A.delays[_b]
						if F<len(A.accounts)-1:console.print(f"[cyan]{STATUS_ICONS[_K]} Waiting {Q} seconds before next account...[/cyan]");time.sleep(Q)
					if C!=J[-1]:
						G=A.delays[_c]
						if hasattr(A,_F)and _D in A.custom_delays:G=A.custom_delays[_D].get(C,G)
						console.print(f"[cyan]{STATUS_ICONS[_K]} Waiting {G} seconds before next bridge...[/cyan]");time.sleep(G)
				console.print(D);A.display_brn_summary(P);R=A.delays[_d];console.print(f"[bold cyan]{STATUS_ICONS[_K]} Completed full cycle. Waiting {R} seconds before starting again...[/bold cyan]");time.sleep(R)
		except KeyboardInterrupt:console.print(f"[yellow]{STATUS_ICONS[_H]} Stopped by user[/yellow]")
		except TrialExpiredException:console.print(f"[bold red]{STATUS_ICONS[_G]} Trial period has expired[/bold red]");time.sleep(3);return
	def check_trial_expiry(A):
		'Check if trial period has expired and raise exception if it has'
		if not A.trial_info:return
		B=pytz.timezone(_A5);C=datetime.now(B).replace(tzinfo=_B);D=A.trial_info[_AE].replace(tzinfo=_B)
		if C>D:raise TrialExpiredException('Trial period has expired')
	def run(A):
		'Main UI loop'
		while _L:
			try:
				if A.trial_info:A.check_trial_expiry()
				A.clear_screen()
				try:
					B=A.display_main_menu()
					if B=='Q':break
					elif B=='RUN_ALL':A.run_all_bridges()
					elif B=='CUSTOM':A.run_custom_bridge_selection()
					elif B==_Ad:A.set_bridge_amount()
					elif B==_Ae:A.set_delay_settings()
					elif B==_Af:A.display_brn_stats()
					elif B in A.bridge_manager.bridge_paths:A.run_single_bridge(B)
					else:console.print(f"[bold red]{STATUS_ICONS[_G]} Invalid choice[/bold red]");time.sleep(2)
				except KeyboardInterrupt:console.print('\n[yellow]Operation interrupted by user. Returning to main menu...[/yellow]');time.sleep(2);continue
				except Exception as C:logger.error(f"Error in UI loop: {C}");console.print(f"[bold red]{STATUS_ICONS[_G]} Error: {C}[/bold red]");console.print(f"[cyan]{STATUS_ICONS[_N]} Waiting 5 seconds before continuing...[/cyan]");time.sleep(5)
			except TrialExpiredException:A.clear_screen();console.print(Panel(f"[bold red]Your trial period has expired.[/bold red]\n\nContact the developer at https://t.me/yoakeid to get full access.",title=f"{STATUS_ICONS[_i]} Trial Expired",border_style=_r));time.sleep(5);break
class TrialExpiredException(Exception):'Exception raised when trial period has expired'
def main():
	'Main entry point for the application'
	try:
		os.system('cls'if os.name=='nt'else'clear');A=get_user_ip();M,D,H=check_ip_access(A);I=_B
		if M:console.print(Panel(f"[bold green]Your IP: {A}[/bold green]\nAccess: [bold green]Full Access[/bold green]\nValid until: [bold green]{D.strftime(_t)}[/bold green]",title=f"{STATUS_ICONS[_i]} IP Verification",border_style=_A))
		elif'trial'in H.lower():I={'ip':A,_AE:D};console.print(Panel(f"[bold yellow]Your IP: {A}[/bold yellow]\nAccess: [bold yellow]1-Hour Trial[/bold yellow]\nExpires: [bold yellow]{D.strftime(_Ac)} WIB[/bold yellow]\n\nContact: https://t.me/kuro12345 for full access",title=f"{STATUS_ICONS[_i]} Trial Access Granted",border_style=_m))
		else:console.print(Panel(f"[bold red]Your IP: {A}[/bold red]\nAccess: [bold red]Denied[/bold red]\n{H}\n\nContact: https://t.me/kuro12345 to get access",title=f"{STATUS_ICONS[_i]} IP Verification Failed",border_style=_r));time.sleep(5);return
		time.sleep(2);N='\n                        🌉 T3RN BRIDGE BOT 🌉\n                              By DYMin\n                         https://t.me/kuro12345\n                    Smart, Fast, Reliable Bridging\n        ';console.print(Panel(N,title='Welcome!',border_style=_C,padding=(1,2)));console.print(Panel('         https://bridge.t2rn.io/ or https://unlock3d.t3rn.io/',title='Bridge URL',border_style=_o));F=[_B];B=threading.Event();C=[_B];time.sleep(3)
		def O():
			M='label';J='address'
			try:
				D=load_config();G=NetworkManager(D);K=TransactionManager(G);N=BridgeManager(D,G,K);E=[];L=[]
				for A in D['accounts']:
					try:
						O=A['private_key'];H=Account.from_key(O);E.append(H)
						if J in A and H.address.lower()!=A[J].lower():print(f"Warning: Address mismatch for {A[M]}. Expected {A[J]}, got {H.address}")
						L.append(A.get(M,f"Account {len(E)}"))
					except Exception as I:print(f"Error creating account: {I}")
				if not E:C[0]='No valid accounts found. Please update your config.json file with valid private keys.';B.set();return
				F[0]=D,G,K,N,E,L
			except Exception as I:C[0]=str(I)
			finally:B.set()
		print('Initializing T3RN Bridge Bot...');E=threading.Thread(target=O);E.daemon=_L;E.start();P=30;J=time.time();K=['|','/','-','\\'];G=0
		while not B.is_set()and time.time()-J<P:print(f"\rInitializing... {K[G]} ({int(time.time()-J)}s)",end='');G=(G+1)%len(K);time.sleep(.2)
		print('\r'+' '*50+'\r',end='')
		if not B.is_set():print('Initialization timed out! Continuing with limited functionality.');E.join(.1)
		if C[0]:print(f"Error during initialization: {C[0]}");return
		if not F[0]:print('Failed to initialize application components.');return
		Q,R,S,T,U,V=F[0];W=UserInterface(Q,R,S,T,U,V,I);W.run()
	except KeyboardInterrupt:print('\nApplication terminated by user.')
	except Exception as L:logger.error(f"Unexpected error: {L}");print(f"Unexpected error: {L}");print('Please check the log file for details.')
if __name__=='__main__':main()
