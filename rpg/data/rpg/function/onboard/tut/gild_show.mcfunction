function rpg:forge/wb/new
function rpg:forge/wb/load_off
data modify storage rpg:onboard g set value {k:"",l:0}
data modify storage rpg:onboard g.k set from entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.gk
data modify storage rpg:onboard g.l set from entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.gl
function rpg:forge/wb/close
execute if data storage rpg:onboard g{k:""} run return run dialog show @s {"type":"minecraft:multi_action","title":["",{"text":"锻造 · 镀金","color":"#E8D9B0","bold":true,"italic":false}],"body":{"type":"minecraft:plain_message","width":320,"contents":["",{"text":"这把武器附不上任何附魔，镀金没有生效。","color":"#C04A3C","bold":false,"italic":false}]},"actions":[{"label":{"text":"下一步：镶嵌","color":"#FFD85A","bold":true,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_ob_do set 1"}}],"columns":1,"can_close_with_escape":false,"pause":false,"after_action":"close"}
function rpg:onboard/tut/gild_dlg with storage rpg:onboard g
