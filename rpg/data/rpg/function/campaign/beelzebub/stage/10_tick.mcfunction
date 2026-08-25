tag @a remove rpg.ch1.stage10.player
tag @s add rpg.ch1.stage10.controller
execute as @a[tag=rpg.ch1.member] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.stage10.controller,limit=1] rpg_ch1_id if score @s rpg_ch1_session = @e[type=minecraft:marker,tag=rpg.ch1.stage10.controller,limit=1] rpg_ch1_session run tag @s add rpg.ch1.stage10.player
tag @s remove rpg.ch1.stage10.controller
execute as @a[tag=rpg.ch1.stage10.player,tag=!rpg.ch1.career.confirmed,scores={rpg_ex_path=1..}] run function rpg:campaign/beelzebub/career_confirm
execute if score @s rpg_ch1_time matches 200 run tellraw @a[tag=rpg.ch1.stage10.player,tag=!rpg.ch1.career.confirmed] ["",{"text":"[选择或确认驱魔道路]","color":"#FFF2A8","bold":true,"italic":false,"click_event":{"action":"run_command","command":"/trigger rpg_panel set 1"},"hover_event":{"action":"show_text","value":{"text":"选择后才会结算首通奖励","color":"gray","bold":false,"italic":false}}}]
execute if score @s rpg_ch1_time matches 600 run tellraw @a[tag=rpg.ch1.stage10.player,tag=!rpg.ch1.career.confirmed] ["",{"text":"[选择或确认驱魔道路]","color":"#FFF2A8","bold":true,"italic":false,"click_event":{"action":"run_command","command":"/trigger rpg_panel set 1"},"hover_event":{"action":"show_text","value":{"text":"选择后才会结算首通奖励","color":"gray","bold":false,"italic":false}}}]
execute if score @s rpg_ch1_time matches 1000.. if entity @a[tag=rpg.ch1.stage10.player,tag=!rpg.ch1.career.confirmed] run scoreboard players set @s rpg_ch1_time 600
execute if score @s rpg_ch1_time matches 600.. unless entity @a[tag=rpg.ch1.stage10.player,tag=!rpg.ch1.career.confirmed] run function rpg:campaign/beelzebub/finish
