# 面板统一版式（add_panel_v2.py）：页签条 → 卡片 → 正文 → 底栏。ui.tab / ui.cards 可不填
execute unless data storage rpg:panel ui.tab run data modify storage rpg:panel ui.tab set value 0
execute unless data storage rpg:panel ui.cards run data modify storage rpg:panel ui.cards set value []
execute unless data storage rpg:panel ui.body[0] run data modify storage rpg:panel ui.body set value [""]
execute unless data storage rpg:panel ui.actions[0] run data modify storage rpg:panel ui.actions append value {"label":{"text":"‹ 生命之树","color":"#9C9A94","bold":false,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_panel set 8"}}
data modify storage rpg:panel ui.els set value []
function rpg:panel/ui/bar with storage rpg:panel ui
data modify storage rpg:panel ui.els append from storage rpg:panel ui.cards[]
data modify storage rpg:panel ui.els append value {type:"minecraft:plain_message",width:340,contents:""}
data modify storage rpg:panel ui.els[-1].contents set from storage rpg:panel ui.body
execute if data storage rpg:panel ui.bw run data modify storage rpg:panel ui.els[-1].width set from storage rpg:panel ui.bw
function rpg:panel/ui/show2 with storage rpg:panel ui
data remove storage rpg:panel ui.tab
data remove storage rpg:panel ui.cards
data remove storage rpg:panel ui.bw
