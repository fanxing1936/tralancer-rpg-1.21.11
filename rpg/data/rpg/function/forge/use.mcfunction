# 主手材料右键。长按期间进度每刻都会触发，用锁挡住重复弹窗。
advancement revoke @s only rpg:forge/use
scoreboard players set @s rpg_fg_lk 4
execute if entity @s[tag=rpg.fg.ui] run return 0
tag @s add rpg.fg.ui
scoreboard players enable @s rpg_fg_do
scoreboard players set @s rpg_fg_op 0
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_mat:"blank"}] run return run function rpg:forge/smelt/open
execute unless items entity @s weapon.offhand #rpg:forge/any unless items entity @s weapon.offhand *[minecraft:custom_data~{sword_tag:1b}] unless items entity @s weapon.offhand *[minecraft:custom_data~{bow_tag:1b}] unless items entity @s weapon.offhand *[minecraft:custom_data~{chestplate_tag:1b}] run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　副手拿着要养成的装备，主手拿材料再右键","color":"#C04A3C","bold":false,"italic":false}]
function rpg:forge/wb/new
function rpg:forge/wb/load_off
execute store result score #ok rpg_fg run function rpg:forge/init
execute if score #ok rpg_fg matches 0 run function rpg:forge/wb/close
execute if score #ok rpg_fg matches 0 run return run tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　这件东西不能养成","color":"#C04A3C","bold":false,"italic":false}]
function rpg:forge/wb/save_off
function rpg:forge/mig/refund
execute store result score @s rpg_fg_uid run data get entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.uid
data modify storage rpg:forge e set from entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_mat:"forge_stone"}] run function rpg:forge/op/xp/open
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_mat:"wash_gem"}] run function rpg:forge/op/wash/open
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_mat:"gild_leaf"}] run function rpg:forge/op/gild/open
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_src:"faith"}] run function rpg:forge/op/src/open_faith
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_src:"hope"}] run function rpg:forge/op/src/open_hope
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_src:"resolve"}] run function rpg:forge/op/src/open_resolve
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_src:"malice"}] run function rpg:forge/op/src/open_malice
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_src:"hatred"}] run function rpg:forge/op/src/open_hatred
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_src:"pride"}] run function rpg:forge/op/src/open_pride
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_rune:"ember"}] run function rpg:forge/op/rune/open_ember
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_rune:"echo"}] run function rpg:forge/op/rune/open_echo
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_rune:"execute"}] run function rpg:forge/op/rune/open_execute
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_rune:"backstab"}] run function rpg:forge/op/rune/open_backstab
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_rune:"bloodpact"}] run function rpg:forge/op/rune/open_bloodpact
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_rune:"poise"}] run function rpg:forge/op/rune/open_poise
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_rune:"hunt"}] run function rpg:forge/op/rune/open_hunt
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_rune:"split"}] run function rpg:forge/op/rune/open_split
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_rune:"meteor"}] run function rpg:forge/op/rune/open_meteor
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_rune:"recoil"}] run function rpg:forge/op/rune/open_recoil
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_rune:"lastbreath"}] run function rpg:forge/op/rune/open_lastbreath
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_rune:"stillwater"}] run function rpg:forge/op/rune/open_stillwater
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_rune:"swift"}] run function rpg:forge/op/rune/open_swift
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_stone:"rift"}] run function rpg:forge/op/stone/open_rift
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_stone:"frost"}] run function rpg:forge/op/stone/open_frost
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_stone:"shadow"}] run function rpg:forge/op/stone/open_shadow
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_stone:"blood"}] run function rpg:forge/op/stone/open_blood
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_stone:"gale"}] run function rpg:forge/op/stone/open_gale
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_stone:"volley"}] run function rpg:forge/op/stone/open_volley
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_stone:"banner"}] run function rpg:forge/op/stone/open_banner
function rpg:forge/wb/close
