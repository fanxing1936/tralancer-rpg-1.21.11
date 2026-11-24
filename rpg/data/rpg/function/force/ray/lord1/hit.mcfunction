tag @s add rpg.fo.hit
scoreboard players set #dmg rpg_fo 160
scoreboard players set #hm rpg_fo 10
function rpg:force/hit
particle minecraft:dust{color:[0.37,0.84,0.55],scale:1.4} ~ ~1 ~ 0.3 0.6 0.3 0 20
