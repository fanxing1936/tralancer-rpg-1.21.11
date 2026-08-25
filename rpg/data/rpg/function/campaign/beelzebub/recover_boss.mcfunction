tag @e[type=minecraft:vindicator,tag=rpg.ch1.boss] remove rpg.ch1.boss.current
execute as @e[type=minecraft:vindicator,tag=rpg.ch1.boss] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.boss.current
kill @e[type=minecraft:vindicator,tag=rpg.ch1.boss.current]
scoreboard players set @s rpg_ch1_empty 0
scoreboard players add @s rpg_ch1_fail 1
execute as @e[type=minecraft:item_display,tag=rpg.ch1.rite] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id at @s run function rpg:inquest/tool/cleanup
tellraw @a[tag=rpg.ch1.current] ["",{"text":"[仪式恢复] ","color":"#B8A98B","bold":true,"italic":false},{"text":"稳定归零或躯壳异常消散；从 Boss 入口检查点重开，不重置调查。","color":"gray","bold":false,"italic":false}]
scoreboard players set @s rpg_ch1_time 0
function rpg:campaign/beelzebub/stage/7_enter
