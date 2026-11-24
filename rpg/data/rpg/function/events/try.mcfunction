# as/at 选中的玩家：主世界才开；不满足条件就换成寻宝者
execute unless dimension minecraft:overworld run return 0
execute store result score #day rpg_ev run time query daytime
scoreboard players set #k rpg_ev 4
execute if score #r rpg_ev matches 1 if score #day rpg_ev matches 13000..22000 if score @s rpg_sef matches 3.. run scoreboard players set #k rpg_ev 1
execute if score #r rpg_ev matches 2 if score @s rpg_sef matches 4.. run scoreboard players set #k rpg_ev 2
execute if score #r rpg_ev matches 3 if score @s rpg_sef matches 5.. run scoreboard players set #k rpg_ev 3
execute if score #r rpg_ev matches 5 if entity @e[type=minecraft:villager,tag=rpg.vacant,distance=..64] run scoreboard players set #k rpg_ev 5
execute if score #r rpg_ev matches 6 if score #day rpg_ev matches 0..11000 run scoreboard players set #k rpg_ev 6
execute if score #k rpg_ev matches 1 run return run function rpg:events/e1/start
execute if score #k rpg_ev matches 2 run return run function rpg:events/e2/start
execute if score #k rpg_ev matches 3 run return run function rpg:events/e3/start
execute if score #k rpg_ev matches 4 run return run function rpg:events/e4/start
execute if score #k rpg_ev matches 5 run return run function rpg:events/e5/start
execute if score #k rpg_ev matches 6 run return run function rpg:merchant/ev/start
