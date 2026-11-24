advancement revoke @s only rpg:merchant/talk_luxury
execute if items entity @s weapon.mainhand minecraft:golden_hoe run return run function rpg:merchant/hoe
execute as @e[type=minecraft:villager,tag=rpg.mer.luxury,distance=..8,limit=1,sort=nearest] run function rpg:merchant_luxury/anim/examine
