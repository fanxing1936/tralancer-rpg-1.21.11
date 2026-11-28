tag @s remove rpg.mkb.morph
tag @s remove rpg.mkb.u1
tag @s remove rpg.mkb.u2
tag @s remove rpg.mkb.u3
scoreboard players set @s rpg_mk_ur 0
data merge entity @s {NoAI:0b,Invulnerable:0b}
attribute @s minecraft:armor base set 8
attribute @s minecraft:movement_speed base set 0.36
scoreboard players set @s rpg_mk_i3 2
scoreboard players set #stage rpg_mk_i3 2
scoreboard players set @s rpg_mk_c 0
scoreboard players set @s rpg_mk_n 0
scoreboard players set @s rpg_mk_k 0
scoreboard players set @s rpg_mk_cb 0
scoreboard players set @s rpg_mk_sk 0
scoreboard players set @s rpg_mk_b 14
bossbar set rpg:michael_boss_i3 name {"text":"\ue334\ue2f5\ue2f1\ue2f9","font":"rpg:michael_boss"}
scoreboard players set @s rpg_mk_s 20
function rpg:michael_boss_i3/music/2
