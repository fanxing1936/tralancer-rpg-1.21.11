# 寒潮［蓄力］—— 由 rpg:advancement/item/tide 在按住右键期间每刻触发。
# 与包里其余蓄力技能同一节拍：每响一次攒一格，攒满由 tide_trigger 放出。
advancement revoke @s only rpg:item/tide
scoreboard players add @s rpg_tide 1
execute at @s run particle snowflake ~ ~1 ~ 0.4 0.6 0.4 0.03 6
