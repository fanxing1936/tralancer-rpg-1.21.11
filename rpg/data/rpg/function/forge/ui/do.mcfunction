# 对话框按钮。先核对，再执行。
scoreboard players operation #do rpg_fg = @s rpg_fg_do
scoreboard players set @s rpg_fg_do 0
scoreboard players enable @s rpg_fg_do
execute if score @s rpg_fg_op matches 10 run return run function rpg:forge/smelt/do
execute if score @s rpg_fg_op matches 0 run return 0
function rpg:forge/wb/new
function rpg:forge/wb/load_off
scoreboard players set #u rpg_fg -1
execute store result score #u rpg_fg run data get entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.uid
function rpg:forge/ui/check_mat
execute unless score #u rpg_fg = @s rpg_fg_uid run scoreboard players set #mm rpg_fg 0
execute if score #mm rpg_fg matches 0 run function rpg:forge/wb/close
execute if score #mm rpg_fg matches 0 run scoreboard players set @s rpg_fg_op 0
execute if score #mm rpg_fg matches 0 run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　装备或材料换过了，这次操作作废，什么也没消耗","color":"#C04A3C","bold":false,"italic":false}]
data modify storage rpg:forge e set from entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq
execute if score @s rpg_fg_op matches 1 if score #do rpg_fg matches 1 run function rpg:forge/op/xp/do
execute if score @s rpg_fg_op matches 2 if score #do rpg_fg matches 3..4 run function rpg:forge/op/wash/do
execute if score @s rpg_fg_op matches 3 if score #do rpg_fg matches 1 run function rpg:forge/op/gild/do
execute if score @s rpg_fg_op matches 4 if score @s rpg_fg_arg matches 0 if score #do rpg_fg matches 1 run function rpg:forge/op/src/do_faith
execute if score @s rpg_fg_op matches 4 if score @s rpg_fg_arg matches 1 if score #do rpg_fg matches 1 run function rpg:forge/op/src/do_hope
execute if score @s rpg_fg_op matches 4 if score @s rpg_fg_arg matches 2 if score #do rpg_fg matches 1 run function rpg:forge/op/src/do_resolve
execute if score @s rpg_fg_op matches 4 if score @s rpg_fg_arg matches 3 if score #do rpg_fg matches 1 run function rpg:forge/op/src/do_malice
execute if score @s rpg_fg_op matches 4 if score @s rpg_fg_arg matches 4 if score #do rpg_fg matches 1 run function rpg:forge/op/src/do_hatred
execute if score @s rpg_fg_op matches 4 if score @s rpg_fg_arg matches 5 if score #do rpg_fg matches 1 run function rpg:forge/op/src/do_pride
execute if score @s rpg_fg_op matches 5 if score @s rpg_fg_arg matches 0 if score #do rpg_fg matches 1.. run function rpg:forge/op/rune/do_ember
execute if score @s rpg_fg_op matches 5 if score @s rpg_fg_arg matches 1 if score #do rpg_fg matches 1.. run function rpg:forge/op/rune/do_echo
execute if score @s rpg_fg_op matches 5 if score @s rpg_fg_arg matches 2 if score #do rpg_fg matches 1.. run function rpg:forge/op/rune/do_execute
execute if score @s rpg_fg_op matches 5 if score @s rpg_fg_arg matches 3 if score #do rpg_fg matches 1.. run function rpg:forge/op/rune/do_backstab
execute if score @s rpg_fg_op matches 5 if score @s rpg_fg_arg matches 4 if score #do rpg_fg matches 1.. run function rpg:forge/op/rune/do_bloodpact
execute if score @s rpg_fg_op matches 5 if score @s rpg_fg_arg matches 5 if score #do rpg_fg matches 1.. run function rpg:forge/op/rune/do_poise
execute if score @s rpg_fg_op matches 5 if score @s rpg_fg_arg matches 6 if score #do rpg_fg matches 1.. run function rpg:forge/op/rune/do_hunt
execute if score @s rpg_fg_op matches 5 if score @s rpg_fg_arg matches 7 if score #do rpg_fg matches 1.. run function rpg:forge/op/rune/do_split
execute if score @s rpg_fg_op matches 5 if score @s rpg_fg_arg matches 8 if score #do rpg_fg matches 1.. run function rpg:forge/op/rune/do_meteor
execute if score @s rpg_fg_op matches 5 if score @s rpg_fg_arg matches 9 if score #do rpg_fg matches 1.. run function rpg:forge/op/rune/do_recoil
execute if score @s rpg_fg_op matches 5 if score @s rpg_fg_arg matches 10 if score #do rpg_fg matches 1.. run function rpg:forge/op/rune/do_lastbreath
execute if score @s rpg_fg_op matches 5 if score @s rpg_fg_arg matches 11 if score #do rpg_fg matches 1.. run function rpg:forge/op/rune/do_stillwater
execute if score @s rpg_fg_op matches 5 if score @s rpg_fg_arg matches 12 if score #do rpg_fg matches 1.. run function rpg:forge/op/rune/do_swift
execute if score @s rpg_fg_op matches 6 if score @s rpg_fg_arg matches 0 if score #do rpg_fg matches 1 run function rpg:forge/op/stone/do_rift
execute if score @s rpg_fg_op matches 6 if score @s rpg_fg_arg matches 1 if score #do rpg_fg matches 1 run function rpg:forge/op/stone/do_frost
execute if score @s rpg_fg_op matches 6 if score @s rpg_fg_arg matches 2 if score #do rpg_fg matches 1 run function rpg:forge/op/stone/do_shadow
execute if score @s rpg_fg_op matches 6 if score @s rpg_fg_arg matches 3 if score #do rpg_fg matches 1 run function rpg:forge/op/stone/do_blood
execute if score @s rpg_fg_op matches 6 if score @s rpg_fg_arg matches 4 if score #do rpg_fg matches 1 run function rpg:forge/op/stone/do_gale
execute if score @s rpg_fg_op matches 6 if score @s rpg_fg_arg matches 5 if score #do rpg_fg matches 1 run function rpg:forge/op/stone/do_volley
execute if score @s rpg_fg_op matches 6 if score @s rpg_fg_arg matches 6 if score #do rpg_fg matches 1 run function rpg:forge/op/stone/do_banner
function rpg:forge/wb/save_off
function rpg:forge/wb/close
scoreboard players set @s rpg_fg_op 0
