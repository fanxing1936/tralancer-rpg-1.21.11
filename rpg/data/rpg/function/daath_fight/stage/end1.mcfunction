# 一段打空：跪下，面具裂开（as/at 影子）
function rpg:daath_fight/sk/end
function rpg:daath_fight/unit/refill
tag @s add rpg.dt.morph
scoreboard players set @s rpg_dt_t 0
data merge entity @s {NoAI:1b,Invulnerable:1b}
execute if score @s rpg_dt_sw matches 1.. run function rpg:daath_fight/steal/lose_w
execute if score @s rpg_dt_sa matches 1.. run function rpg:daath_fight/steal/lose_a
function rpg:daath_fight/eye/off
kill @e[type=minecraft:zombie,tag=rpg.dt.minion,distance=..60]
tag @s remove rpg.dt.loop
function rpg:daath_fight/lamp/all_out
function rpg:daath/anim/enter/kneel
execute facing entity @p[tag=rpg.dt.me] feet rotated ~ 0 run rotate @s ~ ~
playsound minecraft:block.glass.break hostile @a[distance=..48] ~ ~ ~ 1.4 0.5
