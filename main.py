import re
from pyrogram import Client, filters

app = Client("my_bot", api_id=11965840, api_hash="716c845bdc09adf2b6d36b0b63e4a455", bot_token="6652137531:AAGiK3rAZVBSKOh_aPYzYdIFL-lAnKNhEe4")

print("DONE!")

@app.on_message(filters.command("start"))
def start(client, message):
    user_id = message.from_user.id
    welcome_msg = f"Hello, {message.from_user.first_name}! I am your personal trading bot.\n"
    welcome_msg += "Please provide the Signal:\n\n"
    app.send_message(user_id, welcome_msg)

@app.on_message(filters.text)
def handle_text(client, message):
    user_input = message.text
    pair_msg = r'([A-Z0-9]+)/USDT|([A-Z0-9]+)USDT'
    position_msg = r'LONG|SHORT|Long|Short|long|short'
    leverage_msg = r'Leverage : Cross ([0-9]+x)|LEVERAGE ([0-9]+)|LEVERAGE: ([0-9]+x) - ([0-9]+x)|Leverage: ([0-9]+x)|LEVERAGE([0-9]+)|LEVERAGE:([0-9]+x) - ([0-9]+x)|Leverage:([0-9]+x)'
    entry_msg = r'Entry : ([0-9]+.[0-9]+) - ([0-9]+.[0-9]+)|ENTRY: (\d+)/(\d+)|Entry : ([0-9]+ - [0-9]+)'
    stoploss_msg = r'Stoploss : ([0-9]+.[0-9]+)|STOP LOSS (\d+)%|STOP LOSS: (\d+)%'

    pair_match = re.search(pair_msg,user_input)
    position_match = re.search(position_msg,user_input)
    leverage_match = re.search(leverage_msg,user_input)
    entry_match = re.search(entry_msg,user_input)
    tp_match = re.findall(r'(TP \d+: [0-9]+.[0-9]+)',user_input) or re.findall(r'(Target [0-9]+ - [0-9]+.[0-9]+)',user_input) or re.findall(r'(Target [0-9]+ - [0-9]+)',user_input) or re.findall(r'(TP \d+: [0-9]+)',user_input) 
    stoploss_match = re.search(stoploss_msg,user_input)

    if pair_match and position_match and leverage_match and entry_match and tp_match and stoploss_match:
        pair = pair_match.group()
        position = position_match.group()
        leverage = leverage_match.group()
        entry = entry_match.group()
        tp = tp_match
        stoploss = stoploss_match.group()

        if position.upper() == 'SHORT':
            position_found = '🔴 SHORT'
        elif position.upper() == 'LONG':
            position_found = '🟢 LONG'
        else:
            print("Position Invalid!")

        if leverage:
            leverage_no = re.search(r'[0-9]+',leverage)
            leverage_updated = f"LEVERAGE: {leverage_no.group()}x"
        
        if entry:
            entry_no_data = r'([0-9]+.[0-9]+) - ([0-9]+.[0-9]+)|(\d+)/(\d+)|([0-9]+ - [0-9]+)'
            entry_no = re.search(entry_no_data,entry)
            entry_updated = f"ENTRY: {entry_no.group()}"
        


        if stoploss:
            stoploss_no = re.search(r'[0-9]+.[0-9]+|[0-9]+%|[0-9]+',stoploss)
            stoploss_updated = f"STOPLOSS: {stoploss_no.group()}"

        formatted_msg = f"🏆 {pair} 🏆\n\n{position_found}\n\n⚙ {leverage_updated}\n\n👉 {entry_updated}\n\n"

        if tp:
            for i in range(len(tp)):
                tp_no = re.search(r'[0-9]+.[0-9]+',tp[i]) or re.search(r'[0-9]+ - [0-9]+.[0-9]+',tp[i]) or re.search(r'[0-9]+',tp[i]) or re.findall(r'(Target [0-9]+ - [0-9]+)',user_input)
                tp_update = f"TP {i+1} : {tp_no.group()}"
                formatted_msg += f'🎯 {tp_update}\n'

                
        formatted_msg += f"\n🛑 {stoploss_updated}"

        app.send_message(message.from_user.id,formatted_msg)

    else:
        app.send_message(message.from_user.id,"Invalid Format!")

app.run()




