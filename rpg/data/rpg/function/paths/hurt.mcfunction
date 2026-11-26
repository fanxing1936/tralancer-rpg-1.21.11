advancement revoke @s only rpg:paths/hurt
execute unless score @s rpg_ps_22 matches 3 run return 0
tag @s add rpg.pa.me
execute on attacker if entity @s[distance=..5] run damage @s 1 minecraft:thorns by @p[tag=rpg.pa.me]
tag @s remove rpg.pa.me
