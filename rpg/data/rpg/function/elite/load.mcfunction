scoreboard objectives add rpg_el dummy
scoreboard objectives add rpg_el_a1 dummy
scoreboard objectives add rpg_el_a2 dummy
scoreboard objectives add rpg_el_kill dummy
scoreboard objectives add rpg_el_t dummy
scoreboard players set #2 rpg_el 2
scoreboard players set #3 rpg_el 3
scoreboard players set #5 rpg_el 5
scoreboard players set #10 rpg_el 10
scoreboard players set #100 rpg_el 100
scoreboard players set #13 rpg_fo 13
# 首领血条：和正式 Boss 同一套位图横幅（add_elite_bar_art.py）；原版粉色血条贴图是透明的。
# 横幅、王冠与词缀图标、花体英文名合成一条，名字在横幅下方（与正式 Boss 的标题同位）
bossbar remove rpg:elite_champion
bossbar add rpg:elite_champion_bar ""
bossbar set rpg:elite_champion_bar color pink
