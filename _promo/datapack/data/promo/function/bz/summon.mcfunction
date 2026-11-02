# 在你视线前方 10 格召唤别西卜。
scoreboard players set #boss rpg_fall 1
execute positioned ^ ^ ^10 run function rpg:taint/lord4
tellraw @s {"text": "[宣传片] 别西卜已降临。用 promo:bz/cast1..5、promo:bz/ult 点名放招。", "color": "#7A8F22"}
