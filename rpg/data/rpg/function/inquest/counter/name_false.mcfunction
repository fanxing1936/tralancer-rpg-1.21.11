execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..10,sort=nearest,limit=1] run scoreboard players set @s rpg_ex_kind 0
execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..10,sort=nearest,limit=1] run function rpg:inquest/stability/hit20
tellraw @a[distance=..16,gamemode=!spectator] ["",{"text":"[伪名误判] ","color":"dark_red","bold":true,"italic":false},{"text":"错误的名字划伤了法阵。","color":"gray","italic":false}]
playsound minecraft:block.glass.break hostile @a[distance=..18] ~ ~ ~ 1 0.65
kill @e[type=minecraft:armor_stand,tag=rpg.counter.name,distance=..10]
