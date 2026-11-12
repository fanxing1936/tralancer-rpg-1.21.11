scoreboard players operation #id rpg_l2_id = @s rpg_l2_id
scoreboard players set #n rpg_l2_v 0
execute as @e[tag=rpg.lu2f.minion] if score @s rpg_l2_id = #id rpg_l2_id run scoreboard players add #n rpg_l2_v 1
execute if score #n rpg_l2_v matches ..2 positioned ^2 ^ ^1 run function rpg:lucifer_fight/tempt/one
execute if score #n rpg_l2_v matches ..1 positioned ^-2 ^ ^1 run function rpg:lucifer_fight/tempt/one
tag @s add rpg.dm.cast
execute as @a[distance=..12,gamemode=!spectator,gamemode=!creative] at @e[tag=rpg.dm.cast,limit=1] positioned ~ ~4.5 ~ facing entity @s eyes run function rpg:lucifer_fight/fx/line
execute as @a[distance=..12,gamemode=!spectator,gamemode=!creative] at @s run function rpg:lucifer_fight/tempt/pull
tag @s remove rpg.dm.cast
particle block{block_state:{Name:"minecraft:rooted_dirt"}} ~ ~0.3 ~ 3 0.2 3 0.1 50
