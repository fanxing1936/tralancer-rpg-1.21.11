# 在你视线前方 10 格召唤路西法。
scoreboard players set #boss rpg_fall 1
execute positioned ^ ^ ^10 run function rpg:taint/lord1
tellraw @s {"text": "[宣传片] 路西法已降临。用 promo:lucifer/cast1..5、promo:lucifer/ult 点名放招。", "color": "#2FA05A"}
