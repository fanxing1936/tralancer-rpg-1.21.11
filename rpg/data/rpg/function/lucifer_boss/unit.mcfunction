# 载体每刻（as/at 载体）。
execute if entity @s[tag=rpg.lub.end] run return run function rpg:lucifer_boss/finale/tick
# 召唤 NBT 里的 Health 先于属性生效、被原版上限截断；到载体的第一刻再补满（同 inquest/init_health）。
execute if entity @s[tag=!rpg.lub.hp] run return run function rpg:lucifer_boss/hp_init
execute if score #tick rpg_lub matches 0 run function rpg:lucifer_boss/read_hp
scoreboard players operation #m rpg_lub = #tick rpg_lub
scoreboard players set #k rpg_lub 4
scoreboard players operation #m rpg_lub %= #k rpg_lub
execute if score #m rpg_lub matches 0 run function rpg:lucifer_boss/read_hp
execute if score @s rpg_lub matches 1 if score @s rpg_lub_h matches ..1 run return run function rpg:lucifer_boss/stage/end1
execute if score @s rpg_lub matches 2 if score @s rpg_lub_h matches ..1 run return run function rpg:lucifer_boss/stage/end2
function rpg:lucifer_fight/tick
scoreboard players add @s rpg_lub_c 1
function rpg:lucifer_boss/schedule
