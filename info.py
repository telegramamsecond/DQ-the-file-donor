import re
from os import environ
from Script import script 

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

# Bot information
SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(environ['API_ID'])
API_HASH = environ['API_HASH']
BOT_TOKEN = environ['BOT_TOKEN']

# Bot settings
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', True))

PICS = (environ.get('PICS', 'https://telegra.ph/file/9075ca7cbad944afaa823.jpg https://telegra.ph/file/9688c892ad2f2cf5c3f68.jpg https://telegra.ph/file/51683050f583af4c81013.jpg')).split()
NOR_IMG = environ.get("NOR_IMG", "https://telegra.ph/file/46443096bc6895c74a716.jpg")
MELCOW_VID = environ.get("MELCOW_VID", "https://telegra.ph/file/451f038b4e7c2ddd10dc0.mp4")
SPELL_IMG = environ.get("SPELL_IMG", "https://telegra.ph/file/5e2d4418525832bc9a1b9.jpg")

# Admins, Channels & Users
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '732556620').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '-1001526485271').split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = environ.get('AUTH_CHANNEL')
auth_grp = environ.get('AUTH_GROUP')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
AUTH_GROUPS = [int(ch) for ch in auth_grp.split()] if auth_grp else None
support_chat_id = environ.get('SUPPORT_CHAT_ID', '-1002606640247')
reqst_channel = environ.get('REQST_CHANNEL_ID', '-1002606640247')
REQST_CHANNEL = int(reqst_channel) if reqst_channel and id_pattern.search(reqst_channel) else None
SUPPORT_CHAT_ID = int(support_chat_id) if support_chat_id and id_pattern.search(support_chat_id) else None
NO_RESULTS_MSG = bool(environ.get("NO_RESULTS_MSG", False))

# MongoDB information
DATABASE_URI = environ.get('DATABASE_URI', "")
DATABASE_NAME = environ.get('DATABASE_NAME', "cluster0")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')

# Others
DELETE_CHANNELS = [int(dch) if id_pattern.search(dch) else dch for dch in environ.get('DELETE_CHANNELS', '-1001529899497').split()]
MAX_B_TN = environ.get("MAX_B_TN", "5")
MAX_BTN = is_enabled((environ.get('MAX_BTN', "True")), True)
GRP_LNK = environ.get('GRP_LNK', 'https://t.me/+eDjzTT2Ua6kwMTI1')
CHNL_LNK = environ.get('CHNL_LNK', 'https://t.me/+R9zxAI4mCkk0NzVl')
PORT = environ.get("PORT", "8080")
MSG_ALRT = environ.get('MSG_ALRT', 'Wʜᴀᴛ Aʀᴇ Yᴏᴜ Lᴏᴏᴋɪɴɢ Aᴛ ?')
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1001529899497'))
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'DQ_The_File_Donor_Support')
P_TTI_SHOW_OFF = is_enabled((environ.get('P_TTI_SHOW_OFF', "False")), False)
IMDB = is_enabled((environ.get('IMDB', "True")), True)
AUTO_FFILTER = is_enabled((environ.get('AUTO_FFILTER', "True")), True)
AUTO_DELETE = is_enabled((environ.get('AUTO_DELETE', "True")), True)
SINGLE_BUTTON = is_enabled((environ.get('SINGLE_BUTTON', "True")), True)
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", f"{script.CAPTION}")
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", CUSTOM_FILE_CAPTION)
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", f"{script.IMDB_TEMPLATE_TXT}")
LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "False"), False)
SPELL_CHECK_REPLY = is_enabled(environ.get("SPELL_CHECK_REPLY", "True"), True)
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))
FILE_STORE_CHANNEL = [int(ch) for ch in (environ.get('FILE_STORE_CHANNEL', '-1001529899497')).split()]
MELCOW_NEW_USERS = is_enabled((environ.get('MELCOW_NEW_USERS', "True")), True)
PROTECT_CONTENT = is_enabled((environ.get('PROTECT_CONTENT', "False")), False)
PUBLIC_FILE_STORE = is_enabled((environ.get('PUBLIC_FILE_STORE', "True")), True)

INMAL = """താങ്കൾ ആവശ്യപ്പെട്ട ഫയൽ എനിക്ക് കണ്ടെത്താനായില്ല 😕
താഴെ പറയുന്ന കാര്യങ്ങളിൽ ശ്രദ്ധിക്കുക...

=> കറക്റ്റ് സ്പെല്ലിംഗിൽ ചോദിക്കുക.

=> ഒ.ടി.ടി പ്ലാറ്റ്ഫോമുകളിൽ റിലീസ് ആകാത്ത സിനിമകൾ ചോദിക്കരുത് 
<blockquote>ott റിലീസ് ആയതാണ് എങ്കിൽ താഴെയുള്ള റിപ്പോർട്ട് അഡ്മിൻ എന്ന ബട്ടൺ ക്ലിക്ക് ചെയ്തു റിപ്പോർട്ട് ചെയ്യുക.</blockquote>
=> കഴിവതും [സിനിമയുടെ പേര്, വർഷം] ഈ രീതിയിൽ ചോദിക്കുക.

=> സ്പെല്ലിങ്ങ് അറിയാൻ സെർച്ച് ചെയ്യാനായി താഴെ കാണുന്ന ബട്ടൺ ഉപയോഗിക്കാം 😌 [𝖒𝖔𝖗𝖊 𝖎𝖓𝖋𝖔](https://telegra.ph/Group-rules-11-24)"""

INTAM = """நீங்கள் கோரிய கோப்பை என்னால் கண்டுபிடிக்க முடியவில்லை 😕
பின்வருவனவற்றை செய்ய முயற்சிக்கவும்...

=> சரியான எழுத்துப்பிழையுடன் கோரிக்கை

=> OTT இயங்குதளங்களில் வெளியிடப்படாத திரைப்படங்களைக் கேட்க வேண்டாம்
<blockquote>If ott has been released, click the Report Admin button below and report it.</blockquote>
=> [MovieName, year] இந்த வடிவமைப்பில் கேட்க முயற்சிக்கவும்.

=> Google இல் தேட கீழே உள்ள பொத்தானைப் பயன்படுத்தவும் 😌"""

INHIN = """मुझे आपके द्वारा अनुरोधित फ़ाइल नहीं मिली 😕
निम्नलिखित करने का प्रयास करें...

=> सही वर्तनी के साथ अनुरोध

=> उन फिल्मों के बारे में न पूछें जो ओटीटी प्लेटफॉर्म पर रिलीज नहीं हुई हैं
<blockquote>If ott has been released, click the Report Admin button below and report it.</blockquote>
=> इस प्रारूप में [MovieName, year] में पूछने का प्रयास करें।

=> Google पर खोजने के लिए नीचे दिए गए बटन का प्रयोग करें 😌"""

INENG = """I couldn't find the file you requested 😕
Try to do the following...

=> Request with correct spelling

=> Don't ask movies that are not released in OTT platforms
<blockquote>If ott has been released, click the Report Admin button below and report it.</blockquote>
=> Try to ask in [MovieName, year] this format.

=> Use the button below to search on Google 😌"""
SEEP = """📍 If the web series / TV series is requested
Season 5 if you will
Example = (Name) (S05)
Example = DARK S05

If you want this episode
Example = (Name) S05E02
Example = Dark S01E04"""

LOG_STR = "Current Cusomized Configurations are:-\n"
LOG_STR += ("IMDB Results are enabled, Bot will be showing imdb details for you queries.\n" if IMDB else "IMBD Results are disabled.\n")
LOG_STR += ("P_TTI_SHOW_OFF found , Users will be redirected to send /start to Bot PM instead of sending file file directly\n" if P_TTI_SHOW_OFF else "P_TTI_SHOW_OFF is disabled files will be send in PM, instead of sending start.\n")
LOG_STR += ("SINGLE_BUTTON is Found, filename and files size will be shown in a single button instead of two separate buttons\n" if SINGLE_BUTTON else "SINGLE_BUTTON is disabled , filename and file_sixe will be shown as different buttons\n")
LOG_STR += (f"CUSTOM_FILE_CAPTION enabled with value {CUSTOM_FILE_CAPTION}, your files will be send along with this customized caption.\n" if CUSTOM_FILE_CAPTION else "No CUSTOM_FILE_CAPTION Found, Default captions of file will be used.\n")
LOG_STR += ("Long IMDB storyline enabled." if LONG_IMDB_DESCRIPTION else "LONG_IMDB_DESCRIPTION is disabled , Plot will be shorter.\n")
LOG_STR += ("Spell Check Mode Is Enabled, bot will be suggesting related movies if movie not found\n" if SPELL_CHECK_REPLY else "SPELL_CHECK_REPLY Mode disabled\n")
LOG_STR += (f"MAX_LIST_ELM Found, long list will be shortened to first {MAX_LIST_ELM} elements\n" if MAX_LIST_ELM else "Full List of casts and crew will be shown in imdb template, restrict them by adding a value to MAX_LIST_ELM\n")
LOG_STR += f"Your current IMDB template is {IMDB_TEMPLATE}"
