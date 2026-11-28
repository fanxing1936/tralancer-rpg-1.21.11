data modify storage rpg:panel ui set value {"title":["",{"text":"旅程 · ","color":"#C9A646","bold":true,"italic":false},{"text":"见闻录","color":"#E6DFCF","bold":true,"italic":false},{"text":" 𝔗𝔯𝔞𝔳𝔢𝔩 𝔍𝔬𝔲𝔯𝔫𝔞𝔩","color":"#8F7430","bold":false,"italic":false}],"body":[""],"actions":[{"label":{"text":"◆ 群系与城镇","color":"#C9A646","bold":true,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_x_do set 1"}},{"label":{"text":"怪物情报","color":"#9C9A94","bold":false,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_x_do set 2"}},{"label":{"text":"武器熟练","color":"#9C9A94","bold":false,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_x_do set 3"}},{"label":{"text":"‹ 旅程","color":"#9C9A94","bold":false,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_panel set 22"}}]}
data modify storage rpg:panel ui.tab set value 5
data modify storage rpg:panel ui.body append value {"text":"探索点 ","color":"#9C9A94","bold":false,"italic":false}
$data modify storage rpg:panel ui.body append value {"text":"$(pt)","color":"#C9A646","bold":true,"italic":false}
$data modify storage rpg:panel ui.body append value {"text":"　下一份：$(nx)\n","color":"#9C9A94","bold":false,"italic":false}
$data modify storage rpg:panel ui.body append value {"text":"群系 $(bn) / 19　　城镇 $(tn) / 20\n\n","color":"#9C9A94","bold":false,"italic":false}
execute if entity @s[tag=rpg.xb.plains] run data modify storage rpg:panel ui.body append value {"text":"✓ 平原","color":"#E6DFCF","bold":true,"italic":false}
execute unless entity @s[tag=rpg.xb.plains] run data modify storage rpg:panel ui.body append value {"text":"？ ？？？","color":"#797979","bold":false,"italic":false}
data modify storage rpg:panel ui.body append value {"text":"　危险 I\n","color":"#4E994E","bold":false,"italic":false}
execute if entity @s[tag=rpg.xb.forest] run data modify storage rpg:panel ui.body append value {"text":"✓ 森林","color":"#E6DFCF","bold":true,"italic":false}
execute unless entity @s[tag=rpg.xb.forest] run data modify storage rpg:panel ui.body append value {"text":"？ ？？？","color":"#797979","bold":false,"italic":false}
data modify storage rpg:panel ui.body append value {"text":"　危险 I\n","color":"#4E994E","bold":false,"italic":false}
execute if entity @s[tag=rpg.xb.wildfield] run data modify storage rpg:panel ui.body append value {"text":"✓ 原野","color":"#E6DFCF","bold":true,"italic":false}
execute unless entity @s[tag=rpg.xb.wildfield] run data modify storage rpg:panel ui.body append value {"text":"？ ？？？","color":"#797979","bold":false,"italic":false}
data modify storage rpg:panel ui.body append value {"text":"　危险 I\n","color":"#4E994E","bold":false,"italic":false}
execute if entity @s[tag=rpg.xb.lavender] run data modify storage rpg:panel ui.body append value {"text":"✓ 雾月花森林","color":"#E6DFCF","bold":true,"italic":false}
execute unless entity @s[tag=rpg.xb.lavender] run data modify storage rpg:panel ui.body append value {"text":"？ ？？？","color":"#797979","bold":false,"italic":false}
data modify storage rpg:panel ui.body append value {"text":"　危险 I\n","color":"#4E994E","bold":false,"italic":false}
execute if entity @s[tag=rpg.xb.golden] run data modify storage rpg:panel ui.body append value {"text":"✓ 丰饶森林","color":"#E6DFCF","bold":true,"italic":false}
execute unless entity @s[tag=rpg.xb.golden] run data modify storage rpg:panel ui.body append value {"text":"？ ？？？","color":"#797979","bold":false,"italic":false}
data modify storage rpg:panel ui.body append value {"text":"　危险 I\n","color":"#4E994E","bold":false,"italic":false}
execute if entity @s[tag=rpg.xb.desert] run data modify storage rpg:panel ui.body append value {"text":"✓ 沙漠","color":"#E6DFCF","bold":true,"italic":false}
execute unless entity @s[tag=rpg.xb.desert] run data modify storage rpg:panel ui.body append value {"text":"？ ？？？","color":"#797979","bold":false,"italic":false}
data modify storage rpg:panel ui.body append value {"text":"　危险 II\n","color":"#E8D27A","bold":false,"italic":false}
execute if entity @s[tag=rpg.xb.snowfield] run data modify storage rpg:panel ui.body append value {"text":"✓ 雪原","color":"#E6DFCF","bold":true,"italic":false}
execute unless entity @s[tag=rpg.xb.snowfield] run data modify storage rpg:panel ui.body append value {"text":"？ ？？？","color":"#797979","bold":false,"italic":false}
data modify storage rpg:panel ui.body append value {"text":"　危险 II\n","color":"#E8D27A","bold":false,"italic":false}
execute if entity @s[tag=rpg.xb.taiga] run data modify storage rpg:panel ui.body append value {"text":"✓ 云杉木森林","color":"#E6DFCF","bold":true,"italic":false}
execute unless entity @s[tag=rpg.xb.taiga] run data modify storage rpg:panel ui.body append value {"text":"？ ？？？","color":"#797979","bold":false,"italic":false}
data modify storage rpg:panel ui.body append value {"text":"　危险 II\n","color":"#E8D27A","bold":false,"italic":false}
execute if entity @s[tag=rpg.xb.mesa] run data modify storage rpg:panel ui.body append value {"text":"✓ 平顶山沙漠","color":"#E6DFCF","bold":true,"italic":false}
execute unless entity @s[tag=rpg.xb.mesa] run data modify storage rpg:panel ui.body append value {"text":"？ ？？？","color":"#797979","bold":false,"italic":false}
data modify storage rpg:panel ui.body append value {"text":"　危险 III\n","color":"#FFA15C","bold":false,"italic":false}
execute if entity @s[tag=rpg.xb.eroded] run data modify storage rpg:panel ui.body append value {"text":"✓ 侵蚀沙漠","color":"#E6DFCF","bold":true,"italic":false}
execute unless entity @s[tag=rpg.xb.eroded] run data modify storage rpg:panel ui.body append value {"text":"？ ？？？","color":"#797979","bold":false,"italic":false}
data modify storage rpg:panel ui.body append value {"text":"　危险 III\n","color":"#FFA15C","bold":false,"italic":false}
execute if entity @s[tag=rpg.xb.ashwood] run data modify storage rpg:panel ui.body append value {"text":"✓ 焦木林","color":"#E6DFCF","bold":true,"italic":false}
execute unless entity @s[tag=rpg.xb.ashwood] run data modify storage rpg:panel ui.body append value {"text":"？ ？？？","color":"#797979","bold":false,"italic":false}
data modify storage rpg:panel ui.body append value {"text":"　危险 III\n","color":"#FFA15C","bold":false,"italic":false}
execute if entity @s[tag=rpg.xb.stone] run data modify storage rpg:panel ui.body append value {"text":"✓ 石林","color":"#E6DFCF","bold":true,"italic":false}
execute unless entity @s[tag=rpg.xb.stone] run data modify storage rpg:panel ui.body append value {"text":"？ ？？？","color":"#797979","bold":false,"italic":false}
data modify storage rpg:panel ui.body append value {"text":"　危险 III\n","color":"#FFA15C","bold":false,"italic":false}
execute if entity @s[tag=rpg.xb.warped] run data modify storage rpg:panel ui.body append value {"text":"✓ 诡异高原","color":"#E6DFCF","bold":true,"italic":false}
execute unless entity @s[tag=rpg.xb.warped] run data modify storage rpg:panel ui.body append value {"text":"？ ？？？","color":"#797979","bold":false,"italic":false}
data modify storage rpg:panel ui.body append value {"text":"　危险 IV\n","color":"#C04A3C","bold":false,"italic":false}
execute if entity @s[tag=rpg.xb.glacier] run data modify storage rpg:panel ui.body append value {"text":"✓ 巨大冰原","color":"#E6DFCF","bold":true,"italic":false}
execute unless entity @s[tag=rpg.xb.glacier] run data modify storage rpg:panel ui.body append value {"text":"？ ？？？","color":"#797979","bold":false,"italic":false}
data modify storage rpg:panel ui.body append value {"text":"　危险 IV\n","color":"#C04A3C","bold":false,"italic":false}
execute if entity @s[tag=rpg.xb.alpine] run data modify storage rpg:panel ui.body append value {"text":"✓ 高山","color":"#E6DFCF","bold":true,"italic":false}
execute unless entity @s[tag=rpg.xb.alpine] run data modify storage rpg:panel ui.body append value {"text":"？ ？？？","color":"#797979","bold":false,"italic":false}
data modify storage rpg:panel ui.body append value {"text":"　危险 IV\n","color":"#C04A3C","bold":false,"italic":false}
execute if entity @s[tag=rpg.xb.volcano] run data modify storage rpg:panel ui.body append value {"text":"✓ 火山","color":"#E6DFCF","bold":true,"italic":false}
execute unless entity @s[tag=rpg.xb.volcano] run data modify storage rpg:panel ui.body append value {"text":"？ ？？？","color":"#797979","bold":false,"italic":false}
data modify storage rpg:panel ui.body append value {"text":"　危险 V\n","color":"#FF3300","bold":false,"italic":false}
execute if entity @s[tag=rpg.xb.war] run data modify storage rpg:panel ui.body append value {"text":"✓ 战争前线","color":"#E6DFCF","bold":true,"italic":false}
execute unless entity @s[tag=rpg.xb.war] run data modify storage rpg:panel ui.body append value {"text":"？ ？？？","color":"#797979","bold":false,"italic":false}
data modify storage rpg:panel ui.body append value {"text":"　危险 V\n","color":"#FF3300","bold":false,"italic":false}
execute if entity @s[tag=rpg.xb.cliffs] run data modify storage rpg:panel ui.body append value {"text":"✓ 海岸断崖","color":"#E6DFCF","bold":true,"italic":false}
execute unless entity @s[tag=rpg.xb.cliffs] run data modify storage rpg:panel ui.body append value {"text":"？ ？？？","color":"#797979","bold":false,"italic":false}
data modify storage rpg:panel ui.body append value {"text":"　危险 II\n","color":"#E8D27A","bold":false,"italic":false}
execute if entity @s[tag=rpg.xb.sea] run data modify storage rpg:panel ui.body append value {"text":"✓ 海与河","color":"#E6DFCF","bold":true,"italic":false}
execute unless entity @s[tag=rpg.xb.sea] run data modify storage rpg:panel ui.body append value {"text":"？ ？？？","color":"#797979","bold":false,"italic":false}
data modify storage rpg:panel ui.body append value {"text":"　危险 I\n","color":"#4E994E","bold":false,"italic":false}
function rpg:panel/ui/show
