# 升档熔铸（as/at 玩家）
function rpg:forge/fuse/pre
execute if data storage rpg:forge fu{cls:""} run return run tellraw @s ["",{"text":"[熔铸] ","color":"#E39745","bold":true,"italic":false},{"text":"主手要拿着魂火冶炼出来的装备","color":"#FF6B5E","bold":false,"italic":false}]
execute unless score #g rpg_fg matches 3 run return run tellraw @s ["",{"text":"[熔铸] ","color":"#E39745","bold":true,"italic":false},{"text":"升档要主件已经是完美品质","color":"#FF6B5E","bold":false,"italic":false}]
execute if items entity @s weapon.mainhand #rpg:fuse/sword run data modify storage rpg:forge fu.cls set value "sword"
execute if items entity @s weapon.mainhand #rpg:fuse/axe run data modify storage rpg:forge fu.cls set value "axe"
execute if items entity @s weapon.mainhand #rpg:fuse/mace run data modify storage rpg:forge fu.cls set value "mace"
execute if items entity @s weapon.mainhand #rpg:fuse/bow run data modify storage rpg:forge fu.cls set value "bow"
execute if items entity @s weapon.mainhand #rpg:fuse/crossbow run data modify storage rpg:forge fu.cls set value "crossbow"
execute if items entity @s weapon.mainhand #rpg:fuse/head run data modify storage rpg:forge fu.cls set value "head"
execute if items entity @s weapon.mainhand #rpg:fuse/chest run data modify storage rpg:forge fu.cls set value "chest"
execute if items entity @s weapon.mainhand #rpg:fuse/legs run data modify storage rpg:forge fu.cls set value "legs"
execute if items entity @s weapon.mainhand #rpg:fuse/feet run data modify storage rpg:forge fu.cls set value "feet"
function rpg:forge/fuse/up_tier with storage rpg:forge fu
execute if score #tier rpg_fg matches 2.. run return run tellraw @s ["",{"text":"[熔铸] ","color":"#E39745","bold":true,"italic":false},{"text":"史诗已经是最高一档","color":"#FF6B5E","bold":false,"italic":false}]
data modify storage rpg:forge fu.c set value []
execute store result score #sel rpg_fg run data get entity @s SelectedItemSlot
function rpg:forge/fuse/up_scan with storage rpg:forge fu
execute store result score #nc rpg_fg run data get storage rpg:forge fu.c
execute if score #nc rpg_fg matches ..1 run return run tellraw @s ["",{"text":"[熔铸] ","color":"#E39745","bold":true,"italic":false},{"text":"要两把同类、同档、完美品质的祭品","color":"#FF6B5E","bold":false,"italic":false}]
execute if score #tier rpg_fg matches 0 store result score #m rpg_fg run clear @s minecraft:diamond[!minecraft:custom_data] 0
execute if score #tier rpg_fg matches 0 if score #m rpg_fg matches ..1 run return run tellraw @s ["",{"text":"[熔铸] ","color":"#E39745","bold":true,"italic":false},{"text":"下一档的主材不够：钻石 ×2","color":"#FF6B5E","bold":false,"italic":false}]
execute if score #tier rpg_fg matches 1 store result score #m rpg_fg run clear @s minecraft:netherite_ingot[!minecraft:custom_data] 0
execute if score #tier rpg_fg matches 1 if score #m rpg_fg matches ..0 run return run tellraw @s ["",{"text":"[熔铸] ","color":"#E39745","bold":true,"italic":false},{"text":"下一档的主材不够：下界合金锭 ×1","color":"#FF6B5E","bold":false,"italic":false}]
execute if score #tier rpg_fg matches 1 store result score #m rpg_fg run clear @s minecraft:diamond[!minecraft:custom_data] 0
execute if score #tier rpg_fg matches 1 if score #m rpg_fg matches ..1 run return run tellraw @s ["",{"text":"[熔铸] ","color":"#E39745","bold":true,"italic":false},{"text":"下一档的主材不够：钻石 ×2","color":"#FF6B5E","bold":false,"italic":false}]
execute if score #tier rpg_fg matches 0 run clear @s minecraft:diamond[!minecraft:custom_data] 2
execute if score #tier rpg_fg matches 1 run clear @s minecraft:netherite_ingot[!minecraft:custom_data] 1
execute if score #tier rpg_fg matches 1 run clear @s minecraft:diamond[!minecraft:custom_data] 2
scoreboard players set #xa rpg_fg 0
data modify storage rpg:forge fu.c0 set from storage rpg:forge fu.c[0]
function rpg:forge/fuse/eat with storage rpg:forge fu
data remove storage rpg:forge fu.c[0]
data modify storage rpg:forge fu.c0 set from storage rpg:forge fu.c[0]
function rpg:forge/fuse/eat with storage rpg:forge fu
data modify storage rpg:forge old set from entity @s SelectedItem.components."minecraft:custom_data".rpg_eq
function rpg:forge/wb/new
execute store result score #r rpg_fg run random value 0..7
execute store result storage rpg:forge nm.r int 1 run scoreboard players get #r rpg_fg
function rpg:forge/smelt/prefix with storage rpg:forge nm
execute if score #tier rpg_fg matches 0 if data storage rpg:forge fu{cls:"sword"} run function rpg:forge/smelt/m/sword_brave with storage rpg:forge nm
execute if score #tier rpg_fg matches 0 if data storage rpg:forge fu{cls:"axe"} run function rpg:forge/smelt/m/axe_brave with storage rpg:forge nm
execute if score #tier rpg_fg matches 0 if data storage rpg:forge fu{cls:"mace"} run function rpg:forge/smelt/m/mace_brave with storage rpg:forge nm
execute if score #tier rpg_fg matches 0 if data storage rpg:forge fu{cls:"bow"} run function rpg:forge/smelt/m/bow_brave with storage rpg:forge nm
execute if score #tier rpg_fg matches 0 if data storage rpg:forge fu{cls:"crossbow"} run function rpg:forge/smelt/m/crossbow_brave with storage rpg:forge nm
execute if score #tier rpg_fg matches 0 if data storage rpg:forge fu{cls:"head"} run function rpg:forge/smelt/m/head_brave with storage rpg:forge nm
execute if score #tier rpg_fg matches 0 if data storage rpg:forge fu{cls:"chest"} run function rpg:forge/smelt/m/chest_brave with storage rpg:forge nm
execute if score #tier rpg_fg matches 0 if data storage rpg:forge fu{cls:"legs"} run function rpg:forge/smelt/m/legs_brave with storage rpg:forge nm
execute if score #tier rpg_fg matches 0 if data storage rpg:forge fu{cls:"feet"} run function rpg:forge/smelt/m/feet_brave with storage rpg:forge nm
execute if score #tier rpg_fg matches 1 if data storage rpg:forge fu{cls:"sword"} run function rpg:forge/smelt/m/sword_epic with storage rpg:forge nm
execute if score #tier rpg_fg matches 1 if data storage rpg:forge fu{cls:"axe"} run function rpg:forge/smelt/m/axe_epic with storage rpg:forge nm
execute if score #tier rpg_fg matches 1 if data storage rpg:forge fu{cls:"mace"} run function rpg:forge/smelt/m/mace_epic with storage rpg:forge nm
execute if score #tier rpg_fg matches 1 if data storage rpg:forge fu{cls:"bow"} run function rpg:forge/smelt/m/bow_epic with storage rpg:forge nm
execute if score #tier rpg_fg matches 1 if data storage rpg:forge fu{cls:"crossbow"} run function rpg:forge/smelt/m/crossbow_epic with storage rpg:forge nm
execute if score #tier rpg_fg matches 1 if data storage rpg:forge fu{cls:"head"} run function rpg:forge/smelt/m/head_epic with storage rpg:forge nm
execute if score #tier rpg_fg matches 1 if data storage rpg:forge fu{cls:"chest"} run function rpg:forge/smelt/m/chest_epic with storage rpg:forge nm
execute if score #tier rpg_fg matches 1 if data storage rpg:forge fu{cls:"legs"} run function rpg:forge/smelt/m/legs_epic with storage rpg:forge nm
execute if score #tier rpg_fg matches 1 if data storage rpg:forge fu{cls:"feet"} run function rpg:forge/smelt/m/feet_epic with storage rpg:forge nm
execute store result score #mlv rpg_fg run data get storage rpg:forge old.lv
scoreboard players set #mgild rpg_fg 0
execute store result score #q0 rpg_fg run random value 6..10
execute as @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] run function rpg:forge/init
execute if data storage rpg:forge old.xp run data modify entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.xp set from storage rpg:forge old.xp
execute if data storage rpg:forge old.src run data modify entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.src set from storage rpg:forge old.src
execute if data storage rpg:forge old.stone run data modify entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.stone set from storage rpg:forge old.stone
execute if data storage rpg:forge old.runes run data modify entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.runes set from storage rpg:forge old.runes
function rpg:forge/xp/add
function rpg:forge/render
item replace entity @s weapon.mainhand from entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] contents
function rpg:forge/wb/close
scoreboard players add @s rpg_tl_fu 1
particle minecraft:flame ~ ~1 ~ 0.4 0.5 0.4 0.08 50
particle minecraft:end_rod ~ ~1.2 ~ 0.3 0.4 0.3 0.05 20
playsound minecraft:block.anvil.use player @a[distance=..16] ~ ~ ~ 0.8 0.6
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.6 1.2
tellraw @s ["",{"text":"[熔铸] ","color":"#E39745","bold":true,"italic":false},{"text":"升档熔铸完成：装备上了一档，品质回到精良","color":"#C9A646","bold":false,"italic":false}]
