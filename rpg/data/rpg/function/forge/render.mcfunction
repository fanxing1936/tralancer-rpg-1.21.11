# 按 rpg_eq 重算加成修饰、隐藏原版属性行、重画属性块（lore 最后 ln 行）。
data modify storage rpg:forge ui set value {}
data modify storage rpg:forge e set from entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq
execute store result score #b rpg_fg run data get storage rpg:forge e.base
execute store result score #q rpg_fg run data get storage rpg:forge e.q
execute store result score #lv rpg_fg run data get storage rpg:forge e.lv
execute store result score #xp rpg_fg run data get storage rpg:forge e.xp
# 系数 ×10000 = (100+q)(98+2lv)
scoreboard players operation #f rpg_fg = #q rpg_fg
scoreboard players operation #f rpg_fg += #100 rpg_fg
scoreboard players operation #g rpg_fg = #lv rpg_fg
scoreboard players operation #g rpg_fg *= #2 rpg_fg
scoreboard players add #g rpg_fg 98
scoreboard players operation #f rpg_fg *= #g rpg_fg
scoreboard players operation #bn rpg_fg = #f rpg_fg
scoreboard players operation #bn rpg_fg -= #10000 rpg_fg
scoreboard players operation #bn rpg_fg *= #b rpg_fg
scoreboard players operation #bn rpg_fg /= #10000 rpg_fg
execute if data storage rpg:forge e{kind:"melee"} run function rpg:forge/render/mod_melee
execute if data storage rpg:forge e{kind:"armor"} run function rpg:forge/render/mod_armor
# 品质
execute store result storage rpg:forge ui.q int 1 run scoreboard players get #q rpg_fg
data modify storage rpg:forge ui.qs set value ""
execute if score #q rpg_fg matches 0.. run data modify storage rpg:forge ui.qs set value "+"
execute if score #q rpg_fg matches -100..-6 run data modify storage rpg:forge ui merge value {qn:"残次",qc:"#797979"}
execute if score #q rpg_fg matches -5..5 run data modify storage rpg:forge ui merge value {qn:"普通",qc:"#AAAAAA"}
execute if score #q rpg_fg matches 6..10 run data modify storage rpg:forge ui merge value {qn:"精良",qc:"#00AAAA"}
execute if score #q rpg_fg matches 11..15 run data modify storage rpg:forge ui merge value {qn:"完美",qc:"#FFAA00"}
function rpg:forge/render/qp with storage rpg:forge ui
# 等级
execute store result storage rpg:forge ui.lv int 1 run scoreboard players get #lv rpg_fg
execute store result storage rpg:forge ui.xp int 1 run scoreboard players get #xp rpg_fg
scoreboard players operation #need rpg_fg = #lv rpg_fg
scoreboard players operation #need rpg_fg *= #20 rpg_fg
execute store result storage rpg:forge ui.need int 1 run scoreboard players get #need rpg_fg
scoreboard players operation #n rpg_fg = #xp rpg_fg
scoreboard players operation #n rpg_fg *= #5 rpg_fg
scoreboard players operation #n rpg_fg /= #need rpg_fg
execute if score #n rpg_fg matches 0 run data modify storage rpg:forge ui.bar set from storage rpg:forge bars[0]
execute if score #n rpg_fg matches 1 run data modify storage rpg:forge ui.bar set from storage rpg:forge bars[1]
execute if score #n rpg_fg matches 2 run data modify storage rpg:forge ui.bar set from storage rpg:forge bars[2]
execute if score #n rpg_fg matches 3 run data modify storage rpg:forge ui.bar set from storage rpg:forge bars[3]
execute if score #n rpg_fg matches 4 run data modify storage rpg:forge ui.bar set from storage rpg:forge bars[4]
execute if score #n rpg_fg matches 5 run data modify storage rpg:forge ui.bar set from storage rpg:forge bars[5]
execute if score #lv rpg_fg matches ..9 run function rpg:forge/render/lv with storage rpg:forge ui
execute if score #lv rpg_fg matches 10.. run function rpg:forge/render/lv_max
# 镀金
data modify storage rpg:forge ui.gp set value '{"text":"—","color":"#797979","bold":false,"italic":false}'
execute if data storage rpg:forge e{gild:1b} run function rpg:forge/render/gp with storage rpg:forge e
execute if data storage rpg:forge e{gild:1b,gk:"legacy"} run data modify storage rpg:forge ui.gp set value '{"text":"已镀金","color":"#D4AF37","bold":false,"italic":false}'
# 源、符石、符文的名字
data modify storage rpg:forge e.r1 set value "none"
data modify storage rpg:forge e.r2 set value "none"
data modify storage rpg:forge e.r1 set from storage rpg:forge e.runes[0]
execute if data storage rpg:forge e.runes[1] run data modify storage rpg:forge e.r2 set from storage rpg:forge e.runes[1]
function rpg:forge/render/names with storage rpg:forge e
# 神圣之源、且装备 Lv.5 以上：算圣器（index_player 读这个标记）
data remove entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.holy
execute if score #lv rpg_fg matches 5.. if data storage rpg:forge e{src:"faith"} run data modify entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.holy set value 1b
execute if score #lv rpg_fg matches 5.. if data storage rpg:forge e{src:"hope"} run data modify entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.holy set value 1b
execute if score #lv rpg_fg matches 5.. if data storage rpg:forge e{src:"resolve"} run data modify entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.holy set value 1b
execute if score #lv rpg_fg matches ..4 if data storage rpg:forge e{r2:"none"} run data modify storage rpg:forge ui.r2 set value '{"text":"🔒Lv.5","color":"#797979","bold":false,"italic":false}'
execute if items entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] contents *[minecraft:custom_data~{jachin_tag:1b}] run data modify storage rpg:forge ui.tc set value '{"text":"不可镶嵌","color":"#797979","bold":false,"italic":false}'
execute if items entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] contents *[minecraft:custom_data~{boaz_tag:1b}] run data modify storage rpg:forge ui.tc set value '{"text":"不可镶嵌","color":"#797979","bold":false,"italic":false}'
# 数值
scoreboard players operation #v rpg_fg = #b rpg_fg
scoreboard players operation #v rpg_fg += #bn rpg_fg
data modify storage rpg:forge f.key set value "dmg"
function rpg:forge/fmt
execute store result score #v rpg_fg run data get storage rpg:forge e.spd
data modify storage rpg:forge f.key set value "spd"
function rpg:forge/fmt
execute store result score #v rpg_fg run data get storage rpg:forge e.tough
data modify storage rpg:forge f.key set value "tough"
function rpg:forge/fmt
scoreboard players operation #v rpg_fg = #f rpg_fg
scoreboard players operation #v rpg_fg /= #100 rpg_fg
data modify storage rpg:forge f.key set value "fac"
function rpg:forge/fmt
execute store result entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.fac int 1 run scoreboard players get #v rpg_fg
# 画
execute if data storage rpg:forge e{kind:"melee"} run function rpg:forge/render/lines_melee with storage rpg:forge ui
execute if data storage rpg:forge e{kind:"ranged"} run function rpg:forge/render/lines_ranged with storage rpg:forge ui
execute if data storage rpg:forge e{kind:"armor"} run function rpg:forge/render/lines_armor with storage rpg:forge ui
execute store result score #ln rpg_fg run data get storage rpg:forge e.ln
function rpg:forge/render/cut
execute unless data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:lore" run data modify entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:lore" set value []
data modify entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:lore" append from storage rpg:forge L[]
execute store result entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.ln int 1 run data get storage rpg:forge L
