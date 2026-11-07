# 潜行低头长按书。文字里的数字靠宏写进去，所以每次打开都现算。
tag @s add rpg.pact.ui
scoreboard players enable @s rpg_pact_do
execute store result storage rpg:pact ui.bond int 1 run scoreboard players get @s rpg_pact_bond
execute store result storage rpg:pact ui.taint int 1 run scoreboard players get @s rpg_taint
scoreboard players operation #c rpg_pact = @s rpg_pact_cd2
scoreboard players operation #c rpg_pact /= #twenty_t rpg_pact
execute store result storage rpg:pact ui.cd2 int 1 run scoreboard players get #c rpg_pact
scoreboard players operation #c rpg_pact = @s rpg_pact_cd3
scoreboard players operation #c rpg_pact /= #twenty_t rpg_pact
execute store result storage rpg:pact ui.cd3 int 1 run scoreboard players get #c rpg_pact
execute if score @s rpg_pact_lv matches 1 run data modify storage rpg:pact ui.tier set value "第一阶 · 血誓"
execute if score @s rpg_pact_lv matches 2 run data modify storage rpg:pact ui.tier set value "第二阶 · 魂誓"
execute if score @s rpg_pact_lv matches 3 run data modify storage rpg:pact ui.tier set value "第三阶 · 真名"
data modify storage rpg:pact ui.dom set value ""
execute if score @s rpg_pact_dom matches 1 run data modify storage rpg:pact ui.dom set value " · 支配"
function rpg:pact/ui/names
execute if score @s rpg_pact matches 1 run function rpg:pact/ui/next1
execute if score @s rpg_pact matches 2 run function rpg:pact/ui/next2
execute if score @s rpg_pact matches 3 run function rpg:pact/ui/next3
execute if score @s rpg_pact matches 4 run function rpg:pact/ui/next4
execute if score @s rpg_pact matches 5 run function rpg:pact/ui/next5
execute if score @s rpg_pact matches 6 run function rpg:pact/ui/next6
execute if score @s rpg_pact matches 7 run function rpg:pact/ui/next7
execute if score @s rpg_pact matches 1 run function rpg:pact/ui/show1 with storage rpg:pact ui
execute if score @s rpg_pact matches 2 run function rpg:pact/ui/show2 with storage rpg:pact ui
execute if score @s rpg_pact matches 3 run function rpg:pact/ui/show3 with storage rpg:pact ui
execute if score @s rpg_pact matches 4 run function rpg:pact/ui/show4 with storage rpg:pact ui
execute if score @s rpg_pact matches 5 run function rpg:pact/ui/show5 with storage rpg:pact ui
execute if score @s rpg_pact matches 6 run function rpg:pact/ui/show6 with storage rpg:pact ui
execute if score @s rpg_pact matches 7 run function rpg:pact/ui/show7 with storage rpg:pact ui
