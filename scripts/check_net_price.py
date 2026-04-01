import sys
sys.path.append('/home/warwick/.openclaw/workspace/scripts')
from data import get_quote_yf

q = get_quote_yf("NET")
print(q)
