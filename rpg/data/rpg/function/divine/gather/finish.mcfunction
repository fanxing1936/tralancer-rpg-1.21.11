execute as @a if score @s rpg_lt_owner = @e[type=minecraft:marker,tag=rpg.lt.gathering,distance=..1,limit=1] rpg_lt_owner run function rpg:divine/gather/reward
kill @e[type=minecraft:item_display,tag=rpg.ritual.life_tree.prop,distance=..8]
kill @e[type=minecraft:item_display,tag=rpg.ritual.life_tree.cross,distance=..8]
particle minecraft:flash{color:8641023} ~ ~0.4 ~ 0 0 0 0 1 force
particle minecraft:end_rod ~ ~0.4 ~ 2.2 0.5 4.5 0.12 180 force
particle minecraft:totem_of_undying ~ ~0.4 ~ 2.0 0.4 4.2 0.10 120 force
playsound minecraft:ui.toast.challenge_complete master @a[distance=..32] ~ ~ ~ 1 1.25
tellraw @a[distance=..24,gamemode=!spectator] ["",{"text":"[新约] ","color":"#62D9E8","bold":true,"italic":false},{"text":"十源质与真·十字架归于一体；生命之树收束为","color":"gray","bold":false,"italic":false},{"text":"『新约』","color":"#E8F4FF","bold":true,"italic":false},{"text":"。","color":"gray","bold":false,"italic":false}]
kill @s
