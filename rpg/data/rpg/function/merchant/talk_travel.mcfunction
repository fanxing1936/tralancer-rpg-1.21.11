advancement revoke @s only rpg:merchant/talk_travel
execute if items entity @s weapon.mainhand minecraft:golden_hoe run return run function rpg:merchant/hoe
execute as @e[type=minecraft:villager,tag=rpg.mer.travel,distance=..8,limit=1,sort=nearest] run function rpg:merchant_travel/anim/examine
function rpg:quest/start_4
