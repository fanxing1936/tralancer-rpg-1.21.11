# 教皇战：计分板与专用血条。由 add_pope_fight.py 生成。
scoreboard objectives add rpg_pf dummy
scoreboard objectives add rpg_pf_l dummy
execute unless score #stage rpg_pf matches 0.. run scoreboard players set #stage rpg_pf 0
bossbar add minecraft:pope {"text":""}
bossbar set minecraft:pope color pink
bossbar set minecraft:pope style progress
scoreboard players set #fifty rpg_pf 50
scoreboard players set #keep rpg_pf 7
scoreboard players set #ten rpg_pf 10
