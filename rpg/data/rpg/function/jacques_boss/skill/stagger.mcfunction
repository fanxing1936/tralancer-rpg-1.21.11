scoreboard players set @s rpg_jq_sk 11
scoreboard players set @s rpg_jq_t 0
scoreboard players set @s rpg_jq_busy 62
data merge entity @s {NoAI:1b,Invulnerable:0b,NoGravity:0b}
attribute @s minecraft:armor base set 0
function rpg:jacques/weapon/glaive
function rpg:jacques/anim/enter/stun
