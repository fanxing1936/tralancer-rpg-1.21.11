# 震地［蓄力］—— 由 rpg:advancement/item/quake 在按住右键期间每刻触发。
# 与包里其余蓄力技能同一节拍：每响一次攒一格，攒满由 quake_trigger 放出。
advancement revoke @s only rpg:item/quake
scoreboard players add @s rpg_quake 1
execute at @s run particle crit ~ ~1 ~ 0.4 0.6 0.4 0.03 6
