# 第 23 路径「倒吊人」 的页（as 玩家）
function rpg:paths/update
data modify storage rpg:panel ui set value {title:{text:""},body:[],actions:[],tab:2,cards:[]}
data modify storage rpg:panel ui.title set value ["",{"text":"路径 · ","color":"#C9A646","bold":true,"italic":false},{"text":"倒吊人 · Mem מ","color":"#FF7256","bold":true,"italic":false},{"text":" 𝔐𝔢𝔪","color":"#8F7430","bold":false,"italic":false}]
execute unless score @s rpg_ps_23 matches 3 run data modify storage rpg:panel ui.cards append value {"type":"minecraft:item","item":{"id":"minecraft:paper","count":1,"components":{"minecraft:item_model":"rpg:paths/card_23"}},"description":{"contents":["",{"text":"第 23 路径　严厉 — 光辉\n","color":"#E6DFCF","bold":true,"italic":false},{"text":"试炼　生命低于 30% 时击杀 15 只怪","color":"#9C9A94","bold":false,"italic":false}],"width":240},"show_decorations":false,"show_tooltip":false,"width":16,"height":16}
execute if score @s rpg_ps_23 matches 3 run data modify storage rpg:panel ui.cards append value {"type":"minecraft:item","item":{"id":"minecraft:paper","count":1,"components":{"minecraft:item_model":"rpg:paths/card_23_r"}},"description":{"contents":["",{"text":"第 23 路径　严厉 — 光辉\n","color":"#E6DFCF","bold":true,"italic":false},{"text":"试炼　生命低于 30% 时击杀 15 只怪","color":"#9C9A94","bold":false,"italic":false}],"width":240},"show_decorations":false,"show_tooltip":false,"width":16,"height":16}
scoreboard players operation #i rpg_pa = @s rpg_pa_23
scoreboard players operation #i rpg_pa *= #9 rpg_pa
scoreboard players set #g rpg_pa 15
scoreboard players operation #i rpg_pa /= #g rpg_pa
execute if score #i rpg_pa matches 10.. run scoreboard players set #i rpg_pa 9
execute store result storage rpg:paths d.b int 1 run scoreboard players get #i rpg_pa
execute store result storage rpg:paths d.p int 1 run scoreboard players get @s rpg_pa_23
function rpg:paths/page/23_m with storage rpg:paths d
execute if score @s rpg_ps_23 matches 4 run data modify storage rpg:panel ui.actions append value {"label":{"text":"取正位","color":"#C9A646","bold":true,"italic":false},"tooltip":{"text":"低于 30% 时抗性 I","color":"#9C9A94","bold":false,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_pa_do set 123"}}
execute if score @s rpg_ps_23 matches 4 run data modify storage rpg:panel ui.actions append value {"label":{"text":"取逆位","color":"#C9A646","bold":true,"italic":false},"tooltip":{"text":"最大生命 +2","color":"#9C9A94","bold":false,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_pa_do set 223"}}
execute if score @s rpg_ps_23 matches 2 run data modify storage rpg:panel ui.actions append value {"label":{"text":"翻到逆位","color":"#C9A646","bold":true,"italic":false},"tooltip":{"text":"花 1 颗洗炼钻：最大生命 +2","color":"#9C9A94","bold":false,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_pa_do set 223"}}
execute if score @s rpg_ps_23 matches 3 run data modify storage rpg:panel ui.actions append value {"label":{"text":"翻到正位","color":"#C9A646","bold":true,"italic":false},"tooltip":{"text":"花 1 颗洗炼钻：低于 30% 时抗性 I","color":"#9C9A94","bold":false,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_pa_do set 123"}}
data modify storage rpg:panel ui.actions append value {"label":{"text":"‹ 路径","color":"#9C9A94","bold":false,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_pa_do set 1"}}
function rpg:panel/ui/show with storage rpg:panel ui
