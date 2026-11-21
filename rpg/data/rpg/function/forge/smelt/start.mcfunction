# 开炉：再核对一遍，扣料，抽品质，把火点变成冶炼中的标记。
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_mat:"blank"}] run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　主手要拿着器胚","color":"#C04A3C","bold":false,"italic":false}]
scoreboard players operation #me rpg_fg = @s rpg_fg_id
scoreboard players set #fire rpg_fg 0
execute as @e[type=minecraft:marker,tag=rpg.fg.fire,distance=..8] if score @s rpg_fg_eo = #me rpg_fg at @s if block ~ ~ ~ #rpg:forge/soul_fire run scoreboard players set #fire rpg_fg 1
execute if score #fire rpg_fg matches 0 run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　离灵魂火太远了，靠近些再开炉","color":"#C04A3C","bold":false,"italic":false}]
function rpg:forge/smelt/count
function rpg:forge/smelt/enough
scoreboard players set #ok rpg_fg 0
execute if score @s rpg_fg_arg2 matches 0 if score #ok0 rpg_fg matches 1 run scoreboard players set #ok rpg_fg 1
execute if score @s rpg_fg_arg2 matches 1 if score #ok1 rpg_fg matches 1 run scoreboard players set #ok rpg_fg 1
execute if score @s rpg_fg_arg2 matches 2 if score #ok2 rpg_fg matches 1 run scoreboard players set #ok rpg_fg 1
execute if score #ok rpg_fg matches 0 run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　主材不够了","color":"#C04A3C","bold":false,"italic":false}]
execute if score #ns rpg_fg matches 0 run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　至少需要 1 枚残魂","color":"#C04A3C","bold":false,"italic":false}]
scoreboard players operation #souls rpg_fg = #ns rpg_fg
execute if score #souls rpg_fg matches 4.. run scoreboard players set #souls rpg_fg 3
item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}
execute if score @s rpg_fg_arg2 matches 0 run clear @s minecraft:iron_ingot[!minecraft:custom_data] 6
execute if score @s rpg_fg_arg2 matches 1 run clear @s minecraft:diamond[!minecraft:custom_data] 4
execute if score @s rpg_fg_arg2 matches 2 run clear @s minecraft:netherite_ingot[!minecraft:custom_data] 1
execute if score @s rpg_fg_arg2 matches 2 run clear @s minecraft:diamond[!minecraft:custom_data] 4
execute store result storage rpg:forge d.souls int 1 run scoreboard players get #souls rpg_fg
function rpg:forge/smelt/take with storage rpg:forge d
scoreboard players set #best rpg_fg -100
function rpg:forge/smelt/roll
execute as @e[type=minecraft:marker,tag=rpg.fg.fire,distance=..8] if score @s rpg_fg_eo = #me rpg_fg run tag @s add rpg.fg.go
scoreboard players operation @e[type=minecraft:marker,tag=rpg.fg.go] rpg_fg_arg = @s rpg_fg_arg
scoreboard players operation @e[type=minecraft:marker,tag=rpg.fg.go] rpg_fg_arg2 = @s rpg_fg_arg2
scoreboard players operation @e[type=minecraft:marker,tag=rpg.fg.go] rpg_fg_mc = #best rpg_fg
scoreboard players set @e[type=minecraft:marker,tag=rpg.fg.go] rpg_fg_t 60
tag @e[type=minecraft:marker,tag=rpg.fg.go] add rpg.fg.smelt
tag @e[type=minecraft:marker,tag=rpg.fg.go] remove rpg.fg.fire
tag @e[type=minecraft:marker,tag=rpg.fg.go] remove rpg.fg.go
scoreboard players set @s rpg_fg_op 0
playsound minecraft:block.blastfurnace.fire_crackle player @a[distance=..16] ~ ~ ~ 1 0.6
tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　魂火吞下了材料……","color":"#9C9A94","bold":false,"italic":false}]
