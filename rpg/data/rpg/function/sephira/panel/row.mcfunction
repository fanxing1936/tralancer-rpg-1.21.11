# 玩家面板第一行（as 玩家；取代原来的「驱魔等级 / 阅历 / 侵蚀」一行）
scoreboard players add @s rpg_sef 0
scoreboard players add @s rpg_power 0
scoreboard players add @s rpg_gear 0
scoreboard players add @s rpg_sp 0
data modify storage rpg:sephira v set value {tn:"未入阶",tc:"#9C9A94",nx:"—",fl:""}
execute if score @s rpg_sef matches 1 run data modify storage rpg:sephira v merge value {tn:"王国",tc:"#C58A62",nx:"60"}
execute if score @s rpg_sef matches 2 run data modify storage rpg:sephira v merge value {tn:"基础",tc:"#D596F2",nx:"160"}
execute if score @s rpg_sef matches 3 run data modify storage rpg:sephira v merge value {tn:"光辉",tc:"#FF8A4A",nx:"300"}
execute if score @s rpg_sef matches 4 run data modify storage rpg:sephira v merge value {tn:"胜利",tc:"#70DB70",nx:"480"}
execute if score @s rpg_sef matches 5 run data modify storage rpg:sephira v merge value {tn:"美丽",tc:"#FFD85A",nx:"700"}
execute if score @s rpg_sef matches 6 run data modify storage rpg:sephira v merge value {tn:"严厉",tc:"#FF5A62",nx:"950"}
execute if score @s rpg_sef matches 7 run data modify storage rpg:sephira v merge value {tn:"慈悲",tc:"#62B8F0",nx:"1250"}
execute if score @s rpg_sef matches 8 run data modify storage rpg:sephira v merge value {tn:"理解",tc:"#AAB4C3",nx:"1600"}
execute if score @s rpg_sef matches 9 run data modify storage rpg:sephira v merge value {tn:"智慧",tc:"#C9CDD6",nx:"2000"}
execute if score @s rpg_sef matches 10 run data modify storage rpg:sephira v merge value {tn:"王冠",tc:"#FFF2A8",nx:"已至王冠"}
execute if score @s rpg_sef matches 7 unless score @s rpg_daath matches 1 run data modify storage rpg:sephira v.nx set value "1250（先越过达阿特）"
execute store result storage rpg:sephira v.tier int 1 run scoreboard players get @s rpg_sef
execute store result storage rpg:sephira v.pw int 1 run scoreboard players get @s rpg_power
execute store result storage rpg:sephira v.xp int 1 run scoreboard players get @s rpg_ex_xp
execute store result storage rpg:sephira v.gr int 1 run scoreboard players get @s rpg_gear
execute store result storage rpg:sephira v.sp int 1 run scoreboard players get @s rpg_sp
execute store result storage rpg:sephira v.mn int 1 run scoreboard players get @s rpg_mana
execute store result storage rpg:sephira v.mn2 int 1 run scoreboard players get @s rpg_mana2
execute store result storage rpg:sephira v.mx int 1 run scoreboard players get @s rpg_mana_max
execute store result storage rpg:sephira v.vt int 1 run scoreboard players get @s rpg_vital
execute store result storage rpg:sephira v.as int 1 run scoreboard players get @s rpg_assim
execute store result storage rpg:sephira v.tt int 1 run scoreboard players get @s rpg_taint
execute store result storage rpg:sephira v.au int 1 run scoreboard players get @s rpg_lt_auth
function rpg:sephira/panel/row1 with storage rpg:sephira v
execute if score @s rpg_force matches 1 run function rpg:sephira/panel/row_holy with storage rpg:sephira v
execute if score @s rpg_force matches 2 run function rpg:sephira/panel/row_mana with storage rpg:sephira v
execute if score @s rpg_force matches 3 run function rpg:sephira/panel/row_both with storage rpg:sephira v
execute unless score @s rpg_force matches 1.. run function rpg:sephira/panel/row_none with storage rpg:sephira v
execute if score @s rpg_lt_divine matches 2 run function rpg:sephira/panel/row_auth with storage rpg:sephira v
data modify storage rpg:panel ui.actions append value {"label":{"text":"原质","color":"#C9A646","bold":true,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_sef_do set 20"}}
execute if score @s rpg_sef matches 2.. unless score @s rpg_pillar matches 1..3 run data modify storage rpg:panel ui.actions append value {"label":{"text":"选择主柱","color":"#FF8A4A","bold":true,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_sef_do set 9"}}
execute if score @s rpg_sef matches 5.. if score @s rpg_force matches 0 run data modify storage rpg:panel ui.actions append value {"label":{"text":"觉醒","color":"#FFD85A","bold":true,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_sef_do set 19"}}
execute if entity @s[tag=rpg.fallen] if score @s rpg_lt_divine matches 2 run data modify storage rpg:panel ui.actions append value {"label":{"text":"凭新约回头","color":"#FFD85A","bold":true,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_sef_do set 21"}}
