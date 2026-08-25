function rpg:inquest/tool/place/bell
scoreboard players set @s rpg_ex_kind 0
scoreboard players set @s rpg_ex_ctime 0
scoreboard players set @s rpg_ex_ransom 0
scoreboard players set @s rpg_ex_counter 180
scoreboard players add @s rpg_ex_stab 12
execute if score @s rpg_ex_stab matches 101.. run scoreboard players set @s rpg_ex_stab 100
kill @e[type=minecraft:armor_stand,tag=rpg.counter.name,distance=..10]
kill @e[type=minecraft:husk,tag=rpg.counter.clone,distance=..12]
execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14,limit=1] run effect give @s minecraft:strength 8 1 true
execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14,limit=1] run effect give @s minecraft:speed 8 1 true
scoreboard players add @a[tag=rpg.rite.chooser,distance=..16] rpg_ex_xp 2
tellraw @a[distance=..16,gamemode=!spectator] ["",{"text":"[告解铃] ","color":"#FFF2A8","bold":true,"italic":false},{"text":"反仪式被打断；敲铃者已被恶魔注视。","color":"gray","italic":false}]
particle flash{color:16773574} ~ ~1 ~ 0 0 0 0 1 force
