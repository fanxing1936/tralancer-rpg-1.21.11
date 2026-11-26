tag @s remove rpg.dt.hid
execute on passengers if entity @s[type=minecraft:item_display] run data merge entity @s {view_range:1.5f}
execute at @e[type=minecraft:marker,tag=rpg.dt.c,distance=..60,limit=1] run tp @s ~ ~ ~-4
data merge entity @s {Invulnerable:0b}
scoreboard players set #s rpg_dt 60
function rpg:daath_fight/stun
function rpg:daath/look/lit
function rpg:daath_fight/step/fx
