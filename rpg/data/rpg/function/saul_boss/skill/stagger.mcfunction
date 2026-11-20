scoreboard players set @s rpg_sl_sk 12
scoreboard players set @s rpg_sl_t 0
scoreboard players set @s rpg_sl_busy 42
data merge entity @s {NoAI:1b,Invulnerable:0b,NoGravity:0b}
attribute @s minecraft:armor base set 0
function rpg:saul/anim/enter/stun
