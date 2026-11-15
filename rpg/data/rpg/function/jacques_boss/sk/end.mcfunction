scoreboard players set @s rpg_jq_sk 0
scoreboard players set @s rpg_jq_busy 0
data merge entity @s {NoAI:0b,NoGravity:0b,Invulnerable:0b}
attribute @s minecraft:armor base set 10
function rpg:jacques/weapon/glaive
