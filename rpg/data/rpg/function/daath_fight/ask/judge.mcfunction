# 判：站在真的那张牌 3.2 格里
execute if score @s rpg_dt_q matches 0 at @e[type=minecraft:marker,tag=rpg.dt.k0,distance=..60,limit=1] if entity @a[tag=rpg.dt.me,distance=..3.2] run tag @s add rpg.dt.right
execute if score @s rpg_dt_q matches 1 at @e[type=minecraft:marker,tag=rpg.dt.k1,distance=..60,limit=1] if entity @a[tag=rpg.dt.me,distance=..3.2] run tag @s add rpg.dt.right
execute if score @s rpg_dt_q matches 2 at @e[type=minecraft:marker,tag=rpg.dt.k2,distance=..60,limit=1] if entity @a[tag=rpg.dt.me,distance=..3.2] run tag @s add rpg.dt.right
execute as @e[type=minecraft:marker,tag=rpg.dt.km,distance=..60] at @s run function rpg:daath_fight/ask/burst
execute if score @s rpg_dt_q matches 0 at @e[type=minecraft:marker,tag=rpg.dt.k0,distance=..60,limit=1] run function rpg:daath_fight/ask/truth
execute if score @s rpg_dt_q matches 1 at @e[type=minecraft:marker,tag=rpg.dt.k1,distance=..60,limit=1] run function rpg:daath_fight/ask/truth
execute if score @s rpg_dt_q matches 2 at @e[type=minecraft:marker,tag=rpg.dt.k2,distance=..60,limit=1] run function rpg:daath_fight/ask/truth
data merge entity @s {Invulnerable:0b}
execute if entity @s[tag=rpg.dt.right] run return run function rpg:daath_fight/ask/yes
function rpg:daath_fight/ask/no
