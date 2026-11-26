data modify storage rpg:panel ui set value {title:{text:""},body:[],actions:[]}
function rpg:panel/pages/panel_help
data modify storage rpg:panel ui.tab set value 6
execute if entity @s[tag=rpg.panel.hud_off] run data modify storage rpg:panel ui.body append value ["",{"text":"\n"},{"text":"HUD ","color":"#9C9A94","bold":false,"italic":false},{"text":"已隐藏","color":"#4E9FAD","bold":true,"italic":false},{"text":"\n"}]
execute unless entity @s[tag=rpg.panel.hud_off] run data modify storage rpg:panel ui.body append value ["",{"text":"\n"},{"text":"HUD ","color":"#9C9A94","bold":false,"italic":false},{"text":"显示中","color":"#4E994E","bold":true,"italic":false},{"text":"\n"}]
data modify storage rpg:panel ui.actions set value []
data modify storage rpg:panel ui.actions append value {"label":{"text":"HUD 开关","color":"#C9A646","bold":true,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_panel set 5"}}
data modify storage rpg:panel ui.actions append value {"label":{"text":"称号","color":"#C9A646","bold":true,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_panel set 23"}}
function rpg:panel/ui/show with storage rpg:panel ui
