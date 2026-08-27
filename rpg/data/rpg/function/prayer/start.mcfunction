execute unless entity @s[type=minecraft:player,gamemode=!spectator] run return 0
execute if entity @s[nbt={Health:0.0f}] run return 0
execute if score @s rpg_pr_time matches 1.. run return run function rpg:prayer/error/busy
execute if score @s rpg_pr_pending matches 1.. run return run function rpg:prayer/claim
function rpg:prayer/currency
execute store result score @s rpg_pr_have run clear @s minecraft:raw_gold[minecraft:custom_data~{currency_tag:1b}] 0
execute unless score @s rpg_pr_have matches 10.. run return run function rpg:prayer/error/poor
function rpg:prayer/space
execute unless score @s rpg_pr_space matches 1 run return run function rpg:prayer/error/full
execute store result score @s rpg_pr_paid run clear @s minecraft:raw_gold[minecraft:custom_data~{currency_tag:1b}] 10
execute unless score @s rpg_pr_paid matches 10 run return 0
execute store result score @s rpg_pr_roll run random value 1..10000 rpg:prayer
function rpg:prayer/select
scoreboard players set @s rpg_pr_time 40
scoreboard players add @s rpg_pr_total 1
tellraw @s ["",{"text":"[祷告]","color":"#D4AF37","bold":true,"italic":false},{"text":"光正在回应你的祈愿。","color":"#AAB4C3","bold":false,"italic":false}]
playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 0.45 1.05
