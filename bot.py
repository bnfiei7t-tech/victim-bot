import telebot
from telebot.types import LabeledPrice, PreCheckoutQuery, InlineKeyboardMarkup, InlineKeyboardButton
import os, sys, sqlite3
from datetime import datetime
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
class C:
    RED='\033[1;91m'; CYAN='\033[1;96m'; PURPLE='\033[1;95m'; RESET='\033[0m'
BOT_TOKEN="8665194499:AAHm5UsiV_0qjOENnoNT3hntp8E-DMYNBOc"
ADMIN_ID=7495006225
DEV_NAME="FOLK"
DEV_USER="@c_0gj"
DEV_CHANNEL="https://t.me/llll_lIll"
bot=telebot.TeleBot(BOT_TOKEN)
conn=sqlite3.connect("victims.db",check_same_thread=False)
cur=conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS cases (id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,case_type TEXT,case_key TEXT,status TEXT DEFAULT 'new',created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
cur.execute("CREATE TABLE IF NOT EXISTS evidence (id INTEGER PRIMARY KEY AUTOINCREMENT,case_id INTEGER,file_id TEXT,file_type TEXT,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
cur.execute("CREATE TABLE IF NOT EXISTS donations (id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,amount INTEGER,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
conn.commit()
def H(t):
    return "\n🔴🟣🔵🔴🟣🔵🔴🟣🔵🔴🟣🔵🔴🟣🔵🔴\n   『 FOLK 』 • "+t+"\n🔴🟣🔵🔴🟣🔵🔴🟣🔵🔴🟣🔵🔴🟣🔵🔴\n"
def credit():
    return "\n━━━━━━━━━━━━━━━━━━━━━\n💎 المطور: FOLK\n📛 "+DEV_USER+"\n📢 قناتنا: "+DEV_CHANNEL+"\n"
def addD(m):
    m.add(InlineKeyboardButton("💚 ادعم البوت بنجوم",callback_data="donate_menu"))
    return m
def mainM():
    m=InlineKeyboardMarkup(row_width=2)
    m.add(InlineKeyboardButton("🆘 أنا ضحية",callback_data="victim_start"),InlineKeyboardButton("📊 حالتي",callback_data="my_cases"))
    m.add(InlineKeyboardButton("📎 حفظ أدلة",callback_data="save_evidence"),InlineKeyboardButton("👨‍⚖️ مختص",callback_data="expert_menu"))
    m.add(InlineKeyboardButton("🚨 SOS طوارئ",callback_data="sos"),InlineKeyboardButton("📞 جهات رسمية",callback_data="authorities"))
    m.add(InlineKeyboardButton("📚 تعلّم الحماية",callback_data="learn"),InlineKeyboardButton("ℹ️ عن البوت",callback_data="about"))
    m.add(InlineKeyboardButton("💎 المطور",callback_data="developer"),InlineKeyboardButton("📢 قناتنا",url=DEV_CHANNEL))
    return addD(m)
def caseT():
    m=InlineKeyboardMarkup(row_width=2)
    m.add(InlineKeyboardButton("📸 تهديد بصور",callback_data="ct_photos"),InlineKeyboardButton("💰 طلب فدية",callback_data="ct_money"))
    m.add(InlineKeyboardButton("🔓 اختراق حساب",callback_data="ct_hack"),InlineKeyboardButton("📱 اختراق هاتف",callback_data="ct_phone"))
    m.add(InlineKeyboardButton("💳 احتيال مالي",callback_data="ct_fraud"),InlineKeyboardButton("😡 مضايقة",callback_data="ct_harass"))
    m.add(InlineKeyboardButton("❓ شيء آخر",callback_data="ct_other"),InlineKeyboardButton("🔙 رجوع",callback_data="back_main"))
    return addD(m)
CASES={"photos":("📸 تهديد بنشر صور","تهديد بنشر الصور"),"money":("💰 طلب فدية","طلب فدية مالية"),"hack":("🔓 اختراق حساب","اختراق حساب"),"phone":("📱 اختراق هاتف","اختراق هاتف"),"fraud":("💳 احتيال مالي","احتيال مالي"),"harass":("😡 مضايقة","مضايقة إلكترونية"),"other":("❓ أخرى","حالة أخرى")}
STEPS={"photos":"🚨 خطوات فورية:\n\n1️⃣ لا تدفعي أي مال ❌\n2️⃣ لا تحذفي المحادثات ❌\n3️⃣ احفظي كل الأدلة\n4️⃣ لا تتفاعلي معه\n5️⃣ أبلغي: 104","money":"🚨 خطوات فورية:\n\n1️⃣ لا تدفعي ❌\n2️⃣ احفظي الأرقام\n3️⃣ احفظي طرق الدفع\n4️⃣ أبلغي: 104","hack":"🚨 خطوات فورية:\n\n1️⃣ غيّري كلمة المرور\n2️⃣ فعّلي 2FA\n3️⃣ سجّلي خروج\n4️⃣ أبلغي عن الحساب","phone":"🚨 خطوات فورية:\n\n1️⃣ أغلقي الإنترنت\n2️⃣ لا تفتحي التطبيقات\n3️⃣ صوّري الشاشة\n4️⃣ أبلغي: 104","fraud":"🚨 خطوات فورية:\n\n1️⃣ أوقفي التحويلات\n2️⃣ احفظي الإيصالات\n3️⃣ أبلغي البنك","harass":"🚨 خطوات فورية:\n\n1️⃣ احظري المضايق\n2️⃣ احفظي الأدلة\n3️⃣ أبلغي المنصة","other":"🚨 خطوات عامة:\n\n1️⃣ لا تدفعي\n2️⃣ احفظي الأدلة\n3️⃣ أبلغي: 104"}
US={}


def c_start(message):
    name=message.from_user.first_name or "صديقنا"
    text=H("💚 مرحباً "+name)+"\nأنا هنا لمساعدتك.\n💚 أنت لست وحدك.\n\n━━━━━━━━━━━━━━━━━━━━━\nاختر حالتك:\n"+credit()
    bot.send_message(message.chat.id,text,reply_markup=mainM())
    print(C.CYAN+"[+] /start ← "+name+C.RESET)
bot.message_handler(commands=['start','menu'])(c_start)

def c_back(call):
    bot.edit_message_text(H("🔥 القائمة الرئيسية")+"\n🔽 اختر:"+credit(),call.message.chat.id,call.message.message_id,reply_markup=mainM())
    bot.answer_callback_query(call.id)
bot.callback_query_handler(func=lambda c:c.data=="back_main")(c_back)

def c_victim(call):
    text=H("💚 أنت في المكان الصحيح")+"\n💚 اهدئ\n\nاعلم:\n\n✅ ليس ذنبك\n✅ المبتز مجرم\n✅ القانون معك\n✅ لن تدفعي\n\n━━━━━━━━━━━━━━━━━━━━━\n⚠️ مهم:\n\n1. لا تدفعي ❌\n2. لا تحذفي ❌\n3. لا تتفاوضي ❌\n4. لا تعتذري ❌\n\n━━━━━━━━━━━━━━━━━━━━━\n🔽 اختر:\n"+credit()
    bot.edit_message_text(text,call.message.chat.id,call.message.message_id,reply_markup=caseT())
    bot.answer_callback_query(call.id)
bot.callback_query_handler(func=lambda c:c.data=="victim_start")(c_victim)

def c_case(call):
    key=call.data.replace("ct_","")
    name,dbn=CASES.get(key,("❓","حالة"))
    cur.execute("INSERT INTO cases (user_id,case_type,case_key) VALUES (?,?,?)",(call.from_user.id,dbn,key))
    conn.commit()
    cid=cur.lastrowid
    text=H("📁 حالة #"+str(cid))+"\n"+name+"\n\n"+STEPS.get(key,STEPS["other"])+"\n━━━━━━━━━━━━━━━━━━━━━\n✅ حالة #"+str(cid)+"\n"+credit()
    m=InlineKeyboardMarkup(row_width=2)
    m.add(InlineKeyboardButton("📎 حفظ الأدلة",callback_data="ev_"+str(cid)),InlineKeyboardButton("👨‍⚖️ مختص",callback_data="ex_"+str(cid)))
    m.add(InlineKeyboardButton("📞 جهات رسمية",callback_data="authorities"),InlineKeyboardButton("🔙 رجوع",callback_data="back_main"))
    addD(m)
    bot.edit_message_text(text,call.message.chat.id,call.message.message_id,reply_markup=m)
    bot.answer_callback_query(call.id,"✅ #"+str(cid))
bot.callback_query_handler(func=lambda c:c.data.startswith("ct_"))(c_case)

def c_ev(call):
    cid=int(call.data.split("_")[1])
    US[call.from_user.id]={"case_id":cid,"mode":"evidence"}
    text=H("📎 حفظ الأدلة — #"+str(cid))+"\n📸 أرسلي:\n\n1. لقطات شاشة\n2. رقم المبتز\n3. حسابه\n4. صور التهديد\n\n━━━━━━━━━━━━━━━━━━━━━\n⚠️ مشفر\n\nلإيقاف: /stop\n"+credit()
    m=InlineKeyboardMarkup()
    m.add(InlineKeyboardButton("✅ تم",callback_data="ev_done_"+str(cid)))
    addD(m)
    bot.edit_message_text(text,call.message.chat.id,call.message.message_id,reply_markup=m)
    bot.answer_callback_query(call.id)
bot.callback_query_handler(func=lambda c:c.data.startswith("ev_") and not c.data.startswith("ev_done_"))(c_ev)

def h_ev(message):
    st=US.get(message.from_user.id)
    if not st or st.get("mode")!="evidence": return
    cid=st["case_id"]
    if message.photo: fid,ft=message.photo[-1].file_id,"📸 صورة"
    elif message.video: fid,ft=message.video.file_id,"🎥 فيديو"
    elif message.document: fid,ft=message.document.file_id,"📄 ملف"
    elif message.voice: fid,ft=message.voice.file_id,"🎤 صوت"
    elif message.audio: fid,ft=message.audio.file_id,"🎵 صوتية"
    else: return
    cur.execute("INSERT INTO evidence (case_id,file_id,file_type) VALUES (?,?,?)",(cid,fid,ft))
    conn.commit()
    try:
        bot.forward_message(ADMIN_ID,message.chat.id,message.message_id)
        bot.send_message(ADMIN_ID,"📎 دليل — #"+str(cid)+" ("+ft+")")
    except: pass
    m=InlineKeyboardMarkup()
    m.add(InlineKeyboardButton("📎 المزيد",callback_data="ev_"+str(cid)),InlineKeyboardButton("✅ انتهيت",callback_data="ev_done_"+str(cid)))
    addD(m)
    bot.reply_to(message,"✅ تم حفظ "+ft+" — #"+str(cid),reply_markup=m)


def c_ev_done(call):
    cid=int(call.data.split("_")[2])
    US.pop(call.from_user.id,None)
    cur.execute("SELECT COUNT(*) FROM evidence WHERE case_id=?",(cid,))
    count=cur.fetchone()[0]
    text=H("✅ تم حفظ الأدلة")+"\n📁 #"+str(cid)+"\n📎 عدد: "+str(count)+"\n\n━━━━━━━━━━━━━━━━━━━━━\nما التالي؟\n"+credit()
    m=InlineKeyboardMarkup(row_width=2)
    m.add(InlineKeyboardButton("👨‍⚖️ مختص",callback_data="ex_"+str(cid)),InlineKeyboardButton("📞 جهات",callback_data="authorities"))
    m.add(InlineKeyboardButton("🔙 القائمة",callback_data="back_main"))
    addD(m)
    bot.edit_message_text(text,call.message.chat.id,call.message.message_id,reply_markup=m)
    bot.answer_callback_query(call.id)
bot.callback_query_handler(func=lambda c:c.data.startswith("ev_done_"))(c_ev_done)

def c_backcase(call):
    cid=int(call.data.split("_")[2])
    text=H("📁 #"+str(cid))+"\n🔽 اختر:"
    m=InlineKeyboardMarkup(row_width=2)
    m.add(InlineKeyboardButton("📎 حفظ الأدلة",callback_data="ev_"+str(cid)),InlineKeyboardButton("👨‍⚖️ مختص",callback_data="ex_"+str(cid)))
    m.add(InlineKeyboardButton("📞 جهات",callback_data="authorities"),InlineKeyboardButton("🔙 رجوع",callback_data="back_main"))
    addD(m)
    bot.edit_message_text(text,call.message.chat.id,call.message.message_id,reply_markup=m)
    bot.answer_callback_query(call.id)
bot.callback_query_handler(func=lambda c:c.data.startswith("back_case_"))(c_backcase)

def showExp(call,cid):
    text=H("👨‍⚖️ مختص")+"\n📁 #"+str(cid)+"\n\n👩‍⚖️ محامية\n🧑‍💻 خبير سيبراني\n👩‍⚕️ دعم نفسي\n\n━━━━━━━━━━━━━━━━━━━━━\nاختر:\n"
    m=InlineKeyboardMarkup(row_width=2)
    m.add(InlineKeyboardButton("👩‍⚖️ محامية",callback_data="exp_law_"+str(cid)),InlineKeyboardButton("🧑‍💻 خبير",callback_data="exp_tech_"+str(cid)))
    m.add(InlineKeyboardButton("👩‍⚕️ نفسي",callback_data="exp_psy_"+str(cid)),InlineKeyboardButton("👥 الكل",callback_data="exp_all_"+str(cid)))
    m.add(InlineKeyboardButton("🔙 رجوع",callback_data="back_case_"+str(cid)))
    addD(m)
    bot.edit_message_text(text,call.message.chat.id,call.message.message_id,reply_markup=m)
    bot.answer_callback_query(call.id)

def c_expM(call):
    cur.execute("SELECT id FROM cases WHERE user_id=? ORDER BY id DESC LIMIT 1",(call.from_user.id,))
    r=cur.fetchone()
    showExp(call,r[0] if r else 0)
bot.callback_query_handler(func=lambda c:c.data=="expert_menu")(c_expM)

def c_ex(call):
    cid=int(call.data.split("_")[1])
    showExp(call,cid)
bot.callback_query_handler(func=lambda c:c.data.startswith("ex_"))(c_ex)

def c_expContact(call):
    parts=call.data.split("_")
    et=parts[1]
    cid=int(parts[2])
    types={"law":"👩‍⚖️ محامية","tech":"🧑‍💻 خبير","psy":"👩‍⚕️ نفسي","all":"👥 الفريق"}
    label=types.get(et,"مختص")
    try:
        bot.send_message(ADMIN_ID,"🔔 مختص\n📁 #"+str(cid)+"\n👤 "+label+"\n🆔 "+str(call.from_user.id),reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("💬 تواصل",url="tg://user?id="+str(call.from_user.id))))
    except: pass
    text=H("✅ تم الإرسال")+"\n📁 #"+str(cid)+"\n👤 "+label+"\n\n━━━━━━━━━━━━━━━━━━━━━\n⏱️ خلال 5-10 دقائق\n\n💚 أنتِ شجاعة\n"+credit()
    m=InlineKeyboardMarkup()
    m.add(InlineKeyboardButton("📚 حقوقك",callback_data="learn_rights"))
    m.add(InlineKeyboardButton("🔙 القائمة",callback_data="back_main"))
    addD(m)
    bot.edit_message_text(text,call.message.chat.id,call.message.message_id,reply_markup=m)
    bot.answer_callback_query(call.id,"✅")
bot.callback_query_handler(func=lambda c:c.data.startswith("exp_"))(c_expContact)

def c_auth(call):
    text=H("📞 الجهات الرسمية")+"\n🏛️ السيبرانية: 104\n🏛️ الجريمة: 133\n🏛️ الطوارئ: 911\n\n━━━━━━━━━━━━━━━━━━━━━\n📋 قول:\nأنا ضحية ابتزاز، لدي أدلة\n\n⚠️ اذهبي مع شخص تثقين به\n"+credit()
    m=InlineKeyboardMarkup()
    m.add(InlineKeyboardButton("📞 104",url="tel:104"))
    m.add(InlineKeyboardButton("📞 133",url="tel:133"))
    m.add(InlineKeyboardButton("🔙 القائمة",callback_data="back_main"))
    addD(m)
    bot.edit_message_text(text,call.message.chat.id,call.message.message_id,reply_markup=m)
    bot.answer_callback_query(call.id)
bot.callback_query_handler(func=lambda c:c.data=="authorities")(c_auth)

def c_sos(call):
    try:
        bot.send_message(ADMIN_ID,"🚨 SOS!\n🆔 "+str(call.from_user.id)+"\n📛 @"+(call.from_user.username or "بدون")+"\n🕐 "+datetime.now().strftime("%H:%M:%S"),reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("💬 تواصل",url="tg://user?id="+str(call.from_user.id))))
    except: pass
    text=H("🚨 SOS - تم")+"\n✅ إشارة طوارئ\n📞 خلال دقيقة\n\n💚 ابقي هادئة\n"+credit()
    m=InlineKeyboardMarkup()
    m.add(InlineKeyboardButton("🔙 القائمة",callback_data="back_main"))
    addD(m)
    bot.send_message(call.message.chat.id,text,reply_markup=m)
    bot.answer_callback_query(call.id,"🚨")
bot.callback_query_handler(func=lambda c:c.data=="sos")(c_sos)

def c_myc(call):
    cur.execute("SELECT id,case_type,status,created_at FROM cases WHERE user_id=? ORDER BY id DESC LIMIT 10",(call.from_user.id,))
    rows=cur.fetchall()
    if not rows: text=H("📊 حالاتي")+"\n❌ لا توجد"
    else:
        text=H("📊 حالاتي")+"\n"
        for r in rows:
            text=text+"📁 #"+str(r[0])+" • "+str(r[1])+"\n   "+str(r[2])+" • "+str(r[3])[:10]+"\n\n"
    m=InlineKeyboardMarkup()
    m.add(InlineKeyboardButton("🆘 جديدة",callback_data="victim_start"))
    m.add(InlineKeyboardButton("🔙 القائمة",callback_data="back_main"))
    addD(m)
    bot.edit_message_text(text,call.message.chat.id,call.message.message_id,reply_markup=m)
    bot.answer_callback_query(call.id)
bot.callback_query_handler(func=lambda c:c.data=="my_cases")(c_myc)

def c_learn(call):
    text=H("📚 تعلّم الحماية")+"\n🛡️ نصائح:\n\n1️⃣ فعّلي 2FA\n2️⃣ لا تشاركي صوراً\n3️⃣ كلمات مرور قوية\n4️⃣ لا تفتحي روابط مجهولة\n5️⃣ حدّثي التطبيقات\n6️⃣ لا تقبلي صداقات مجهولة\n\n━━━━━━━━━━━━━━━━━━━━━\n🚨 علامات الاختراق:\n• بطارية تنفد بسرعة\n• بيانات كثيرة\n• تطبيقات غريبة\n"+credit()
    m=InlineKeyboardMarkup(row_width=1)
    m.add(InlineKeyboardButton("📖 حقوقك القانونية",callback_data="learn_rights"))
    m.add(InlineKeyboardButton("🎯 ما هو الابتزاز؟",callback_data="learn_def"))
    m.add(InlineKeyboardButton("💚 كيف أحمي نفسي؟",callback_data="learn_protect"))
    m.add(InlineKeyboardButton("🔙 القائمة",callback_data="back_main"))
    addD(m)
    bot.edit_message_text(text,call.message.chat.id,call.message.message_id,reply_markup=m)
    bot.answer_callback_query(call.id)
bot.callback_query_handler(func=lambda c:c.data=="learn")(c_learn)

def c_learnSub(call):
    sub=call.data.replace("learn_","")
    rights="📖 حقوقك القانونية\n━━━━━━━━━━━━━━━━━━━━━\n\n🇮🇶 في القانون العراقي:\n\n✅ الابتزاز الإلكتروني جريمة\n   (قانون 175 لسنة 1969)\n\n✅ عقوبة المبتز:\n   • حبس 3-15 سنة\n   • غرامة مالية كبيرة\n\n✅ حقوقك:\n   • تقديم بلاغ مجاني\n   • الحصول على محامي\n   • حماية هويتك\n   • التعويض"
    defn="🎯 ما هو الابتزاز؟\n━━━━━━━━━━━━━━━━━━━━━\n\n🎯 تعريف:\n\nاستخدام التهديد أو الإكراه\nللحصول على:\n• مال\n• خدمات\n• صور إضافية\n• تنازلات\n\n━━━━━━━━━━━━━━━━━━━━━\n📊 أنواعه:\n1. ابتزاز صور\n2. ابتزاز مالي\n3. ابتزاز جنسي\n4. ابتزاز إلكتروني\n\n━━━━━━━━━━━━━━━━━━━━━\n⚠️ لا تقعي في الفخ:\n• لا تدفعي ❌\n• لا تتفاوضي ❌\n• أبلغي فوراً ✅"
    prot="💚 كيف أحمي نفسي؟\n━━━━━━━━━━━━━━━━━━━━━\n\n💚 الحماية:\n\n1️⃣ الوعي\n   • معرفة الأنماط\n   • الحذر من الغرباء\n\n2️⃣ الأمان الرقمي\n   • 2FA\n   • كلمات مرور قوية\n   • تحديثات دورية\n\n3️⃣ الخصوصية\n   • لا صور خاصة\n   • لا معلومات شخصية\n   • لا ثقة عمياء\n\n━━━━━━━━━━━━━━━━━━━━━\n🚨 إذا حدث:\n• لا تخافي\n• احفظي الأدلة\n• أبلغي فوراً"
    content={"rights":("📖 حقوقك القانونية",rights),"def":("🎯 ما هو الابتزاز؟",defn),"protect":("💚 كيف أحمي نفسي؟",prot)}
    title,body=content.get(sub,("📚 معلومة","لا يوجد محتوى"))
    text=H(title)+"\n"+body+credit()
    m=InlineKeyboardMarkup()
    m.add(InlineKeyboardButton("🔙 رجوع",callback_data="learn"))
    m.add(InlineKeyboardButton("🏠 القائمة",callback_data="back_main"))
    addD(m)
    bot.edit_message_text(text,call.message.chat.id,call.message.message_id,reply_markup=m)
    bot.answer_callback_query(call.id)
bot.callback_query_handler(func=lambda c:c.data.startswith("learn_"))(c_learnSub)

def c_dev(call):
    text=H("💎 المطور")+"\n\n💎 الاسم: FOLK\n📛 اليوزر: "+DEV_USER+"\n📢 القناة: "+DEV_CHANNEL+"\n\n━━━━━━━━━━━━━━━━━━━━━\n💚 شكراً لدعمك\n"
    m=InlineKeyboardMarkup()
    m.add(InlineKeyboardButton("📢 قناتنا",url=DEV_CHANNEL))
    m.add(InlineKeyboardButton("🔙 رجوع",callback_data="back_main"))
    addD(m)
    bot.edit_message_text(text,call.message.chat.id,call.message.message_id,reply_markup=m)
    bot.answer_callback_query(call.id)
bot.callback_query_handler(func=lambda c:c.data=="developer")(c_dev)

def c_about(call):
    text=H("ℹ️ عن البوت")+"\n🛡️ FOLK Victim Support\n\n💎 المطور: FOLK\n📛 "+DEV_USER+"\n📢 "+DEV_CHANNEL+"\n\n━━━━━━━━━━━━━━━━━━━━━\n🎯 هدفنا:\nمساعدة ضحايا الابتزاز\n\n━━━━━━━━━━━━━━━━━━━━━\n📞 للطوارئ:\n• سيبراني: 104\n• عام: 911\n\n━━━━━━━━━━━━━━━━━━━━━\n💚 البوت مجاني 100%\n"
    m=InlineKeyboardMarkup()
    m.add(InlineKeyboardButton("🔙 رجوع",callback_data="back_main"))
    addD(m)
    bot.edit_message_text(text,call.message.chat.id,call.message.message_id,reply_markup=m)
    bot.answer_callback_query(call.id)
bot.callback_query_handler(func=lambda c:c.data=="about")(c_about)

def c_saveEv(call):
    cur.execute("SELECT id FROM cases WHERE user_id=? ORDER BY id DESC LIMIT 1",(call.from_user.id,))
    r=cur.fetchone()
    if not r:
        bot.answer_callback_query(call.id,"❌ ابدأي بحالة أولاً",show_alert=True)
        return
    cid=r[0]
    US[call.from_user.id]={"case_id":cid,"mode":"evidence"}
    text=H("📎 حفظ الأدلة — #"+str(cid))+"\n📸 أرسلي:\n\n1. لقطات شاشة\n2. رقم المبتز\n3. حسابه\n4. صور التهديد\n\n━━━━━━━━━━━━━━━━━━━━━\n⚠️ مشفر بالكامل\n\nلإيقاف: /stop\n"+credit()
    m=InlineKeyboardMarkup()
    m.add(InlineKeyboardButton("✅ انتهيت",callback_data="ev_done_"+str(cid)))
    addD(m)
    bot.send_message(call.message.chat.id,text,reply_markup=m)
    bot.answer_callback_query(call.id)
bot.callback_query_handler(func=lambda c:c.data=="save_evidence")(c_saveEv)

def c_donM(call):
    text=H("💚 دعم البوت")+"\n🌟 مجاني 100% للضحايا\n🌟 دعمك يساعدنا:\n   • استمرار الخدمة\n   • مساعدة المزيد\n   • تطوير الميزات\n\n━━━━━━━━━━━━━━━━━━━━━\n💰 اختر المبلغ (نجوم):\n"
    m=InlineKeyboardMarkup(row_width=3)
    amounts=[15,50,100,250,500,1000,2500,5000]
    for a in amounts:
        m.add(InlineKeyboardButton("⭐ "+str(a),callback_data="don_"+str(a)))
    m.add(InlineKeyboardButton("💰 مبلغ مخصص",callback_data="don_custom"))
    m.add(InlineKeyboardButton("🔙 رجوع",callback_data="back_main"))
    bot.edit_message_text(text,call.message.chat.id,call.message.message_id,reply_markup=m)
    bot.answer_callback_query(call.id)
bot.callback_query_handler(func=lambda c:c.data=="donate_menu")(c_donM)

def c_don(call):
    if call.data=="don_custom":
        msg=bot.send_message(call.message.chat.id,"💰 أدخل العدد (15-10000):")
        bot.register_next_step_handler(msg,custDon)
        bot.answer_callback_query(call.id)
        return
    try: amt=int(call.data.replace("don_",""))
    except: return
    sendInv(call.message.chat.id,amt)
    bot.answer_callback_query(call.id,"⭐ "+str(amt))
bot.callback_query_handler(func=lambda c:c.data.startswith("don_"))(c_don)

def custDon(message):
    try:
        amt=int(message.text.strip())
        if amt<15 or amt>10000:
            bot.reply_to(message,"❌ الحد بين 15 و 10000")
            return
        sendInv(message.chat.id,amt)
    except ValueError:
        bot.reply_to(message,"❌ أدخل رقماً صحيحاً")

def sendInv(chat_id,amount):
    try:
        bot.send_invoice(chat_id=chat_id,title="💚 دعم بوت مساعدة الضحايا",description="تبرع بـ "+str(amount)+" نجمة",invoice_payload="donation_"+str(amount),provider_token="",currency="XTR",prices=[LabeledPrice(label="تبرع",amount=amount)],start_parameter="donate")
    except Exception as e:
        bot.send_message(chat_id,"❌ خطأ: "+str(e))

def checkout(q:PreCheckoutQuery):
    bot.answer_pre_checkout_query(q.id,ok=True)
bot.pre_checkout_query_handler(func=lambda q:True)(checkout)

def payment(message):
    p=message.successful_payment
    amt=p.total_amount
    user=message.from_user
    cur.execute("INSERT INTO donations (user_id,amount) VALUES (?,?)",(user.id,amt))
    conn.commit()
    text=H("✅ تم استلام تبرعك!")+"\n⭐ "+str(amt)+"\n💚 شكراً "+(user.first_name or "")+"\n\n🌟 أنت بطل حقيقي 🌟\n"+credit()
    bot.send_message(message.chat.id,text,reply_markup=mainM())
    try:
        bot.send_message(ADMIN_ID,"💰 تبرع: "+str(amt)+" ⭐\n👤 "+(user.first_name or ""))
    except: pass
bot.message_handler(content_types=['successful_payment'])(payment)

def c_stop(message):
    US.pop(message.from_user.id,None)
    bot.send_message(message.chat.id,"✅ تم الإنهاء",reply_markup=mainM())
bot.message_handler(commands=['stop'])(c_stop)

def c_admin(message):
    if message.from_user.id!=ADMIN_ID: return
    cur.execute("SELECT COUNT(*) FROM cases"); t=cur.fetchone()[0]
    cur.execute("SELECT SUM(amount) FROM donations"); s=cur.fetchone()[0] or 0
    cur.execute("SELECT COUNT(DISTINCT user_id) FROM donations"); d=cur.fetchone()[0]
    text=H("👑 لوحة المشرف")+"\n📁 الحالات: "+str(t)+"\n⭐ النجوم: "+str(s)+"\n👥 المتبرعون: "+str(d)+"\n"
    bot.send_message(message.chat.id,text)
bot.message_handler(commands=['admin'])(c_admin)

def c_help(message):
    text=H("📚 مساعدة")+"\n🆘 ضحية ← خطوات فورية\n📎 حفظ أدلة\n👨‍⚖️ مختص\n🚨 SOS\n📞 جهات رسمية\n📚 تعلّم\n💚 دعم\n"+credit()
    bot.send_message(message.chat.id,text,reply_markup=mainM())
bot.message_handler(commands=['help'])(c_help)

if __name__=="__main__":
    os.system('clear')
    print(C.RED+"╔═════════════════════════════════════════════╗")
    print(C.CYAN+"║   "+C.PURPLE+"FOLK Victim Support Bot v6.0"+C.CYAN+"           ║")
    print(C.CYAN+"╚═════════════════════════════════════════════╝"+C.RESET)
    print(C.CYAN+"[+]"+C.RESET+" المشرف: "+C.RED+str(ADMIN_ID)+C.RESET)
    print(C.RED+"[*]"+C.RESET+" البوت يعمل...")
    bot.infinity_polling()
bot.message_handler(content_types=['photo','video','document','voice','audio'])(h_ev)
