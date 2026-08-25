scoreboard players set @s rpg_ex_stage 5
data merge entity @s {Health:700f,CustomNameVisible:1b}
execute if entity @a[tag=rpg.rite.chooser,distance=..14,scores={rpg_ex_path=1,rpg_ex_lvl=4..}] run data merge entity @s {Health:640f}
attribute @s minecraft:knockback_resistance modifier remove rpg:rite_lock
tag @s remove rpg.rite.locked
data merge entity @s {NoAI:0b,Motion:[0d,0d,0d]}
tag @s remove rpg.exorcism.bound
tag @s remove rpg.exorcism.visible
effect clear @s minecraft:resistance
effect clear @s minecraft:slowness
effect clear @s minecraft:glowing
effect give @s minecraft:strength 20 1 true
effect give @s minecraft:speed 20 1 true
execute on passengers run tag @s add rpg.outcome.eliminate
tag @s add rpg.rite.subject
execute on passengers run scoreboard players operation @s rpg_dm_lord = @e[type=minecraft:vindicator,tag=rpg.rite.subject,limit=1] rpg_dm_lord
tag @s remove rpg.rite.subject
scoreboard players add @a[tag=rpg.rite.chooser,distance=..14] rpg_ex_xp 8
tellraw @a[distance=..24,gamemode=!spectator] ["",{"text":"[裁决·消灭] ","color":"#FF6B5E","bold":true,"italic":false},{"text":"仪式解除锁血；恶魔以 700 生命狂暴复苏。","color":"gray","italic":false}]
