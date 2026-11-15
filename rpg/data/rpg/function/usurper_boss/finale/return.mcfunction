# 权柄归还：签了新约的玩家，白金光线连回去，权柄补满
execute as @e[tag=rpg.unit.f,distance=..48,scores={rpg_lt_divine=2}] at @s positioned ~ ~1.2 ~ facing entity @e[type=minecraft:vindicator,tag=rpg.usb,limit=1,sort=nearest] eyes run function rpg:usurper_boss/morph/line
scoreboard players set @e[tag=rpg.unit,distance=..48,scores={rpg_lt_divine=2}] rpg_lt_auth 100
tellraw @a[distance=..48,scores={rpg_lt_divine=2}] ["",{"text":"[权柄] ","color":"#62D9E8","bold":true,"italic":false},{"text":"被篡夺的权柄归还；你的权柄完整度已补满。","color":"#E8F4FF","bold":false,"italic":false}]
execute as @e[tag=rpg.unit.f,distance=..48] at @s run function rpg:usurper_boss/finale/glint
