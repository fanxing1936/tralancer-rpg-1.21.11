# 每秒：不在试炼里却还有东西没还的人（服务器重启、异常）
schedule function rpg:daath_fight/sec 20t
execute as @a unless score @s rpg_dt matches 1.. if score @s rpg_dt_got matches 1.. run function rpg:daath_fight/steal/late
# 场次早没了人还留在深渊里：送回主世界
execute in rpg:daath as @a[distance=0..] unless score @s rpg_dt matches 1.. run function rpg:daath_fight/pl/stray_home
