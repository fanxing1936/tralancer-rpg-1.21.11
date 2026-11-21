# 工作台里的装备进系统：判种类、迁移旧数据、算基础值、画属性块。
# 返回 1 = 已登记；0 = 不是装备。
execute if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq run return 1
scoreboard players set #k rpg_fg 0
execute if items entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] contents #rpg:forge/armor run scoreboard players set #k rpg_fg 3
execute if score #k rpg_fg matches 0 if items entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] contents #rpg:forge/ranged run scoreboard players set #k rpg_fg 2
execute if score #k rpg_fg matches 0 if items entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] contents #rpg:forge/melee run scoreboard players set #k rpg_fg 1
execute if score #k rpg_fg matches 0 if items entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] contents *[minecraft:custom_data~{chestplate_tag:1b}] run scoreboard players set #k rpg_fg 3
execute if score #k rpg_fg matches 0 if items entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] contents *[minecraft:custom_data~{bow_tag:1b}] run scoreboard players set #k rpg_fg 2
execute if score #k rpg_fg matches 0 if items entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] contents *[minecraft:custom_data~{sword_tag:1b}] run scoreboard players set #k rpg_fg 1
execute if score #k rpg_fg matches 0 run return 0
function rpg:forge/mig/item
data modify entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq set value {v:1,q:0,lv:1,xp:0,gild:0b,gk:"",gl:0,src:"none",stone:"none",ln:0,base:0,spd:0,tough:0}
execute if score #k rpg_fg matches 1 run data modify entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq merge value {kind:"melee",runes:["none","none"]}
execute if score #k rpg_fg matches 2 run data modify entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq merge value {kind:"ranged",runes:["none","none"],base:100}
execute if score #k rpg_fg matches 3 run data modify entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq merge value {kind:"armor",runes:["none"]}
scoreboard players add #uid rpg_fg 1
execute store result entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.uid int 1 run scoreboard players get #uid rpg_fg
execute store result entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.lv int 1 run scoreboard players get #mlv rpg_fg
execute if score #mgild rpg_fg matches 1 run data modify entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq merge value {gild:1b,gk:"legacy"}
execute if score #k rpg_fg matches 2..3 if data storage rpg:forge mig.src run data remove storage rpg:forge mig.src
execute if data storage rpg:forge mig.src run data modify entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.src set from storage rpg:forge mig.src
execute if score #k rpg_fg matches 1 run function rpg:forge/base/melee
execute if score #k rpg_fg matches 3 run function rpg:forge/base/armor
execute if score #q0 rpg_fg matches -100.. store result entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.q int 1 run scoreboard players get #q0 rpg_fg
scoreboard players set #q0 rpg_fg -1000
function rpg:forge/render
return 1
