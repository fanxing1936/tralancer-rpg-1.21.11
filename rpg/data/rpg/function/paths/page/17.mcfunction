# 第 17 路径「恋人」 的页（as 玩家）
function rpg:paths/update
data modify storage rpg:panel ui set value {title:{text:""},body:[],actions:[],tab:2,cards:[]}
data modify storage rpg:panel ui.title set value ["",{"text":"路径 · ","color":"#C9A646","bold":true,"italic":false},{"text":"恋人 · Zayin ז","color":"#D4C68E","bold":true,"italic":false},{"text":" ℨ𝔞𝔶𝔦𝔫","color":"#8F7430","bold":false,"italic":false}]
execute unless score @s rpg_ps_17 matches 3 run data modify storage rpg:panel ui.cards append value {"type":"minecraft:item","item":{"id":"minecraft:paper","count":1,"components":{"minecraft:item_model":"rpg:paths/card_17"}},"description":{"contents":["",{"text":"第 17 路径　理解 — 美丽\n","color":"#E6DFCF","bold":true,"italic":false},{"text":"试炼　近战与弓弩各杀 1 只首领精英","color":"#9C9A94","bold":false,"italic":false}],"width":240},"show_decorations":false,"show_tooltip":false,"width":16,"height":16}
execute if score @s rpg_ps_17 matches 3 run data modify storage rpg:panel ui.cards append value {"type":"minecraft:item","item":{"id":"minecraft:paper","count":1,"components":{"minecraft:item_model":"rpg:paths/card_17_r"}},"description":{"contents":["",{"text":"第 17 路径　理解 — 美丽\n","color":"#E6DFCF","bold":true,"italic":false},{"text":"试炼　近战与弓弩各杀 1 只首领精英","color":"#9C9A94","bold":false,"italic":false}],"width":240},"show_decorations":false,"show_tooltip":false,"width":16,"height":16}
scoreboard players operation #i rpg_pa = @s rpg_pa_17
scoreboard players operation #i rpg_pa *= #9 rpg_pa
scoreboard players set #g rpg_pa 2
scoreboard players operation #i rpg_pa /= #g rpg_pa
execute if score #i rpg_pa matches 10.. run scoreboard players set #i rpg_pa 9
execute store result storage rpg:paths d.b int 1 run scoreboard players get #i rpg_pa
execute store result storage rpg:paths d.p int 1 run scoreboard players get @s rpg_pa_17
function rpg:paths/page/17_m with storage rpg:paths d
execute if score @s rpg_ps_17 matches 4 run data modify storage rpg:panel ui.actions append value {"label":{"text":"取正位","color":"#C9A646","bold":true,"italic":false},"tooltip":{"text":"副手有物时护甲 +2","color":"#9C9A94","bold":false,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_pa_do set 117"}}
execute if score @s rpg_ps_17 matches 4 run data modify storage rpg:panel ui.actions append value {"label":{"text":"取逆位","color":"#C9A646","bold":true,"italic":false},"tooltip":{"text":"双持武器时伤害 +4%","color":"#9C9A94","bold":false,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_pa_do set 217"}}
execute if score @s rpg_ps_17 matches 2 run data modify storage rpg:panel ui.actions append value {"label":{"text":"翻到逆位","color":"#C9A646","bold":true,"italic":false},"tooltip":{"text":"花 1 颗洗炼钻：双持武器时伤害 +4%","color":"#9C9A94","bold":false,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_pa_do set 217"}}
execute if score @s rpg_ps_17 matches 3 run data modify storage rpg:panel ui.actions append value {"label":{"text":"翻到正位","color":"#C9A646","bold":true,"italic":false},"tooltip":{"text":"花 1 颗洗炼钻：副手有物时护甲 +2","color":"#9C9A94","bold":false,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_pa_do set 117"}}
data modify storage rpg:panel ui.actions append value {"label":{"text":"‹ 路径","color":"#9C9A94","bold":false,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_pa_do set 1"}}
function rpg:panel/ui/show with storage rpg:panel ui
