scoreboard players operation #id rpg_l2_id = @s rpg_l2_id
scoreboard players set #alive rpg_l2_v 0
execute as @e[type=minecraft:vindicator,tag=rpg.lu2] if score @s rpg_l2_id = #id rpg_l2_id run scoreboard players set #alive rpg_l2_v 1
execute if score #alive rpg_l2_v matches 1 run return 0
particle dust_color_transition{from_color:[0.37,0.84,0.55],to_color:[0.0,0.29,0.11],scale:1.2} ~ ~1 ~ 0.4 0.8 0.4 0.02 18
particle block{block_state:{Name:"minecraft:moss_block"}} ~ ~0.5 ~ 0.4 0.4 0.4 0.1 16
tp @s ~ -256 ~
kill @s
