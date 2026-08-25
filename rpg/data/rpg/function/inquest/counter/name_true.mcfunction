execute on attacker run scoreboard players add @s rpg_ex_xp 3
execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..10,sort=nearest,limit=1] run scoreboard players set @s rpg_ex_kind 0
execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..10,sort=nearest,limit=1] run function rpg:inquest/stability/restore
tellraw @a[distance=..16,gamemode=!spectator] ["",{"text":"[真名击破] ","color":"#31D97C","bold":true,"italic":false},{"text":"傲慢的伪名失去效力。","color":"gray","italic":false}]
playsound minecraft:block.amethyst_block.chime player @a[distance=..18] ~ ~ ~ 0.9 1.6
kill @e[type=minecraft:armor_stand,tag=rpg.counter.name,distance=..10]
