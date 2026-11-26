# 力页签：觉醒了就去技能页，没有就说明
execute if score @s rpg_force matches 1.. run return run function rpg:force/page/default
data modify storage rpg:panel ui set value {title:{text:""},body:[],actions:[],tab:3}
data modify storage rpg:panel ui.title set value ["",{"text":"力","color":"#C9A646","bold":true,"italic":false},{"text":" 𝔙𝔦𝔯𝔱𝔲𝔰","color":"#8F7430","bold":false,"italic":false}]
data modify storage rpg:panel ui.body append value ["",{"text":"到美丽阶（第 5 阶）会第一次感觉到力：","color":"#9C9A94","bold":false,"italic":false},{"text":"圣力","color":"#C9A646","bold":true,"italic":false},{"text":" 拿命换，","color":"#9C9A94","bold":false,"italic":false},{"text":"魔力","color":"#A276BE","bold":true,"italic":false},{"text":" 拿魔化换。觉醒以后这里是技能树与技能槽。\n","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_sef matches 5.. run data modify storage rpg:panel ui.actions append value {"label":{"text":"觉醒","color":"#C9A646","bold":true,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_sef_do set 19"}}
function rpg:panel/ui/show with storage rpg:panel ui
