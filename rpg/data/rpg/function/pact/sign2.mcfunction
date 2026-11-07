# 第 2 柱 · 利维坦（嫉妒）
scoreboard players set @s rpg_pact 2
scoreboard players set @s rpg_pact_cd 300
tag @s add rpg.pact
# 补签不重置进度：只有从没立过约的人才从一阶开始。
execute unless score @s rpg_pact_lv matches 1.. run scoreboard players set @s rpg_pact_lv 1
scoreboard players add @s rpg_pact_dom 0
function rpg:pact/attr
function rpg:pact/book/fresh
title @s times 5 50 15
title @s title ["",{"text":"◆ ","italic":false,"color":"#8F7430","bold":true},{"text":"契 约 已 立","italic":false,"color":"#387AB7","bold":true},{"text":" ◆","italic":false,"color":"#8F7430","bold":true}]
title @s subtitle ["",{"text":"利","italic":false,"color":"#387AB7","bold":true},{"text":"维坦 · 嫉妒","italic":false,"color":"#387AB7","bold":true},{"text":" 𝔈𝔫𝔳𝔶","italic":false,"color":"#8F7430"},{"text":"  魔神借契约进入你的心","italic":false,"color":"#9C9A94"}]
playsound minecraft:block.end_portal.spawn master @s ~ ~ ~ 0.8 0.6
playsound minecraft:entity.wither.spawn master @a[distance=..32] ~ ~ ~ 0.5 1.4
execute at @s run particle sculk_charge_pop ~ ~1 ~ 0.5 0.8 0.5 0.1 60
execute at @s run particle minecraft:flash{color:5218032} ~ ~1 ~ 0 0 0 0 1
