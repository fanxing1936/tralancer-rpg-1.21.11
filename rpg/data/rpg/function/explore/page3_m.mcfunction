data modify storage rpg:panel ui set value {"title":["",{"text":"旅程 · ","color":"#C9A646","bold":true,"italic":false},{"text":"见闻录","color":"#E6DFCF","bold":true,"italic":false},{"text":" 𝔗𝔯𝔞𝔳𝔢𝔩 𝔍𝔬𝔲𝔯𝔫𝔞𝔩","color":"#8F7430","bold":false,"italic":false}],"body":[""],"actions":[{"label":{"text":"群系与城镇","color":"#9C9A94","bold":false,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_x_do set 1"}},{"label":{"text":"怪物情报","color":"#9C9A94","bold":false,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_x_do set 2"}},{"label":{"text":"◆ 武器熟练","color":"#C9A646","bold":true,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_x_do set 3"}},{"label":{"text":"‹ 旅程","color":"#9C9A94","bold":false,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_panel set 22"}}]}
data modify storage rpg:panel ui.tab set value 5
data modify storage rpg:panel ui.body append value {"text":"同一类武器命中越多，越顺手：200 / 800 / 2000 次各升一级，每级伤害 +3%。\n\n","color":"#9C9A94","bold":false,"italic":false}
data modify storage rpg:panel ui.body append value {"text":"长剑　","color":"#E6DFCF","bold":true,"italic":false}
execute if entity @s[tag=rpg.ms.sword3] run data modify storage rpg:panel ui.body append value {"text":"3 级","color":"#C9A646","bold":true,"italic":false}
execute if entity @s[tag=rpg.ms.sword2] unless entity @s[tag=rpg.ms.sword3] run data modify storage rpg:panel ui.body append value {"text":"2 级","color":"#C9A646","bold":true,"italic":false}
execute if entity @s[tag=rpg.ms.sword1] unless entity @s[tag=rpg.ms.sword2] run data modify storage rpg:panel ui.body append value {"text":"1 级","color":"#C9A646","bold":true,"italic":false}
execute unless entity @s[tag=rpg.ms.sword1] run data modify storage rpg:panel ui.body append value {"text":"未入门","color":"#797979","bold":false,"italic":false}
$data modify storage rpg:panel ui.body append value {"text":"　命中 $(ms_sword)\n","color":"#9C9A94","bold":false,"italic":false}
data modify storage rpg:panel ui.body append value {"text":"战斧　","color":"#E6DFCF","bold":true,"italic":false}
execute if entity @s[tag=rpg.ms.axe3] run data modify storage rpg:panel ui.body append value {"text":"3 级","color":"#C9A646","bold":true,"italic":false}
execute if entity @s[tag=rpg.ms.axe2] unless entity @s[tag=rpg.ms.axe3] run data modify storage rpg:panel ui.body append value {"text":"2 级","color":"#C9A646","bold":true,"italic":false}
execute if entity @s[tag=rpg.ms.axe1] unless entity @s[tag=rpg.ms.axe2] run data modify storage rpg:panel ui.body append value {"text":"1 级","color":"#C9A646","bold":true,"italic":false}
execute unless entity @s[tag=rpg.ms.axe1] run data modify storage rpg:panel ui.body append value {"text":"未入门","color":"#797979","bold":false,"italic":false}
$data modify storage rpg:panel ui.body append value {"text":"　命中 $(ms_axe)\n","color":"#9C9A94","bold":false,"italic":false}
data modify storage rpg:panel ui.body append value {"text":"重锤　","color":"#E6DFCF","bold":true,"italic":false}
execute if entity @s[tag=rpg.ms.mace3] run data modify storage rpg:panel ui.body append value {"text":"3 级","color":"#C9A646","bold":true,"italic":false}
execute if entity @s[tag=rpg.ms.mace2] unless entity @s[tag=rpg.ms.mace3] run data modify storage rpg:panel ui.body append value {"text":"2 级","color":"#C9A646","bold":true,"italic":false}
execute if entity @s[tag=rpg.ms.mace1] unless entity @s[tag=rpg.ms.mace2] run data modify storage rpg:panel ui.body append value {"text":"1 级","color":"#C9A646","bold":true,"italic":false}
execute unless entity @s[tag=rpg.ms.mace1] run data modify storage rpg:panel ui.body append value {"text":"未入门","color":"#797979","bold":false,"italic":false}
$data modify storage rpg:panel ui.body append value {"text":"　命中 $(ms_mace)　（破甲）\n","color":"#9C9A94","bold":false,"italic":false}
data modify storage rpg:panel ui.body append value {"text":"长弓　","color":"#E6DFCF","bold":true,"italic":false}
execute if entity @s[tag=rpg.ms.bow3] run data modify storage rpg:panel ui.body append value {"text":"3 级","color":"#C9A646","bold":true,"italic":false}
execute if entity @s[tag=rpg.ms.bow2] unless entity @s[tag=rpg.ms.bow3] run data modify storage rpg:panel ui.body append value {"text":"2 级","color":"#C9A646","bold":true,"italic":false}
execute if entity @s[tag=rpg.ms.bow1] unless entity @s[tag=rpg.ms.bow2] run data modify storage rpg:panel ui.body append value {"text":"1 级","color":"#C9A646","bold":true,"italic":false}
execute unless entity @s[tag=rpg.ms.bow1] run data modify storage rpg:panel ui.body append value {"text":"未入门","color":"#797979","bold":false,"italic":false}
$data modify storage rpg:panel ui.body append value {"text":"　命中 $(ms_bow)\n","color":"#9C9A94","bold":false,"italic":false}
data modify storage rpg:panel ui.body append value {"text":"劲弩　","color":"#E6DFCF","bold":true,"italic":false}
execute if entity @s[tag=rpg.ms.crossbow3] run data modify storage rpg:panel ui.body append value {"text":"3 级","color":"#C9A646","bold":true,"italic":false}
execute if entity @s[tag=rpg.ms.crossbow2] unless entity @s[tag=rpg.ms.crossbow3] run data modify storage rpg:panel ui.body append value {"text":"2 级","color":"#C9A646","bold":true,"italic":false}
execute if entity @s[tag=rpg.ms.crossbow1] unless entity @s[tag=rpg.ms.crossbow2] run data modify storage rpg:panel ui.body append value {"text":"1 级","color":"#C9A646","bold":true,"italic":false}
execute unless entity @s[tag=rpg.ms.crossbow1] run data modify storage rpg:panel ui.body append value {"text":"未入门","color":"#797979","bold":false,"italic":false}
$data modify storage rpg:panel ui.body append value {"text":"　命中 $(ms_crossbow)\n","color":"#9C9A94","bold":false,"italic":false}
function rpg:panel/ui/show
