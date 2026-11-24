scoreboard players operation @s rpg_bt_day = #day rpg_ev
execute store result score @s rpg_bt_t1 run random value 1..8
execute store result score #d rpg_ev run random value 1..7
execute store result score #e rpg_ev run random value 1..7
execute if score #e rpg_ev = #d rpg_ev run function rpg:events/bt/bump
scoreboard players operation @s rpg_bt_t2 = @s rpg_bt_t1
scoreboard players operation @s rpg_bt_t2 += #d rpg_ev
scoreboard players operation @s rpg_bt_t3 = @s rpg_bt_t1
scoreboard players operation @s rpg_bt_t3 += #e rpg_ev
execute if score @s rpg_bt_t2 matches 9.. run scoreboard players remove @s rpg_bt_t2 8
execute if score @s rpg_bt_t3 matches 9.. run scoreboard players remove @s rpg_bt_t3 8
scoreboard players set @s rpg_bt_p1 0
scoreboard players set @s rpg_bt_p2 0
scoreboard players set @s rpg_bt_p3 0
scoreboard players set @s rpg_bt_c1 0
scoreboard players set @s rpg_bt_c2 0
scoreboard players set @s rpg_bt_c3 0
tag @s remove rpg.bt.all
