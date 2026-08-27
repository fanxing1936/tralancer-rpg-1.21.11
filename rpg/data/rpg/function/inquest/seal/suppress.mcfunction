scoreboard players remove @s rpg_agit 20
execute if score @s rpg_agit matches ..-1 run scoreboard players set @s rpg_agit 0
scoreboard players set @s rpg_rel_cd 600
scoreboard players set @s rpg_rel_hold 31
effect give @s minecraft:slowness 8 0 true
tellraw @s ["",{"text":"[遗物压制] ","color":"#62D9E8","bold":true,"italic":false},{"text":"躁动 -20；代价：全部遗物能力冷却 30 秒，缓慢 I 持续 8 秒。","color":"gray","bold":false,"italic":false}]
playsound minecraft:block.respawn_anchor.deplete player @s ~ ~ ~ 0.8 1.4
