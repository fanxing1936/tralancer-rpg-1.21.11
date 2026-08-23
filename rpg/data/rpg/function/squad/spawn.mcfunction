# 在雇主身前两格把人召出来。
execute at @s anchored eyes positioned ^ ^ ^2 run function rpg:squad/spawn_at
scoreboard players add @s rpg_sq_n 1
function rpg:hud/m17
playsound minecraft:entity.villager.yes player @s ~ ~ ~ 1 1
playsound minecraft:block.anvil_use player @a[distance=..12] ~ ~ ~ 0.6 1.4
