execute if score @s devil matches 150 store result score @s random run random value 1..3
execute if score @s random matches 1 if score @s devil matches 150 run function rpg:entities/warden/phase1_minion
execute if score @s random matches 2 if score @s devil matches 150 at @a[distance=..20,limit=1,sort=random] run playsound minecraft:entity.ghast.death player @a[distance=..15]
execute if score @s random matches 2 if score @s devil matches 150 at @a[distance=..20,limit=1,sort=random] run effect give @s slowness 3 255 true
execute if score @s random matches 2 if score @s devil matches 150 at @a[distance=..20,limit=1,sort=random] run effect give @s glowing 3 255 true
execute if score @s random matches 2 if score @s devil matches 150 at @a[distance=..20,limit=1,sort=random] run damage @s 10 minecraft:wither
scoreboard players reset @s random
execute if score @s devil matches 150..151 run effect give @s minecraft:instant_health 1 3 true
execute if score @s devil matches 100..105 at @a[distance=..20] run summon evoker_fangs
execute if score @s devil matches 40 if entity @a[distance=..5] run playsound minecraft:entity.vex.charge player @a[distance=..15]
execute if score @s devil matches 50 if entity @a[distance=..5] run particle squid_ink ~1 ~1 ~1 -2 -1 -2 1 96
execute if score @s devil matches 50 if entity @a[distance=..5] run execute positioned ~ ~1 ~ run function rpg:effect/pseudo_explosion/owned_p8
