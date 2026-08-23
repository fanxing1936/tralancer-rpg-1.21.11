# 8 行原本各自扫一遍全实体表找 @e[type=minecraft:vindicator,tag=devil2,tag=boss]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[type=minecraft:vindicator,tag=devil2,tag=boss] at @s run particle sculk_soul ~0.1 ~1.5 ~0.1 -0.2 -0.5 -0.2 0.1 1

execute as @e[type=minecraft:vindicator,tag=devil2,tag=boss] at @s if score @s devil matches 50 at @a[distance=..15] run particle minecraft:elder_guardian
execute as @e[type=minecraft:vindicator,tag=devil2,tag=boss] at @s if score @s devil matches 50..51 run playsound minecraft:entity.allay.death player @a[distance=..15]
##斩击
execute as @e[type=minecraft:vindicator,tag=devil2,tag=boss] at @s if score @s devil matches 150 run summon armor_stand ^ ^ ^3 {Invisible:1b,CustomName:[{"text":"devil_attack"}],Invulnerable:1b}
execute as @e[type=minecraft:vindicator,tag=devil2,tag=boss] at @s if score @s devil matches 150 run summon armor_stand ^3 ^ ^3 {Invisible:1b,CustomName:[{"text":"devil_attack"}],Invulnerable:1b}
execute as @e[type=minecraft:vindicator,tag=devil2,tag=boss] at @s if score @s devil matches 150 run summon armor_stand ^-3 ^ ^3 {Invisible:1b,CustomName:[{"text":"devil_attack"}],Invulnerable:1b}
execute as @e[type=minecraft:vindicator,tag=devil2,tag=boss] at @s if score @s devil matches 150 run playsound minecraft:item.mace.smash_air player @a[distance=..20]
execute as @e[type=minecraft:vindicator,tag=devil2,tag=boss] at @s if score @s devil matches 150 run execute as @e[name=devil_attack,type=armor_stand] at @s run tp @s ~ ~ ~ facing entity @a[distance=..20,limit=1,sort=random]
