
import re
from config import *

# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

import re
async def validate_query(q):
    query = q
            # Checking if the length of the query is less than 2. If it is, it returns.
    if len(query) < 2:
        return False
   

# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

    if re.findall(r"((^\/|^,|^:|^\.|^[\U0001F600-\U000E007F]).*)", query):
        return False
    
    # Checking if the message contains a link.
    if ("https://" or "http://") in query:
        return False

    # It removes the year from the search query.|hello|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|kitt
    query = re.sub(r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|gib)(\sme)?)|new|hd|\(|\)|dedo|print|fulllatest|br((o|u)h?)*um(o)*|aya((um(o)*)?|any(one)|with\ssk)*ubtitle(s)?)", "", query.lower(), flags=re.IGNORECASE)
    return query.strip()


# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

class AsyncIter:    
    def __init__(self, items):    
        self.items = items    

    async def __aiter__(self):    
        for item in self.items:    
            yield item  


# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================
