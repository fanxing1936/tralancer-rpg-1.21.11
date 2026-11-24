advancement revoke @s only rpg:merchant/trade_travel
execute as @e[type=minecraft:villager,tag=rpg.mer.travel,distance=..8,limit=1,sort=nearest] run function rpg:merchant_travel/anim/bow
