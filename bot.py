import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

anlik_calisan = []

@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
  global anlik_calisan
  anlik_calisan.remove(event.chat_id)


@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("**Old Tag Bot**, Qrupda və ya kanalda demək olar ki, hər bir üzvü qeyd edə bilərəm ★\nDaha çoxu üçün **/help**'ə tıklayın.",
                    buttons=(
                      [Button.url('🌟 Qrupa Sal', 'https://t.me/oldtagbot?startgroup=a'),
                      Button.url('🗨️ Qrupumuz', 'https://t.me/oldmafiagroup'),
                      Button.url('🚀 Sahibim', 'https://t.me/Nadjafoovv')]
                    ),
                    link_preview=False
                   )
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**Old Tag Bot'un Yardım Menyusu**\n\nKomut: /all \n  Bu əmri başqalarına danışmaq istədiyiniz mətnlə birlikdə istifadə edə bilərsiniz. \n`Nümunə: /hamının sabahı xeyir!` \nBu əmri cavab olaraq istifadə edə bilərsiniz. istənilən mesaj Bot istifadəçiləri cavab mesajına işarələyəcək"
  await event.reply(helptext,
                    buttons=(
                      [Button.url('🌟 Qrupa Sal', 'https://t.me/oldtagbot?startgroup=a'),
                       Button.url('🗨️ Qrupumuz', 'https://t.me/oldmafiagroup'),
                      Button.url('🚀 Sahibim', 'https://t.me/Nadjafoovv')]
                    ),
                    link_preview=False
                   )


@client.on(events.NewMessage(pattern="^/all ?(.*)"))
async def mentionall(event):
  global anlik_calisan
  if event.is_private:
    return await event.respond("__Bu əmr qruplarda və kanallarda istifadə edilə bilər.!__")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("__Yalnız idarəçilər hamısını qeyd edə bilər!__")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("__Köhnə yazılar üçün üzvləri qeyd edə bilmərəm! (qrupa əlavə edilməzdən əvvəl göndərilən mesajlar)__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__Mənə bir arqument ver!__")
  else:
    return await event.respond("__Mesajı cavablandırın və ya başqalarını qeyd etmək üçün mənə mətn yazın!__")
    
  if mode == "text_on_cmd":
    anlik_calisan.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        await event.respond("Proses Uğurla Dayandırıldı ❌")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
  
  if mode == "text_on_reply":
    anlik_calisan.append(event.chat_id)
 
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        await event.respond("Proses Uğurla Dayandırıldı ❌")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""


print(">> Bot işləyir narahat olma <<")
client.run_until_disconnected()
