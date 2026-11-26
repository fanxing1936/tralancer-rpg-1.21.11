# 第 12 路径「魔术师」 的页（as 玩家）
function rpg:paths/update
data modify storage rpg:panel ui set value {title:{text:""},body:[],actions:[],tab:2,cards:[]}
data modify storage rpg:panel ui.title set value ["",{"text":"路径 · ","color":"#C9A646","bold":true,"italic":false},{"text":"魔术师 · Beth ב","color":"#D4D3B5","bold":true,"italic":false},{"text":" 𝔅𝔢𝔱𝔥","color":"#8F7430","bold":false,"italic":false}]
execute unless score @s rpg_ps_12 matches 3 run data modify storage rpg:panel ui.cards append value {"type":"minecraft:item","item":{"id":"minecraft:paper","count":1,"components":{"minecraft:item_model":"rpg:paths/card_12"}},"description":{"contents":["",{"text":"第 12 路径　王冠 — 理解\n","color":"#E6DFCF","bold":true,"italic":false},{"text":"试炼　把 4 个技能升到 3 级","color":"#9C9A94","bold":false,"italic":false}],"width":240},"show_decorations":false,"show_tooltip":false,"width":16,"height":16}
execute if score @s rpg_ps_12 matches 3 run data modify storage rpg:panel ui.cards append value {"type":"minecraft:item","item":{"id":"minecraft:paper","count":1,"components":{"minecraft:item_model":"rpg:paths/card_12_r"}},"description":{"contents":["",{"text":"第 12 路径　王冠 — 理解\n","color":"#E6DFCF","bold":true,"italic":false},{"text":"试炼　把 4 个技能升到 3 级","color":"#9C9A94","bold":false,"italic":false}],"width":240},"show_decorations":false,"show_tooltip":false,"width":16,"height":16}
scoreboard players operation #i rpg_pa = @s rpg_pa_12
scoreboard players operation #i rpg_pa *= #9 rpg_pa
scoreboard players set #g rpg_pa 4
scoreboard players operation #i rpg_pa /= #g rpg_pa
execute if score #i rpg_pa matches 10.. run scoreboard players set #i rpg_pa 9
execute store result storage rpg:paths d.b int 1 run scoreboard players get #i rpg_pa
execute store result storage rpg:paths d.p int 1 run scoreboard players get @s rpg_pa_12
function rpg:paths/page/12_m with storage rpg:paths d
execute if score @s rpg_ps_12 matches 4 run data modify storage rpg:panel ui.actions append value {"label":{"text":"取正位","color":"#C9A646","bold":true,"italic":false},"tooltip":{"text":"力的消耗 −10%","color":"#9C9A94","bold":false,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_pa_do set 112"}}
execute if score @s rpg_ps_12 matches 4 run data modify storage rpg:panel ui.actions append value {"label":{"text":"取逆位","color":"#C9A646","bold":true,"italic":false},"tooltip":{"text":"终式冷却 −20%","color":"#9C9A94","bold":false,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_pa_do set 212"}}
execute if score @s rpg_ps_12 matches 2 run data modify storage rpg:panel ui.actions append value {"label":{"text":"翻到逆位","color":"#C9A646","bold":true,"italic":false},"tooltip":{"text":"花 1 颗洗炼钻：终式冷却 −20%","color":"#9C9A94","bold":false,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_pa_do set 212"}}
execute if score @s rpg_ps_12 matches 3 run data modify storage rpg:panel ui.actions append value {"label":{"text":"翻到正位","color":"#C9A646","bold":true,"italic":false},"tooltip":{"text":"花 1 颗洗炼钻：力的消耗 −10%","color":"#9C9A94","bold":false,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_pa_do set 112"}}
data modify storage rpg:panel ui.actions append value {"label":{"text":"‹ 路径","color":"#9C9A94","bold":false,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_pa_do set 1"}}
function rpg:panel/ui/show with storage rpg:panel ui
