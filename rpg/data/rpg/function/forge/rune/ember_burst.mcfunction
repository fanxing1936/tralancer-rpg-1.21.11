scoreboard players set @s rpg_fg_burn 0
scoreboard players set @s rpg_fg_bt 0
damage @s 6 rpg:forge_bonus by @a[tag=rpg.fg.atk,limit=1]
execute store result score @s damage_action run data get entity @s Health
particle minecraft:lava ~ ~1 ~ 0.3 0.4 0.3 0 10
particle minecraft:flame ~ ~1 ~ 0.3 0.5 0.3 0.08 24
playsound minecraft:entity.blaze.shoot player @a[distance=..16] ~ ~ ~ 0.8 0.8
