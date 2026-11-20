tag @s remove rpg.slb.morph
tag @s remove rpg.slb.u1
tag @s remove rpg.slb.u2
tag @s remove rpg.slb.u3
scoreboard players set @s rpg_sl_ur 0
data merge entity @s {NoAI:0b,Invulnerable:0b}
attribute @s minecraft:armor base set 6
attribute @s minecraft:movement_speed base set 0.38
scoreboard players set @s rpg_sl 2
scoreboard players set #stage rpg_sl 2
scoreboard players set @s rpg_sl_c 0
scoreboard players set @s rpg_sl_n 0
scoreboard players set @s rpg_sl_k 0
scoreboard players set @s rpg_sl_cb 0
scoreboard players set @s rpg_sl_sk 0
scoreboard players set @s rpg_sl_b 14
bossbar set rpg:saul_boss name {"text":"\ue2b4\ue275\ue271\ue279","font":"rpg:saul_boss"}
scoreboard players set @s rpg_sl_s 20
function rpg:saul_boss/music/2
