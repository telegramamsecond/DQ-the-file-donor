# Kanged From @TroJanZheX
import asyncio
import re
import ast
import math
import random
import time

from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Script import script
import pyrogram
from database.connections_mdb import active_connection, all_connections, delete_connection, if_active, make_active, \
    make_inactive
from info import ADMINS, AUTH_CHANNEL, AUTH_USERS, SUPPORT_CHAT_ID, CUSTOM_FILE_CAPTION, MSG_ALRT, PICS, AUTH_GROUPS, P_TTI_SHOW_OFF, GRP_LNK, CHNL_LNK, NOR_IMG, LOG_CHANNEL, SPELL_IMG, MAX_B_TN, IMDB, \
    SINGLE_BUTTON, SPELL_CHECK_REPLY, IMDB_TEMPLATE, NO_RESULTS_MSG, INMAL, INTAM, INHIN, INENG, SEEP
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply, CallbackQuery, InputMediaPhoto
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid, ListenerTimeout
from utils import get_size, is_subscribed, get_poster, search_gagala, temp, get_settings, save_group_settings
from database.users_chats_db import db
from database.ia_filterdb import Media, get_file_details, get_search_results, get_bad_files
from database.filters_mdb import (
    del_all,
    find_filter,
    get_filters,
)
from database.gfilters_mdb import (
    find_gfilter,
    get_gfilters,
    del_allg
)
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
MYRE = ["CAADBQAD2AMAAvjDaFSsTHfTpJDaShYE", "CAACAgUAAyEFAASbXix3AAPvaON_uhWTWNjvKUG715WbMrFBCMMAAmEDAALutVlWDVTw_ueui9YeBA", "CAACAgUAAyEFAASbXix3AAPsaON_pO3qu4TrOL_4mkKbSdnQQoMAAkoLAAKD1lhUGp0Vhdd8A0UeBA", "CAACAgUAAyEFAASbXix3AAPbaON_IXVmPTbJ4u5sUvDzr3zxhR8AAlsNAAIxkVlUUD-nRyfRZoAeBA", "CAACAgUAAyEFAASbXix3AAPdaON_JchnDRUzsJasPq8ub3wvrn4AAjsKAAIDYllU5m3DiHYZdg8eBA", "CAACAgUAAyEFAASbXix3AAPeaON_NF3iECQZ6QV4V4IFPVURP0EAAoYLAAKJyVhUSmI-aQQUsbAeBA", "CAACAgUAAyEFAASbXix3AAPgaON_Rg-yZEMwddIJGut7t0ut1x4AArwJAALUlllUK4QSuWIpAAE0HgQ", "CAACAgUAAyEFAASbXix3AAPhaON_U4dhoTqnV9sN9KC4vEuxNPwAAlkLAALsflhUhi4MtxorquYeBA", "CAADBQADDQMAAtC6kVRSm-hyq9LjMRYE", "CAADBQADowEAAsuvXSk7LlkDJBYrnRYE", "CAADBQADAQcAAljMOFdOolwetNErQxYE", "CAADBQADeAMAArLJgFRXeMmuvdTQchYE", "CAADBQADsAMAAgYG8VSFaQgU6X596BYE", "CAADBQAD6AMAAi8MwVS1_PRa7JTUWxYE", "CAADBQADOgIAAnRfsFRgDjrWSQK3kxYE", "CAADBQADRAQAAlaVaVSKDdtGH1UJKhYE", ]

BUTTONS = {}
BUT = {}
SPELL_CHECK = {}
RESEND = {}
RAT = ["🍫", "🍟", "🍓", "🎈", "🍹", "🌻", "🍭", "🍿", "🪁", "🗼", "📮", "🎬", "🧯",]
PHOTT = ["https://telegra.ph/file/9075ca7cbad944afaa823.jpg", "https://telegra.ph/file/9688c892ad2f2cf5c3f68.jpg", "https://telegra.ph/file/51683050f583af4c81013.jpg",]


@Client.on_message(filters.group & filters.text & filters.incoming)
async def give_filter(client, message):
    search = message.text.strip()
    y = search.split()
    x = "_".join(y)
    sesna = x.lower()
    
    try:
        nyva = BUT[sesna]
    except:
        pass
    else:
        cap = f"<b>Hᴇʏ 🙌{message.from_user.mention}, Hᴇʀᴇ ɪs Wʜᴀᴛ I Fᴏᴜɴᴅ Iɴ Mʏ Dᴀᴛᴀʙᴀsᴇ Fᴏʀ Yᴏᴜʀ Qᴜᴇʀʏ {search}.</b>"
        try:
            btn = nyva['buttons']
        except:
            BUT.pop(f"{sesna}")
        else:
            fuk = await message.reply_text(text=cap, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)
            files, offset, total_results = await get_search_results(message.chat.id, search.lower(), offset=0, filter=True)
            if int(total_results) != int(nyva['total']):
                BUT.pop(f"{sesna}")
            await manual_filters(client, message)
            try:
                count = RESEND.get(f"{sesna}")
            except:
                pass
            else:
                new = int(count) + 1
                RESEND.pop(f"{sesna}")
                RESEND[sesna] = int(f"{new}")
            settings = await get_settings(message.chat.id)
            try:
                if settings['auto_delete']:
                    await asyncio.sleep(300)
                    await fuk.delete()
                    try:
                        await message.delete()
                    except:
                        pass
                    return
            except KeyError:
                grpid = await active_connection(str(message.from_user.id))
                await save_group_settings(grpid, 'auto_delete', True)
                settings = await get_settings(message.chat.id)
                if settings['auto_delete']:
                    await asyncio.sleep(300)
                    await fuk.delete()
                    try:
                        await message.delete()
                    except:
                        pass
                    return
    manual = await manual_filters(client, message)
    if manual == False:
        await auto_filter(client, message)

@Client.on_message(filters.private & filters.text & filters.incoming)
async def pm_text(bot, message):
    user = message.from_user.first_name 
    content = message.text
    user_id = message.from_user.id
    if content.startswith("/") or content.startswith("#"): return  # ignore commands and hashtags
    if user_id in ADMINS: return # ignore admins
    
    """await message.reply_text("<b>Yᴏᴜʀ ᴍᴇssᴀɢᴇ ʜᴀs ʙᴇᴇɴ sᴇɴᴛ ᴛᴏ ᴍʏ ᴍᴏᴅᴇʀᴀᴛᴏʀs !</b>")
    await bot.send_message(
        chat_id=LOG_CHANNEL,
        text=f"<b>#𝐏𝐌_𝐌𝐒𝐆\n\nNᴀᴍᴇ : {user}\n\nID : {user_id}\n\nMᴇssᴀɢᴇ : {content}</b>"
    )"""

@Client.on_callback_query(filters.regex(r"^hhnext"))
async def next_page(bot, query):
    ident, req, key, offset = query.data.split("_")
    clicked = query.from_user.id
    if clicked in ADMINS: 
        typed = query.from_user.id
    else:
        try:
            typed = query.message.reply_to_message.from_user.id
        except:
            typed = query.from_user.id
    if clicked != typed:
        return await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    try:
        offset = int(offset)
    except:
        offset = 0
    search = BUTTONS.get(key)
    if not search:
        await query.answer(script.OLD_ALRT_TXT.format(query.from_user.first_name),show_alert=True)
        return
    files, n_offset, total = await get_search_results(query.message.chat.id, search, offset=offset, filter=True)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    if not files:
        return
    try:
        oam = f"{random.choice(RAT)}"
        oamm = f"{random.choice(RAT)}"
        btn = []
        for file in files:
            sz = get_size(file.file_size)
            tt = file.file_name.title().lstrip()
            fg = re.sub(r"(_|\-|\.|\#|\B@\w+|\[.*?\]|\+)", " ", tt, flags=re.IGNORECASE)
            try:
                fn = fg.replace("  ", " ")
            except:
                fn = fg
            if fn == "None":
                fn = re.sub(r"(#|\B@\w+|\[.*?\]|mkv|mp4|avi|https?://\S+|www\.\S+|srt|\~|\©|\_|\.)", " ", file.caption, flags=re.IGNORECASE).strip()
            filenaame = f"{oam}{sz[0:3]} {sz[-2:]}{oamm}{fn}"
            btn.append([InlineKeyboardButton(text=f"{filenaame}",callback_data=f'files#{file.file_id}')])
    except:
        await query.answer(script.OLD_ALRT_TXT.format(query.from_user.first_name),show_alert=True)
        return
        
    try:
        settings = await get_settings(query.message.chat.id)
        if settings['max_btn']:
            if 0 < offset <= 10:
                off_set = 0
            elif offset == 0:
                off_set = None
            else:
                off_set = offset - 10
            if n_offset == 0:
                btn.append(
                    [InlineKeyboardButton("⇍ʙᴀᴄᴋ", callback_data=f"next_{req}_{key}_{off_set}"), InlineKeyboardButton(f"🎪{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}🎪", callback_data="pages"), InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data="instr_close")]                                                                                                    
                )
            elif off_set is None:
                btn.append([InlineKeyboardButton("ᴩᴀɢᴇ", callback_data="pages"), InlineKeyboardButton(f"🎪{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}🎪", callback_data="pages"), InlineKeyboardButton("⇏ɴᴇxᴛ⇏", callback_data=f"next_{req}_{key}_{n_offset}")])
            else:
                btn.append(
                    [
                        InlineKeyboardButton("⇍ʙᴀᴄᴋ", callback_data=f"next_{req}_{key}_{off_set}"),
                        InlineKeyboardButton(f"🎪{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}🎪", callback_data="pages"),
                        InlineKeyboardButton("⇏ɴᴇxᴛ⇏", callback_data=f"next_{req}_{key}_{n_offset}")
                    ],
                )
        else:
            if 0 < offset <= int(MAX_B_TN):
                off_set = 0
            elif offset == 0:
                off_set = None
            else:
                off_set = offset - int(MAX_B_TN)
            if n_offset == 0:
                btn.append(
                    [InlineKeyboardButton("⇍ʙᴀᴄᴋ", callback_data=f"next_{req}_{key}_{off_set}"), InlineKeyboardButton(f"{math.ceil(int(offset)/int(MAX_B_TN))+1} / {math.ceil(total/int(MAX_B_TN))}", callback_data="pages"), InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data="instr_close")]
                )
            elif off_set is None:
                btn.append([InlineKeyboardButton("ᴩᴀɢᴇ", callback_data="pages"), InlineKeyboardButton(f"{math.ceil(int(offset)/int(MAX_B_TN))+1} / {math.ceil(total/int(MAX_B_TN))}", callback_data="pages"), InlineKeyboardButton("⇏ɴᴇxᴛ⇏", callback_data=f"next_{req}_{key}_{n_offset}")])
            else:
                btn.append(
                    [
                        InlineKeyboardButton("⇍ʙᴀᴄᴋ", callback_data=f"next_{req}_{key}_{off_set}"),
                        InlineKeyboardButton(f"{math.ceil(int(offset)/int(MAX_B_TN))+1} / {math.ceil(total/int(MAX_B_TN))}", callback_data="pages"),
                        InlineKeyboardButton("⇏ɴᴇxᴛ⇏", callback_data=f"next_{req}_{key}_{n_offset}")
                    ],
                )
    except KeyError:
        await save_group_settings(query.message.chat.id, 'max_btn', False)
        settings = await get_settings(query.message.chat.id)
        if settings['max_btn']:
            if 0 < offset <= 10:
                off_set = 0
            elif offset == 0:
                off_set = None
            else:
                off_set = offset - 10
            if n_offset == 0:
                btn.append(
                    [InlineKeyboardButton("⌫ 𝐁𝐀𝐂𝐊", callback_data=f"next_{req}_{key}_{off_set}"), InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages")]
                )
            elif off_set is None:
                btn.append([InlineKeyboardButton("𝐏𝐀𝐆𝐄", callback_data="pages"), InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages"), InlineKeyboardButton("𝐍𝐄𝐗𝐓 ➪", callback_data=f"next_{req}_{key}_{n_offset}"), InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data="instr_close")])
            else:
                btn.append(
                    [
                        InlineKeyboardButton("⌫ 𝐁𝐀𝐂𝐊", callback_data=f"next_{req}_{key}_{off_set}"),
                        InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages"),
                        InlineKeyboardButton("𝐍𝐄𝐗𝐓 ➪", callback_data=f"next_{req}_{key}_{n_offset}")
                    ],
                )
        else:
            if 0 < offset <= int(MAX_B_TN):
                off_set = 0
            elif offset == 0:
                off_set = None
            else:
                off_set = offset - int(MAX_B_TN)
            if n_offset == 0:
                btn.append(
                    [InlineKeyboardButton("⇍ʙᴀᴄᴋ", callback_data=f"next_{req}_{key}_{off_set}"), InlineKeyboardButton(f"{math.ceil(int(offset)/int(MAX_B_TN))+1} / {math.ceil(total/int(MAX_B_TN))}", callback_data="pages"), InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data="instr_close")]
                )
            elif off_set is None:
                btn.append([InlineKeyboardButton("ᴩᴀɢᴇ", callback_data="pages"), InlineKeyboardButton(f"{math.ceil(int(offset)/int(MAX_B_TN))+1} / {math.ceil(total/int(MAX_B_TN))}", callback_data="pages"), InlineKeyboardButton("𝐍𝐄𝐗𝐓 ➪", callback_data=f"next_{req}_{key}_{n_offset}")])
            else:
                btn.append(
                    [
                        InlineKeyboardButton("⇍ʙᴀᴄᴋ", callback_data=f"next_{req}_{key}_{off_set}"),
                        InlineKeyboardButton(f"🎪{math.ceil(int(offset)/int(MAX_B_TN))+1} / {math.ceil(total/int(MAX_B_TN))}🎪", callback_data="pages"),
                        InlineKeyboardButton("⇏ɴᴇxᴛ⇏", callback_data=f"next_{req}_{key}_{n_offset}")
                    ],
                )
    btn.insert(0, [
        InlineKeyboardButton("⚡ Cʜᴇᴄᴋ Bᴏᴛ PM ⚡", url=f"https://t.me/{temp.U_NAME}")
    ])
    try:
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(btn)
        )
    except MessageNotModified:
        pass
    return


@Client.on_callback_query(filters.regex(r"^spol"))
async def advantage_spoll_choker(bot, query):
    _, user, movie_ = query.data.split('#')
    movies = SPELL_CHECK.get(query.message.reply_to_message.id)
    if not movies:
        return await query.answer(script.OLD_ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    if int(user) != 0 and query.from_user.id != int(user):
        userid = query.from_user.id if query.from_user else None
        if int(userid) not in ADMINS:  
            return await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    await query.answer("𝚙𝚛𝚘𝚌𝚎𝚜𝚜𝚒𝚗𝚐........") 
    if movie_ == "close_spellcheck":
        return await query.message.delete()
    movie = movies[(int(movie_))]
    d = await query.message.edit(script.TOP_ALRT_MSG)
    k = await manual_filters(bot, query.message, text=movie)
    if k == False:
        files, offset, total_results = await get_search_results(query.message.chat.id, movie, offset=0, filter=True)
        if files:
            k = (movie, files, offset, total_results)
            await d.delete()
            await auto_filter(bot, query, k)
        else:
            reqstr1 = query.from_user.id if query.from_user else 0
            reqstr = await bot.get_users(reqstr1)
            kuttons = []
            kuttons.append(
                [InlineKeyboardButton(text="ᴍᴀʟ", callback_data="instr_mal"), InlineKeyboardButton(text="ᴛᴀᴍ", callback_data="instr_tam"), InlineKeyboardButton(text="ʜɪɴ", callback_data="instr_hin"), InlineKeyboardButton(text="ᴇɴɢ", callback_data="instr_eng")]
            )
            kuttons.append(
                [InlineKeyboardButton(text="ᴄʟᴏꜱᴇ", callback_data="instr_close")]
            )
            reply_markup = InlineKeyboardMarkup(kuttons)
            if not query.from_user:
                return await d.delete()
            await d.edit_text(f"{movie}\n\n <b>I couldn't find anything related to your request. 🤧Try reading the instructions below 👇</b>", reply_markup=reply_markup)
            return
            


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    byttons = [
        [
            InlineKeyboardButton(text="ᴀʙᴏᴜᴛ 💡",callback_data="about"),
            InlineKeyboardButton(text="ʜᴇʟᴩ ⛑️",callback_data="helpppl")
        ],
        [
            InlineKeyboardButton(text="ʀᴇᴄᴇɴᴛ 📚",callback_data="recent"),
            InlineKeyboardButton("ᴄʜᴀɴɴᴇʟ 🍿", url="https://t.me/+R9zxAI4mCkk0NzVl")   
        ],
        [
            InlineKeyboardButton("ɢʀᴏᴜᴩ 1 🎪", url="https://t.me/+PBGW_EV3ldY5YjJl"),
            InlineKeyboardButton("ɢʀᴏᴜᴩ 2 🎪", url="https://t.me/+eDjzTT2Ua6kwMTI1")   
        ],
        [
            InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘs ➕", url=f"http://t.me/{temp.U_NAME}?startgroup=true")   
        ]
    ]
    if query.data == "close_data":
        await query.message.delete()
    elif query.data == "gfiltersdeleteallconfirm":
        await del_allg(query.message, 'gfilters')
        await query.answer("Done !")
        return
    elif query.data == "gfiltersdeleteallcancel": 
        await query.message.reply_to_message.delete()
        await query.message.delete()
        await query.answer("Process Cancelled !")
        return
    elif query.data == "delallconfirm":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            grpid = await active_connection(str(userid))
            if grpid is not None:
                grp_id = grpid
                try:
                    chat = await client.get_chat(grpid)
                    title = chat.title
                except:
                    await query.message.edit_text("Mᴀᴋᴇ sᴜʀᴇ I'ᴍ ᴘʀᴇsᴇɴᴛ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ!!", quote=True)
                    return await query.answer(MSG_ALRT)
            else:
                await query.message.edit_text(
                    "I'ᴍ ɴᴏᴛ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ ᴀɴʏ ɢʀᴏᴜᴘs!\nCʜᴇᴄᴋ /connections ᴏʀ ᴄᴏɴɴᴇᴄᴛ ᴛᴏ ᴀɴʏ ɢʀᴏᴜᴘs",
                    quote=True
                )
                return await query.answer(MSG_ALRT)

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            title = query.message.chat.title

        else:
            return await query.answer(MSG_ALRT)

        st = await client.get_chat_member(grp_id, userid)
        if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
            await del_all(query.message, grp_id, title)
        else:
            await query.answer("Yᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴇ Gʀᴏᴜᴘ Oᴡɴᴇʀ ᴏʀ ᴀɴ Aᴜᴛʜ Usᴇʀ ᴛᴏ ᴅᴏ ᴛʜᴀᴛ!", show_alert=True)
    elif query.data == "delallcancel":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            await query.message.reply_to_message.delete()
            await query.message.delete()

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            st = await client.get_chat_member(grp_id, userid)
            if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
                await query.message.delete()
                try:
                    await query.message.reply_to_message.delete()
                except:
                    pass
            else:
                await query.answer("Tʜᴀᴛ's ɴᴏᴛ ғᴏʀ ʏᴏᴜ!!", show_alert=True)
    elif "groupcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        act = query.data.split(":")[2]
        hr = await client.get_chat(int(group_id))
        title = hr.title
        user_id = query.from_user.id

        if act == "":
            stat = "CONNECT"
            cb = "connectcb"
        else:
            stat = "DISCONNECT"
            cb = "disconnect"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{stat}", callback_data=f"{cb}:{group_id}"),
             InlineKeyboardButton("DELETE", callback_data=f"deletecb:{group_id}")],
            [InlineKeyboardButton("BACK", callback_data="backcb")]
        ])

        await query.message.edit_text(
            f"Gʀᴏᴜᴘ Nᴀᴍᴇ : **{title}**\nGʀᴏᴜᴘ ID : `{group_id}`",
            reply_markup=keyboard,
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return await query.answer(MSG_ALRT)
    elif "connectcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title

        user_id = query.from_user.id

        mkact = await make_active(str(user_id), str(group_id))

        if mkact:
            await query.message.edit_text(
                f"Cᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ **{title}**",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await query.message.edit_text('Sᴏᴍᴇ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ!!', parse_mode=enums.ParseMode.MARKDOWN)
        return await query.answer(MSG_ALRT)
    elif "disconnect" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title
        user_id = query.from_user.id

        mkinact = await make_inactive(str(user_id))

        if mkinact:
            await query.message.edit_text(
                f"Dɪsᴄᴏɴɴᴇᴄᴛᴇᴅ ғʀᴏᴍ **{title}**",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await query.message.edit_text(
                f"Sᴏᴍᴇ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ!!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        return await query.answer(MSG_ALRT)
    elif "deletecb" in query.data:
        await query.answer()

        user_id = query.from_user.id
        group_id = query.data.split(":")[1]

        delcon = await delete_connection(str(user_id), str(group_id))

        if delcon:
            await query.message.edit_text(
                "Sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ᴄᴏɴɴᴇᴄᴛɪᴏɴ !"
            )
        else:
            await query.message.edit_text(
                f"Sᴏᴍᴇ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ!!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        return await query.answer(MSG_ALRT)
    elif query.data == "backcb":
        await query.answer()

        userid = query.from_user.id

        groupids = await all_connections(str(userid))
        if groupids is None:
            await query.message.edit_text(
                "Tʜᴇʀᴇ ᴀʀᴇ ɴᴏ ᴀᴄᴛɪᴠᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴs!! Cᴏɴɴᴇᴄᴛ ᴛᴏ sᴏᴍᴇ ɢʀᴏᴜᴘs ғɪʀsᴛ.",
            )
            return await query.answer(MSG_ALRT)
        buttons = []
        for groupid in groupids:
            try:
                ttl = await client.get_chat(int(groupid))
                title = ttl.title
                active = await if_active(str(userid), str(groupid))
                act = " - ACTIVE" if active else ""
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}"
                        )
                    ]
                )
            except:
                pass
        if buttons:
            await query.message.edit_text(
                "Yᴏᴜʀ ᴄᴏɴɴᴇᴄᴛᴇᴅ ɢʀᴏᴜᴘ ᴅᴇᴛᴀɪʟs ;\n\n",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
    elif "gfilteralert" in query.data:
        grp_id = query.message.chat.id
        i = query.data.split(":")[1]
        keyword = query.data.split(":")[2]
        reply_text, btn, alerts, fileid = await find_gfilter('gfilters', keyword)
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await query.answer(alert, show_alert=True)
    elif "alertmessage" in query.data:
        grp_id = query.message.chat.id
        i = query.data.split(":")[1]
        keyword = query.data.split(":")[2]
        reply_text, btn, alerts, fileid = await find_filter(grp_id, keyword)
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await query.answer(alert, show_alert=True)
    
    clicked = query.from_user.id
    if clicked in ADMINS: 
        typed = query.from_user.id
    else:
        try:
            typed = query.message.reply_to_message.from_user.id
        except:
            typed = query.from_user.id
            
    if query.data.startswith("file"):      
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('Nᴏ sᴜᴄʜ ғɪʟᴇ ᴇxɪsᴛ.')
        files = files_[0]
        title = re.sub(r"(#|\B@\w+|\~|\©|\-|\_|\.|\@)", " ", files.file_name, flags=re.IGNORECASE).strip()
        target_emoji = "🔞"
        if target_emoji in title:
            ident = "filep"
        chat_type = query.message.chat.type
        if chat_type == enums.ChatType.PRIVATE:
            await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
            return
        
        size = get_size(files.file_size)
        if title == "None":
            try:
                title = re.sub(r"(#|\B@\w+|\[.*?\]|https?://\S+|www\.\S+|\~|\©|\_|\.|\@)", " ", files.caption, flags=re.IGNORECASE).strip()
            except:
                title = "None"
                await client.send_cached_media(chat_id=LOG_CHANNEL, file_id=file_id, caption="check the file")
        try:
            title2 = re.sub(r"(#|\B@\w+|mkv|mp4|avi|srt|\~|\©|\_|\.|\@)", " ", files.caption, flags=re.IGNORECASE).strip()
        except:
            title2 = "None"
        short_to_full_map = {'tam': 'tamil', 'tel': 'telugu', 'hin': 'hindi', 'eng': 'english', 'multi': 'multi-audio✅', 'mal': 'malayalam'}
        for old_word, new_word in short_to_full_map.items():
            titfle = title.replace(old_word, new_word)
        chk = f"{titfle} {title2}".lower()
        language = re.findall(r"\b(arabic|english|hindi|tamil|telugu|assamese|bengali|gujarati|kannada|kashmiri|konkani|malayalam|manipuri|marathi|nepali|odia|punjabi|sanskrit|santali|sindhi|chinese|spanish|russian|urdu|indonesian|german|japanese|korean|french|italian|polish|portuguese|catalan|czech|danish|greek|basque|filipino|finnish|galician|hebrew|croatian|hungarian|malay|norwegian|bokmål|dutch|romanian|swedish|thai|turkish|ukrainian|vietnamese)\b", chk, re.IGNORECASE)
        if language:
            myrlist = list(dict.fromkeys(language))
            ress = ', '.join(myrlist)
            resss = ress.title()
            language = f"<b>\n🔊 Audio : {resss}</b>"
        resolutions = re.findall(r"\b(144p|240p|360p|540p|1440p|480p|720p|1080p|2160p)\b", chk, re.IGNORECASE)
        if resolutions:
            mylist = list(dict.fromkeys(resolutions))
            res = ' '.join(mylist)
            try:
                title = title.replace(res, "")
            except:
                pass
            mach = "hevc"
            if mach in chk:
                resolutions = f"<b>\n🎥Quality : {res} [ʜᴇᴠᴄ💡]</b>"
            else:
                resolutions = f"<b>\n🎥Quality : {res}</b>"
        duration = re.findall(r"\b(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d\b|\s\dh\d.*m\d.*s\s|\dh\d.*m\s", chk, re.IGNORECASE)
        if duration:
            myylist = list(dict.fromkeys(duration))
            rees = ' '.join(myylist)
            duration = f"<b>\n⏳ : {rees}</b>".title()
        sub = re.findall(r"\b(\be.?sub|eng.?sub|english.?sub|malayalam.?sub|multi.?sub|\bm.?sub|hin.?sub|japanese.?subs|hindi.?sub|\bmal.?sub)\b", chk, re.IGNORECASE)
        if sub:
            sub = sub[0].replace(" ", "")
            short_too_full_map = {'esub': 'english sub', 'malsub': 'malayalam sub', 'msub': 'malayalam sub', 'hin': 'hindi', 'eng': 'english', 'multi': 'multiple', 'mal': 'malayalam'}
            for old_worrd, new_worrd in short_too_full_map.items():
                if sub == old_worrd:
                    sub = sub.replace(old_worrd, new_worrd) 
            sub = f"<b>\n{sub[:-3]} subtitle✅</b>".title()
        settings = await get_settings(query.message.chat.id)
        f_caption = f"<blockquote><b>#𝙵𝙸𝙻𝙴_𝙽𝙰𝙼𝙴⇛</b><code>{title}</code>\n{f'{resolutions}' if resolutions else ''}{f'{duration}' if duration else ''}{f'{language}' if language else ''}{f'{sub}' if sub else ''}</blockquote>\n\n <b>ʙʏ⇛[ᴏɴᴀɪʀ_ғɪʟᴛᴇʀᵇᵒᵗ](https://t.me/On_air_Filter_bot)</b>"
        bettons = [[InlineKeyboardButton("ɢʀᴏᴜᴩ 1", url="https://t.me/+PBGW_EV3ldY5YjJl"), InlineKeyboardButton("ɢʀᴏᴜᴩ 2", url="https://t.me/+eDjzTT2Ua6kwMTI1")]]

        try:
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                if clicked == typed:
                    await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                    return
                else:
                    await query.answer(f"Hᴇʏ {query.from_user.first_name}, Tʜɪs Is Nᴏᴛ Yᴏᴜʀ Mᴏᴠɪᴇ Rᴇǫᴜᴇsᴛ. Rᴇǫᴜᴇsᴛ Yᴏᴜʀ's !", show_alert=True)
            elif settings['botpm']:
                if clicked == typed:
                    await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                    return
                else:
                    await query.answer(f"Hᴇʏ {query.from_user.first_name}, Tʜɪs Is Nᴏᴛ Yᴏᴜʀ Mᴏᴠɪᴇ Rᴇǫᴜᴇsᴛ. Rᴇǫᴜᴇsᴛ Yᴏᴜʀ's !", show_alert=True)
            else:
                if clicked == typed:
                    await client.send_cached_media(
                        chat_id=query.from_user.id,
                        file_id=file_id,
                        caption=f_caption,
                        reply_markup=InlineKeyboardMarkup(bettons),
                        protect_content=True if ident == "filep" else False
                    )
                else:
                    await query.answer(f"Hᴇʏ {query.from_user.first_name}, Tʜɪs Is Nᴏᴛ Yᴏᴜʀ Mᴏᴠɪᴇ Rᴇǫᴜᴇsᴛ. Rᴇǫᴜᴇsᴛ Yᴏᴜʀ's !", show_alert=True)
                await query.answer('Cʜᴇᴄᴋ PM, I ʜᴀᴠᴇ sᴇɴᴛ ғɪʟᴇs ɪɴ PM', show_alert=True)
        except UserIsBlocked:
            await query.answer('Uɴʙʟᴏᴄᴋ ᴛʜᴇ ʙᴏᴛ ᴍᴀʜɴ !', show_alert=True)
        except PeerIdInvalid:
            await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
        except Exception as e:
            await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
    elif query.data.startswith("instr"):
        ident, lang = query.data.split("_")
        if clicked != typed:
            await query.answer(f"Hᴇʏ {query.from_user.first_name}, Tʜɪs Is Nᴏᴛ Yᴏᴜʀ Mᴏᴠɪᴇ Rᴇǫᴜᴇsᴛ. Rᴇǫᴜᴇsᴛ Yᴏᴜʀ's !", show_alert=True)
            return
        if lang  == "close":
            await query.message.delete()
            try:
                await query.message.reply_to_message.delete()
            except:
                await query.answer("👀")
            return
        try:
            message = query.message.reply_to_message
        except:
            buttons = []
            await query.message.delete()
            return
            
        kuttons = []
        try:
            x = message.text.split()
        except:
            await query.message.delete()
            return
        else:
            hari = "+".join(x)
            kuttons.append(
                [InlineKeyboardButton(text=f"ɢᴏᴏɢʟᴇ 🍿", url=f"https://google.com/search?q={hari}"),InlineKeyboardButton(text=f"ᴏʀ ɪᴍᴅʙ 🍿", url=f"https://www.imdb.com/find?q={hari}")]
            )
            kuttons.append(
                [InlineKeyboardButton(text="ʀᴇᴩᴏʀᴛ ᴛᴏ ᴀᴅᴍɪɴ",callback_data=f"report_{hari}")]
            )
        reply_markup = InlineKeyboardMarkup(kuttons)
        if lang  == "mal":
            a = await query.message.edit_text(INMAL, disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)
        elif lang  == "tam":
            a = await query.message.edit_text(INTAM, disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)
        elif lang  == "hin":
            a = await query.message.edit_text(INHIN, disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)
        elif lang  == "eng":
            a = await query.message.edit_text(INENG, disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)
        try:
            await query.message.edit_reply_markup(reply_markup)
        except: 
            await a.delete()
        else:
            await asyncio.sleep(55)
            await a.delete()
        try:
            await message.delete()
        except:
            return
    elif query.data.startswith("report"):
        if clicked != typed:
            await query.answer(f"Hᴇʏ {query.from_user.first_name}, Tʜɪs Is Nᴏᴛ Yᴏᴜʀ Mᴏᴠɪᴇ Rᴇǫᴜᴇsᴛ. Rᴇǫᴜᴇsᴛ Yᴏᴜʀ's !", show_alert=True)
            return
        if query.message.reply_to_message:
            from_user = query.from_user.id if query.from_user else None
            btn = [[
                    InlineKeyboardButton("ɴᴏᴛ ❌", callback_data=f"onavailable#{from_user}"), InlineKeyboardButton("ꜰɪxᴇᴅ", callback_data=f"oploaded#{from_user}")
                  ]]
            try:
                await client.send_message(chat_id=LOG_CHANNEL,text=f"{query.message.reply_to_message.text}", reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True)
            except:
                await query.answer("𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈 Reported to Admins 👮‍♂",show_alert=True)
            else:
                await query.answer("𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈 Reported to Admins 👮‍♂ \n\n Thanks for your contribution",show_alert=True)
        return await query.message.delete()
    elif query.data.startswith("recent"):
        try:
            # nyva = RESEND.keys()
            nyva = sorted(RESEND.items(), key=lambda item: item[1])
        except Exception as e:
            await query.answer(f"some error occurred, try again {e}",show_alert=True)
            return await query.message.delete()
        else:
            oamm = f"{random.choice(RAT)}"
            btn = []
            for file, value in reversed(nyva):
                tt = file.title().lstrip()
                fn = re.sub(r"(_|\-|\.|\#|\@|\+)", " ", tt, flags=re.IGNORECASE)
                filenaame = f"{oamm} {fn}"
                btn.append([InlineKeyboardButton(text=f"{filenaame}",callback_data=f"pmx₹{file}")])
        try:
            ident, go = query.data.split("_")
        except:
            if len(btn) > 8:
                btn = btn[:8]  
                btn.append([InlineKeyboardButton('Hᴏᴍᴇ 🏠', callback_data='start'), InlineKeyboardButton('ɴᴇxᴛ ⇏', callback_data='recent_next')])
            else:
                btn.append([InlineKeyboardButton('Hᴏᴍᴇ 🏠', callback_data='start'), InlineKeyboardButton('Cʟᴏsᴇ', callback_data='instr_close')])
        else:
            if len(btn) > 8:
                btn = btn[8:18]  
                btn.append([InlineKeyboardButton('⇍ ʙᴀᴄᴋ', callback_data='recent'), InlineKeyboardButton('Cʟᴏsᴇ', callback_data='instr_close')])
            else:
                btn.append([InlineKeyboardButton('Hᴏᴍᴇ 🏠', callback_data='start'), InlineKeyboardButton('Cʟᴏsᴇ', callback_data='instr_close')])
        reply_markup = InlineKeyboardMarkup(btn)
        try:
            await query.message.edit_text(text="Select any recent file 👇", reply_markup=reply_markup, disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)
        except:
            try:
                await client.send_message(chat_id=query.from_user.id, text=script.START_TXT.format(query.from_user.mention, temp.U_NAME, temp.B_NAME), reply_markup=InlineKeyboardMarkup(byttons), disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)
            except:
                pass
        return 
                
    elif query.data.startswith("onavailable"):
        ident, from_user = query.data.split("#")
        btn = [[
                InlineKeyboardButton("⚠️ Uɴᴀᴠᴀɪʟᴀʙʟᴇ ⚠️", callback_data=f"unalert#{from_user}")
              ]]
        
        if query.from_user.id in ADMINS:
            user = await client.get_users(from_user)
            reply_markup = InlineKeyboardMarkup(btn)
            content = query.message.text
            await query.message.edit_text(f"<b><strike>{content}</strike></b>")
            await query.message.edit_reply_markup(reply_markup)
            await query.answer("Sᴇᴛ ᴛᴏ Uɴᴀᴠᴀɪʟᴀʙʟᴇ !")
            try:
                await client.send_message(chat_id=int(from_user), text=f"<b>Hᴇʏ {user.mention}, Your movie suggestion has been declined.Unfortunately, we’re unable to process this request at the moment. Thank you for understanding 🙏</b>")
            except UserIsBlocked:
                await client.send_message(chat_id=int(SUPPORT_CHAT_ID), text=f"<b>Hᴇʏ {user.id}, Sᴏʀʀʏ Yᴏᴜʀ ʀᴇᴏ̨ᴜᴇsᴛ ɪs ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ. Sᴏ ᴏᴜʀ ᴍᴏᴅᴇʀᴀᴛᴏʀs ᴄᴀɴ'ᴛ ᴜᴘʟᴏᴀᴅ ɪᴛ.\n\nNᴏᴛᴇ: Tʜɪs ᴍᴇssᴀɢᴇ ɪs sᴇɴᴛ ᴛᴏ ᴛʜɪs ɢʀᴏᴜᴘ ʙᴇᴄᴀᴜsᴇ ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ᴛʜᴇ ʙᴏᴛ. Tᴏ sᴇɴᴅ ᴛʜɪs ᴍᴇssᴀɢᴇ ᴛᴏ ʏᴏᴜʀ PM, Mᴜsᴛ ᴜɴʙʟᴏᴄᴋ ᴛʜᴇ ʙᴏᴛ.</b>", reply_markup=InlineKeyboardMarkup(btn))
        else:
            await query.answer("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ sᴜғғɪᴄɪᴀɴᴛ ʀɪɢᴛs ᴛᴏ ᴅᴏ ᴛʜɪs !", show_alert=True)
    elif query.data.startswith("oploaded"):
        ident, from_user = query.data.split("#")
        btn = [[
                InlineKeyboardButton("✅ Uᴘʟᴏᴀᴅᴇᴅ ✅", callback_data=f"upalert#{from_user}")
              ]]
        
        if query.from_user.id in ADMINS:
            user = await client.get_users(from_user)
            reply_markup = InlineKeyboardMarkup(btn)
            content = query.message.text
            await query.message.edit_text(f"<b><strike>{content}</strike></b>")
            await query.message.edit_reply_markup(reply_markup)
            await query.answer("movie Uᴘʟᴏᴀᴅᴇᴅ !")
            try:
                await client.send_message(chat_id=int(from_user), text=f"<b>Hᴇʏ {user.mention}, ✅ Your movie suggestion {content} has been uploaded.  Thank you for your contribution </b>")
            except UserIsBlocked:
                await client.send_message(chat_id=int(SUPPORT_CHAT_ID), text=f"<b>Hᴇʏ {user.id}, Yᴏᴜʀ ʀᴇᴏ̨ᴜᴇsᴛ ʜᴀs ʙᴇᴇɴ ᴜᴘʟᴏᴀᴅᴇᴅ ʙʏ ᴏᴜʀ ᴍᴏᴅᴇʀᴀᴛᴏʀs. Kɪɴᴅʟʏ sᴇᴀʀᴄʜ ᴀɢᴀɪɴ.\n\nNᴏᴛᴇ: Tʜɪs ᴍᴇssᴀɢᴇ ɪs sᴇɴᴛ ᴛᴏ ᴛʜɪs ɢʀᴏᴜᴘ ʙᴇᴄᴀᴜsᴇ ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ᴛʜᴇ ʙᴏᴛ. Tᴏ sᴇɴᴅ ᴛʜɪs ᴍᴇssᴀɢᴇ ᴛᴏ ʏᴏᴜʀ PM, Mᴜsᴛ ᴜɴʙʟᴏᴄᴋ ᴛʜᴇ ʙᴏᴛ.</b>", reply_markup=InlineKeyboardMarkup(btn))
        else:
            await query.answer("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ sᴜғғɪᴄɪᴀɴᴛ ʀɪɢᴛs ᴛᴏ ᴅᴏ ᴛʜɪs !", show_alert=True)
    elif query.data.startswith("checksub"):
        if AUTH_CHANNEL and not await is_subscribed(client, query):
            await query.answer("Jᴏɪɴ ᴏᴜʀ ɢʀᴏᴜᴩ ᴍᴀʜɴ! 😒", show_alert=True)
            return
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('Nᴏ sᴜᴄʜ ғɪʟᴇ ᴇxɪsᴛ.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)
            except Exception as e:
                logger.exception(e)
                f_caption = f_caption
        if f_caption is None:
            f_caption = f"{title}"
        await query.answer()
        await client.send_cached_media(
            chat_id=query.from_user.id,
            file_id=file_id,
            caption=f_caption,
            protect_content=True if ident == 'checksubp' else False
        )
        await query.message.delete()
    elif query.data == "pages":
        await query.answer("👀 ʟᴏᴏᴋ ᴀᴛ ɴᴇxᴛ ᴘᴀɢᴇ 🤓")

    elif query.data.startswith("pmx"):
        if clicked != typed:
            await query.answer(f"Hᴇʏ {query.from_user.first_name}, Tʜɪs Is Nᴏᴛ Yᴏᴜʀ Mᴏᴠɪᴇ Rᴇǫᴜᴇsᴛ. Rᴇǫᴜᴇsᴛ Yᴏᴜʀ's !", show_alert=True)
            return
        ident, search = query.data.split("₹")
        try:
            nyva = BUT[search]
        except:
            await query.answer("Nᴏ sᴜᴄʜ ғɪʟᴇ ᴇxɪsᴛ, try again 🛟", show_alert=True)
            return await query.message.delete()
        else:
            cap = f"<b>Hᴇʏ 🙌{query.from_user.mention}, Hᴇʀᴇ ɪs Wʜᴀᴛ I Fᴏᴜɴᴅ Iɴ Mʏ Dᴀᴛᴀʙᴀsᴇ</b>"
            try:
                btn = nyva['buttons']
            except:
                BUT.pop(f"{search}")
            else:
                fuk = await query.message.reply_photo(photo=f"{random.choice(PHOTT)}", caption=cap, reply_markup=InlineKeyboardMarkup(btn))
                await query.message.delete()
                await asyncio.sleep(300)
                await fuk.delete()
        return 
     
    elif query.data.startswith("opnsetgrp"):
        ident, grp_id = query.data.split("#")
        userid = query.from_user.id if query.from_user else None
        st = await client.get_chat_member(grp_id, userid)
        if (
                st.status != enums.ChatMemberStatus.ADMINISTRATOR
                and st.status != enums.ChatMemberStatus.OWNER
                and str(userid) not in ADMINS
        ):
            await query.answer("Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Tʜᴇ Rɪɢʜᴛs Tᴏ Dᴏ Tʜɪs !", show_alert=True)
            return
        title = query.message.chat.title
        settings = await get_settings(grp_id)
        if settings is not None:
            buttons = [
                [
                    InlineKeyboardButton('Fɪʟᴛᴇʀ Bᴜᴛᴛᴏɴ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Sɪɴɢʟᴇ' if settings["button"] else 'Dᴏᴜʙʟᴇ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Fɪʟᴇ Sᴇɴᴅ Mᴏᴅᴇ', callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Mᴀɴᴜᴀʟ Sᴛᴀʀᴛ' if settings["botpm"] else 'Aᴜᴛᴏ Sᴇɴᴅ',
                                         callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Pʀᴏᴛᴇᴄᴛ Cᴏɴᴛᴇɴᴛ',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["file_secure"] else '✘ Oғғ',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Iᴍᴅʙ', callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["imdb"] else '✘ Oғғ',
                                         callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Sᴘᴇʟʟ Cʜᴇᴄᴋ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["spell_check"] else '✘ Oғғ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Wᴇʟᴄᴏᴍᴇ Msɢ', callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["welcome"] else '✘ Oғғ',
                                         callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Aᴜᴛᴏ-Dᴇʟᴇᴛᴇ',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}'),
                    InlineKeyboardButton('10 Mɪɴs' if settings["auto_delete"] else '✘ Oғғ',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Aᴜᴛᴏ-Fɪʟᴛᴇʀ',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["auto_ffilter"] else '✘ Oғғ',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Mᴀx Bᴜᴛᴛᴏɴs',
                                         callback_data=f'setgs#max_btn#{settings["max_btn"]}#{str(grp_id)}'),
                    InlineKeyboardButton('10' if settings["max_btn"] else f'{MAX_B_TN}',
                                         callback_data=f'setgs#max_btn#{settings["max_btn"]}#{str(grp_id)}')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_text(
                text=f"<b>Cʜᴀɴɢᴇ Yᴏᴜʀ Sᴇᴛᴛɪɴɢs Fᴏʀ {title} As Yᴏᴜʀ Wɪsʜ ⚙</b>",
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML
            )
            await query.message.edit_reply_markup(reply_markup)
        
    elif query.data.startswith("opnsetpm"):
        ident, grp_id = query.data.split("#")
        userid = query.from_user.id if query.from_user else None
        st = await client.get_chat_member(grp_id, userid)
        if (
                st.status != enums.ChatMemberStatus.ADMINISTRATOR
                and st.status != enums.ChatMemberStatus.OWNER
                and str(userid) not in ADMINS
        ):
            await query.answer("Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Tʜᴇ Rɪɢʜᴛs Tᴏ Dᴏ Tʜɪs !", show_alert=True)
            return
        title = query.message.chat.title
        settings = await get_settings(grp_id)
        btn2 = [[
                 InlineKeyboardButton("Cʜᴇᴄᴋ PM", url=f"t.me/{temp.U_NAME}")
               ]]
        reply_markup = InlineKeyboardMarkup(btn2)
        await query.message.edit_text(f"<b>Yᴏᴜʀ sᴇᴛᴛɪɴɢs ᴍᴇɴᴜ ғᴏʀ {title} ʜᴀs ʙᴇᴇɴ sᴇɴᴛ ᴛᴏ ʏᴏᴜʀ PM</b>")
        await query.message.edit_reply_markup(reply_markup)
        if settings is not None:
            buttons = [
                [
                    InlineKeyboardButton('Fɪʟᴛᴇʀ Bᴜᴛᴛᴏɴ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Sɪɴɢʟᴇ' if settings["button"] else 'Dᴏᴜʙʟᴇ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Fɪʟᴇ Sᴇɴᴅ Mᴏᴅᴇ', callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Mᴀɴᴜᴀʟ Sᴛᴀʀᴛ' if settings["botpm"] else 'Aᴜᴛᴏ Sᴇɴᴅ',
                                         callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Pʀᴏᴛᴇᴄᴛ Cᴏɴᴛᴇɴᴛ',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["file_secure"] else '✘ Oғғ',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Iᴍᴅʙ', callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["imdb"] else '✘ Oғғ',
                                         callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Sᴘᴇʟʟ Cʜᴇᴄᴋ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["spell_check"] else '✘ Oғғ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Wᴇʟᴄᴏᴍᴇ Msɢ', callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["welcome"] else '✘ Oғғ',
                                         callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Aᴜᴛᴏ-Dᴇʟᴇᴛᴇ',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}'),
                    InlineKeyboardButton('10 Mɪɴs' if settings["auto_delete"] else '✘ Oғғ',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Aᴜᴛᴏ-Fɪʟᴛᴇʀ',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["auto_ffilter"] else '✘ Oғғ',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Mᴀx Bᴜᴛᴛᴏɴs',
                                         callback_data=f'setgs#max_btn#{settings["max_btn"]}#{str(grp_id)}'),
                    InlineKeyboardButton('10' if settings["max_btn"] else f'{MAX_B_TN}',
                                         callback_data=f'setgs#max_btn#{settings["max_btn"]}#{str(grp_id)}')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await client.send_message(
                chat_id=userid,
                text=f"<b>Cʜᴀɴɢᴇ Yᴏᴜʀ Sᴇᴛᴛɪɴɢs Fᴏʀ {title} As Yᴏᴜʀ Wɪsʜ ⚙</b>",
                reply_markup=reply_markup,
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML,
                reply_to_message_id=query.message.id
            )

    elif query.data.startswith("show_option"):
        ident, from_user = query.data.split("#")
        btn = [[
                InlineKeyboardButton("ꜰɪx❌", callback_data=f"unavailable#{from_user}"), InlineKeyboardButton("ꜰɪxᴇᴅ", callback_data=f"uploaded#{from_user}"), InlineKeyboardButton("ᴡᴀʀɴ", callback_data=f"dontmov#{from_user}")
              ]]
     
        if query.from_user.id in ADMINS:
            user = await client.get_users(from_user)
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_reply_markup(reply_markup)
            await query.answer("Hᴇʀᴇ ᴀʀᴇ ᴛʜᴇ ᴏᴘᴛɪᴏɴs !")
        else:
            await query.answer("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ sᴜғғɪᴄɪᴀɴᴛ ʀɪɢᴛs ᴛᴏ ᴅᴏ ᴛʜɪs !", show_alert=True)
        
    elif query.data.startswith("unavailable"):
        ident, from_user = query.data.split("#")
        btn = [[
                InlineKeyboardButton("⚠️ Uɴᴀᴠᴀɪʟᴀʙʟᴇ ⚠️", callback_data=f"unalert#{from_user}")
              ]]
        
        if query.from_user.id in ADMINS:
            user = await client.get_users(from_user)
            reply_markup = InlineKeyboardMarkup(btn)
            content = query.message.text
            await query.message.edit_text(f"<b><strike>{content}</strike></b>")
            await query.message.edit_reply_markup(reply_markup)
            await query.answer("Sᴇᴛ ᴛᴏ Uɴᴀᴠᴀɪʟᴀʙʟᴇ !")
            try:
                await client.send_message(chat_id=int(from_user), text=f"<b>Hᴇʏ {user.mention}, Sᴏʀʀʏ Yᴏᴜʀ 𝙸𝚂𝚂𝚄𝙴 ɪs ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ 𝚃𝙾 𝙵𝙸𝚇 .</b>")
            except UserIsBlocked:
                await client.send_message(chat_id=int(SUPPORT_CHAT_ID), text=f"<b>Hᴇʏ {user.mention}, Sᴏʀʀʏ Yᴏᴜʀ ʀᴇᴏ̨ᴜᴇsᴛ ɪs ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ. Sᴏ ᴏᴜʀ ᴍᴏᴅᴇʀᴀᴛᴏʀs ᴄᴀɴ'ᴛ ᴜᴘʟᴏᴀᴅ ɪᴛ.\n\nNᴏᴛᴇ: Tʜɪs ᴍᴇssᴀɢᴇ ɪs sᴇɴᴛ ᴛᴏ ᴛʜɪs ɢʀᴏᴜᴘ ʙᴇᴄᴀᴜsᴇ ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ᴛʜᴇ ʙᴏᴛ. Tᴏ sᴇɴᴅ ᴛʜɪs ᴍᴇssᴀɢᴇ ᴛᴏ ʏᴏᴜʀ PM, Mᴜsᴛ ᴜɴʙʟᴏᴄᴋ ᴛʜᴇ ʙᴏᴛ.</b>", reply_markup=InlineKeyboardMarkup(btn))
        else:
            await query.answer("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ sᴜғғɪᴄɪᴀɴᴛ ʀɪɢᴛs ᴛᴏ ᴅᴏ ᴛʜɪs !", show_alert=True)

    elif query.data.startswith("dontmov"):
        ident, from_user = query.data.split("#")
        if query.from_user.id in ADMINS:
            user = await client.get_users(from_user)
            content = query.message.text
            await query.message.edit_text(f"<b><strike>{content}</strike></b>")
            await query.answer("Sᴇᴛ ᴛᴏ warn !")
            try:
                await client.send_message(chat_id=int(from_user), text=f"<b>Hᴇʏ {user.mention},🚫 don't ask movies in bot pm, ask only in group ✅ \n\n</b> <blockquote>NEXT BAN💡</blockquote> ")
            except UserIsBlocked:
                await client.send_message(chat_id=int(SUPPORT_CHAT_ID), text=f"<b>Hᴇʏ {user.mention}, Sᴏʀʀʏ Yᴏᴜʀ ʀᴇᴏ̨ᴜᴇsᴛ ɪs ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ. Sᴏ ᴏᴜʀ ᴍᴏᴅᴇʀᴀᴛᴏʀs ᴄᴀɴ'ᴛ ᴜᴘʟᴏᴀᴅ ɪᴛ.\n\nNᴏᴛᴇ: Tʜɪs ᴍᴇssᴀɢᴇ ɪs sᴇɴᴛ ᴛᴏ ᴛʜɪs ɢʀᴏᴜᴘ ʙᴇᴄᴀᴜsᴇ ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ᴛʜᴇ ʙᴏᴛ. Tᴏ sᴇɴᴅ ᴛʜɪs ᴍᴇssᴀɢᴇ ᴛᴏ ʏᴏᴜʀ PM, Mᴜsᴛ ᴜɴʙʟᴏᴄᴋ ᴛʜᴇ ʙᴏᴛ.</b>", reply_markup=InlineKeyboardMarkup(btn))
        else:
            await query.answer("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ sᴜғғɪᴄɪᴀɴᴛ ʀɪɢᴛs ᴛᴏ ᴅᴏ ᴛʜɪs !", show_alert=True)

    elif query.data.startswith("uploaded"):
        ident, from_user = query.data.split("#")
        btn = [[
                InlineKeyboardButton("✅ Uᴘʟᴏᴀᴅᴇᴅ ✅", callback_data=f"upalert#{from_user}")
              ]]
        
        if query.from_user.id in ADMINS:
            user = await client.get_users(from_user)
            reply_markup = InlineKeyboardMarkup(btn)
            content = query.message.text
            await query.message.edit_text(f"<b><strike>{content}</strike></b>")
            await query.message.edit_reply_markup(reply_markup)
            await query.answer("Sᴇᴛ ᴛᴏ Uᴘʟᴏᴀᴅᴇᴅ !")
            try:
                await client.send_message(chat_id=int(from_user), text=f"<b>Hᴇʏ {user.mention}, 𝚁𝙴𝙿𝙾𝚁𝚃𝙴𝙳 𝙸𝚂𝚂𝚄𝙴 ʜᴀs ʙᴇᴇɴ 𝙵𝙸𝚇𝙴𝙳 ᴏᴜʀ ᴍᴏᴅᴇʀᴀᴛᴏʀs.😎</b>")
            except UserIsBlocked:
                await client.send_message(chat_id=int(SUPPORT_CHAT_ID), text=f"<b>Hᴇʏ {user.mention}, Yᴏᴜʀ ʀᴇᴏ̨ᴜᴇsᴛ ʜᴀs ʙᴇᴇɴ ᴜᴘʟᴏᴀᴅᴇᴅ ʙʏ ᴏᴜʀ ᴍᴏᴅᴇʀᴀᴛᴏʀs. Kɪɴᴅʟʏ sᴇᴀʀᴄʜ ᴀɢᴀɪɴ.\n\nNᴏᴛᴇ: Tʜɪs ᴍᴇssᴀɢᴇ ɪs sᴇɴᴛ ᴛᴏ ᴛʜɪs ɢʀᴏᴜᴘ ʙᴇᴄᴀᴜsᴇ ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ᴛʜᴇ ʙᴏᴛ. Tᴏ sᴇɴᴅ ᴛʜɪs ᴍᴇssᴀɢᴇ ᴛᴏ ʏᴏᴜʀ PM, Mᴜsᴛ ᴜɴʙʟᴏᴄᴋ ᴛʜᴇ ʙᴏᴛ.</b>", reply_markup=InlineKeyboardMarkup(btn))
        else:
            await query.answer("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ sᴜғғɪᴄɪᴀɴᴛ ʀɪɢᴛs ᴛᴏ ᴅᴏ ᴛʜɪs !", show_alert=True)

    elif query.data.startswith("already_available"):
        ident, from_user = query.data.split("#")
        btn = [[
                InlineKeyboardButton("🟢 Aʟʀᴇᴀᴅʏ Aᴠᴀɪʟᴀʙʟᴇ 🟢", callback_data=f"alalert#{from_user}")
              ]]
        btn2 = [[
                 InlineKeyboardButton("Vɪᴇᴡ Sᴛᴀᴛᴜs", url=f"{query.message.link}")
               ]]
        if query.from_user.id in ADMINS:
            user = await client.get_users(from_user)
            reply_markup = InlineKeyboardMarkup(btn)
            content = query.message.text
            await query.message.edit_text(f"<b><strike>{content}</strike></b>")
            await query.message.edit_reply_markup(reply_markup)
            await query.answer("Sᴇᴛ ᴛᴏ Aʟʀᴇᴀᴅʏ Aᴠᴀɪʟᴀʙʟᴇ !")
            try:
                await client.send_message(chat_id=int(from_user), text=f"<b>Hᴇʏ {user.mention}, Yᴏᴜʀ ʀᴇᴏ̨ᴜᴇsᴛ ɪs ᴀʟʀᴇᴀᴅʏ ᴀᴠᴀɪʟᴀʙʟᴇ ᴏɴ ᴏᴜʀ ʙᴏᴛ's ᴅᴀᴛᴀʙᴀsᴇ. Kɪɴᴅʟʏ sᴇᴀʀᴄʜ ᴀɢᴀɪɴ.</b>", reply_markup=InlineKeyboardMarkup(btn2))
            except UserIsBlocked:
                await client.send_message(chat_id=int(SUPPORT_CHAT_ID), text=f"<b>Hᴇʏ {user.mention}, Yᴏᴜʀ ʀᴇᴏ̨ᴜᴇsᴛ ɪs ᴀʟʀᴇᴀᴅʏ ᴀᴠᴀɪʟᴀʙʟᴇ ᴏɴ ᴏᴜʀ ʙᴏᴛ's ᴅᴀᴛᴀʙᴀsᴇ. Kɪɴᴅʟʏ sᴇᴀʀᴄʜ ᴀɢᴀɪɴ.\n\nNᴏᴛᴇ: Tʜɪs ᴍᴇssᴀɢᴇ ɪs sᴇɴᴛ ᴛᴏ ᴛʜɪs ɢʀᴏᴜᴘ ʙᴇᴄᴀᴜsᴇ ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ᴛʜᴇ ʙᴏᴛ. Tᴏ sᴇɴᴅ ᴛʜɪs ᴍᴇssᴀɢᴇ ᴛᴏ ʏᴏᴜʀ PM, Mᴜsᴛ ᴜɴʙʟᴏᴄᴋ ᴛʜᴇ ʙᴏᴛ.</b>", reply_markup=InlineKeyboardMarkup(btn2))
        else:
            await query.answer("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ sᴜғғɪᴄɪᴀɴᴛ ʀɪɢᴛs ᴛᴏ ᴅᴏ ᴛʜɪs !", show_alert=True)

    elif query.data.startswith("alalert"):
        ident, from_user = query.data.split("#")
        if int(query.from_user.id) == int(from_user):
            user = await client.get_users(from_user)
            await query.answer(f"Hᴇʏ {user.first_name}, Yᴏᴜʀ Rᴇᴏ̨ᴜᴇsᴛ ɪs Aʟʀᴇᴀᴅʏ Aᴠᴀɪʟᴀʙʟᴇ !", show_alert=True)
        else:
            await query.answer("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ sᴜғғɪᴄɪᴀɴᴛ ʀɪɢᴛs ᴛᴏ ᴅᴏ ᴛʜɪs !", show_alert=True)

    elif query.data.startswith("upalert"):
        ident, from_user = query.data.split("#")
        if int(query.from_user.id) == int(from_user):
            user = await client.get_users(from_user)
            await query.answer(f"Hᴇʏ {user.first_name}, Yᴏᴜʀ Rᴇᴏ̨ᴜᴇsᴛ ɪs Uᴘʟᴏᴀᴅᴇᴅ !", show_alert=True)
        else:
            await query.answer("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ sᴜғғɪᴄɪᴀɴᴛ ʀɪɢᴛs ᴛᴏ ᴅᴏ ᴛʜɪs !", show_alert=True)
        
    elif query.data.startswith("unalert"):
        ident, from_user = query.data.split("#")
        if int(query.from_user.id) == int(from_user):
            user = await client.get_users(from_user)
            await query.answer(f"Hᴇʏ {user.first_name}, Yᴏᴜʀ Rᴇᴏ̨ᴜᴇsᴛ ɪs Uɴᴀᴠᴀɪʟᴀʙʟᴇ !", show_alert=True)
        else:
            await query.answer("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ sᴜғғɪᴄɪᴀɴᴛ ʀɪɢᴛs ᴛᴏ ᴅᴏ ᴛʜɪs !", show_alert=True)

    elif query.data == "reqinfo":
        await query.answer(text=script.REQINFO, show_alert=True)

    elif query.data == "minfo":
        await query.answer(text=script.MINFO, show_alert=True)

    elif query.data == "sinfo":
        await query.answer(text=script.SINFO, show_alert=True)

    elif query.data == "start":
        buttons = [[
                    InlineKeyboardButton('Iɴʟɪɴᴇ Sᴇᴀʀᴄʜ ', switch_inline_query_current_chat='')
                ],[
                    InlineKeyboardButton("ɢʀᴏᴜᴩ 1 🎪", url="https://t.me/+PBGW_EV3ldY5YjJl"),
                    InlineKeyboardButton("ɢʀᴏᴜᴩ 2 🎪", url="https://t.me/+eDjzTT2Ua6kwMTI1")                  
                  ]]
        
        reply_mmarkup = InlineKeyboardMarkup(buttons)
        if query.message.text:
            try:
                await client.edit_message_media(
                    query.message.chat.id, 
                    query.message.id, 
                    InputMediaPhoto(random.choice(PICS)))
            except:
                await query.message.edit_text(
                    text=script.START_TXT.format(query.from_user.mention, temp.U_NAME, temp.B_NAME),
                    reply_markup=InlineKeyboardMarkup(byttons),
                    disable_web_page_preview=True,
                    parse_mode=enums.ParseMode.HTML)
                return
            else:
                await query.message.edit_text(
                    text=script.START_TXT.format(query.from_user.mention, temp.U_NAME, temp.B_NAME),
                    reply_markup=reply_mmarkup,
                    parse_mode=enums.ParseMode.HTML)
                await query.answer(MSG_ALRT)
        else: 
            try:
                await client.send_message(chat_id=query.from_user.id, text=script.START_TXT.format(query.from_user.mention, temp.U_NAME, temp.B_NAME), reply_markup=InlineKeyboardMarkup(byttons), disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)
            except:
                pass
            await query.message.delete()
        
            
            

    elif query.data == "filters":
        buttons = [[
            InlineKeyboardButton('Mᴀɴᴜᴀʟ FIʟᴛᴇʀ', callback_data='manuelfilter'),
            InlineKeyboardButton('Aᴜᴛᴏ FIʟᴛᴇʀ', callback_data='autofilter')
        ],[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='help'),
            InlineKeyboardButton('Gʟᴏʙᴀʟ Fɪʟᴛᴇʀs', callback_data='global_filters')
        ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.ALL_FILTERS.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "global_filters":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='filters')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.GFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    
    elif query.data == "help":
        buttons = [[
            InlineKeyboardButton('FIʟᴛᴇʀs', callback_data='filters'),
            InlineKeyboardButton('Fɪʟᴇ Sᴛᴏʀᴇ', callback_data='store_file')
        ], [
            InlineKeyboardButton('Cᴏɴɴᴇᴄᴛɪᴏɴ', callback_data='coct'),
            InlineKeyboardButton('Exᴛʀᴀ Mᴏᴅs', callback_data='extra')
        ], [
            InlineKeyboardButton('Hᴏᴍᴇ', callback_data='start'),
            InlineKeyboardButton('Sᴛᴀᴛᴜs', callback_data='stats')
        ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.HELP_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        
    elif query.data == "about":
        await query.answer()
        buttons = [[
            InlineKeyboardButton('Sᴛᴀᴛᴜs', callback_data='stats'),
            InlineKeyboardButton('Sᴏᴜʀᴄᴇ Cᴏᴅᴇ', callback_data='source')
        ],[
            InlineKeyboardButton('Hᴏᴍᴇ 🏠', callback_data='start'),
            InlineKeyboardButton('Cʟᴏsᴇ', callback_data='instr_close')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.message.edit_text(
                text=script.ABOUT_TXT.format(temp.B_NAME),
                reply_markup=reply_markup,
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML
            )
        except:
            try:
                await client.send_message(chat_id=query.from_user.id, text=script.START_TXT.format(query.from_user.mention, temp.U_NAME, temp.B_NAME), reply_markup=InlineKeyboardMarkup(byttons), disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)
            except:
                pass
            
            
    elif query.data == "source":
        await query.answer()
        buttons = [[
            InlineKeyboardButton('𝐍𝐎', callback_data='start'),
            InlineKeyboardButton('𝐘𝐄𝐒', callback_data='stiker')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        
        try:
            await query.message.edit_text(
                text="Do you want it?",
                reply_markup=reply_markup,
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML
            )
        except:
            try:
                await client.send_message(chat_id=query.from_user.id, text=script.START_TXT.format(query.from_user.mention, temp.U_NAME, temp.B_NAME), reply_markup=InlineKeyboardMarkup(byttons), disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)
            except:
                pass
            
            
    elif query.data == "helpppl":
        await query.answer()
        buttons = [[
            InlineKeyboardButton('𝐍𝐎', callback_data='start'),
            InlineKeyboardButton('𝐘𝐄𝐒', callback_data='helpyes')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.message.edit_text(
                text="𝘈𝘳𝘦 𝘺𝘰𝘶 𝘧𝘢𝘤𝘦𝘪𝘯𝘨 𝘢𝘯𝘺 𝘪𝘴𝘴𝘶𝘦 𝘰𝘯 𝘵𝘩𝘦 𝘧𝘪𝘭𝘵𝘦𝘳 𝘣𝘰𝘵.?",
                reply_markup=reply_markup,
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML
            )
        except:
            try:
                await client.send_message(chat_id=query.from_user.id, text=script.START_TXT.format(query.from_user.mention, temp.U_NAME, temp.B_NAME), reply_markup=InlineKeyboardMarkup(byttons), disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)
            except:
                pass
            
            
    elif query.data == "helpyes":
        await query.answer()
        buttons = [[
            InlineKeyboardButton('ᴄᴀɴ`ᴛ ꜰɪɴᴅ ᴛʜᴇ ᴍᴏᴠɪᴇ', callback_data='dcode_film')
        ],[
            InlineKeyboardButton('ꜰɪʟᴇ ɪꜱꜱᴜᴇ', callback_data='dcode_file')
        ],[
            InlineKeyboardButton('ʙᴏᴛ/ɢʀᴏᴜᴩ ʙʟᴏᴄᴋ ɪꜱꜱᴜᴇ', callback_data='dcode_grup')
        ],[
            InlineKeyboardButton('ᴏᴛʜᴇʀ..', callback_data='dcode_othr')
        ],[
            InlineKeyboardButton('Hᴏᴍᴇ 🏠', callback_data='start'),
            InlineKeyboardButton('Cʟᴏsᴇ', callback_data='instr_close')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.message.edit_text(
                text="select a category to report your issue 👇",
                reply_markup=reply_markup,
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML
            )
        except:
            try:
                await client.send_message(chat_id=query.from_user.id, text=script.START_TXT.format(query.from_user.mention, temp.U_NAME, temp.B_NAME), reply_markup=InlineKeyboardMarkup(byttons), disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)
            except:
                pass
            
            
    elif query.data.startswith("dcode"):
        ident, scn = query.data.split("_")
        if scn  == "film":
            a = "Just sent me the movie not available in the bot \n\n nb:❗Don't ask movies that are not released in OTT platforms" 
        elif scn == "file":
            a = "Just sent me the file id that facing any issue"
        elif scn == "grup":
            a = "just sent the group/bot name"
        elif scn == "othr":
            a = "ᴊᴜsᴛ sᴇɴᴅ ᴍᴇ ᴛʜᴇ ᴏᴛʜᴇʀ ɪꜱꜱᴜᴇꜱ"
        man = query.from_user.id
        await query.message.delete()
        try:
            nx = await client.ask(text=f"**{a}**", chat_id=man, timeout=40, reply_markup=ForceReply(placeholder="type issue"))
        except ListenerTimeout:
            await client.send_message(chat_id=man, text=f"**ᴛɪᴍᴇ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ ᴏꜰ 40 ꜱᴇᴄᴏɴᴅꜱ \n\n ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ** ♻️", disable_web_page_preview=True)
            return  
        gg = nx.text
        if gg.startswith("/") or gg.startswith("#"):
            await nx.reply("__ᴛʜɪs ɪs ᴀɴ ɪɴᴠᴀʟɪᴅ ᴍᴇssᴀɢᴇ ᴛʀʏ ᴀɢᴀɪɴ__ ♻️")
            return
        if man != nx.from_user.id:
            await nx.reply("__ᴛʜɪs ɪs ᴀɴ ɪɴᴠᴀʟɪᴅ ᴍᴇssᴀɢᴇ ᴛʀʏ ᴀɢᴀɪɴ__ ♻️")
            return
        await nx.reply("<blockquote> 𝚈𝙾𝚄𝚁 𝙸𝚂𝚂𝚄𝙴 𝙸𝚂 𝚁𝙴𝙿𝙾𝚁𝚃𝙴𝙳 𝚃𝙾 𝚃𝙷𝙴 𝙰𝙳𝙼𝙸𝙽𝚂</blockquote>  \n\n Please wait for some time to fix 😊")
        reporter = str(man)
        btn = [[InlineKeyboardButton('Show Options', callback_data=f'show_option#{reporter}')]]
        await client.send_message(chat_id=LOG_CHANNEL,text=f"⚠️ ATTENTION! \n issue> {scn} \n\n **{nx.text}** \n ID: {man}", reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True)
        return 
    elif query.data == "stiker":
        pari = await query.message.edit_text(
            text="𝐏𝐥𝐳 𝐰𝐚𝐢𝐭, 𝐬𝐞𝐧𝐝𝐢𝐧𝐠.....",
            parse_mode=enums.ParseMode.HTML
        )
        await asyncio.sleep(2) # 😢 https://github.com/EvamariaTG/EvaMaria/blob/master/plugins/p_ttishow.py#L17 😬 wait a bit, before checking.
        await query.message.reply_sticker(sticker=f"{random.choice(MYRE)}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="ꜱᴛᴀʀᴛ",callback_data="start")]]))
        await pari.delete()
        
    elif query.data == "manuelfilter":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='filters'),
            InlineKeyboardButton('Bᴜᴛᴛᴏɴs', callback_data='button')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.MANUELFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "button":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='manuelfilter')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.BUTTON_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "autofilter":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='filters')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.AUTOFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "coct":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='help')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.CONNECTION_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "extra":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='help'),
            InlineKeyboardButton('Aᴅᴍɪɴ', callback_data='admin')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.EXTRAMOD_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    
    elif query.data == "store_file":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='help')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.FILE_STORE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    
    elif query.data == "admin":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='extra')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ADMIN_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "stats":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='about'),
            InlineKeyboardButton('⟲ Rᴇғʀᴇsʜ', callback_data='rfrsh')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        tottl = await Media.count_documents()
        total = f"35{tottl}" 
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "rfrsh":
        await query.answer("Fetching MongoDb DataBase")
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='about'),
            InlineKeyboardButton('⟲ Rᴇғʀᴇsʜ', callback_data='rfrsh')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        tottl = await Media.count_documents()
        total = f"35{tottl}" 
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "owner_info":
        return await query.answer("🤖 ɴᴀᴍᴇ: ғɪʟᴛᴇʀ -x- v2.8\n\n🎪ᴄʀᴇᴀᴛᴏʀ: sᴀʀᴀɴ\n\n📚ʟᴀɴɢᴜᴀɢᴇ: ᴘʏᴛʜᴏɴ3\n\n🌀 ʟɪʙʀᴀʀʏ : ᴘʏʀᴏɢʀᴀᴍ ᴀsʏɴᴄɪᴏ 1.13.0",show_alert=True)
                
    elif query.data.startswith("setgs"):
        ident, set_type, status, grp_id = query.data.split("#")
        grpid = await active_connection(str(query.from_user.id))

        if str(grp_id) != str(grpid):
            await query.message.edit("Yᴏᴜʀ Aᴄᴛɪᴠᴇ Cᴏɴɴᴇᴄᴛɪᴏɴ Hᴀs Bᴇᴇɴ Cʜᴀɴɢᴇᴅ. Gᴏ Tᴏ /connections ᴀɴᴅ ᴄʜᴀɴɢᴇ ʏᴏᴜʀ ᴀᴄᴛɪᴠᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴ.")
            return await query.answer(MSG_ALRT)

        if status == "True":
            await save_group_settings(grpid, set_type, False)
        else:
            await save_group_settings(grpid, set_type, True)

        settings = await get_settings(grpid)

        if settings is not None:
            buttons = [
                [
                    InlineKeyboardButton('Fɪʟᴛᴇʀ Bᴜᴛᴛᴏɴ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Sɪɴɢʟᴇ' if settings["button"] else 'Dᴏᴜʙʟᴇ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Fɪʟᴇ Sᴇɴᴅ Mᴏᴅᴇ', callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Mᴀɴᴜᴀʟ Sᴛᴀʀᴛ' if settings["botpm"] else 'Aᴜᴛᴏ Sᴇɴᴅ',
                                         callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Pʀᴏᴛᴇᴄᴛ Cᴏɴᴛᴇɴᴛ',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["file_secure"] else '✘ Oғғ',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Iᴍᴅʙ', callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["imdb"] else '✘ Oғғ',
                                         callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Sᴘᴇʟʟ Cʜᴇᴄᴋ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["spell_check"] else '✘ Oғғ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Wᴇʟᴄᴏᴍᴇ Msɢ', callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["welcome"] else '✘ Oғғ',
                                         callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Aᴜᴛᴏ-Dᴇʟᴇᴛᴇ',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}'),
                    InlineKeyboardButton('10 Mɪɴs' if settings["auto_delete"] else '✘ Oғғ',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Aᴜᴛᴏ-Fɪʟᴛᴇʀ',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✔ Oɴ' if settings["auto_ffilter"] else '✘ Oғғ',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Mᴀx Bᴜᴛᴛᴏɴs',
                                         callback_data=f'setgs#max_btn#{settings["max_btn"]}#{str(grp_id)}'),
                    InlineKeyboardButton('10' if settings["max_btn"] else f'{MAX_B_TN}',
                                         callback_data=f'setgs#max_btn#{settings["max_btn"]}#{str(grp_id)}')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_reply_markup(reply_markup)

    elif query.data.startswith("next"):
        if clicked != typed:
            await query.answer(f"Hᴇʏ {query.from_user.first_name}, Tʜɪs Is Nᴏᴛ Yᴏᴜʀ Mᴏᴠɪᴇ Rᴇǫᴜᴇsᴛ. Rᴇǫᴜᴇsᴛ Yᴏᴜʀ's !", show_alert=True)
            return
        try:
            ident, index, keyword = query.data.split("_")
        except KeyError:
            await query.answer(" You are using this for one of my old message, please send the request again ",show_alert=True)
            await query.message.delete()
            return
        else:
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer(" You are using this for one of my old message, please send the request again ",show_alert=True)
                return await query.message.delete()
            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⇍ ʙᴀᴄᴋ ⇍", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton(f"🎪 {int(index)+2}/{data['total']}🎪", callback_data="pages"),InlineKeyboardButton(text="🕯️ ᴄʟᴏꜱᴇ", callback_data="instr_close")]
                )
                buttons.insert(0, [InlineKeyboardButton("⚡ Cʜᴇᴄᴋ Bᴏᴛ PM ⚡", url=f"https://t.me/{temp.U_NAME}")])
                try:
                    await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
                except MessageNotModified:
                    await query.answer("❗️Message Not Modified❗️")
                except Exception as e:
                    await query.answer()
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⇍ ʙᴀᴄᴋ ⇍", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton(f"🎪{int(index)+2}/{data['total']}🎪", callback_data="pages"),InlineKeyboardButton("⇏ ɴᴇxᴛ ⇏", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.insert(0, [InlineKeyboardButton("⚡ Cʜᴇᴄᴋ Bᴏᴛ PM ⚡", url=f"https://t.me/{temp.U_NAME}")])
                try:
                    await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
                except MessageNotModified:
                    await query.answer("❗️Message Not Modified❗️")
                except Exception as e:
                    await query.answer()
                return
    elif query.data.startswith("back"):
        if clicked != typed:
            await query.answer(f"Hᴇʏ {query.from_user.first_name}, Tʜɪs Is Nᴏᴛ Yᴏᴜʀ Mᴏᴠɪᴇ Rᴇǫᴜᴇsᴛ. Rᴇǫᴜᴇsᴛ Yᴏᴜʀ's !", show_alert=True)
            return
        try:
            ident, index, keyword = query.data.split("_")
        except KeyError:
            await query.answer(" You are using this for one of my old message, please send the request again ",show_alert=True)
            await query.message.delete()
            return
        else:
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return await query.message.delete()

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton(f"🎪 Pages {int(index)}/{data['total']}🎪", callback_data="pages"),InlineKeyboardButton("⇏ ɴᴇxᴛ ⇏", callback_data=f"next_{int(index)-1}_{keyword}")]                   
                )
                buttons.insert(0, [InlineKeyboardButton("⚡ Cʜᴇᴄᴋ Bᴏᴛ PM ⚡", url=f"https://t.me/{temp.U_NAME}")])
                try:
                    await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
                except MessageNotModified:
                    await query.answer("❗️Message Not Modified❗️")
                except Exception as e:
                    await query.answer()
                return 
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("⇍ ʙᴀᴄᴋ ⇍", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton(f"🎪{int(index)}/{data['total']}🎪", callback_data="pages"),InlineKeyboardButton("⇏ ɴᴇxᴛ ⇏", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.insert(0, [InlineKeyboardButton("⚡ Cʜᴇᴄᴋ Bᴏᴛ PM ⚡", url=f"https://t.me/{temp.U_NAME}")])
                try:
                    await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
                except MessageNotModified:
                    await query.answer("❗️Message Not Modified❗️")
                except Exception as e: 
                    await query.answer()
                return

def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]          
        n += 1
        
async def auto_filter(client, msg, spoll=False):
    reqstr1 = msg.from_user.id if msg.from_user else 0
    reqstr = await client.get_users(reqstr1)
    if not spoll:
        message = msg
        settings = await get_settings(message.chat.id)
        if message.text.startswith("/"): return  # ignore commands
        if re.findall("((^\/|^,|^!|^[\U0001F600-\U000E007F]).*)", message.text):
            await asyncio.sleep(3)
            try:
                await message.delete()
            except:
                pass
            return
        men = message.from_user.mention if message.from_user else "Anonymous" 
        if len(message.text) <= 2:
            kk = await message.reply_text(f"{men},ɪɴᴄʟᴜᴅᴇ ʏᴇᴀʀ ᴏғ ᴛʜᴇ ᴍᴏᴠɪᴇ. \n\n 𝚜𝚎𝚗𝚝👉 ᴍᴏᴠɪᴇ ɴᴀᴍᴇ & yᴇᴀʀ")
            await asyncio.sleep(20)
            await kk.delete()
            try:
                await message.delete()
            except Exception as e:
                print(e)
                return
        elif 2 < len(message.text) < 70:
            pari = re.sub(r"(:|\'|\~|\-|[(]|[)]|\[|\]|\.|\,|\;|\_)", " ", message.text, flags=re.IGNORECASE)
            yinfo = "\n<blockquote>📍 ɪɴᴄʟᴜᴅᴇ ᴍᴏᴠɪᴇ ʏᴇᴀʀ ғᴏʀ ʙᴇᴛᴛᴇʀ ᴀᴄᴄᴜʀᴀᴄʏ</blockquote>"
            try:
                search = pari.replace("  ", " ")
            except:
                search = pari
            files, offset, total_results = await get_search_results(message.chat.id ,search.lower(), max_results=200, offset=0, filter=True)
            if not files:
                if settings["spell_check"]:
                    return await advantage_spell_chok(client, msg)
                query = re.sub(r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|English|english|Hindi|hindi|Telugu|telugu|1080p|720p|HEVC|Esub|Kannada|kannada|br((o|u)h?)*|^h(e|a)?(l)*(o)*|mal(ayalam)?|t(h)?amil|file|Tamil|find|und(o)*|kit(t(i|y)?)?o(w)?|thar(u)?(o)*w?|kittum(o)*|aya(k)*(um(o)*)?|full\smovie|any(one)|with\ssubtitle(s)?)", "", search, flags=re.IGNORECASE)
                yy = query.split()
                xx = "_".join(yy)
                sessna = xx.lower()
                try:
                    nyvaa = BUT[sessna]
                except:
                    xiles, xffset, xotal_results = await get_search_results(message.chat.id ,query.lower(), max_results=200, offset=0, filter=True)
                else:
                    cap = f"<b>Hᴇʏ 🙌{men}, Hᴇʀᴇ ɪs Wʜᴀᴛ I Fᴏᴜɴᴅ Iɴ Mʏ Dᴀᴛᴀʙᴀsᴇ Fᴏʀ Yᴏᴜʀ Qᴜᴇʀʏ {query}.</b>{f'{yinfo}' if len(query) <= 5 else ''}"
                    try:
                        btn = nyvaa['buttons']
                    except:
                        BUT.pop(f"{sessna}")
                    else:
                        fuk = await message.reply_text(text=cap[:1024], reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)
                        files, offset, total_results = await get_search_results(message.chat.id, query.lower(), offset=0, filter=True)
                        if int(total_results) != int(nyvaa['total']):
                            BUT.pop(f"{sessna}")
                        await asyncio.sleep(300)
                        await fuk.delete()
                        try:
                            await message.delete()
                        except:
                            pass
                        return
                if xiles:
                    files = xiles
                    offset = xffset
                    total_results = xotal_results
                    search = query
                else:
                    mach = ["episode", "season"]
                    text_words = set(message.text.lower().split())
                    for word in mach:
                        if word in text_words:
                            kj = await message.reply_text(SEEP, disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)
                            await asyncio.sleep(30)
                            await kj.delete() 
                            try:
                                await message.delete()
                            except Exception as e:
                                print(e)
                            return
                    kuttons = []
                    kuttons.append(
                        [InlineKeyboardButton(text="ᴍᴀʟ", callback_data="instr_mal"), InlineKeyboardButton(text="ᴛᴀᴍ", callback_data="instr_tam"), InlineKeyboardButton(text="ʜɪɴ", callback_data="instr_hin"), InlineKeyboardButton(text="ᴇɴɢ", callback_data="instr_eng")]
                    )
                    kuttons.append(
                        [InlineKeyboardButton(text="ᴄʟᴏꜱᴇ", callback_data="instr_close")]
                    )
                    reply_markup = InlineKeyboardMarkup(kuttons)
                    kk = await message.reply_text(f"<b>Hey {men}, I couldn't ❌ find anything related to your request </b>\n\n<blockquote>📍 Try reading the instructions below 👇</blockquote>", reply_markup=reply_markup)
                    await asyncio.sleep(150)
                    await kk.delete()
                    try:
                        await message.delete()
                    except Exception as e:
                        print(e)
                    if NO_RESULTS_MSG:
                        await client.send_message(chat_id=LOG_CHANNEL, text=(script.NORSLTS.format(reqstr.id, reqstr.mention, search)))
                    return
        else:
            try:
                await message.delete()
            except:
                pass
            return
    else:
        settings = await get_settings(msg.message.chat.id)
        message = msg.message.reply_to_message  # msg will be callback query
        search, files, offset, total_results = spoll
    pre = 'filep' if settings['file_secure'] else 'file'
    oam = f"{random.choice(RAT)}"
    oamm = f"{random.choice(RAT)}"
    try:
       btn = []
       for file in files:
           sz = get_size(file.file_size)
           tt = file.file_name.title().lstrip()
           if tt == "None":
               tt = file.caption.lstrip()
           fg = re.sub(r"(_|\~|\©|\®|\-|\.|\#|\B@\w+|https?://\S+|www\.\S+|\[.*?\]|[(]|[)]|\+)", " ", tt, flags=re.IGNORECASE).strip()
           try:
               fn = fg.replace("  ", " ")
           except:
               fn = fg
           filenaame = f"{oam}{sz[0:3]} {sz[-2:]}{oamm}{fn}"
           btn.append([InlineKeyboardButton(text=f"{filenaame}",callback_data=f'{pre}#{file.file_id}')])
    except:
        try:
            await message.delete()
        except Exception as e:
            print(e)
        return
        
    
    if len(btn) > 6: 
        btns = list(split_list(btn, 6)) 
        keyword = f"{message.chat.id}-{message.id}"
        BUTTONS[keyword] = {
            "total" : len(btns),
            "buttons" : btns
        }
        data = BUTTONS[keyword]
        bttn = data['buttons'][0].copy()
        btn = bttn
        btn.append(
            [InlineKeyboardButton("ᴩᴀɢᴇ", callback_data="pages"),InlineKeyboardButton(text=f"🎪 1/{data['total']} 🎪",callback_data="pages"),InlineKeyboardButton(text="⇏ ɴᴇxᴛ ⇏",callback_data=f"next_0_{keyword}")]
        )
    else:
        btn.append(
            [InlineKeyboardButton("💡 ᴄʟᴏꜱᴇ", callback_data="instr_close")]
        )
    """if offset != "":
        key = f"{message.chat.id}-{message.id}"
        BUTTONS[key] = search
        req = message.from_user.id if message.from_user else 0
        try:
            settings = await get_settings(message.chat.id)
            if settings['max_btn']:
                btn.append(
                    [InlineKeyboardButton("ᴩᴀɢᴇ", callback_data="pages"), InlineKeyboardButton(text=f"🎪1/{math.ceil(int(total_results)/10)}🎪",callback_data="pages"), InlineKeyboardButton(text="⇏ɴᴇxᴛ⇏",callback_data=f"next_{req}_{key}_{offset}")]
                )
            else:
                btn.append(
                    [InlineKeyboardButton("ᴩᴀɢᴇ", callback_data="pages"), InlineKeyboardButton(text=f"🎪1/{math.ceil(int(total_results)/int(MAX_B_TN))}🎪",callback_data="pages"), InlineKeyboardButton(text="⇏ɴᴇxᴛ⇏",callback_data=f"next_{req}_{key}_{offset}")]
                )
        except KeyError:
            await save_group_settings(message.chat.id, 'max_btn', False)
            settings = await get_settings(message.chat.id)
            if settings['max_btn']:
                btn.append(
                    [InlineKeyboardButton("𝐏𝐀𝐆𝐄", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/10)}",callback_data="pages"), InlineKeyboardButton(text="𝐍𝐄𝐗𝐓 ➪",callback_data=f"next_{req}_{key}_{offset}")]
                )
            else:
                btn.append(
                    [InlineKeyboardButton("𝐏𝐀𝐆𝐄", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/int(MAX_B_TN))}",callback_data="pages"), InlineKeyboardButton(text="𝐍𝐄𝐗𝐓 ➪",callback_data=f"next_{req}_{key}_{offset}")]
                )"""
    
    btn.insert(0, [
        InlineKeyboardButton(" Cʜᴇᴄᴋ Bᴏᴛ PM ", url=f"https://t.me/{temp.U_NAME}")
    ])
    sch = search.strip()
    y = sch.split()
    x = "_".join(y)
    sesna = x.lower()
    BUT[sesna] = {"total" : str(total_results), "buttons" : btn}
    try:
        nyva = RESEND[sesna]
    except:
        RESEND[sesna] = int("1")
    imdb = await get_poster(search, file=(files[0]).file_name) if settings["imdb"] else None
    TEMPLATE = settings['template']
    if imdb:
        cap = TEMPLATE.format(
            query=search,
            title=imdb['title'],
            votes=imdb['votes'],
            aka=imdb["aka"],
            seasons=imdb["seasons"],
            box_office=imdb['box_office'],
            localized_title=imdb['localized_title'],
            kind=imdb['kind'],
            imdb_id=imdb["imdb_id"],
            cast=imdb["cast"],
            runtime=imdb["runtime"],
            countries=imdb["countries"],
            certificates=imdb["certificates"],
            languages=imdb["languages"],
            director=imdb["director"],
            writer=imdb["writer"],
            producer=imdb["producer"],
            composer=imdb["composer"],
            cinematographer=imdb["cinematographer"],
            music_team=imdb["music_team"],
            distributors=imdb["distributors"],
            release_date=imdb['release_date'],
            year=imdb['year'],
            genres=imdb['genres'],
            poster=imdb['poster'],
            plot=imdb['plot'],
            rating=imdb['rating'],
            url=imdb['url'],
            **locals()
        )
    else:
        mach1 = "episode"
        mach2 = "season"
        text_words = message.text.lower()
        if mach1 in text_words or mach2 in text_words:
            cap = f"<b>Hᴇʏ {message.from_user.mention}, Hᴇʀᴇ ɪs Wʜᴀᴛ I Fᴏᴜɴᴅ Iɴ Mʏ Dᴀᴛᴀʙᴀsᴇ Fᴏʀ Yᴏᴜʀ Qᴜᴇʀʏ {search}.</b>\n <blockquote>{SEEP}</blockquote>"
        else:
            cap = f"<b>Hᴇʏ {message.from_user.mention}, Hᴇʀᴇ ɪs Wʜᴀᴛ I Fᴏᴜɴᴅ Iɴ Mʏ Dᴀᴛᴀʙᴀsᴇ Fᴏʀ Yᴏᴜʀ Qᴜᴇʀʏ {search}.</b>{f'{yinfo}' if len(search) <= 5 else ''}"
    if imdb and imdb.get('poster'):
        try:
            if message.chat.id == SUPPORT_CHAT_ID:
                await message.reply_text(f"<b>Hᴇʏ {message.from_user.mention}, {str(total_results)} ʀᴇsᴜʟᴛs ᴀʀᴇ ғᴏᴜɴᴅ ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ ғᴏʀ ʏᴏᴜʀ ᴏ̨ᴜᴇʀʏ {search}. Kɪɴᴅʟʏ ᴜsᴇ ɪɴʟɪɴᴇ sᴇᴀʀᴄʜ ᴏʀ ᴍᴀᴋᴇ ᴀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴀᴅᴅ ᴍᴇ ᴀs ᴀᴅᴍɪɴ ᴛᴏ ɢᴇᴛ ᴍᴏᴠɪᴇ ғɪʟᴇs. Tʜɪs ɪs ᴀ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ sᴏ ᴛʜᴀᴛ ʏᴏᴜ ᴄᴀɴ'ᴛ ɢᴇᴛ ғɪʟᴇs ғʀᴏᴍ ʜᴇʀᴇ...\n\nFᴏʀ Mᴏᴠɪᴇs, Jᴏɪɴ @free_movies_all_languages</b>")
            else:
                hehe = await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024], reply_markup=InlineKeyboardMarkup(btn))
                try:
                    if settings['auto_delete']:
                        await asyncio.sleep(300)
                        await hehe.delete()
                        try:
                            await message.delete()
                        except:
                            pass
                except KeyError:
                    grpid = await active_connection(str(message.from_user.id))
                    await save_group_settings(grpid, 'auto_delete', True)
                    settings = await get_settings(message.chat.id)
                    if settings['auto_delete']:
                        await asyncio.sleep(300)
                        await hehe.delete()
                        try:
                            await message.delete()
                        except:
                            pass
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            if message.chat.id == SUPPORT_CHAT_ID:
                await message.reply_text(f"<b>Hᴇʏ {message.from_user.mention}, {str(total_results)} ʀᴇsᴜʟᴛs ᴀʀᴇ ғᴏᴜɴᴅ ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ ғᴏʀ ʏᴏᴜʀ ᴏ̨ᴜᴇʀʏ {search}. Kɪɴᴅʟʏ ᴜsᴇ ɪɴʟɪɴᴇ sᴇᴀʀᴄʜ ᴏʀ ᴍᴀᴋᴇ ᴀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴀᴅᴅ ᴍᴇ ᴀs ᴀᴅᴍɪɴ ᴛᴏ ɢᴇᴛ ᴍᴏᴠɪᴇ ғɪʟᴇs. Tʜɪs ɪs ᴀ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ sᴏ ᴛʜᴀᴛ ʏᴏᴜ ᴄᴀɴ'ᴛ ɢᴇᴛ ғɪʟᴇs ғʀᴏᴍ ʜᴇʀᴇ...\n\nFᴏʀ Mᴏᴠɪᴇs, Jᴏɪɴ @free_movies_all_languages</b>")
            else:
                pic = imdb.get('poster')
                poster = pic.replace('.jpg', "._V1_UX360.jpg")
                hmm = await message.reply_photo(photo=poster, caption=cap[:1024], reply_markup=InlineKeyboardMarkup(btn))
                try:
                    if settings['auto_delete']:
                        await asyncio.sleep(300)
                        await hmm.delete()
                        try:
                            await message.delete()
                        except:
                            pass
                except KeyError:
                    grpid = await active_connection(str(message.from_user.id))
                    await save_group_settings(grpid, 'auto_delete', True)
                    settings = await get_settings(message.chat.id)
                    if settings['auto_delete']:
                        await asyncio.sleep(300)
                        await hmm.delete()
                        try:
                            await message.delete()
                        except:
                            pass
        except Exception as e:
            if message.chat.id == SUPPORT_CHAT_ID:
                await message.reply_text(f"<b>Hᴇʏ {message.from_user.mention}, {str(total_results)} ʀᴇsᴜʟᴛs ᴀʀᴇ ғᴏᴜɴᴅ ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ ғᴏʀ ʏᴏᴜʀ ᴏ̨ᴜᴇʀʏ {search}. Kɪɴᴅʟʏ ᴜsᴇ ɪɴʟɪɴᴇ sᴇᴀʀᴄʜ ᴏʀ ᴍᴀᴋᴇ ᴀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴀᴅᴅ ᴍᴇ ᴀs ᴀᴅᴍɪɴ ᴛᴏ ɢᴇᴛ ᴍᴏᴠɪᴇ ғɪʟᴇs. Tʜɪs ɪs ᴀ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ sᴏ ᴛʜᴀᴛ ʏᴏᴜ ᴄᴀɴ'ᴛ ɢᴇᴛ ғɪʟᴇs ғʀᴏᴍ ʜᴇʀᴇ...\n\nFᴏʀ Mᴏᴠɪᴇs, Jᴏɪɴ </b>")
            else:
                logger.exception(e)
                fek = await message.reply_photo(photo=NOR_IMG, caption=cap, reply_markup=InlineKeyboardMarkup(btn))
                try:
                    if settings['auto_delete']:
                        await asyncio.sleep(300)
                        await fek.delete()
                        try:
                            await message.delete()
                        except:
                            pass
                except KeyError:
                    grpid = await active_connection(str(message.from_user.id))
                    await save_group_settings(grpid, 'auto_delete', True)
                    settings = await get_settings(message.chat.id)
                    if settings['auto_delete']:
                        await asyncio.sleep(300)
                        await fek.delete()
                        try:
                            await message.delete()
                        except:
                            pass
    else:
        if message.chat.id == SUPPORT_CHAT_ID:
            await message.reply_text(f"<b>Hᴇʏ {message.from_user.mention}, {str(total_results)} ʀᴇsᴜʟᴛs ᴀʀᴇ ғᴏᴜɴᴅ ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ ғᴏʀ ʏᴏᴜʀ ᴏ̨ᴜᴇʀʏ {search}. Kɪɴᴅʟʏ ᴜsᴇ ɪɴʟɪɴᴇ sᴇᴀʀᴄʜ ᴏʀ ᴍᴀᴋᴇ ᴀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴀᴅᴅ ᴍᴇ ᴀs ᴀᴅᴍɪɴ ᴛᴏ ɢᴇᴛ ᴍᴏᴠɪᴇ ғɪʟᴇs. Tʜɪs ɪs ᴀ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ sᴏ ᴛʜᴀᴛ ʏᴏᴜ ᴄᴀɴ'ᴛ ɢᴇᴛ ғɪʟᴇs ғʀᴏᴍ ʜᴇʀᴇ...\n\nFᴏʀ Mᴏᴠɪᴇs, Jᴏɪɴ </b>")
        else:
            hehe = await message.reply_text(text=cap[:1024], reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)
            try:
                if settings['auto_delete']:
                    await asyncio.sleep(300)
                    await hehe.delete()
                    try:
                        await message.delete()
                    except:
                        pass
            except KeyError:
                grpid = await active_connection(str(message.from_user.id))
                await save_group_settings(grpid, 'auto_delete', True)
                settings = await get_settings(message.chat.id)
                if settings['auto_delete']:
                    await asyncio.sleep(300)
                    await hehe.delete()
                    try:
                        await message.delete()
                    except:
                        pass
            
    if spoll:
        await msg.message.delete()


async def advantage_spell_chok(client, msg): #modified spell check
    mv_id = msg.id
    mv_rqst = msg.text
    reqstr1 = msg.from_user.id if msg.from_user else 0
    reqstr = await client.get_users(reqstr1)
    settings = await get_settings(msg.chat.id)
    query = re.sub(
        r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|English|english|Hindi|hindi|Telugu|telugu|1080p|720p|HEVC|Esub|Kannada|kannada|br((o|u)h?)*|^h(e|a)?(l)*(o)*|mal(ayalam)?|t(h)?amil|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|thar(u)?(o)*w?|kittum(o)*|aya(k)*(um(o)*)?|full\smovie|any(one)|with\ssubtitle(s)?)",
        "", msg.text, flags=re.IGNORECASE)  # plis contribute some common words
    query = query.strip() + " movie"
    try:
        movies = await get_poster(mv_rqst, bulk=True)
    except Exception as e:
        logger.exception(e)
        reqst_gle = mv_rqst.replace(" ", "+")
        button = [[
                   InlineKeyboardButton("Gᴏᴏɢʟᴇ", url=f"https://www.google.com/search?q={reqst_gle}")
        ]]
        if NO_RESULTS_MSG:
            await client.send_message(chat_id=LOG_CHANNEL, text=(script.NORSLTS.format(reqstr.id, reqstr.mention, mv_rqst)))
        k = await msg.reply_photo(
            photo=SPELL_IMG, 
            caption=script.I_CUDNT.format(mv_rqst),
            reply_markup=InlineKeyboardMarkup(button)
        )
        await asyncio.sleep(30)
        await k.delete()
        try:
            await msg.delete()
        except:
            pass
        return
    movielist = []
    if not movies:
        reqst_gle = mv_rqst.replace(" ", "+")
        button = [[
                   InlineKeyboardButton("Gᴏᴏɢʟᴇ", url=f"https://www.google.com/search?q={reqst_gle}")
        ]]
        await client.send_message(chat_id=LOG_CHANNEL, text=(script.NORSLTS.format(reqstr.id, reqstr.mention, mv_rqst)))
        k = await msg.reply_photo(
            photo=SPELL_IMG, 
            caption=script.I_CUDNT.format(mv_rqst),
            reply_markup=InlineKeyboardMarkup(button)
        )
        await asyncio.sleep(30)
        await k.delete()
        try:
            await msg.delete()
        except:
            pass
        return
    movielist += [movie.get('title') for movie in movies]
    movielist += [f"{movie.get('title')} {movie.get('year')}" for movie in movies]
    SPELL_CHECK[mv_id] = movielist
    btn = [
        [
            InlineKeyboardButton(
                text=movie_name.strip(),
                callback_data=f"spol#{reqstr1}#{k}",
            )
        ]
        for k, movie_name in enumerate(movielist)
    ]
    btn.append([InlineKeyboardButton(text="Close", callback_data=f'spol#{reqstr1}#close_spellcheck')])
    spell_check_del = await msg.reply_photo(
        photo=(SPELL_IMG),
        caption=(script.CUDNT_FND.format(mv_rqst)),
        reply_markup=InlineKeyboardMarkup(btn)
    )
    try:
        if settings['auto_delete']:
            await asyncio.sleep(600)
            try:
                await msg.delete()
            except:
                pass
            await spell_check_del.delete()
    except KeyError:
            grpid = await active_connection(str(message.from_user.id))
            await save_group_settings(grpid, 'auto_delete', True)
            settings = await get_settings(message.chat.id)
            if settings['auto_delete']:
                await asyncio.sleep(600)
                try:
                    await msg.delete()
                except:
                    pass
                await spell_check_del.delete()


async def manual_filters(client, message, text=False):
    settings = await get_settings(message.chat.id)
    group_id = message.chat.id
    name = text or message.text
    searrch = name.strip()
    y = searrch.split()
    x = "_".join(y)
    sesna = x.lower()
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    keywords = await get_filters(group_id)
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_filter(group_id, keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            joelkb = await client.send_message(
                                group_id, 
                                reply_text, 
                                disable_web_page_preview=True,
                                protect_content=True if settings["file_secure"] else False,
                                reply_to_message_id=reply_id
                            )
                            try:
                                nyva = BUT[sesna]
                            except:
                                await auto_filter(client, message)
                            try:
                                if settings['auto_delete']:
                                    await asyncio.sleep(360)
                                    try:
                                        await message.delete()
                                    except:
                                        pass
                                    await joelkb.delete()
                            except KeyError:
                                grpid = await active_connection(str(message.from_user.id))
                                await save_group_settings(grpid, 'auto_delete', True)
                                settings = await get_settings(message.chat.id)
                                if settings['auto_delete']:
                                    await asyncio.sleep(360)
                                    try:
                                        await message.delete()
                                    except:
                                        pass
                                    await joelkb.delete()

                        else:
                            button = eval(btn)
                            hmm = await client.send_message(
                                group_id,
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                protect_content=True if settings["file_secure"] else False,
                                reply_to_message_id=reply_id
                            )
                            try:
                                nyva = BUT[sesna]
                            except:
                                await auto_filter(client, message)
                            try:
                                if settings['auto_delete']:
                                    await asyncio.sleep(360)
                                    try:
                                        await message.delete()
                                    except:
                                        pass
                                    await hmm.delete()
                            except KeyError:
                                grpid = await active_connection(str(message.from_user.id))
                                await save_group_settings(grpid, 'auto_delete', True)
                                settings = await get_settings(message.chat.id)
                                if settings['auto_delete']:
                                    await asyncio.sleep(360)
                                    try:
                                        await message.delete()
                                    except:
                                        pass
                                    await hmm.delete()

                    elif btn == "[]":
                        oto = await client.send_cached_media(
                            group_id,
                            fileid,
                            caption=reply_text or "",
                            protect_content=True if settings["file_secure"] else False,
                            reply_to_message_id=reply_id
                        )
                        try:
                            nyva = BUT[sesna]
                        except:
                            await auto_filter(client, message)
                        try:
                            if settings['auto_delete']:
                                await asyncio.sleep(360)
                                try:
                                    await message.delete()
                                except:
                                    pass
                                await oto.delete()
                        except KeyError:
                            grpid = await active_connection(str(message.from_user.id))
                            await save_group_settings(grpid, 'auto_delete', True)
                            settings = await get_settings(message.chat.id)
                            if settings['auto_delete']:
                                await asyncio.sleep(160)
                                try:
                                    await message.delete()
                                except:
                                    pass
                                await oto.delete()

                    else:
                        button = eval(btn)
                        dlt = await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id=reply_id
                        )
                        try:
                            nyva = BUT[sesna]
                        except:
                            await auto_filter(client, message)
                        try:
                            if settings['auto_delete']:
                                await asyncio.sleep(360)
                                try:
                                    await message.delete()
                                except:
                                    pass
                                await dlt.delete()
                        except KeyError:
                            grpid = await active_connection(str(message.from_user.id))
                            await save_group_settings(grpid, 'auto_delete', True)
                            settings = await get_settings(message.chat.id)
                            if settings['auto_delete']:
                                await asyncio.sleep(160)
                                try:
                                    await message.delete()
                                except:
                                    pass
                                await dlt.delete()

                except Exception as e:
                    logger.exception(e)
                break
            else:
                pass              
    else:
        return False

async def global_filters(client, message, text=False):
    settings = await get_settings(message.chat.id)
    group_id = message.chat.id
    name = text or message.text
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    keywords = await get_gfilters('gfilters')
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_gfilter('gfilters', keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            joelkb = await client.send_message(
                                group_id, 
                                reply_text, 
                                disable_web_page_preview=True,
                                reply_to_message_id=reply_id
                            )
                            
                        else:
                            button = eval(btn)
                            hmm = await client.send_message(
                                group_id,
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                reply_to_message_id=reply_id
                            )

                    elif btn == "[]":
                        oto = await client.send_cached_media(
                            group_id,
                            fileid,
                            caption=reply_text or "",
                            reply_to_message_id=reply_id
                        )

                    else:
                        button = eval(btn)
                        dlt = await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id=reply_id
                        )

                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False
