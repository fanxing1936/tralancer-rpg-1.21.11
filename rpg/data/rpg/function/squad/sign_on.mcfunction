# 钱付了，把眼前那个待雇者收编。
execute as @e[type=minecraft:husk,tag=rpg.sq.free,distance=..6,limit=1,sort=nearest] run function rpg:squad/sign_one
function rpg:hud/m49
playsound minecraft:entity.villager.yes player @s ~ ~ ~ 1 1
playsound minecraft:block.anvil_use player @a[distance=..12] ~ ~ ~ 0.6 1.4
