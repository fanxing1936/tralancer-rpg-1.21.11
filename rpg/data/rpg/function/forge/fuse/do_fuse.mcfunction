# 熔铸（as/at 玩家）
function rpg:forge/fuse/pre
execute if data storage rpg:forge fu{cls:""} run return run tellraw @s ["",{"text":"[熔铸] ","color":"#E39745","bold":true,"italic":false},{"text":"主手要拿着魂火冶炼出来的装备","color":"#FF6B5E","bold":false,"italic":false}]
execute if score #g rpg_fg matches 3 if score #st rpg_fg matches 5.. run return run tellraw @s ["",{"text":"[熔铸] ","color":"#E39745","bold":true,"italic":false},{"text":"已经五颗淬炼星了","color":"#FF6B5E","bold":false,"italic":false}]
execute if score #nc rpg_fg matches ..1 run return run tellraw @s ["",{"text":"[熔铸] ","color":"#E39745","bold":true,"italic":false},{"text":"背包里同类的祭品不够两把（品质不低于主件低一档）","color":"#FF6B5E","bold":false,"italic":false}]
execute if score #ns rpg_fg < #need rpg_fg run return run tellraw @s ["",{"text":"[熔铸] ","color":"#E39745","bold":true,"italic":false},{"text":"残魂不够","color":"#FF6B5E","bold":false,"italic":false}]
scoreboard players set #xa rpg_fg 0
data modify storage rpg:forge fu.c0 set from storage rpg:forge fu.c[0]
function rpg:forge/fuse/eat with storage rpg:forge fu
data remove storage rpg:forge fu.c[0]
data modify storage rpg:forge fu.c0 set from storage rpg:forge fu.c[0]
function rpg:forge/fuse/eat with storage rpg:forge fu
scoreboard players operation #k rpg_fg = #need rpg_fg
function rpg:forge/fuse/pay
function rpg:forge/wb/new
function rpg:forge/wb/load_main
execute if score #g rpg_fg matches 0 store result entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.q int 1 run random value -5..5
execute if score #g rpg_fg matches 1 store result entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.q int 1 run random value 6..10
execute if score #g rpg_fg matches 2 store result entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.q int 1 run random value 11..15
execute if score #g rpg_fg matches 3 run scoreboard players add #st rpg_fg 1
execute if score #g rpg_fg matches 3 store result entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.star int 1 run scoreboard players get #st rpg_fg
function rpg:forge/xp/add
function rpg:forge/render
function rpg:forge/wb/save_main
function rpg:forge/wb/close
scoreboard players add @s rpg_tl_fu 1
particle minecraft:flame ~ ~1 ~ 0.3 0.4 0.3 0.06 30
particle minecraft:lava ~ ~1 ~ 0.2 0.2 0.2 0 8
summon minecraft:item_display ~ ~1.2 ~ {Tags:["rpg.fu.fx"],billboard:"center",item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:town/fx_fuse_spark"}},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.5f,1.5f,1.5f]}}
schedule function rpg:forge/fuse/fx_clear 12t
playsound minecraft:block.anvil.use player @a[distance=..16] ~ ~ ~ 0.8 0.8
playsound minecraft:block.trial_spawner.eject_item block @a[distance=..16] ~ ~ ~ 1 0.9
execute if score #g rpg_fg matches ..2 run tellraw @s ["",{"text":"[熔铸] ","color":"#E39745","bold":true,"italic":false},{"text":"熔铸完成：品质升了一档","color":"#C9A646","bold":false,"italic":false}]
execute if score #g rpg_fg matches 3 run tellraw @s ["",{"text":"[熔铸] ","color":"#E39745","bold":true,"italic":false},{"text":"熔铸完成：加了一颗淬炼星","color":"#C9A646","bold":false,"italic":false}]
