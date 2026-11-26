# 第 20 路径「隐者」 的页（as 玩家）
function rpg:paths/update
data modify storage rpg:panel ui set value {title:{text:""},body:[],actions:[],tab:2,cards:[]}
data modify storage rpg:panel ui.title set value ["",{"text":"路径 · ","color":"#C9A646","bold":true,"italic":false},{"text":"隐者 · Yod י","color":"#B0C8A5","bold":true,"italic":false},{"text":" 𝔜𝔬𝔡","color":"#8F7430","bold":false,"italic":false}]
execute unless score @s rpg_ps_20 matches 3 run data modify storage rpg:panel ui.cards append value {"type":"minecraft:item","item":{"id":"minecraft:paper","count":1,"components":{"minecraft:item_model":"rpg:paths/card_20"}},"description":{"contents":["",{"text":"第 20 路径　慈悲 — 美丽\n","color":"#E6DFCF","bold":true,"italic":false},{"text":"试炼　在失乐园灰烬边境独处 15 分钟并活着出来","color":"#9C9A94","bold":false,"italic":false}],"width":240},"show_decorations":false,"show_tooltip":false,"width":16,"height":16}
execute if score @s rpg_ps_20 matches 3 run data modify storage rpg:panel ui.cards append value {"type":"minecraft:item","item":{"id":"minecraft:paper","count":1,"components":{"minecraft:item_model":"rpg:paths/card_20_r"}},"description":{"contents":["",{"text":"第 20 路径　慈悲 — 美丽\n","color":"#E6DFCF","bold":true,"italic":false},{"text":"试炼　在失乐园灰烬边境独处 15 分钟并活着出来","color":"#9C9A94","bold":false,"italic":false}],"width":240},"show_decorations":false,"show_tooltip":false,"width":16,"height":16}
scoreboard players operation #i rpg_pa = @s rpg_pa_20
scoreboard players operation #i rpg_pa *= #9 rpg_pa
scoreboard players set #g rpg_pa 900
scoreboard players operation #i rpg_pa /= #g rpg_pa
execute if score #i rpg_pa matches 10.. run scoreboard players set #i rpg_pa 9
execute store result storage rpg:paths d.b int 1 run scoreboard players get #i rpg_pa
execute store result storage rpg:paths d.p int 1 run scoreboard players get @s rpg_pa_20
function rpg:paths/page/20_m with storage rpg:paths d
execute if score @s rpg_ps_20 matches 4 run data modify storage rpg:panel ui.actions append value {"label":{"text":"取正位","color":"#C9A646","bold":true,"italic":false},"tooltip":{"text":"潜行速度 +30%","color":"#9C9A94","bold":false,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_pa_do set 120"}}
execute if score @s rpg_ps_20 matches 4 run data modify storage rpg:panel ui.actions append value {"label":{"text":"取逆位","color":"#C9A646","bold":true,"italic":false},"tooltip":{"text":"力条上限 +10","color":"#9C9A94","bold":false,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_pa_do set 220"}}
execute if score @s rpg_ps_20 matches 2 run data modify storage rpg:panel ui.actions append value {"label":{"text":"翻到逆位","color":"#C9A646","bold":true,"italic":false},"tooltip":{"text":"花 1 颗洗炼钻：力条上限 +10","color":"#9C9A94","bold":false,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_pa_do set 220"}}
execute if score @s rpg_ps_20 matches 3 run data modify storage rpg:panel ui.actions append value {"label":{"text":"翻到正位","color":"#C9A646","bold":true,"italic":false},"tooltip":{"text":"花 1 颗洗炼钻：潜行速度 +30%","color":"#9C9A94","bold":false,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_pa_do set 120"}}
data modify storage rpg:panel ui.actions append value {"label":{"text":"‹ 路径","color":"#9C9A94","bold":false,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_pa_do set 1"}}
function rpg:panel/ui/show with storage rpg:panel ui
