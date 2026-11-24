advancement revoke @s only rpg:merchant/trade_smith
execute as @e[type=minecraft:villager,tag=rpg.mer.smith,distance=..8,limit=1,sort=nearest] run function rpg:merchant_smith/anim/bow
