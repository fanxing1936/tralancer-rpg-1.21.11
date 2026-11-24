scoreboard players set #t rpg_ev 0
execute store result score #now rpg_ev run time query gametime
scoreboard players enable @a rpg_jr_do
# 进行中的事件
execute if score #ev rpg_ev matches 1.. run function rpg:events/run
# 每 10 分钟掷一次
scoreboard players add #roll rpg_ev 1
execute if score #roll rpg_ev matches 600.. run function rpg:events/roll
# 悬赏换日
execute store result score #day rpg_ev run time query day
execute as @a[scores={rpg_ob=100}] unless score @s rpg_bt_day = #day rpg_ev run function rpg:events/bt/reroll
execute as @e[type=minecraft:villager,tag=rpg.mer.mystery] run function rpg:merchant/stamp
