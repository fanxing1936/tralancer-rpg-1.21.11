execute store result storage rpg:onboard tmp.id int 1 run scoreboard players get @s rpg_fg_id
# 新人：记下出生的位置，进黑屏，先听世界观旁白，再到欢迎页起名
tag @s add rpg.ob
scoreboard players set @s rpg_ob 17
scoreboard players set @s rpg_ob_lv 0
function rpg:onboard/save_pos with storage rpg:onboard tmp
# 原来的游戏模式：结束时还原（不是一律生存）
scoreboard players set @s rpg_ob_gm 0
execute if entity @s[gamemode=creative] run scoreboard players set @s rpg_ob_gm 1
execute if entity @s[gamemode=adventure] run scoreboard players set @s rpg_ob_gm 2
# 老玩家身上的护甲、副手、主手先收起来，教学用的格子要空着；结束时原样还回去
function rpg:onboard/stash/put with storage rpg:onboard tmp
function rpg:onboard/hold/enter
tag @s add rpg.ob.wait
scoreboard players set @s rpg_ob_t 0
